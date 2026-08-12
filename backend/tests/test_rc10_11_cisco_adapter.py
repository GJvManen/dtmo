from __future__ import annotations

import pytest

from dtmo.credentialed_source_executor import (
    CREDENTIALED_EXECUTION_PROFILES,
    _resolve_secret,
    execute_source,
    parse_cisco_openvuln,
)
from dtmo.source_catalog import CISCO_CREDENTIAL_REFERENCE, catalog_by_id
from dtmo.source_executor import SourceExecutionError
from dtmo.sources import SourceDefinition, validate_secret_ref

API_FIXTURE_VALUE = "fixture-value"


def _cisco_source(*, enabled: bool = True, secret_ref: str | None = None) -> SourceDefinition:
    return SourceDefinition(
        id="cisco-security-advisories",
        name="Cisco Security Advisories",
        source_type="json-feed",
        endpoint_url="https://apix.cisco.com/security/advisories/v2",
        enabled=enabled,
        interval_seconds=3600,
        reliability="authoritative",
        secret_ref=secret_ref if secret_ref is not None else CISCO_CREDENTIAL_REFERENCE,
        created_by="admin",
        updated_by="admin",
    )


def test_cisco_catalog_contract_is_supported_and_credential_referenced() -> None:
    source = catalog_by_id("cisco-security-advisories")
    assert source is not None
    assert source.endpoint_url == "https://apix.cisco.com/security/advisories/v2"
    assert source.execution_profile == "cisco-openvuln-v2"
    assert source.execution_status == "supported"
    assert source.secret_ref == CISCO_CREDENTIAL_REFERENCE
    assert validate_secret_ref(source.secret_ref) == CISCO_CREDENTIAL_REFERENCE
    assert source.execution_profile in CREDENTIALED_EXECUTION_PROFILES


def test_cisco_parser_normalizes_advisory_and_preserves_raw() -> None:
    payload = {
        "advisories": [
            {
                "advisoryId": "cisco-sa-example-1234",
                "advisoryTitle": "Cisco Example Vulnerability",
                "publicationUrl": "https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-example-1234",
                "summary": "Example Cisco advisory.",
                "firstPublished": "2026-08-11T00:00:00",
                "sir": "High",
                "csafUrl": "https://sec.cloudapps.cisco.com/example.json",
            }
        ]
    }
    records = parse_cisco_openvuln(payload, reliability="authoritative")
    assert len(records) == 1
    assert records[0].external_id == "cisco-sa-example-1234"
    assert records[0].title == "Cisco Example Vulnerability"
    assert records[0].confidence == 95
    assert records[0].raw == payload["advisories"][0]


def test_cisco_parser_fails_closed_on_missing_advisories() -> None:
    with pytest.raises(SourceExecutionError, match="advisories list"):
        parse_cisco_openvuln({"items": []}, reliability="authoritative")
    with pytest.raises(SourceExecutionError, match="no usable advisories"):
        parse_cisco_openvuln({"advisories": [{"advisoryId": "invalid"}]}, reliability="authoritative")


def test_secret_reference_is_fail_closed_and_legacy_env_ref_normalizes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CISCO_OPENVULN_TOKEN", raising=False)
    with pytest.raises(SourceExecutionError, match="not available"):
        _resolve_secret(CISCO_CREDENTIAL_REFERENCE)
    unsupported_reference = "plain:" + "fixture"
    with pytest.raises(SourceExecutionError, match="unsupported"):
        _resolve_secret(unsupported_reference)
    monkeypatch.setenv("CISCO_OPENVULN_TOKEN", API_FIXTURE_VALUE)
    assert _resolve_secret("env://CISCO_OPENVULN_TOKEN") == API_FIXTURE_VALUE


@pytest.mark.asyncio
async def test_cisco_dispatch_uses_credentialed_executor(monkeypatch: pytest.MonkeyPatch) -> None:
    source = _cisco_source()
    monkeypatch.setenv("CISCO_OPENVULN_TOKEN", API_FIXTURE_VALUE)

    def fake_fetch(url: str, *, token: str, timeout: float):
        assert url.endswith("/latest/25?summaryDetails=true&productNames=true")
        assert token == API_FIXTURE_VALUE
        assert timeout == 20.0
        return [
            {
                "advisoryId": "cisco-sa-dispatch-1234",
                "advisoryTitle": "Dispatch advisory",
                "publicationUrl": "https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-dispatch-1234",
                "summary": "Dispatch test",
            }
        ]

    monkeypatch.setattr("dtmo.credentialed_source_executor._fetch_json_bearer_sync", fake_fetch)
    result = await execute_source(source)
    assert result.status == "completed"
    assert len(result.records) == 1
    assert result.records[0].external_id == "cisco-sa-dispatch-1234"
