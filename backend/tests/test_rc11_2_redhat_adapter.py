from __future__ import annotations

import pytest

from dtmo.redhat_adapter import REDHAT_EXECUTION_PROFILE, parse_redhat_csaf_ids
from dtmo.source_catalog import catalog_by_id
from dtmo.source_executor import SourceExecutionError
from dtmo.source_framework import SOURCE_ADAPTER_REGISTRY, execute_source
from dtmo.sources import SourceDefinition


def _source() -> SourceDefinition:
    return SourceDefinition(
        id="redhat-security",
        name="Red Hat Product Security",
        source_type="json-feed",
        endpoint_url="https://access.redhat.com/hydra/rest/securitydata",
        enabled=True,
        interval_seconds=3600,
        reliability="authoritative",
        secret_ref=None,
        created_by="admin",
        updated_by="admin",
    )


def test_redhat_catalog_and_framework_contract() -> None:
    source = catalog_by_id("redhat-security")
    assert source is not None
    assert source.execution_status == "supported"
    assert source.execution_profile == REDHAT_EXECUTION_PROFILE
    assert source.endpoint_url == "https://access.redhat.com/hydra/rest/securitydata"
    spec = SOURCE_ADAPTER_REGISTRY.get(REDHAT_EXECUTION_PROFILE)
    assert spec is not None
    assert spec.execution_kind == "anonymous"
    assert spec.requires_secret is False


def test_redhat_index_is_bounded_deduplicated_and_fail_closed() -> None:
    payload = [{"RHSA": f"RHSA-2026:{index:05d}"} for index in range(1, 40)]
    payload.insert(1, {"RHSA": "RHSA-2026:00001"})
    identifiers = parse_redhat_csaf_ids(payload)
    assert len(identifiers) == 25
    assert identifiers[0] == "RHSA-2026:00001"
    assert len(set(identifiers)) == len(identifiers)
    with pytest.raises(SourceExecutionError, match="must be a list"):
        parse_redhat_csaf_ids({"RHSA": "RHSA-2026:00001"})
    with pytest.raises(SourceExecutionError, match="no usable RHSA"):
        parse_redhat_csaf_ids([{"RHSA": "not-an-rhsa"}])


@pytest.mark.asyncio
async def test_redhat_framework_dispatch_fetches_index_and_csaf(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    def fake_fetch(url: str, *, timeout: float):
        calls.append(url)
        assert timeout == 20.0
        if "/csaf.json?" in url:
            assert "created_days_ago=10" in url
            assert "per_page=25" in url
            assert "isCompressed=false" in url
            return [{"RHSA": "RHSA-2026:12345"}]
        assert url.endswith("/csaf/RHSA-2026:12345.json?isCompressed=false")
        return {
            "document": {
                "title": "Red Hat security advisory",
                "tracking": {
                    "id": "RHSA-2026:12345",
                    "initial_release_date": "2026-08-11T00:00:00Z",
                },
                "notes": [
                    {
                        "category": "summary",
                        "title": "Topic",
                        "text": "A Red Hat security update is available.",
                    }
                ],
            },
            "vulnerabilities": [{"cve": "CVE-2026-12345"}],
        }

    monkeypatch.setattr("dtmo.redhat_adapter._fetch_json_sync", fake_fetch)
    result = await execute_source(_source())
    assert result.status == "completed"
    assert result.error is None
    assert len(result.records) == 1
    assert result.records[0].external_id == "RHSA-2026:12345"
    assert result.records[0].raw["document"]["tracking"]["id"] == "RHSA-2026:12345"
    assert len(calls) == 2


@pytest.mark.asyncio
async def test_redhat_tracking_mismatch_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_fetch(url: str, *, timeout: float):
        if "/csaf.json?" in url:
            return [{"RHSA": "RHSA-2026:12345"}]
        return {
            "document": {
                "title": "Mismatched advisory",
                "tracking": {"id": "RHSA-2026:99999"},
            }
        }

    monkeypatch.setattr("dtmo.redhat_adapter._fetch_json_sync", fake_fetch)
    result = await execute_source(_source())
    assert result.status == "failed"
    assert result.records == []
    assert "does not match" in str(result.error)
