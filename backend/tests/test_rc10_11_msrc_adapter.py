import pytest

from dtmo.msrc_adapter import MSRCAdapterError, parse_msrc_cvrf_document, parse_msrc_update_ids
from dtmo.source_catalog import catalog_by_id
from dtmo.source_executor import SUPPORTED_REGISTRY_EXECUTION_PROFILES, execute_registered_source
from dtmo.sources import SourceDefinition


def _msrc_source(*, enabled: bool = True) -> SourceDefinition:
    return SourceDefinition(
        id="msrc-security-update-guide",
        name="Microsoft Security Response Center",
        source_type="json-feed",
        endpoint_url="https://api.msrc.microsoft.com/cvrf/v3.0",
        enabled=enabled,
        interval_seconds=3600,
        reliability="authoritative",
        secret_ref=None,
        created_by="admin",
        updated_by="admin",
    )


def test_msrc_catalog_source_is_executable() -> None:
    source = catalog_by_id("msrc-security-update-guide")
    assert source is not None
    assert source.endpoint_url == "https://api.msrc.microsoft.com/cvrf/v3.0"
    assert source.execution_profile == "msrc-cvrf-v3"
    assert source.execution_status == "supported"
    assert source.execution_profile in SUPPORTED_REGISTRY_EXECUTION_PROFILES


def test_msrc_update_discovery_is_bounded_and_validated() -> None:
    payload = {
        "value": [
            {
                "ID": f"2026-{month}",
                "CurrentReleaseDate": f"2026-{index:02d}-10T00:00:00Z",
            }
            for index, month in enumerate(
                ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan"],
                start=1,
            )
        ]
    }
    ids = parse_msrc_update_ids(payload)
    assert len(ids) <= 12
    assert all(value.startswith("2026-") for value in ids)


def test_msrc_update_discovery_skips_invalid_entries_and_deduplicates() -> None:
    payload = {
        "value": [
            None,
            {"ID": "invalid", "CurrentReleaseDate": "2026-12-01"},
            {"ID": "2026-Aug", "CurrentReleaseDate": "2026-08-12"},
            {"id": "2026-aug", "currentReleaseDate": "2026-08-11"},
            {"ID": "2026-jul", "CurrentReleaseDate": "2026-07-10"},
        ]
    }
    assert parse_msrc_update_ids(payload) == ["2026-aug", "2026-jul"]


def test_msrc_update_discovery_rejects_empty_valid_set() -> None:
    with pytest.raises(MSRCAdapterError, match="no valid CVRF"):
        parse_msrc_update_ids({"value": [{"ID": "bad"}, "not-a-record"]})


def test_msrc_cvrf_normalizes_update_and_preserves_raw_provenance() -> None:
    payload = {
        "DocumentTitle": {"Value": "August 2026 Security Updates"},
        "DocumentTracking": {"CurrentReleaseDate": "2026-08-11T00:00:00Z"},
        "DocumentNotes": [{"Value": "Microsoft security update release."}],
        "Vulnerability": [{"CVE": "CVE-2026-12345"}],
    }
    record = parse_msrc_cvrf_document(
        payload,
        update_id="2026-aug",
        reliability="authoritative",
        document_url="https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/2026-aug",
    )
    assert record.external_id == "MSRC-2026-aug"
    assert record.object_type == "security-advisory"
    assert record.title == "August 2026 Security Updates"
    assert record.summary == "Microsoft security update release."
    assert record.published_at == "2026-08-11T00:00:00Z"
    assert record.source_reliability == "authoritative"
    assert record.confidence == 95
    assert record.raw == payload


def test_msrc_cvrf_supports_string_title_lowercase_note_and_initial_release() -> None:
    payload = {
        "DocumentTitle": "Monthly release",
        "DocumentTracking": {"InitialReleaseDate": "2026-07-01T00:00:00Z"},
        "DocumentNotes": [{"value": "Lowercase note field"}],
        "ProductTree": {"FullProductName": []},
    }
    record = parse_msrc_cvrf_document(
        payload,
        update_id="2026-jul",
        reliability="authoritative",
        document_url="https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/2026-jul",
    )
    assert record.title == "Monthly release"
    assert record.summary == "Lowercase note field"
    assert record.published_at == "2026-07-01T00:00:00Z"


def test_msrc_cvrf_uses_safe_fallbacks_when_optional_metadata_is_absent() -> None:
    payload = {"Vulnerability": [{"CVE": "CVE-2026-1"}]}
    record = parse_msrc_cvrf_document(
        payload,
        update_id="2026-jun",
        reliability="authoritative",
        document_url="https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/2026-jun",
    )
    assert record.title == "Microsoft Security Update 2026-jun"
    assert record.summary == "Microsoft Security Response Center CVRF security update."
    assert record.published_at is None


def test_msrc_adapter_fails_closed_on_invalid_shapes() -> None:
    with pytest.raises(MSRCAdapterError):
        parse_msrc_update_ids({"items": []})
    with pytest.raises(MSRCAdapterError):
        parse_msrc_cvrf_document(
            {},
            update_id="bad-id",
            reliability="authoritative",
            document_url="https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/bad-id",
        )
    with pytest.raises(MSRCAdapterError, match="JSON object"):
        parse_msrc_cvrf_document(
            [],
            update_id="2026-aug",
            reliability="authoritative",
            document_url="https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/2026-aug",
        )
    with pytest.raises(MSRCAdapterError, match="no vulnerability or product data"):
        parse_msrc_cvrf_document(
            {"DocumentTitle": "Empty update"},
            update_id="2026-aug",
            reliability="authoritative",
            document_url="https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/2026-aug",
        )


@pytest.mark.asyncio
async def test_msrc_executor_dispatches_updates_and_cvrf_documents(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    def fake_fetch(url: str, *, timeout: float) -> object:
        calls.append(url)
        assert timeout == 20.0
        if url.endswith("/updates"):
            return {"value": [{"ID": "2026-aug", "CurrentReleaseDate": "2026-08-11"}]}
        if url.endswith("/cvrf/2026-aug"):
            return {
                "DocumentTitle": {"Value": "August 2026 Security Updates"},
                "Vulnerability": [{"CVE": "CVE-2026-12345"}],
            }
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr("dtmo.source_executor._fetch_json_sync", fake_fetch)
    result = await execute_registered_source(_msrc_source())
    assert result.status == "completed"
    assert len(result.records) == 1
    assert result.records[0].external_id == "MSRC-2026-aug"
    assert calls == [
        "https://api.msrc.microsoft.com/cvrf/v3.0/updates",
        "https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/2026-aug",
    ]


@pytest.mark.asyncio
async def test_msrc_executor_returns_failed_result_for_invalid_discovery(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "dtmo.source_executor._fetch_json_sync",
        lambda url, *, timeout: {"value": []},
    )
    result = await execute_registered_source(_msrc_source())
    assert result.status == "failed"
    assert result.records == []
    assert result.error is not None
    assert "no valid CVRF document IDs" in result.error
