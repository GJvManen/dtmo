from __future__ import annotations

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from dtmo.audit import AuditDecision
from dtmo.audit.store import (
    append_persistent_audit_event,
    load_audit_chain,
    verify_persistent_audit_chain,
)
from dtmo.persistence.audit_models import AuditEventRecord
from dtmo.persistence.models import Base


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def test_persistent_append_preserves_transactional_chain_continuity() -> None:
    with _session() as session:
        first = append_persistent_audit_event(
            session,
            principal="analyst@example.test",
            principal_type="human",
            action="intelligence.review",
            resource="intelligence:item-1",
            decision=AuditDecision.ALLOW,
            request_id="request-1",
            provenance_reference="source:1",
        )
        second = append_persistent_audit_event(
            session,
            principal="publisher@example.test",
            principal_type="human",
            action="intelligence.share_approve",
            resource="intelligence:item-1",
            decision=AuditDecision.ALLOW,
            request_id="request-2",
            provenance_reference="source:1",
        )
        session.commit()

        records = session.scalars(
            select(AuditEventRecord).order_by(AuditEventRecord.sequence_number)
        ).all()
        assert [record.sequence_number for record in records] == [1, 2]
        assert second.previous_hash == first.event_hash
        assert verify_persistent_audit_chain(session) == (True, None)


def test_rollback_does_not_advance_persisted_chain() -> None:
    with _session() as session:
        append_persistent_audit_event(
            session,
            principal="analyst@example.test",
            principal_type="human",
            action="intelligence.review",
            resource="intelligence:item-1",
            decision=AuditDecision.ALLOW,
            request_id="request-1",
        )
        session.rollback()
        assert load_audit_chain(session) == []

        event = append_persistent_audit_event(
            session,
            principal="analyst@example.test",
            principal_type="human",
            action="intelligence.review",
            resource="intelligence:item-1",
            decision=AuditDecision.ALLOW,
            request_id="request-2",
        )
        session.commit()
        record = session.scalar(select(AuditEventRecord))
        assert record is not None
        assert record.sequence_number == 1
        assert record.event_hash == event.event_hash


def test_database_tampering_is_detected_by_chain_verification() -> None:
    with _session() as session:
        append_persistent_audit_event(
            session,
            principal="analyst@example.test",
            principal_type="human",
            action="intelligence.review",
            resource="intelligence:item-1",
            decision=AuditDecision.ALLOW,
            request_id="request-1",
        )
        session.commit()
        record = session.scalar(select(AuditEventRecord))
        assert record is not None
        record.principal = "attacker@example.test"
        session.commit()
        valid, reason = verify_persistent_audit_chain(session)
        assert not valid
        assert reason == "event hash mismatch at position 0"
