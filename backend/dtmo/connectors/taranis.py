from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

from dtmo.connectors.base import Connector, ConnectorRecord, ConnectorResult


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

    def _checkpoint_file(self) -> Path:
        return Path(self.settings.taranis_checkpoint_path)

    def _load_checkpoint(self) -> dict[str, int]:
        path = self._checkpoint_file()
        if not path.exists():
            return {"news_items": 0, "stories": 0}
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError("Taranis checkpoint is unreadable") from exc
        if not isinstance(payload, dict):
            raise ValueError("Taranis checkpoint must be an object")
        result: dict[str, int] = {}
        for field in ("news_items", "stories"):
            value = payload.get(field, 0)
            if not isinstance(value, int) or value < 0:
                raise ValueError(f"Taranis checkpoint {field} must be a non-negative integer")
            result[field] = value
        return result

    def _save_checkpoint(self, checkpoint: dict[str, int]) -> None:
        path = self._checkpoint_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(checkpoint, sort_keys=True) + "\n", encoding="utf-8")
        tmp.replace(path)

    async def _fetch_collection(
        self,
        client: httpx.AsyncClient,
        *,
        path: str,
        field: str,
        checkpoint: int,
    ) -> tuple[list[dict[str, Any]], int]:
        page_size = self.settings.taranis_page_size
        backtrack = self.settings.taranis_reconcile_pages * page_size
        offset = max(0, checkpoint - backtrack)
        start_offset = offset
        collected: list[dict[str, Any]] = []
        for _ in range(self.settings.taranis_max_pages):
            response = await client.get(
                path,
                headers=self._headers(),
                params={"limit": page_size, "offset": offset},
            )
            response.raise_for_status()
            page = _objects(response.json(), field=field)
            collected.extend(page)
            offset += len(page)
            if len(page) < page_size:
                break
        else:
            if offset == start_offset:
                raise ValueError(f"Taranis {field} pagination made no progress")
        return collected, max(checkpoint, offset)

    async def fetch(self, client: httpx.AsyncClient) -> Any:
        base = self.settings.taranis_api_base.rstrip("/")
        if not base:
            raise ValueError("Taranis API base is required")
        checkpoint = self._load_checkpoint()
        news, news_next = await self._fetch_collection(
            client,
            path=f"{base}/api/assess/news-items",
            field="news_items",
            checkpoint=checkpoint["news_items"],
        )
        stories, stories_next = await self._fetch_collection(
            client,
            path=f"{base}/api/assess/stories",
            field="stories",
            checkpoint=checkpoint["stories"],
        )
        return {
            "news_items": news,
            "stories": stories,
            "_checkpoint": {"news_items": news_next, "stories": stories_next},
        }

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

    async def run(self) -> ConnectorResult:
        started = datetime.now(timezone.utc).isoformat()
        last_error: Exception | None = None
        for attempt in range(1, self.settings.connector_max_attempts + 1):
            try:
                async with httpx.AsyncClient(
                    timeout=self.settings.connector_timeout_seconds,
                    follow_redirects=True,
                ) as client:
                    payload = await self.fetch(client)
                records = self.parse(payload)
                checkpoint = payload.get("_checkpoint")
                if not isinstance(checkpoint, dict):
                    raise ValueError("Taranis successful fetch has no checkpoint candidate")
                self._save_checkpoint({"news_items": int(checkpoint["news_items"]), "stories": int(checkpoint["stories"])})
                return ConnectorResult(
                    connector_id=self.id,
                    started_at=started,
                    finished_at=datetime.now(timezone.utc).isoformat(),
                    records=records,
                    attempts=attempt,
                    status="completed",
                )
            except (httpx.HTTPError, ValueError, KeyError, OSError) as exc:
                last_error = exc
                self.log.warning("connector_attempt_failed", attempt=attempt, error=str(exc))
        return ConnectorResult(
            connector_id=self.id,
            started_at=started,
            finished_at=datetime.now(timezone.utc).isoformat(),
            records=[],
            attempts=self.settings.connector_max_attempts,
            status="failed",
            error=str(last_error),
        )
