from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from dtmo.audit.chain import AuditDecision, append_audit_event
from dtmo.persistence.models import Base
from dtmo.persistence.privacy_models import MinimizedAuditProjectionRecord
from dtmo.privacy import minimize_audit_event
from dtmo.privacy.store import persist_minimized_projection, purge_expired_projections

SECRET = b"p" * 32


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def _evidence(*, occurred_at: datetime):
    event = append_audit_event(
        (),
        principal="analyst@example.test",
        principal_type="human",
        action="authorization.denied",
        resource="/api/v1/audit",
        decision=AuditDecision.DENY,
        request_id="request-1",
        occurred_at=occurred_at,
    )
    return minimize_audit_event(
        event,
        secret=SECRET,
        now=occurred_at + timedelta(minutes=1),
        retention_days=30,
    )


def test_persist_is_idempotent_and_does_not_store_direct_identifiers() -> None:
    now = datetime(2026, 8, 6, tzinfo=UTC)
    evidence = _evidence(occurred_at=now - timedelta(days=1))
    with _session() as session:
        first = persist_minimized_projection(
            session, evidence=evidence, retention_days=30, legal_hold=False, now=now
        )
        second = persist_minimized_projection(
            session, evidence=evidence, retention_days=30, legal_hold=False, now=now
        )
        session.commit()
        records = session.scalars(select(MinimizedAuditProjectionRecord)).all()

    assert first.event_id == second.event_id
    assert len(records) == 1
    serialized = repr(records[0].__dict__)
    assert "analyst@example.test" not in serialized
    assert "/api/v1/audit" not in serialized
    assert "request-1" not in serialized


def test_purge_deletes_only_expired_non_held_projections() -> None:
    now = datetime(2026, 8, 6, tzinfo=UTC)
    expired = _evidence(occurred_at=now - timedelta(days=31))
    held = _evidence(occurred_at=now - timedelta(days=32))
    active = _evidence(occurred_at=now - timedelta(days=2))
    with _session() as session:
        persist_minimized_projection(session, evidence=expired, retention_days=30, legal_hold=False, now=now)
        persist_minimized_projection(session, evidence=held, retention_days=30, legal_hold=True, now=now)
        persist_minimized_projection(session, evidence=active, retention_days=30, legal_hold=False, now=now)
        result = purge_expired_projections(session, now=now)
        session.commit()
        remaining = session.scalars(select(MinimizedAuditProjectionRecord)).all()

    assert result.deleted == 1
    assert result.retained_on_legal_hold == 1
    assert {str(record.event_id) for record in remaining} == {held.event_id, active.event_id}


def test_existing_projection_can_only_escalate_to_legal_hold() -> None:
    now = datetime(2026, 8, 6, tzinfo=UTC)
    evidence = _evidence(occurred_at=now - timedelta(days=1))
    with _session() as session:
        record = persist_minimized_projection(
            session, evidence=evidence, retention_days=30, legal_hold=False, now=now
        )
        persist_minimized_projection(
            session, evidence=evidence, retention_days=30, legal_hold=True, now=now
        )
        session.commit()
        assert record.legal_hold is True
