from __future__ import annotations

from datetime import datetime, timezone

import pytest

import dtmo.main as main_module
from dtmo.api.schemas import IntelligenceIngestResponse
from dtmo.connectors.base import ConnectorRecord, ConnectorResult


def _record(external_id: str) -> ConnectorRecord:
    return ConnectorRecord(
        external_id=external_id,
        object_type="vulnerability",
        title=f"Example {external_id}",
        url="https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
        summary="Known exploited vulnerability",
        published_at="2026-08-10",
        source_reliability="authoritative",
        confidence=98,
        raw={"cveID": external_id},
    )


class _NoopConnectorStateStore:
    """Keep this unit contract scoped to connector -> canonical ingest behavior.

    Built-in runtime-state persistence is integration-tested against PostgreSQL by the
    dedicated Automation recovery journey. These legacy unit tests intentionally run
    without a database service and therefore replace only that additional observability
    store while retaining the real connector result aggregation path.
    """

    def __init__(self, session: object) -> None:
        del session

    def record_run(self, **kwargs: object) -> None:
        del kwargs


def _isolate_runtime_state_persistence(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main_module, "ConnectorStateStore", _NoopConnectorStateStore)


@pytest.mark.asyncio
async def test_cisa_run_persists_and_indexes_every_fetched_record(monkeypatch: pytest.MonkeyPatch) -> None:
    records = [_record("CVE-2026-0001"), _record("CVE-2026-0002")]
    now = datetime.now(timezone.utc).isoformat()

    async def fake_run(self: object) -> ConnectorResult:
        del self
        return ConnectorResult(
            connector_id="cisa-kev",
            started_at=now,
            finished_at=now,
            records=records,
            attempts=1,
            status="completed",
        )

    calls: list[tuple[str, str]] = []

    async def fake_ingest(connector_id: str, record: ConnectorRecord) -> IntelligenceIngestResponse:
        calls.append((connector_id, record.external_id))
        return IntelligenceIngestResponse(
            id=record.external_id,
            inserted=True,
            review_status="candidate",
            share_approved=False,
            raw_object_key=f"raw/{record.external_id}",
            raw_sha256="a" * 64,
            indexed=True,
        )

    monkeypatch.setattr(main_module.CisaKevConnector, "run", fake_run)
    monkeypatch.setattr(main_module, "ingest_connector_record", fake_ingest)
    _isolate_runtime_state_persistence(monkeypatch)

    result = await main_module.run_cisa_kev()

    assert calls == [
        ("cisa-kev", "CVE-2026-0001"),
        ("cisa-kev", "CVE-2026-0002"),
    ]
    assert result["status"] == "completed"
    assert result["records"] == 2
    assert result["inserted"] == 2
    assert result["indexed"] == 2


@pytest.mark.asyncio
async def test_failed_connector_run_never_ingests_records(monkeypatch: pytest.MonkeyPatch) -> None:
    now = datetime.now(timezone.utc).isoformat()

    async def fake_run(self: object) -> ConnectorResult:
        del self
        return ConnectorResult(
            connector_id="cisa-kev",
            started_at=now,
            finished_at=now,
            records=[],
            attempts=4,
            status="failed",
            error="upstream unavailable",
        )

    async def unexpected_ingest(connector_id: str, record: ConnectorRecord) -> IntelligenceIngestResponse:
        raise AssertionError(f"unexpected ingest: {connector_id} {record.external_id}")

    monkeypatch.setattr(main_module.CisaKevConnector, "run", fake_run)
    monkeypatch.setattr(main_module, "ingest_connector_record", unexpected_ingest)
    _isolate_runtime_state_persistence(monkeypatch)

    result = await main_module.run_cisa_kev()

    assert result["status"] == "failed"
    assert result["inserted"] == 0
    assert result["indexed"] == 0
