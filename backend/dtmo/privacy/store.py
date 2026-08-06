from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from dtmo.audit.chain import AuditEvent
from dtmo.persistence.privacy_models import AuditProjectionRecord

from .evidence import minimize_audit_event


@dataclass(frozen=True, slots=True)
class PurgeResult:
    deleted: int
    cutoff: datetime


def store_minimized_projection(
    session: Session,
    *,
    event: AuditEvent,
    secret: bytes,
    retention_days: int,
    legal_hold: bool = False,
    legal_hold_reference: str | None = None,
    now: datetime | None = None,
) -> AuditProjectionRecord:
    current = (now or datetime.now(UTC)).astimezone(UTC)
    hold_reference = legal_hold_reference.strip() if legal_hold_reference else None
    if legal_hold and not hold_reference:
        raise ValueError("legal hold reference is required")
    if not legal_hold and hold_reference:
        raise ValueError("legal hold reference requires an active legal hold")

    minimized = minimize_audit_event(
        event,
        secret=secret,
        now=current,
        retention_days=retention_days,
        legal_hold=legal_hold,
    )
    source_event_id = UUID(minimized.event_id)
    existing = session.get(AuditProjectionRecord, source_event_id)
    if existing is not None:
        if existing.source_event_hash != minimized.event_hash:
            raise ValueError("projection source hash does not match existing record")
        return existing

    record = AuditProjectionRecord(
        source_event_id=source_event_id,
        occurred_at=minimized.occurred_at,
        principal_reference=minimized.principal_reference,
        principal_type=minimized.principal_type,
        action=minimized.action,
        resource_reference=minimized.resource_reference,
        decision=minimized.decision,
        request_reference=minimized.request_reference,
        source_event_hash=minimized.event_hash,
        retention_expires_at=minimized.occurred_at + timedelta(days=retention_days),
        legal_hold=legal_hold,
        legal_hold_reference=hold_reference,
        created_at=current,
    )
    session.add(record)
    session.flush()
    return record


def set_projection_legal_hold(
    session: Session,
    *,
    source_event_id: UUID,
    enabled: bool,
    reference: str | None,
) -> AuditProjectionRecord:
    record = session.get(AuditProjectionRecord, source_event_id, with_for_update=True)
    if record is None:
        raise LookupError("audit projection not found")
    normalized = reference.strip() if reference else None
    if enabled and not normalized:
        raise ValueError("legal hold reference is required")
    if not enabled and normalized:
        raise ValueError("legal hold reference must be empty when hold is disabled")
    record.legal_hold = enabled
    record.legal_hold_reference = normalized
    session.flush()
    return record


def purge_expired_projections(
    session: Session,
    *,
    now: datetime | None = None,
    batch_size: int = 500,
) -> PurgeResult:
    if batch_size < 1 or batch_size > 10_000:
        raise ValueError("batch size must be between 1 and 10000")
    cutoff = (now or datetime.now(UTC)).astimezone(UTC)
    identifiers = list(
        session.scalars(
            select(AuditProjectionRecord.source_event_id)
            .where(
                AuditProjectionRecord.retention_expires_at <= cutoff,
                AuditProjectionRecord.legal_hold.is_(False),
            )
            .order_by(AuditProjectionRecord.retention_expires_at)
            .limit(batch_size)
            .with_for_update(skip_locked=True)
        )
    )
    if not identifiers:
        return PurgeResult(deleted=0, cutoff=cutoff)
    result = session.execute(
        delete(AuditProjectionRecord).where(AuditProjectionRecord.source_event_id.in_(identifiers))
    )
    return PurgeResult(deleted=int(result.rowcount or 0), cutoff=cutoff)
