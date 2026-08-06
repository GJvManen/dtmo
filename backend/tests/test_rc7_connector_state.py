from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from dtmo.connectors.state import (
    ConnectorHealthEvent,
    ConnectorQuarantineRecord,
    ConnectorRuntimeState,
    ConnectorStateStore,
    QuarantineInput,
)
from dtmo.persistence.models import Base


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def test_failures_are_persisted_and_isolate_only_the_failing_connector() -> None:
    with _session() as session:
        store = ConnectorStateStore(session, failure_threshold=3, isolation_minutes=15)
        observed = datetime(2026, 8, 6, 15, 0, tzinfo=UTC)
        for offset in range(3):
            store.record_run(
                connector_id="cisa-kev",
                run_id=uuid4(),
                succeeded=False,
                duration_seconds=1.2,
                record_count=0,
                quarantined=[],
                error_code="upstream_unavailable",
                observed_at=observed + timedelta(minutes=offset),
            )
        store.record_run(
            connector_id="nvd",
            run_id=uuid4(),
            succeeded=True,
            duration_seconds=0.4,
            record_count=5,
            quarantined=[],
            observed_at=observed,
        )

        cisa = session.get(ConnectorRuntimeState, "cisa-kev")
        nvd = session.get(ConnectorRuntimeState, "nvd")
        assert cisa is not None and cisa.health_status == "isolated"
        assert cisa.consecutive_failures == 3
        assert store.is_isolated("cisa-kev", now=observed + timedelta(minutes=3))
        assert nvd is not None and nvd.health_status == "healthy"
        assert not store.is_isolated("nvd", now=observed + timedelta(minutes=3))
        assert len(store.health_history("cisa-kev")) == 3


def test_quarantine_recovery_requires_human_review_and_never_publishes() -> None:
    with _session() as session:
        store = ConnectorStateStore(session)
        run_id = uuid4()
        store.record_run(
            connector_id="cisa-kev",
            run_id=run_id,
            succeeded=True,
            duration_seconds=0.5,
            record_count=1,
            quarantined=[QuarantineInput("malformed_record", {"cveID": None})],
        )
        record = session.scalar(select(ConnectorQuarantineRecord))
        assert record is not None
        assert record.recovery_status == "pending"
        assert record.publish_approved is False

        with pytest.raises(ValueError, match="human reviewer"):
            store.recover_quarantine(
                record.id,
                decision="released_to_candidate",
                human_reviewer="service:connector",
                review_reference="REV-1",
            )

        recovered = store.recover_quarantine(
            record.id,
            decision="released_to_candidate",
            human_reviewer="analyst@example.org",
            review_reference="REV-1",
        )
        assert recovered.recovery_status == "released_to_candidate"
        assert recovered.publish_approved is False
        assert recovered.recovered_by == "analyst@example.org"

        event = session.scalar(select(ConnectorHealthEvent))
        assert event is not None and event.publish_approved is False


def test_success_closes_isolation_and_resets_failure_count() -> None:
    with _session() as session:
        store = ConnectorStateStore(session, failure_threshold=1)
        store.record_run(
            connector_id="cisa-kev",
            run_id=uuid4(),
            succeeded=False,
            duration_seconds=1,
            record_count=0,
            quarantined=[],
        )
        state = store.record_run(
            connector_id="cisa-kev",
            run_id=uuid4(),
            succeeded=True,
            duration_seconds=1,
            record_count=2,
            quarantined=[],
        )
        assert state.health_status == "healthy"
        assert state.consecutive_failures == 0
        assert state.circuit_open_until is None
