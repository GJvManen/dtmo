from __future__ import annotations

from typing import Any

import httpx

from dtmo.connectors.base import Connector, ConnectorRecord


_DISTRIBUTION_LABELS = {
    "0": "your-organisation-only",
    "1": "this-community-only",
    "2": "connected-communities",
    "3": "all-communities",
    "4": "sharing-group",
    "5": "inherit",
}


def _list_of_dicts(value: Any, *, field: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"MISP {field} must be a list")
    result: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError(f"MISP {field} entry is not an object")
        result.append(item)
    return result


def _tags(value: Any) -> list[str]:
    result: list[str] = []
    for tag in _list_of_dicts(value, field="Tag"):
        name = tag.get("name")
        if isinstance(name, str) and name.strip():
            result.append(name.strip())
    return result


def _galaxies(value: Any) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for galaxy in _list_of_dicts(value, field="Galaxy"):
        clusters: list[dict[str, Any]] = []
        for cluster in _list_of_dicts(galaxy.get("GalaxyCluster"), field="GalaxyCluster"):
            clusters.append(
                {
                    "uuid": cluster.get("uuid"),
                    "type": cluster.get("type"),
                    "value": cluster.get("value"),
                    "tag_name": cluster.get("tag_name"),
                }
            )
        result.append(
            {
                "uuid": galaxy.get("uuid"),
                "type": galaxy.get("type"),
                "name": galaxy.get("name"),
                "clusters": clusters,
            }
        )
    return result


def _distribution(value: Any) -> dict[str, Any]:
    raw = str(value) if value is not None else None
    return {
        "value": raw,
        "label": _DISTRIBUTION_LABELS.get(raw or "", "unknown"),
    }


def _attribute_projection(attribute: dict[str, Any]) -> dict[str, Any]:
    return {
        "uuid": attribute.get("uuid"),
        "type": attribute.get("type"),
        "category": attribute.get("category"),
        "value": attribute.get("value"),
        "comment": attribute.get("comment"),
        "to_ids": attribute.get("to_ids"),
        "timestamp": attribute.get("timestamp"),
        "first_seen": attribute.get("first_seen"),
        "last_seen": attribute.get("last_seen"),
        "object_relation": attribute.get("object_relation"),
        "distribution": _distribution(attribute.get("distribution")),
        "sharing_group_id": attribute.get("sharing_group_id"),
        "tags": _tags(attribute.get("Tag")),
        "galaxies": _galaxies(attribute.get("Galaxy")),
    }


def _object_projection(obj: dict[str, Any]) -> dict[str, Any]:
    return {
        "uuid": obj.get("uuid"),
        "name": obj.get("name"),
        "meta_category": obj.get("meta-category"),
        "description": obj.get("description"),
        "timestamp": obj.get("timestamp"),
        "distribution": _distribution(obj.get("distribution")),
        "sharing_group_id": obj.get("sharing_group_id"),
        "attributes": [
            _attribute_projection(attribute)
            for attribute in _list_of_dicts(obj.get("Attribute"), field="Object.Attribute")
        ],
        "references": [
            {
                "uuid": reference.get("uuid"),
                "referenced_uuid": reference.get("referenced_uuid"),
                "relationship_type": reference.get("relationship_type"),
                "comment": reference.get("comment"),
            }
            for reference in _list_of_dicts(obj.get("ObjectReference"), field="ObjectReference")
        ],
    }


def normalize_misp_event(event: dict[str, Any]) -> dict[str, Any]:
    event_uuid = event.get("uuid")
    if not isinstance(event_uuid, str) or not event_uuid.strip():
        raise ValueError("MISP event has no UUID")
    tags = _tags(event.get("Tag"))
    orgc_value = event.get("Orgc")
    orgc: dict[str, Any] = orgc_value if isinstance(orgc_value, dict) else {}
    attributes = [
        _attribute_projection(attribute)
        for attribute in _list_of_dicts(event.get("Attribute"), field="Attribute")
    ]
    objects = [
        _object_projection(obj)
        for obj in _list_of_dicts(event.get("Object"), field="Object")
    ]
    return {
        "event_uuid": event_uuid.strip(),
        "event_id": event.get("id"),
        "info": event.get("info"),
        "date": event.get("date"),
        "timestamp": event.get("timestamp"),
        "published": event.get("published"),
        "publish_timestamp": event.get("publish_timestamp"),
        "organisation": {
            "uuid": orgc.get("uuid"),
            "name": orgc.get("name"),
        },
        "distribution": _distribution(event.get("distribution")),
        "sharing_group_id": event.get("sharing_group_id"),
        "tags": tags,
        "tlp_tags": sorted(tag for tag in tags if tag.lower().startswith("tlp:")),
        "galaxies": _galaxies(event.get("Galaxy")),
        "attributes": attributes,
        "objects": objects,
        "restriction_authoritative": True,
        "read_only_import": True,
        "external_share_authorized": False,
    }


class MispReadConnector(Connector):
    id = "misp"
    reliability = "trusted"

    async def fetch(self, client: httpx.AsyncClient) -> Any:
        base = self.settings.misp_api_base.rstrip("/")
        if not base:
            raise ValueError("MISP API base is required")
        api_key = self.settings.misp_api_key.get_secret_value().strip()
        if not api_key:
            raise ValueError("MISP API key is required")
        response = await client.post(
            f"{base}/events/restSearch",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": api_key,
            },
            json={
                "returnFormat": "json",
                "limit": self.settings.misp_event_limit,
                "page": 1,
                "order": "timestamp desc",
            },
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, (list, dict)):
            raise ValueError("MISP events/restSearch returned unsupported JSON")
        return payload

    @staticmethod
    def _events(payload: Any) -> list[dict[str, Any]]:
        raw_events: Any = payload
        if isinstance(payload, dict):
            raw_events = payload.get("response", payload.get("events", payload.get("Event")))
        if isinstance(raw_events, dict):
            raw_events = [raw_events]
        if not isinstance(raw_events, list):
            raise ValueError("MISP payload has no event list")
        events: list[dict[str, Any]] = []
        for item in raw_events:
            if not isinstance(item, dict):
                raise ValueError("MISP event entry is not an object")
            event = item.get("Event", item)
            if not isinstance(event, dict):
                raise ValueError("MISP Event wrapper is not an object")
            events.append(event)
        return events

    def parse(self, payload: Any) -> list[ConnectorRecord]:
        base = self.settings.misp_api_base.rstrip("/")
        records: list[ConnectorRecord] = []
        for event in self._events(payload):
            projection = normalize_misp_event(event)
            event_uuid = str(projection["event_uuid"])
            raw = dict(event)
            raw["_dtmo_misp"] = projection
            info = event.get("info")
            summary = info.strip() if isinstance(info, str) else ""
            records.append(
                ConnectorRecord(
                    external_id=event_uuid,
                    object_type="cti_event",
                    title=summary or event_uuid,
                    url=f"{base}/events/view/{event_uuid}",
                    summary=summary,
                    published_at=str(event.get("date")) if event.get("date") is not None else None,
                    source_reliability=self.reliability,
                    confidence=85,
                    raw=raw,
                )
            )
        return records
