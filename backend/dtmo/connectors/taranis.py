from __future__ import annotations

from typing import Any

import httpx

from dtmo.connectors.base import Connector, ConnectorRecord


def _objects(payload: Any, *, field: str) -> list[dict[str, Any]]:
    value = payload
    if isinstance(payload, dict):
        for key in (field, "items", "data", "results"):
            if key in payload:
                value = payload[key]
                break
    if not isinstance(value, list):
        raise ValueError(f"Taranis {field} response must contain a list")
    result: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError(f"Taranis {field} entry is not an object")
        result.append(item)
    return result


def _stable_id(item: dict[str, Any], *, object_type: str) -> str:
    value = item.get("id", item.get("uuid"))
    if not isinstance(value, (str, int)) or not str(value).strip():
        raise ValueError(f"Taranis {object_type} has no stable id")
    return f"taranis:{object_type}:{str(value).strip()}"


def _text(item: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _handling(item: dict[str, Any]) -> dict[str, Any]:
    raw = item.get("tlp", item.get("classification", item.get("marking")))
    if raw is None or not str(raw).strip():
        return {"upstream": None, "dtmo": "review-required", "mapped": False}
    normalized = str(raw).strip().lower().replace("tlp:", "")
    mapping = {
        "clear": "clear",
        "white": "clear",
        "green": "green",
        "amber": "amber",
        "amber+strict": "amber+strict",
        "red": "red",
    }
    mapped = mapping.get(normalized)
    if mapped is None:
        return {"upstream": str(raw), "dtmo": "review-required", "mapped": False}
    return {"upstream": str(raw), "dtmo": mapped, "mapped": True}


def normalize_taranis_item(item: dict[str, Any], *, object_type: str, instance: str) -> dict[str, Any]:
    external_id = _stable_id(item, object_type=object_type)
    source = item.get("osint_source", item.get("source"))
    source_id: str | None = None
    if isinstance(source, dict):
        raw_source_id = source.get("id", source.get("uuid"))
        if raw_source_id is not None:
            source_id = str(raw_source_id)
    elif source is not None:
        source_id = str(source)
    return {
        "adapter": "taranis-read-v1",
        "instance": instance,
        "upstream_object_type": object_type,
        "upstream_id": external_id.split(":", 2)[2],
        "canonical_external_id": external_id,
        "upstream_source_id": source_id,
        "handling": _handling(item),
        "read_only_import": True,
        "external_share_authorized": False,
    }


class TaranisReadConnector(Connector):
    id = "taranis"
    reliability = "trusted"

    def _headers(self) -> dict[str, str]:
        token = self.settings.taranis_api_token.get_secret_value().strip()
        if not token:
            raise ValueError("Taranis API token is required")
        return {"Accept": "application/json", "Authorization": f"Bearer {token}"}

    async def fetch(self, client: httpx.AsyncClient) -> Any:
        base = self.settings.taranis_api_base.rstrip("/")
        if not base:
            raise ValueError("Taranis API base is required")
        headers = self._headers()
        news = await client.get(
            f"{base}/api/assess/news-items",
            headers=headers,
            params={"limit": self.settings.taranis_page_size, "offset": 0},
        )
        news.raise_for_status()
        stories = await client.get(
            f"{base}/api/assess/stories",
            headers=headers,
            params={"limit": min(self.settings.taranis_page_size, 400), "offset": 0},
        )
        stories.raise_for_status()
        return {"news_items": news.json(), "stories": stories.json()}

    def parse(self, payload: Any) -> list[ConnectorRecord]:
        if not isinstance(payload, dict):
            raise ValueError("Taranis response must be an object")
        base = self.settings.taranis_api_base.rstrip("/")
        records: list[ConnectorRecord] = []
        for object_type, field in (("news-item", "news_items"), ("story", "stories")):
            for item in _objects(payload.get(field), field=field):
                projection = normalize_taranis_item(item, object_type=object_type, instance=base)
                upstream_id = projection["upstream_id"]
                title = _text(item, "title", "headline", "name") or str(upstream_id)
                summary = _text(item, "summary", "description", "content")
                raw = dict(item)
                raw["_dtmo_taranis"] = projection
                records.append(
                    ConnectorRecord(
                        external_id=str(projection["canonical_external_id"]),
                        object_type="article" if object_type == "news-item" else "report",
                        title=title,
                        url=_text(item, "url", "link") or f"{base}/assess/{object_type}s/{upstream_id}",
                        summary=summary,
                        published_at=_text(item, "published", "published_at", "created", "created_at") or None,
                        source_reliability=self.reliability,
                        confidence=80,
                        raw=raw,
                    )
                )
        return records
