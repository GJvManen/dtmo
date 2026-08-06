from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from dtmo.persistence.privacy_models import MinimizedAuditProjectionRecord

from .evidence import MinimizedAuditEvidence


@dataclass(frozen=True, slots=True)
class PurgeResult:
    deleted: int
    retained_on_legal_hold: int


def persist_minimized_projection(
    session: Session,
    *,
    evidence: MinimizedAuditEvidence,
    retention_days: int,
    legal_hold: bool,
    now: datetime | None = None,
) -> MinimizedAuditProjectionRecord:
    if retention_days < 1:
        raise ValueError("retention days must be at least one")
    current = (now or datetime.now(UTC)).astimezone(UTC)
    expires_at = evidence.occurred_at.astimezone(UTC) + timedelta(days=retention_days)
    existing = session.get(MinimizedAuditProjectionRecord, UUID(evidence.event_id))
    if existing is not None:
        if existing.source_event_hash != evidence.event_hash:
            raise ValueError("projection event identity conflicts with source evidence")
        if legal_hold and not existing.legal_hold:
            existing.legal_hold = True
        return existing
    record = MinimizedAuditProjectionRecord(
        event_id=UUID(evidence.event_id),
        occurred_at=evidence.occurred_at.astimezone(UTC),
        principal_reference=evidence.principal_reference,
        principal_type=evidence.principal_type,
        action=evidence.action,
        resource_reference=evidence.resource_reference,
        decision=evidence.decision,
        request_reference=evidence.request_reference,
        source_event_hash=evidence.event_hash,
        expires_at=expires_at,
        legal_hold=legal_hold,
        created_at=current,
    )
    session.add(record)
    session.flush()
    return record


def purge_expired_projections(session: Session, *, now: datetime | None = None) -> PurgeResult:
    current = (now or datetime.now(UTC)).astimezone(UTC)
    held = session.scalar(
        select(MinimizedAuditProjectionRecord)
        .where(
            MinimizedAuditProjectionRecord.expires_at <= current,
            MinimizedAuditProjectionRecord.legal_hold.is_(True),
        )
        .with_only_columns(MinimizedAuditProjectionRecord.event_id)
    )
    held_count = 0 if held is None else 1
    result = session.execute(
        delete(MinimizedAuditProjectionRecord).where(
            MinimizedAuditProjectionRecord.expires_at <= current,
            MinimizedAuditProjectionRecord.legal_hold.is_(False),
        )
    )
    return PurgeResult(deleted=int(result.rowcount or 0), retained_on_legal_hold=held_count)
