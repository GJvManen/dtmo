from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any
from uuid import UUID, NAMESPACE_URL, uuid5

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from dtmo.audit import AuditDecision
from dtmo.audit.store import append_persistent_audit_event
from dtmo.auth.policy import Principal
from dtmo.config import Settings
from dtmo.persistence.models import IntelligenceItem


class MispExportError(RuntimeError):
    """Raised when a governed MISP export cannot be performed safely."""


_TLP_RANK = {
    "tlp:clear": 0,
    "tlp:white": 0,
    "tlp:green": 1,
    "tlp:amber": 2,
    "tlp:amber+strict": 3,
    "tlp:red": 4,
}


@dataclass(frozen=True, slots=True)
class PreparedMispExport:
    item_id: UUID
    replay_key: str
    event_uuid: str
    payload: dict[str, Any]


@dataclass(frozen=True, slots=True)
class MispExportResult:
    item_id: UUID
    replay_key: str
    event_uuid: str
    misp_event_id: str | None
    audit_event_id: UUID


def _normalized_tlp(value: str) -> str:
    candidate = value.strip().lower()
    if candidate not in _TLP_RANK:
        raise MispExportError("unsupported TLP value")
    return candidate


def _validate_distribution(distribution: int, sharing_group_id: str | None) -> None:
    if distribution not in {0, 1, 2, 3, 4}:
        raise MispExportError("MISP distribution must be between 0 and 4")
    if distribution == 4 and not (sharing_group_id or "").strip():
        raise MispExportError("sharing-group distribution requires sharing_group_id")
    if distribution != 4 and sharing_group_id:
        raise MispExportError("sharing_group_id is only valid for distribution 4")


def _authoritative_misp_restrictions(item: IntelligenceItem) -> dict[str, Any] | None:
    restrictions = item.metadata_json.get("misp_restrictions")
    if not isinstance(restrictions, dict) or not restrictions.get("restriction_authoritative"):
        return None
    return restrictions


def _enforce_source_restrictions(
    item: IntelligenceItem,
    *,
    distribution: int,
    sharing_group_id: str | None,
    tlp: str,
) -> None:
    restrictions = _authoritative_misp_restrictions(item)
    if restrictions is None:
        return

    source_distribution = restrictions.get("distribution")
    if isinstance(source_distribution, dict):
        source_distribution = source_distribution.get("value")
    if source_distribution is not None and str(source_distribution) != str(distribution):
        raise MispExportError("authoritative MISP distribution cannot be changed on re-export")

    source_group = restrictions.get("sharing_group_id")
    normalized_source_group = str(source_group).strip() if source_group not in {None, ""} else None
    normalized_requested_group = sharing_group_id.strip() if sharing_group_id else None
    if normalized_source_group != normalized_requested_group:
        raise MispExportError("authoritative MISP sharing group cannot be changed on re-export")

    source_tlp_tags = restrictions.get("tlp_tags")
    if isinstance(source_tlp_tags, list) and source_tlp_tags:
        normalized_source = [_normalized_tlp(str(tag)) for tag in source_tlp_tags]
        most_restrictive = max(normalized_source, key=lambda tag: _TLP_RANK[tag])
        if _TLP_RANK[tlp] < _TLP_RANK[most_restrictive]:
            raise MispExportError("requested TLP is less restrictive than authoritative source TLP")


def _event_payload(
    item: IntelligenceItem,
    *,
    event_uuid: str,
    distribution: int,
    sharing_group_id: str | None,
    tlp: str,
) -> dict[str, Any]:
    event: dict[str, Any] = {
        "uuid": event_uuid,
        "info": item.title,
        "distribution": str(distribution),
        "published": False,
        "analysis": "2",
        "threat_level_id": "4",
        "Tag": [{"name": tlp}],
        "Attribute": [
            {
                "type": "link",
                "category": "External analysis",
                "value": item.canonical_url,
                "to_ids": False,
                "comment": item.summary[:1000],
                "distribution": "5",
            }
        ],
    }
    if sharing_group_id:
        event["sharing_group_id"] = sharing_group_id
    return {"Event": event}


def _replay_key(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _export_records(item: IntelligenceItem) -> list[dict[str, Any]]:
    value = item.metadata_json.get("misp_exports")
    if not isinstance(value, list):
        return []
    # JSON columns do not track nested in-place mutation by default. Return
    # copy-on-write records so finalization/uncertain transitions assign a
    # genuinely changed top-level value that SQLAlchemy persists reliably.
    return [dict(entry) for entry in value if isinstance(entry, dict)]


def prepare_misp_export(
    session: Session,
    *,
    item_id: UUID,
    principal: Principal,
    request_id: str,
    distribution: int,
    sharing_group_id: str | None,
    tlp: str,
) -> PreparedMispExport:
    item = session.scalar(
        select(IntelligenceItem).where(IntelligenceItem.id == item_id).with_for_update()
    )
    if item is None:
        raise MispExportError("intelligence item not found")
    if principal.is_service_account:
        raise MispExportError("service accounts cannot export intelligence to MISP")
    if item.review_status != "reviewed" or not item.share_approved:
        raise MispExportError("intelligence requires separate human review and share approval before MISP export")
    if not str(item.metadata_json.get("share_approved_by", "")).strip():
        raise MispExportError("share approval attribution is missing")
    if item.source_id == "misp" and _authoritative_misp_restrictions(item) is None:
        raise MispExportError(
            "MISP-origin intelligence cannot be re-exported until its authoritative source restrictions are projected"
        )

    _validate_distribution(distribution, sharing_group_id)
    normalized_tlp = _normalized_tlp(tlp)
    _enforce_source_restrictions(
        item,
        distribution=distribution,
        sharing_group_id=sharing_group_id,
        tlp=normalized_tlp,
    )

    event_uuid = str(uuid5(NAMESPACE_URL, f"dtmo:misp-export:{item.id}:{item.content_hash}"))
    payload = _event_payload(
        item,
        event_uuid=event_uuid,
        distribution=distribution,
        sharing_group_id=sharing_group_id,
        tlp=normalized_tlp,
    )
    replay_key = _replay_key(payload)
    existing = _export_records(item)
    if any(
        record.get("event_uuid") == event_uuid
        and record.get("status") in {"pending", "success", "uncertain"}
        for record in existing
    ):
        append_persistent_audit_event(
            session,
            principal=principal.subject,
            principal_type="human",
            action="intelligence.misp_export",
            resource=f"intelligence:{item.id}",
            decision=AuditDecision.DENY,
            request_id=request_id,
            provenance_reference=item.canonical_url,
        )
        session.flush()
        raise MispExportError(
            "MISP export replay blocked for this canonical revision; inspect prior delivery evidence before retry"
        )

    item.metadata_json = {
        **item.metadata_json,
        "misp_exports": [
            *existing,
            {
                "replay_key": replay_key,
                "event_uuid": event_uuid,
                "status": "pending",
                "requested_by": principal.subject,
                "distribution": str(distribution),
                "sharing_group_id": sharing_group_id,
                "tlp": normalized_tlp,
                "request_id": request_id,
            },
        ],
    }
    session.flush()
    return PreparedMispExport(item.id, replay_key, event_uuid, payload)


def finalize_misp_export(
    session: Session,
    *,
    prepared: PreparedMispExport,
    principal: Principal,
    request_id: str,
    misp_event_id: str | None,
) -> MispExportResult:
    item = session.scalar(
        select(IntelligenceItem).where(IntelligenceItem.id == prepared.item_id).with_for_update()
    )
    if item is None:
        raise MispExportError("intelligence item disappeared during MISP export")
    records = _export_records(item)
    updated = False
    for record in records:
        if record.get("replay_key") == prepared.replay_key and record.get("status") == "pending":
            record["status"] = "success"
            record["misp_event_id"] = misp_event_id
            updated = True
            break
    if not updated:
        raise MispExportError("MISP export reservation is missing")
    item.metadata_json = {**item.metadata_json, "misp_exports": records}
    event = append_persistent_audit_event(
        session,
        principal=principal.subject,
        principal_type="human",
        action="intelligence.misp_export",
        resource=f"intelligence:{item.id}",
        decision=AuditDecision.ALLOW,
        request_id=request_id,
        provenance_reference=item.canonical_url,
    )
    session.flush()
    return MispExportResult(item.id, prepared.replay_key, prepared.event_uuid, misp_event_id, event.event_id)


def mark_misp_export_uncertain(
    session: Session,
    *,
    prepared: PreparedMispExport,
    principal: Principal,
    request_id: str,
) -> None:
    item = session.scalar(
        select(IntelligenceItem).where(IntelligenceItem.id == prepared.item_id).with_for_update()
    )
    if item is None:
        return
    records = _export_records(item)
    for record in records:
        if record.get("replay_key") == prepared.replay_key and record.get("status") == "pending":
            record["status"] = "uncertain"
            break
    item.metadata_json = {**item.metadata_json, "misp_exports": records}
    append_persistent_audit_event(
        session,
        principal=principal.subject,
        principal_type="human",
        action="intelligence.misp_export",
        resource=f"intelligence:{item.id}",
        decision=AuditDecision.DENY,
        request_id=request_id,
        provenance_reference=item.canonical_url,
    )
    session.flush()


async def deliver_misp_event(
    prepared: PreparedMispExport,
    *,
    settings: Settings,
    client: httpx.AsyncClient,
) -> str | None:
    base = settings.misp_api_base.rstrip("/")
    api_key = settings.misp_api_key.get_secret_value().strip()
    if not base or not api_key:
        raise MispExportError("MISP export requires configured runtime endpoint and API key")
    if settings.production and not base.startswith("https://"):
        raise MispExportError("production MISP export requires HTTPS")

    response = await client.post(
        f"{base}/events/add",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": api_key,
        },
        json=prepared.payload,
    )
    response.raise_for_status()
    body = response.json()
    if not isinstance(body, dict):
        raise MispExportError("MISP events/add returned unsupported JSON")
    event = body.get("Event")
    if not isinstance(event, dict):
        response_value = body.get("response")
        event = response_value.get("Event") if isinstance(response_value, dict) else None
    if not isinstance(event, dict):
        raise MispExportError("MISP events/add response contains no Event object")
    response_uuid = event.get("uuid")
    if response_uuid is not None and str(response_uuid) != prepared.event_uuid:
        raise MispExportError("MISP response UUID does not match deterministic export UUID")
    event_id = event.get("id")
    return str(event_id) if event_id is not None else None
