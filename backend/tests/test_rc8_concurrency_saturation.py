from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

from dtmo.performance.concurrency_saturation import (
    SaturationBudget,
    load_saturation_budget,
    run_saturation_harness,
)


PROFILE = Path("config/performance/phase5_workload_profile.json")


def test_profile_loads_saturation_budget() -> None:
    budget = load_saturation_budget(PROFILE)
    assert budget.peak_concurrent_users == 50
    assert budget.api_read_requests_per_second == 100
    assert budget.ingestion_records_per_second == 100
    assert budget.api_read_p95_ms == 300
    assert budget.data_loss_max_records == 0


def test_profile_rejects_publication(tmp_path: Path) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["governance"]["load_test_may_publish"] = True
    candidate = tmp_path / "profile.json"
    candidate.write_text(json.dumps(profile), encoding="utf-8")
    with pytest.raises(ValueError, match="forbid publication"):
        load_saturation_budget(candidate)


def test_profile_rejects_production_personal_data(tmp_path: Path) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["privacy"]["production_personal_data_allowed"] = True
    candidate = tmp_path / "profile.json"
    candidate.write_text(json.dumps(profile), encoding="utf-8")
    with pytest.raises(ValueError, match="production personal data"):
        load_saturation_budget(candidate)


def test_harness_observes_concurrency_without_loss() -> None:
    budget = SaturationBudget(
        peak_concurrent_users=50,
        api_read_requests_per_second=100,
        ingestion_records_per_second=100,
        api_read_p95_ms=300,
        error_rate_max_percent=1.0,
        data_loss_max_records=0,
    )
    result = asyncio.run(run_saturation_harness(
        budget=budget,
        duration_seconds=0.25,
        concurrency=10,
        scaled_read_rps=40,
        scaled_ingest_rps=40,
    ))
    assert result.decision == "pass"
    assert result.max_inflight_operations == 10
    assert result.data_loss_records == 0
    assert result.error_rate_percent == 0
    assert result.publication_state_preserved is True


def test_harness_rejects_concurrency_above_contract() -> None:
    budget = SaturationBudget(50, 100, 100, 300, 1.0, 0)
    with pytest.raises(ValueError, match="peak_concurrent_users"):
        asyncio.run(run_saturation_harness(
            budget=budget,
            duration_seconds=0.1,
            concurrency=51,
            scaled_read_rps=10,
            scaled_ingest_rps=10,
        ))


def test_harness_rejects_scaled_rate_above_contract() -> None:
    budget = SaturationBudget(50, 100, 100, 300, 1.0, 0)
    with pytest.raises(ValueError, match="scaled_read_rps"):
        asyncio.run(run_saturation_harness(
            budget=budget,
            duration_seconds=0.1,
            concurrency=10,
            scaled_read_rps=101,
            scaled_ingest_rps=10,
        ))
