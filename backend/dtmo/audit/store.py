from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from dtmo.persistence.audit_models import AuditEventRecord

from .chain import AuditDecision, AuditEvent, append_audit_event, verify_audit_chain


class AuditChainConflict(RuntimeError):
    """Raised when the persisted chain changed during an append transaction."""


def _to_event(record: AuditEventRecord) -> AuditEvent:
    return AuditEvent(
        event_id=record.event_id,
        occurred_at=record.occurred_at,
        principal=record.principal,
        principal_type=record.principal_type,
        action=record.action,
        resource=record.resource,
        decision=AuditDecision(record.decision),
        request_id=record.request_id,
        provenance_reference=record.provenance_reference,
        previous_hash=record.previous_hash,
        event_hash=record.event_hash,
        schema_version=record.schema_version,
    )


def load_audit_chain(session: Session) -> list[AuditEvent]:
    records = session.scalars(
        select(AuditEventRecord).order_by(AuditEventRecord.sequence_number)
    ).all()
    return [_to_event(record) for record in records]


def append_persistent_audit_event(
    session: Session,
    *,
    principal: str,
    principal_type: str,
    action: str,
    resource: str,
    decision: AuditDecision,
    request_id: str,
    provenance_reference: str | None = None,
) -> AuditEvent:
    latest = session.scalar(
        select(AuditEventRecord)
        .order_by(AuditEventRecord.sequence_number.desc())
        .limit(1)
        .with_for_update()
    )
    existing: Sequence[AuditEvent] = () if latest is None else (_to_event(latest),)
    event = append_audit_event(
        existing,
        principal=principal,
        principal_type=principal_type,
        action=action,
        resource=resource,
        decision=decision,
        request_id=request_id,
        provenance_reference=provenance_reference,
    )
    sequence_number = 1 if latest is None else latest.sequence_number + 1
    session.add(
        AuditEventRecord(
            sequence_number=sequence_number,
            event_id=event.event_id,
            occurred_at=event.occurred_at,
            principal=event.principal,
            principal_type=event.principal_type,
            action=event.action,
            resource=event.resource,
            decision=event.decision.value,
            request_id=event.request_id,
            provenance_reference=event.provenance_reference,
            previous_hash=event.previous_hash,
            event_hash=event.event_hash,
            schema_version=event.schema_version,
        )
    )
    session.flush()
    return event


def verify_persistent_audit_chain(session: Session) -> tuple[bool, str | None]:
    return verify_audit_chain(load_audit_chain(session))
