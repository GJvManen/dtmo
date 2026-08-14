from __future__ import annotations

from typing import Any
from urllib.parse import quote

import httpx

from dtmo.connectors.base import Connector, ConnectorRecord
from dtmo.intelligence import IntelligenceType


_ALLOWED_INDICATOR_TYPES = {"domain", "ip", "cve", "cryptocurrency", "ssh-key"}


def _split_gid(gid: str) -> tuple[str, str | None, str]:
    parts = gid.split(":", 2)
    if len(parts) != 3 or not all(parts):
        raise ValueError("AIL object global id must use type:subtype:id")
    obj_type, subtype, obj_id = parts
    return obj_type, None if subtype == "None" else subtype, obj_id


def _investigation_references(payload: dict[str, Any]) -> list[dict[str, str]]:
    value = payload.get("investigations", payload.get("investigation"))
    if value is None:
        return []
    if isinstance(value, (str, int)):
        return [{"id": str(value)}]
    if isinstance(value, dict):
        value = [value]
    if not isinstance(value, list):
        raise ValueError("AIL investigation references must be a list, object or identifier")

    references: list[dict[str, str]] = []
    for entry in value:
        if isinstance(entry, (str, int)):
            references.append({"id": str(entry)})
            continue
        if not isinstance(entry, dict):
            raise ValueError("AIL investigation reference entry is unsupported")
        identifier = entry.get("uuid", entry.get("id"))
        if identifier is not None and str(identifier).strip():
            references.append({"id": str(identifier).strip()})
    return references


def normalize_ail_object(gid: str, payload: dict[str, Any]) -> dict[str, Any]:
    obj_type, subtype, obj_id = _split_gid(gid)
    if obj_type not in _ALLOWED_INDICATOR_TYPES:
        raise ValueError(f"AIL object type {obj_type!r} is outside the DTMO indicator allowlist")

    returned_type = payload.get("type")
    if returned_type is not None and str(returned_type) != obj_type:
        raise ValueError("AIL object type does not match requested global id")
    returned_id = payload.get("id")
    if returned_id is not None and str(returned_id) != obj_id:
        raise ValueError("AIL object id does not match requested global id")

    return {
        "global_id": gid,
        "indicator_type": obj_type,
        "indicator_subtype": subtype,
        "indicator_value": obj_id,
        "investigation_references": _investigation_references(payload),
        "read_only_import": True,
        "data_minimized": True,
        "raw_content_imported": False,
        "external_share_authorized": False,
    }


class AilReadConnector(Connector):
    """Read explicit AIL objects; never schedule, create or run crawlers."""

    id = "ail"
    reliability = "trusted"

    def _targets(self) -> list[str]:
        targets = [value.strip() for value in self.settings.ail_object_global_ids.split(",") if value.strip()]
        if not targets:
            raise ValueError("AIL connector requires explicit object global ids")
        return targets[: self.settings.ail_object_limit]

    async def fetch(self, client: httpx.AsyncClient) -> Any:
        base = self.settings.ail_api_base.rstrip("/")
        if not base:
            raise ValueError("AIL API base is required")
        api_key = self.settings.ail_api_key.get_secret_value().strip()
        if not api_key:
            raise ValueError("AIL API key is required")

        results: list[dict[str, Any]] = []
        for gid in self._targets():
            response = await client.get(
                f"{base}/api/v1/object",
                params={"gid": gid},
                headers={"Accept": "application/json", "Authorization": api_key},
            )
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise ValueError("AIL api/v1/object returned unsupported JSON")
            results.append({"gid": gid, "object": payload})
        return results

    def parse(self, payload: Any) -> list[ConnectorRecord]:
        if not isinstance(payload, list):
            raise ValueError("AIL payload must be a list of explicitly requested objects")
        base = self.settings.ail_api_base.rstrip("/")
        records: list[ConnectorRecord] = []
        for entry in payload:
            if not isinstance(entry, dict):
                raise ValueError("AIL payload entry is not an object")
            gid = entry.get("gid")
            obj = entry.get("object")
            if not isinstance(gid, str) or not isinstance(obj, dict):
                raise ValueError("AIL payload entry requires gid and object")
            projection = normalize_ail_object(gid, obj)
            indicator_type = str(projection["indicator_type"])
            indicator_value = str(projection["indicator_value"])
            canonical_url = f"{base}/api/v1/object?gid={quote(gid, safe='')}"
            records.append(
                ConnectorRecord(
                    external_id=gid,
                    object_type=IntelligenceType.INDICATOR.value,
                    title=f"AIL {indicator_type} indicator",
                    url=canonical_url,
                    summary=f"AIL extracted {indicator_type} indicator: {indicator_value}",
                    published_at=None,
                    source_reliability=self.reliability,
                    confidence=75,
                    raw={"_dtmo_ail": projection},
                )
            )
        return records
