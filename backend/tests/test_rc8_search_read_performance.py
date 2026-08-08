from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from dtmo.performance.search_read import (
    SearchReadBudget,
    load_search_read_budget,
    run_search_read_harness,
    synthetic_document,
)


PROFILE = Path("config/performance/phase5_workload_profile.json")


def test_profile_drives_search_budget() -> None:
    budget = load_search_read_budget(PROFILE)
    assert budget.requests_per_second == 40
    assert budget.p95_ms == 800
    assert budget.p99_ms == 1500
    assert budget.error_rate_max_percent == 1.0


def test_search_profile_fails_closed_if_publication_is_allowed(tmp_path: Path) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["governance"]["load_test_may_publish"] = True
    path = tmp_path / "unsafe.json"
    path.write_text(json.dumps(profile), encoding="utf-8")
    with pytest.raises(ValueError, match="forbid publication"):
        load_search_read_budget(path)


def test_synthetic_documents_retain_provenance_and_no_publish_approval() -> None:
    document = synthetic_document(7)
    assert document["external_id"] == "synthetic-00000007"
    assert str(document["source_uri"]).startswith("https://example.test/")
    assert document["publish_approved"] is False
    assert document["fixture_class"] == "synthetic-performance"


@pytest.mark.asyncio
async def test_search_harness_passes_with_provenance_and_nonpublication_hits() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["x-correlation-id"].startswith("perf-search-")
        return httpx.Response(
            200,
            json={
                "hits": {
                    "hits": [
                        {
                            "_source": {
                                "external_id": "synthetic-1",
                                "source_uri": "https://example.test/source/1",
                                "publish_approved": False,
                            }
                        }
                    ]
                }
            },
        )

    result = await run_search_read_harness(
        endpoint="https://search.test",
        index_name="dtmo-test",
        budget=SearchReadBudget(40, 800, 1500, 1.0),
        duration_seconds=0.05,
        concurrency=2,
        transport=httpx.MockTransport(handler),
    )
    assert result.total_requests == 2
    assert result.failed_requests == 0
    assert result.provenance_preserved is True
    assert result.publication_state_preserved is True
    assert result.decision == "pass"


@pytest.mark.asyncio
async def test_search_harness_fails_closed_if_hit_is_publish_approved() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "hits": {
                    "hits": [
                        {
                            "_source": {
                                "external_id": "synthetic-1",
                                "source_uri": "https://example.test/source/1",
                                "publish_approved": True,
                            }
                        }
                    ]
                }
            },
        )

    result = await run_search_read_harness(
        endpoint="https://search.test",
        index_name="dtmo-test",
        budget=SearchReadBudget(40, 800, 1500, 1.0),
        duration_seconds=0.025,
        concurrency=1,
        transport=httpx.MockTransport(handler),
    )
    assert result.publication_state_preserved is False
    assert result.decision == "fail"


@pytest.mark.asyncio
async def test_search_harness_fails_closed_on_search_errors() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={"error": "unavailable"})

    result = await run_search_read_harness(
        endpoint="https://search.test",
        index_name="dtmo-test",
        budget=SearchReadBudget(40, 800, 1500, 1.0),
        duration_seconds=0.025,
        concurrency=1,
        transport=httpx.MockTransport(handler),
    )
    assert result.failed_requests == result.total_requests
    assert result.error_rate_percent == 100.0
    assert result.decision == "fail"
