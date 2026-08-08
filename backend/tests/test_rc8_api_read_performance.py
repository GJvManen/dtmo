from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from dtmo.performance.api_read import ApiReadBudget, load_api_read_budget, run_api_read_harness


PROFILE = Path("config/performance/phase5_workload_profile.json")


def test_profile_drives_api_read_budget() -> None:
    budget = load_api_read_budget(PROFILE)
    assert budget.requests_per_second == 100
    assert budget.p95_ms == 300
    assert budget.p99_ms == 750
    assert budget.error_rate_max_percent == 1.0


def test_profile_fails_closed_if_publication_is_allowed(tmp_path: Path) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["governance"]["load_test_may_publish"] = True
    path = tmp_path / "unsafe.json"
    path.write_text(json.dumps(profile), encoding="utf-8")
    with pytest.raises(ValueError, match="forbid publication"):
        load_api_read_budget(path)


@pytest.mark.asyncio
async def test_api_read_harness_passes_only_with_governance_markers() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["x-correlation-id"].startswith("perf-api-read-")
        return httpx.Response(
            200,
            json={
                "status": "healthy",
                "publication_gate": "human-approval-required",
                "authentication": "api-key-and-rbac",
            },
        )

    result = await run_api_read_harness(
        target_url="https://dtmo.test/health",
        budget=ApiReadBudget(100, 300, 750, 1.0),
        duration_seconds=0.05,
        concurrency=5,
        transport=httpx.MockTransport(handler),
    )
    assert result.total_requests == 5
    assert result.failed_requests == 0
    assert result.publication_gate_preserved is True
    assert result.authentication_boundary_reported is True
    assert result.decision == "pass"


@pytest.mark.asyncio
async def test_api_read_harness_fails_closed_on_missing_publication_gate() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"status": "healthy", "authentication": "api-key-and-rbac"})

    result = await run_api_read_harness(
        target_url="https://dtmo.test/health",
        budget=ApiReadBudget(100, 300, 750, 1.0),
        duration_seconds=0.02,
        concurrency=2,
        transport=httpx.MockTransport(handler),
    )
    assert result.publication_gate_preserved is False
    assert result.decision == "fail"


@pytest.mark.asyncio
async def test_api_read_harness_fails_closed_on_http_errors() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={"detail": "unavailable"})

    result = await run_api_read_harness(
        target_url="https://dtmo.test/health",
        budget=ApiReadBudget(100, 300, 750, 1.0),
        duration_seconds=0.02,
        concurrency=2,
        transport=httpx.MockTransport(handler),
    )
    assert result.failed_requests == result.total_requests
    assert result.error_rate_percent == 100.0
    assert result.decision == "fail"


@pytest.mark.asyncio
async def test_api_read_harness_rejects_non_http_target() -> None:
    with pytest.raises(ValueError, match="HTTP"):
        await run_api_read_harness(
            target_url="file:///etc/passwd",
            budget=ApiReadBudget(100, 300, 750, 1.0),
            duration_seconds=0.01,
            concurrency=1,
        )
