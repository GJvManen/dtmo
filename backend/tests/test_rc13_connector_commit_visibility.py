from __future__ import annotations

from collections.abc import AsyncIterator

import pytest

import dtmo.api.routes as routes_module
from dtmo.api.schemas import IntelligenceIngestResponse
from dtmo.connectors.base import ConnectorRecord


def _record() -> ConnectorRecord:
    return ConnectorRecord(
        external_id="CVE-2026-COMMIT",
        object_type="vulnerability",
        title="Commit visibility fixture",
        url="https://example.invalid/CVE-2026-COMMIT",
        summary="Connector persistence must commit before success is returned.",
        published_at="2026-08-12",
        source_reliability="authoritative",
        confidence=98,
        raw={"cveID": "CVE-2026-COMMIT"},
    )


class _CommitAwareDatabase:
    def __init__(self, *, fail_commit: bool = False) -> None:
        self.committed = False
        self.fail_commit = fail_commit
        self.session_object = object()

    async def session(self) -> AsyncIterator[object]:
        yield self.session_object
        if self.fail_commit:
            raise RuntimeError("synthetic commit failure")
        self.committed = True


@pytest.mark.asyncio
async def test_connector_ingest_returns_only_after_session_commit(monkeypatch: pytest.MonkeyPatch) -> None:
    database = _CommitAwareDatabase()
    persistence_observations: list[bool] = []

    async def fake_persist(*args: object, **kwargs: object) -> IntelligenceIngestResponse:
        del args, kwargs
        persistence_observations.append(database.committed)
        return IntelligenceIngestResponse(
            id="11111111-1111-1111-1111-111111111111",
            inserted=True,
            review_status="candidate",
            share_approved=False,
            raw_object_key="raw/CVE-2026-COMMIT.json",
            raw_sha256="a" * 64,
            indexed=True,
        )

    monkeypatch.setattr(routes_module, "database", database)
    monkeypatch.setattr(routes_module, "_persist_intelligence", fake_persist)

    receipt = await routes_module.ingest_connector_record("cisa-kev", _record())

    assert persistence_observations == [False]
    assert database.committed is True
    assert receipt.inserted is True
    assert receipt.indexed is True


@pytest.mark.asyncio
async def test_connector_ingest_never_reports_success_when_commit_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    database = _CommitAwareDatabase(fail_commit=True)

    async def fake_persist(*args: object, **kwargs: object) -> IntelligenceIngestResponse:
        del args, kwargs
        return IntelligenceIngestResponse(
            id="22222222-2222-2222-2222-222222222222",
            inserted=True,
            review_status="candidate",
            share_approved=False,
            raw_object_key="raw/CVE-2026-COMMIT.json",
            raw_sha256="b" * 64,
            indexed=True,
        )

    monkeypatch.setattr(routes_module, "database", database)
    monkeypatch.setattr(routes_module, "_persist_intelligence", fake_persist)

    with pytest.raises(RuntimeError, match="synthetic commit failure"):
        await routes_module.ingest_connector_record("cisa-kev", _record())

    assert database.committed is False
