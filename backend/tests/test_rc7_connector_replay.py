from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from dtmo.connectors.provenance import IngestionContext, normalize_connector_records
from dtmo.connectors.replay import ConnectorReplayClaim, ConnectorReplayStore
from dtmo.persistence.models import Base


def test_cross_run_replay_is_quarantined_and_never_publishes() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    raw = {"cveID": "CVE-2026-4321", "dateAdded": "2026-08-07"}

    with Session(engine) as session:
        replay = ConnectorReplayStore(session)
        first = normalize_connector_records(
            [raw],
            context=IngestionContext(
                connector_id="cisa-kev",
                run_id=uuid4(),
                source_uri="https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
                fetched_at=datetime(2026, 8, 7, 8, 0, tzinfo=UTC),
                confidence=95,
            ),
            external_id_field="cveID",
            source_timestamp_field="dateAdded",
            replay_registry=replay,
        )
        session.commit()
        assert len(first.candidates) == 1
        assert first.publish_approved is False

        second = normalize_connector_records(
            [raw],
            context=IngestionContext(
                connector_id="cisa-kev",
                run_id=uuid4(),
                source_uri="https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
                fetched_at=datetime(2026, 8, 7, 9, 0, tzinfo=UTC),
                confidence=95,
            ),
            external_id_field="cveID",
            source_timestamp_field="dateAdded",
            replay_registry=replay,
        )
        assert second.candidates == ()
        assert len(second.quarantined) == 1
        assert second.quarantined[0].reason == "replayed_record"
        assert second.quarantined[0].publish_approved is False
        claims = list(session.scalars(select(ConnectorReplayClaim)))
        assert len(claims) == 1
        assert claims[0].publish_approved is False


def test_materially_changed_payload_is_not_suppressed_as_replay() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        replay = ConnectorReplayStore(session)
        context_one = IngestionContext(
            connector_id="cisa-kev",
            run_id=uuid4(),
            source_uri="https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
            fetched_at=datetime(2026, 8, 7, 8, 0, tzinfo=UTC),
            confidence=95,
        )
        first = normalize_connector_records(
            [{"cveID": "CVE-2026-4321", "dateAdded": "2026-08-07", "action": "old"}],
            context=context_one,
            external_id_field="cveID",
            replay_registry=replay,
        )
        session.commit()
        assert len(first.candidates) == 1

        second = normalize_connector_records(
            [{"cveID": "CVE-2026-4321", "dateAdded": "2026-08-07", "action": "updated"}],
            context=IngestionContext(
                connector_id="cisa-kev",
                run_id=uuid4(),
                source_uri=context_one.source_uri,
                fetched_at=datetime(2026, 8, 7, 9, 0, tzinfo=UTC),
                confidence=95,
            ),
            external_id_field="cveID",
            replay_registry=replay,
        )
        assert len(second.candidates) == 1
        assert second.quarantined == ()
