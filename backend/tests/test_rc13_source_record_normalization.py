from __future__ import annotations

from collections.abc import AsyncIterator

import pytest

import dtmo.api.routes as routes_module
from dtmo.api.schemas import IntelligenceIngestRequest, IntelligenceIngestResponse
from dtmo.connectors.base import ConnectorRecord


class _CommitAwareDatabase:
    def __init__(self) -> None:
        self.committed = False
        self.session_object = object()

    async def session(self) -> AsyncIterator[object]:
        yield self.session_object
        self.committed = True


def _advisory_record(*, url: str = "https://example.invalid/advisory") -> ConnectorRecord:
    return ConnectorRecord(
        external_id="ADVISORY-2026-1",
        object_type="security-advisory",
        title="Advisory normalization fixture",
        url=url,
        summary="Supported advisory aliases must map to the canonical enum.",
        published_at="2026-08-12",
        source_reliability="authoritative",
        confidence=96,
        raw={"kind": "security-advisory"},
    )


def test_supported_advisory_alias_normalizes_to_canonical_enum() -> None:
    assert routes_module._normalize_connector_item_type("security-advisory") == "advisory"
    assert routes_module._normalize_connector_item_type("advisory") == "advisory"
    assert routes_module._normalize_connector_item_type("vulnerability") == "vulnerability"


def test_unknown_connector_item_type_fails_closed() -> None:
    with pytest.raises(ValueError, match="unsupported connector item type"):
        routes_module._normalize_connector_item_type("threat-intelligence")


def test_nvd_uses_stable_https_canonical_url_even_when_raw_reference_is_ftp() -> None:
    record = ConnectorRecord(
        external_id="CVE-2000-0388",
        object_type="vulnerability",
        title="CVE-2000-0388",
        url="ftp://ftp.freebsd.org/pub/FreeBSD/CERT/advisories/example.asc",
        summary="Historical NVD record with a non-HTTP upstream reference.",
        published_at="2000-05-01",
        source_reliability="authoritative",
        confidence=94,
        raw={"references": [{"url": "ftp://ftp.freebsd.org/pub/FreeBSD/CERT/advisories/example.asc"}]},
    )

    assert routes_module._canonical_connector_url("nvd-cve", record) == (
        "https://nvd.nist.gov/vuln/detail/CVE-2000-0388"
    )
    assert record.raw["references"][0]["url"].startswith("ftp://")


@pytest.mark.asyncio
async def test_connector_normalization_occurs_before_canonical_validation_and_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = _CommitAwareDatabase()
    observed: list[IntelligenceIngestRequest] = []
    record = ConnectorRecord(
        external_id="CVE-2000-0388",
        object_type="security-advisory",
        title="NVD normalization fixture",
        url="ftp://ftp.freebsd.org/pub/FreeBSD/CERT/advisories/example.asc",
        summary="Both canonical type and URL require bounded normalization.",
        published_at="2000-05-01",
        source_reliability="authoritative",
        confidence=94,
        raw={"references": [{"url": "ftp://ftp.freebsd.org/pub/FreeBSD/CERT/advisories/example.asc"}]},
    )

    async def fake_persist(
        request: IntelligenceIngestRequest,
        *,
        actor_subject: str,
        session: object,
    ) -> IntelligenceIngestResponse:
        assert actor_subject == "connector:nvd-cve"
        assert session is database.session_object
        observed.append(request)
        return IntelligenceIngestResponse(
            id="33333333-3333-3333-3333-333333333333",
            inserted=True,
            review_status="candidate",
            share_approved=False,
            raw_object_key="raw/CVE-2000-0388.json",
            raw_sha256="c" * 64,
            indexed=True,
        )

    monkeypatch.setattr(routes_module, "database", database)
    monkeypatch.setattr(routes_module, "_persist_intelligence", fake_persist)

    receipt = await routes_module.ingest_connector_record("nvd-cve", record)

    assert receipt.inserted is True
    assert database.committed is True
    assert len(observed) == 1
    request = observed[0]
    assert request.item_type == "advisory"
    assert str(request.canonical_url) == "https://nvd.nist.gov/vuln/detail/CVE-2000-0388"
    assert str(request.provenance[0].source_url) == "https://nvd.nist.gov/vuln/detail/CVE-2000-0388"
    assert request.raw_payload["references"][0]["url"].startswith("ftp://")
