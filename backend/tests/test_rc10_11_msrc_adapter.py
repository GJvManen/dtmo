import pytest

from dtmo.msrc_adapter import MSRCAdapterError, parse_msrc_cvrf_document, parse_msrc_update_ids
from dtmo.source_catalog import catalog_by_id
from dtmo.source_executor import SUPPORTED_REGISTRY_EXECUTION_PROFILES


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
    assert record.source_reliability == "authoritative"
    assert record.confidence == 95
    assert record.raw == payload


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
