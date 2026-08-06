from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum

from dtmo.audit.chain import AuditEvent


class EvidenceDisposition(StrEnum):
    KEEP = "keep"
    EXPIRE = "expire"
    LEGAL_HOLD = "legal_hold"


@dataclass(frozen=True, slots=True)
class MinimizedAuditEvidence:
    event_id: str
    occurred_at: datetime
    principal_reference: str
    principal_type: str
    action: str
    resource_reference: str
    decision: str
    request_reference: str
    event_hash: str
    disposition: EvidenceDisposition


def _require_aware(value: datetime, name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return value.astimezone(UTC)


def _reference(value: str, *, secret: bytes, purpose: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{purpose} value is required")
    digest = hmac.new(secret, f"{purpose}:{normalized}".encode(), hashlib.sha256).hexdigest()
    return f"{purpose}:v1:{digest}"


def retention_disposition(
    *,
    occurred_at: datetime,
    now: datetime,
    retention_days: int,
    legal_hold: bool = False,
) -> EvidenceDisposition:
    if retention_days < 1:
        raise ValueError("retention days must be at least one")
    occurred = _require_aware(occurred_at, "occurred_at")
    current = _require_aware(now, "now")
    if legal_hold:
        return EvidenceDisposition.LEGAL_HOLD
    if occurred > current:
        raise ValueError("evidence occurrence cannot be in the future")
    expires_at = occurred + timedelta(days=retention_days)
    return EvidenceDisposition.EXPIRE if current >= expires_at else EvidenceDisposition.KEEP


def minimize_audit_event(
    event: AuditEvent,
    *,
    secret: bytes,
    now: datetime,
    retention_days: int,
    legal_hold: bool = False,
) -> MinimizedAuditEvidence:
    if len(secret) < 32:
        raise ValueError("privacy pseudonymization secret must be at least 32 bytes")
    disposition = retention_disposition(
        occurred_at=event.occurred_at,
        now=now,
        retention_days=retention_days,
        legal_hold=legal_hold,
    )
    return MinimizedAuditEvidence(
        event_id=str(event.event_id),
        occurred_at=event.occurred_at.astimezone(UTC),
        principal_reference=_reference(event.principal, secret=secret, purpose="principal"),
        principal_type=event.principal_type,
        action=event.action,
        resource_reference=_reference(event.resource, secret=secret, purpose="resource"),
        decision=event.decision.value,
        request_reference=_reference(event.request_id, secret=secret, purpose="request"),
        event_hash=event.event_hash,
        disposition=disposition,
    )
