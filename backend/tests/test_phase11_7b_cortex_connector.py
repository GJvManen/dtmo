from __future__ import annotations

import httpx
import pytest
from pydantic import SecretStr, ValidationError

from dtmo.config import Settings
from dtmo.integrations.cortex import CortexAdapter, CortexPolicyError


def _settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "environment": "test",
        "cortex_api_base": "https://cortex.example.test",
        "cortex_api_token": SecretStr("analyze-token"),
        "cortex_allowed_analyzers": "VirusTotal_GetReport_3_0,Shodan_Host_1_0",
        "cortex_wait_seconds": 2,
    }
    values.update(overrides)
    return Settings(**values)


@pytest.mark.asyncio
async def test_analyzer_only_connector_uses_bearer_auth_and_preserves_authority() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "POST":
            return httpx.Response(200, json={"id": "job-7", "analyzerId": "VirusTotal_GetReport_3_0", "status": "Waiting"})
        return httpx.Response(
            200,
            json={
                "id": "job-7",
                "analyzerId": "VirusTotal_GetReport_3_0",
                "status": "Success",
                "report": {"summary": {"taxonomies": [{"level": "malicious"}]}, "full": {"score": 90}},
            },
        )

    adapter = CortexAdapter(_settings())
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await adapter.analyze(
            client,
            canonical_id="indicator:7",
            observable_type="domain",
            observable_value="example.test",
            analyzer_id="VirusTotal_GetReport_3_0",
            tlp=1,
        )

    assert result.job_id == "job-7"
    assert result.status == "success"
    assert result.report["external_share_authorized"] is False
    assert result.report["local_compromise_proven"] is False
    assert result.raw["_dtmo_cortex"]["responders_allowed"] is False
    assert requests[0].headers["Authorization"] == "Bearer analyze-token"
    assert requests[0].url.path == "/api/analyzer/VirusTotal_GetReport_3_0/run"
    assert requests[1].url.path == "/api/job/job-7/waitreport"


def test_request_policy_fails_closed_on_unapproved_analyzer_type_and_tlp() -> None:
    adapter = CortexAdapter(_settings())
    with pytest.raises(CortexPolicyError, match="allowlist"):
        adapter._validate_request(observable_type="domain", observable_value="example.test", analyzer_id="Unknown", tlp=1)
    with pytest.raises(CortexPolicyError, match="not approved"):
        adapter._validate_request(observable_type="mail", observable_value="person@example.test", analyzer_id="VirusTotal_GetReport_3_0", tlp=1)
    with pytest.raises(CortexPolicyError, match="TLP"):
        adapter._validate_request(observable_type="domain", observable_value="example.test", analyzer_id="VirusTotal_GetReport_3_0", tlp=9)


def test_result_identity_mismatch_fails_closed() -> None:
    adapter = CortexAdapter(_settings())
    with pytest.raises(CortexPolicyError, match="job identity mismatch"):
        adapter._normalize_report(
            canonical_id="indicator:1",
            observable_type="ip",
            observable_value="192.0.2.1",
            analyzer_id="Shodan_Host_1_0",
            expected_job_id="expected",
            payload={"id": "other", "analyzerId": "Shodan_Host_1_0", "status": "Success", "report": {}},
        )
    with pytest.raises(CortexPolicyError, match="analyzer identity mismatch"):
        adapter._normalize_report(
            canonical_id="indicator:1",
            observable_type="ip",
            observable_value="192.0.2.1",
            analyzer_id="Shodan_Host_1_0",
            expected_job_id="job",
            payload={"id": "job", "analyzerId": "Other", "status": "Success", "report": {}},
        )


def test_production_requires_https_token_and_explicit_analyzer_allowlist() -> None:
    base: dict[str, object] = {
        "environment": "production",
        "minio_secure": True,
        "minio_secret_key": SecretStr("object-secret"),
        "jwt_jwks_json": SecretStr('{"keys":[{"kty":"RSA","kid":"test"}]}'),
        "privacy_pseudonymization_secret": SecretStr("x" * 32),
        "feature_cortex_analysis": True,
    }
    with pytest.raises(ValidationError, match="HTTPS"):
        Settings(**base, cortex_api_base="http://cortex.internal", cortex_api_token=SecretStr("token"), cortex_allowed_analyzers="VT")
    with pytest.raises(ValidationError, match="runtime API token"):
        Settings(**base, cortex_api_base="https://cortex.internal", cortex_api_token=SecretStr(""), cortex_allowed_analyzers="VT")
    with pytest.raises(ValidationError, match="analyzer allowlist"):
        Settings(**base, cortex_api_base="https://cortex.internal", cortex_api_token=SecretStr("token"), cortex_allowed_analyzers="")
