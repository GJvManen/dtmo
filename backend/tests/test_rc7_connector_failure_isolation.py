from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from dtmo.connectors.health import (
    ConnectorIsolatedError,
    evaluate_connector_execution,
    require_connector_execution,
)
from dtmo.connectors.state import ConnectorRuntimeState, ConnectorStateStore
from dtmo.persistence.models import Base


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def _record_failure(store: ConnectorStateStore, connector_id: str, observed_at: datetime) -> None:
    store.record_run(
        connector_id=connector_id,
        run_id=uuid4(),
        succeeded=False,
        duration_seconds=1.0,
        record_count=0,
        quarantined=[],
        error_code="upstream_unavailable",
        observed_at=observed_at,
    )


def test_repeated_failures_open_a_bounded_connector_local_circuit() -> None:
    with _session() as session:
        store = ConnectorStateStore(session, failure_threshold=3, isolation_minutes=15)
        started = datetime(2026, 8, 7, 13, 0, tzinfo=UTC)
        for offset in range(3):
            _record_failure(store, "cisa-kev", started + timedelta(minutes=offset))

        decision = evaluate_connector_execution(store, "cisa-kev", now=started + timedelta(minutes=3))

        assert decision.allowed is False
        assert decision.reason == "circuit_open"
        assert decision.health_status == "isolated"
        assert decision.consecutive_failures == 3
        assert decision.retry_at == started + timedelta(minutes=17)
        assert decision.publish_approved is False
        assert len(store.health_history("cisa-kev")) == 3


def test_isolated_source_cannot_block_an_independent_connector() -> None:
    with _session() as session:
        store = ConnectorStateStore(session, failure_threshold=1, isolation_minutes=15)
        observed = datetime(2026, 8, 7, 13, 0, tzinfo=UTC)
        _record_failure(store, "cisa-kev", observed)

        isolated = evaluate_connector_execution(store, "cisa-kev", now=observed + timedelta(minutes=1))
        independent = evaluate_connector_execution(store, "nvd", now=observed + timedelta(minutes=1))

        assert isolated.allowed is False
        assert independent.allowed is True
        assert independent.reason == "no_health_history"
        assert independent.connector_id == "nvd"
        assert independent.publish_approved is False


def test_execution_guard_fails_closed_while_circuit_is_open() -> None:
    with _session() as session:
        store = ConnectorStateStore(session, failure_threshold=1, isolation_minutes=15)
        observed = datetime(2026, 8, 7, 13, 0, tzinfo=UTC)
        _record_failure(store, "cisa-kev", observed)

        with pytest.raises(ConnectorIsolatedError) as exc_info:
            require_connector_execution(store, "cisa-kev", now=observed + timedelta(minutes=1))

        assert exc_info.value.decision.reason == "circuit_open"
        assert exc_info.value.decision.publish_approved is False


def test_expired_isolation_allows_recovery_probe_without_publication_approval() -> None:
    with _session() as session:
        store = ConnectorStateStore(session, failure_threshold=1, isolation_minutes=15)
        observed = datetime(2026, 8, 7, 13, 0, tzinfo=UTC)
        _record_failure(store, "cisa-kev", observed)

        decision = require_connector_execution(store, "cisa-kev", now=observed + timedelta(minutes=16))

        assert decision.allowed is True
        assert decision.reason == "recovery_probe"
        assert decision.publish_approved is False


def test_health_decision_handles_naive_persisted_circuit_timestamp_as_utc() -> None:
    with _session() as session:
        session.add(
            ConnectorRuntimeState(
                connector_id="cisa-kev",
                consecutive_failures=3,
                circuit_open_until=datetime(2026, 8, 7, 13, 15),
                health_status="isolated",
                updated_at=datetime(2026, 8, 7, 13, 0),
            )
        )
        session.commit()
        store = ConnectorStateStore(session)

        decision = evaluate_connector_execution(
            store,
            "cisa-kev",
            now=datetime(2026, 8, 7, 13, 5, tzinfo=UTC),
        )

        assert decision.allowed is False
        assert decision.retry_at == datetime(2026, 8, 7, 13, 15, tzinfo=UTC)
        assert decision.publish_approved is False


def test_blank_connector_id_is_rejected() -> None:
    with _session() as session:
        store = ConnectorStateStore(session)
        with pytest.raises(ValueError, match="connector_id is required"):
            evaluate_connector_execution(store, "   ")
