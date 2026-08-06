from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Iterable
from uuid import UUID, uuid4

GENESIS_HASH = "0" * 64


class AuditDecision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    RECORD = "record"


@dataclass(frozen=True, slots=True)
class AuditEvent:
    event_id: UUID
    occurred_at: datetime
    principal: str
    principal_type: str
    action: str
    resource: str
    decision: AuditDecision
    request_id: str
    provenance_reference: str | None
    previous_hash: str
    event_hash: str
    schema_version: int = 1


def _canonical_payload(event: AuditEvent) -> bytes:
    payload = asdict(event)
    payload.pop("event_hash")
    payload["event_id"] = str(event.event_id)
    payload["occurred_at"] = event.occurred_at.astimezone(UTC).isoformat(timespec="microseconds")
    payload["decision"] = event.decision.value
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def calculate_event_hash(event: AuditEvent) -> str:
    return hashlib.sha256(_canonical_payload(event)).hexdigest()


def append_audit_event(
    events: Iterable[AuditEvent],
    *,
    principal: str,
    principal_type: str,
    action: str,
    resource: str,
    decision: AuditDecision,
    request_id: str,
    provenance_reference: str | None = None,
    occurred_at: datetime | None = None,
    event_id: UUID | None = None,
) -> AuditEvent:
    existing = tuple(events)
    previous_hash = existing[-1].event_hash if existing else GENESIS_HASH
    unsigned = AuditEvent(
        event_id=event_id or uuid4(),
        occurred_at=occurred_at or datetime.now(UTC),
        principal=principal.strip(),
        principal_type=principal_type.strip(),
        action=action.strip(),
        resource=resource.strip(),
        decision=decision,
        request_id=request_id.strip(),
        provenance_reference=provenance_reference,
        previous_hash=previous_hash,
        event_hash="",
    )
    if not all((unsigned.principal, unsigned.principal_type, unsigned.action, unsigned.resource, unsigned.request_id)):
        raise ValueError("audit identity, action, resource and request ID are required")
    return AuditEvent(**{**asdict(unsigned), "event_hash": calculate_event_hash(unsigned)})


def verify_audit_chain(events: Iterable[AuditEvent]) -> tuple[bool, str | None]:
    expected_previous = GENESIS_HASH
    seen_event_ids: set[UUID] = set()
    for position, event in enumerate(events):
        if event.event_id in seen_event_ids:
            return False, f"duplicate event_id at position {position}"
        seen_event_ids.add(event.event_id)
        if event.previous_hash != expected_previous:
            return False, f"broken previous_hash at position {position}"
        if event.event_hash != calculate_event_hash(event):
            return False, f"event hash mismatch at position {position}"
        expected_previous = event.event_hash
    return True, None
