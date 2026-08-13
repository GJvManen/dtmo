from __future__ import annotations

from typing import Any

import pytest
from fastapi import HTTPException

from dtmo.admin_sources import SourceCreateRequest, _authentication_mode, _validate_manual_auth_contract
from dtmo.connectors.base import ConnectorResult
from dtmo.source_executor import SourceExecutionError
from dtmo.source_onboarding import test_manual_source as run_manual_source_test
from dtmo.source_onboarding_experience import _PAGE, _SCRIPT, router
from dtmo.sources import SourceDefinition


def _manual_source(*, enabled: bool = False, secret_ref: str | None = None) -> SourceDefinition:
    return SourceDefinition(
        id="sector-feed",
        name="Sector feed",
        source_type="json-feed",
        endpoint_url="https://example.org/feed.json",
        enabled=enabled,
        interval_seconds=3600,
        reliability="medium",
        secret_ref=secret_ref,
        created_by="admin-tester",
        updated_by="admin-tester",
    )


def test_canonical_sources_surface_exposes_disabled_first_onboarding() -> None:
    assert 'id="source-onboarding"' in _PAGE
    assert "Nieuwe intelligencebron registreren" in _PAGE
    assert "Disabled-first" in _PAGE
    assert "Schedule / freshness" in _PAGE
    assert "Authentication mode" in _PAGE
    assert "Logical secret reference" in _PAGE
    assert "Owner" in _PAGE
    assert "pre-activation test" in _PAGE.lower()
    assert "/ui/source-onboarding-experience.js" in _PAGE
    assert 'id="source-enabled"' not in _PAGE


def test_onboarding_script_never_creates_an_enabled_source() -> None:
    assert "enabled: false" in _SCRIPT
    assert "/api/v1/admin/sources'" in _SCRIPT
    assert "/validate`" in _SCRIPT
    assert "/test`" in _SCRIPT
    assert "JSON.stringify({enabled:true})" in _SCRIPT
    assert "validated !== true || checks.tested !== true" in _SCRIPT
    assert "result.ingested === false" in _SCRIPT


def test_source_response_authentication_mode_and_owner_are_truthful() -> None:
    anonymous = _manual_source()
    credentialed = _manual_source(secret_ref="env:SOURCE_TOKEN")
    assert _authentication_mode(anonymous) == "anonymous"
    assert _authentication_mode(credentialed) == "credentialed-secret-reference"
    assert anonymous.created_by == "admin-tester"


def test_manual_credential_reference_requires_code_reviewed_adapter() -> None:
    request = SourceCreateRequest(
        id="sector-feed",
        name="Sector feed",
        source_type="json-feed",
        endpoint_url="https://example.org/feed.json",
        enabled=False,
        interval_seconds=3600,
        reliability="medium",
        secret_ref="env:SOURCE_TOKEN",
    )
    with pytest.raises(HTTPException) as exc_info:
        _validate_manual_auth_contract(request)
    assert exc_info.value.status_code == 400
    assert "code-reviewed registered adapter" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_disabled_manual_source_can_be_pretested_without_activation_or_ingest(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = _manual_source(enabled=False)

    def fake_fetch(url: str, *, timeout: float) -> dict[str, Any]:
        assert url == source.endpoint_url
        assert timeout == 3.0
        return {
            "items": [
                {
                    "external_id": "TEST-1",
                    "title": "Test advisory",
                    "url": "https://example.org/advisories/1",
                    "summary": "Pre-activation parser check",
                    "confidence": 80,
                }
            ]
        }

    monkeypatch.setattr("dtmo.source_onboarding._fetch_json_sync", fake_fetch)
    result = await run_manual_source_test(source, timeout_seconds=3.0)

    assert isinstance(result, ConnectorResult)
    assert result.status == "completed"
    assert len(result.records) == 1
    assert source.enabled is False


@pytest.mark.asyncio
async def test_catalog_supported_source_cannot_bypass_governed_adapter_with_pretest() -> None:
    source = SourceDefinition(
        id="nvd-cve",
        name="NVD",
        source_type="json-feed",
        endpoint_url="https://services.nvd.nist.gov/rest/json/cves/2.0",
        enabled=False,
        interval_seconds=3600,
        reliability="authoritative",
        secret_ref=None,
        created_by="admin-tester",
        updated_by="admin-tester",
    )
    with pytest.raises(SourceExecutionError, match="governed adapter execution path"):
        await run_manual_source_test(source)


def test_source_onboarding_router_owns_canonical_console_roots() -> None:
    routes = [route for route in router.routes if route.path in {"/", "/ui/console"}]
    assert {route.path for route in routes} == {"/", "/ui/console"}
    assert all(route.endpoint.__module__ == "dtmo.source_onboarding_experience" for route in routes)
