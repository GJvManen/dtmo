from __future__ import annotations

import httpx
import pytest
from pydantic import SecretStr, ValidationError

from dtmo.config import Settings
from dtmo.integrations.intelowl import IntelOwlAdapter, IntelOwlPolicyError


def _settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "environment": "test",
        "intelowl_api_base": "https://intelowl.example.test",
        "intelowl_api_token": SecretStr("read-enrich-token"),
        "intelowl_allowed_analyzers": "VirusTotal,Shodan",
        "intelowl_max_poll_attempts": 3,
        "intelowl_poll_interval_seconds": 0,
    }
    values.update(overrides)
    return Settings(**values)


@pytest.mark.asyncio
async def test_bounded_enrichment_disables_connectors_and_preserves_provenance() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "POST":
            return httpx.Response(200, json={"job_id": 77})
        return httpx.Response(
            200,
            json={
                "job_id": 77,
                "status": "finished",
                "reports": [{"analyzer_name": "VirusTotal", "status": "success", "report": {"verdict": "malicious"}}],
            },
        )

    adapter = IntelOwlAdapter(_settings())
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await adapter.enrich(
            client,
            canonical_id="indicator:1",
            observable_type="domain",
            observable_value="example.test",
            handling="green",
            analyzers=["VirusTotal"],
            external_analyzers={"VirusTotal"},
        )

    assert result.job_id == "77"
    assert result.partial is False
    assert result.reports[0]["local_compromise_proven"] is False
    assert result.raw["_dtmo_intelowl"]["external_share_authorized"] is False
    assert requests[0].headers["Authorization"] == "Token read-enrich-token"
    assert b'"connectors_requested":[]' in requests[0].content


def test_allowlist_and_handling_fail_closed_before_network() -> None:
    adapter = IntelOwlAdapter(_settings())
    with pytest.raises(IntelOwlPolicyError, match="allowlist"):
        adapter._validate_request(
            observable_type="domain",
            observable_value="example.test",
            handling="green",
            analyzers=["Unapproved"],
        )
    with pytest.raises(IntelOwlPolicyError, match="forbids external"):
        adapter._validate_request(
            observable_type="domain",
            observable_value="example.test",
            handling="TLP:RED",
            analyzers=["VirusTotal"],
            external_analyzers={"VirusTotal"},
        )
    with pytest.raises(IntelOwlPolicyError, match="not approved"):
        adapter._validate_request(
            observable_type="email",
            observable_value="person@example.test",
            handling="green",
            analyzers=["VirusTotal"],
        )


@pytest.mark.asyncio
async def test_unknown_analyzer_and_job_identity_mismatch_fail_closed() -> None:
    adapter = IntelOwlAdapter(_settings())
    with pytest.raises(IntelOwlPolicyError, match="unknown analyzer"):
        adapter._normalize_job(
            canonical_id="indicator:1",
            observable_type="ip",
            observable_value="192.0.2.1",
            expected_job_id="4",
            payload={"job_id": 4, "status": "finished", "reports": [{"analyzer_name": "Unknown"}]},
            analyzers=["VirusTotal"],
        )
    with pytest.raises(IntelOwlPolicyError, match="identity mismatch"):
        adapter._normalize_job(
            canonical_id="indicator:1",
            observable_type="ip",
            observable_value="192.0.2.1",
            expected_job_id="4",
            payload={"job_id": 5, "status": "finished", "reports": []},
            analyzers=["VirusTotal"],
        )


def test_partial_success_is_explicit_not_fabricated_success() -> None:
    adapter = IntelOwlAdapter(_settings())
    result = adapter._normalize_job(
        canonical_id="indicator:1",
        observable_type="hash",
        observable_value="a" * 64,
        expected_job_id="8",
        payload={
            "job_id": 8,
            "status": "finished",
            "reports": [
                {"analyzer_name": "VirusTotal", "status": "success"},
                {"analyzer_name": "Shodan", "status": "failed"},
            ],
        },
        analyzers=["VirusTotal", "Shodan"],
    )
    assert result.partial is True
    assert result.status == "finished"


@pytest.mark.asyncio
async def test_429_and_timeout_are_bounded_http_failures() -> None:
    adapter = IntelOwlAdapter(_settings(intelowl_max_poll_attempts=1))

    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(429))) as client:
        with pytest.raises(httpx.HTTPStatusError):
            await adapter.enrich(
                client,
                canonical_id="indicator:1",
                observable_type="domain",
                observable_value="example.test",
                handling="green",
                analyzers=["VirusTotal"],
            )

    calls = 0
    def pending(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if request.method == "POST":
            return httpx.Response(200, json={"job_id": 9})
        return httpx.Response(200, json={"job_id": 9, "status": "running", "reports": []})

    async with httpx.AsyncClient(transport=httpx.MockTransport(pending)) as client:
        with pytest.raises(IntelOwlPolicyError, match="polling exceeded"):
            await adapter.enrich(
                client,
                canonical_id="indicator:1",
                observable_type="domain",
                observable_value="example.test",
                handling="green",
                analyzers=["VirusTotal"],
            )
    assert calls == 2


def test_production_requires_https_token_and_analyzer_allowlist() -> None:
    base: dict[str, object] = {
        "environment": "production",
        "minio_secure": True,
        "minio_secret_key": SecretStr("object-secret"),
        "jwt_jwks_json": SecretStr('{"keys":[{"kty":"RSA","kid":"test"}]}'),
        "privacy_pseudonymization_secret": SecretStr("x" * 32),
        "feature_intelowl_enrichment": True,
    }
    with pytest.raises(ValidationError, match="HTTPS"):
        Settings(**base, intelowl_api_base="http://intelowl.internal", intelowl_api_token=SecretStr("token"), intelowl_allowed_analyzers="VT")
    with pytest.raises(ValidationError, match="runtime API token"):
        Settings(**base, intelowl_api_base="https://intelowl.internal", intelowl_api_token=SecretStr(""), intelowl_allowed_analyzers="VT")
    with pytest.raises(ValidationError, match="analyzer allowlist"):
        Settings(**base, intelowl_api_base="https://intelowl.internal", intelowl_api_token=SecretStr("token"), intelowl_allowed_analyzers="")
