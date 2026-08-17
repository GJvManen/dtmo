from __future__ import annotations

import httpx
import pytest

from dtmo.integrations.cortex import CortexAnalyzerConnector, CortexConnectorConfig, CortexPolicyError


@pytest.mark.asyncio
async def test_cortex_connector_runs_only_allowlisted_analyzer_and_imports_report() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "POST":
            assert request.url.path == "/api/analyzer/Allowed_1/run"
            assert request.headers["authorization"] == "Bearer secret"
            return httpx.Response(200, json={"id": "job-1"})
        assert request.url.path == "/api/job/job-1/report"
        assert request.url.params["atMost"] == "30s"
        return httpx.Response(200, json={"id": "job-1", "status": "Success", "report": {"summary": "ok"}})

    connector = CortexAnalyzerConnector(
        CortexConnectorConfig(
            api_base="https://cortex.example",
            api_token="secret",
            allowed_analyzers=frozenset({"Allowed_1"}),
        )
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await connector.analyze(
            client,
            canonical_id="item-1",
            observable_type="ip",
            observable_value="192.0.2.10",
            analyzer_id="Allowed_1",
            tlp="amber",
        )

    assert len(requests) == 2
    assert result.job_id == "job-1"
    assert result.status == "success"
    assert result.report["_dtmo_cortex"]["responder_execution_authorized"] is False
    assert result.report["_dtmo_cortex"]["external_share_authorized"] is False
    assert result.report["_dtmo_cortex"]["local_compromise_proven"] is False


@pytest.mark.asyncio
async def test_cortex_connector_fails_closed_for_unapproved_analyzer() -> None:
    connector = CortexAnalyzerConnector(
        CortexConnectorConfig(
            api_base="https://cortex.example",
            api_token="secret",
            allowed_analyzers=frozenset({"Allowed_1"}),
        )
    )
    async with httpx.AsyncClient() as client:
        with pytest.raises(CortexPolicyError, match="allowlist"):
            await connector.analyze(
                client,
                canonical_id="item-1",
                observable_type="ip",
                observable_value="192.0.2.10",
                analyzer_id="NotAllowed",
                tlp="green",
            )


def test_cortex_connector_requires_token() -> None:
    connector = CortexAnalyzerConnector(
        CortexConnectorConfig(
            api_base="https://cortex.example",
            api_token="",
            allowed_analyzers=frozenset({"Allowed_1"}),
        )
    )
    with pytest.raises(CortexPolicyError, match="token"):
        connector._headers()
