from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from dtmo.audit.chain import AuditDecision, AuditEvent, append_audit_event
from dtmo.persistence.audit_models import AuditEventRecord
from dtmo.persistence.models import Base
from dtmo.persistence.privacy_models import AuditProjectionRecord
from dtmo.privacy.store import (
    purge_expired_projections,
    set_projection_legal_hold,
    store_minimized_projection,
)

SECRET = b"p" * 32


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def _event(session: Session, *, occurred_at: datetime) -> AuditEvent:
    event = append_audit_event(
        (),
        principal="analyst@example.test",
        principal_type="human",
        action="token.revoke",
        resource="token:jti:sensitive-token-id",
        decision=AuditDecision.ALLOW,
        request_id="request-sensitive-id",
        provenance_reference='{"reason":"credential theft"}',
        occurred_at=occurred_at,
    )
    sequence = int(session.scalar(select(func.count()).select_from(AuditEventRecord)) or 0) + 1
    session.add(
        AuditEventRecord(
            sequence_number=sequence,
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


def test_projection_storage_excludes_direct_identifiers_and_is_idempotent() -> None:
    now = datetime(2026, 8, 6, tzinfo=UTC)
    with _session() as session:
        event = _event(session, occurred_at=now - timedelta(days=1))
        first = store_minimized_projection(
            session, event=event, secret=SECRET, retention_days=90, now=now
        )
        second = store_minimized_projection(
            session, event=event, secret=SECRET, retention_days=90, now=now
        )
        assert first.source_event_id == second.source_event_id
        serialized = repr(first)
        assert "analyst@example.test" not in serialized
        assert "sensitive-token-id" not in serialized
        assert "request-sensitive-id" not in serialized
        assert first.retention_expires_at == event.occurred_at + timedelta(days=90)


def test_purge_removes_only_expired_non_held_projections_and_preserves_source_audit() -> None:
    now = datetime(2026, 8, 6, tzinfo=UTC)
    with _session() as session:
        expired_event = _event(session, occurred_at=now - timedelta(days=91))
        held_event = _event(session, occurred_at=now - timedelta(days=91, seconds=1))
        active_event = _event(session, occurred_at=now - timedelta(days=1))
        expired = store_minimized_projection(
            session, event=expired_event, secret=SECRET, retention_days=90, now=now
        )
        held = store_minimized_projection(
            session,
            event=held_event,
            secret=SECRET,
            retention_days=90,
            legal_hold=True,
            legal_hold_reference="case-2026-0042",
            now=now,
        )
        active = store_minimized_projection(
            session, event=active_event, secret=SECRET, retention_days=90, now=now
        )
        result = purge_expired_projections(session, now=now)
        session.flush()

        remaining = set(session.scalars(select(AuditProjectionRecord.source_event_id)))
        source_ids = set(session.scalars(select(AuditEventRecord.event_id)))
        assert result.deleted == 1
        assert expired.source_event_id not in remaining
        assert held.source_event_id in remaining
        assert active.source_event_id in remaining
        assert {expired.source_event_id, held.source_event_id, active.source_event_id} <= source_ids


def test_legal_hold_can_be_released_before_purge() -> None:
    now = datetime(2026, 8, 6, tzinfo=UTC)
    with _session() as session:
        event = _event(session, occurred_at=now - timedelta(days=91))
        projection = store_minimized_projection(
            session, event=event, secret=SECRET, retention_days=90, now=now
        )
        held = set_projection_legal_hold(
            session,
            source_event_id=projection.source_event_id,
            enabled=True,
            reference="legal-2026-17",
        )
        assert held.legal_hold
        assert purge_expired_projections(session, now=now).deleted == 0

        released = set_projection_legal_hold(
            session,
            source_event_id=projection.source_event_id,
            enabled=False,
            reference=None,
        )
        assert not released.legal_hold
        assert purge_expired_projections(session, now=now).deleted == 1


def test_purge_is_bounded_by_batch_size() -> None:
    now = datetime(2026, 8, 6, tzinfo=UTC)
    with _session() as session:
        for offset in range(3):
            event = _event(
                session,
                occurred_at=now - timedelta(days=91, seconds=offset),
            )
            store_minimized_projection(
                session, event=event, secret=SECRET, retention_days=90, now=now
            )
        assert purge_expired_projections(session, now=now, batch_size=2).deleted == 2
        remaining = session.scalar(select(func.count()).select_from(AuditProjectionRecord))
        assert remaining == 1
