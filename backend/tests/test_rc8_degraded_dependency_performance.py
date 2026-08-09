from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

from dtmo.performance.degraded_dependency import (
    DegradedDependencyBudget,
    load_degraded_dependency_budget,
    run_degraded_dependency_harness,
)


PROFILE = Path("config/performance/phase5_workload_profile.json")


def test_profile_loads_degraded_dependency_budget() -> None:
    budget = load_degraded_dependency_budget(PROFILE)
    assert budget.ingestion_records_per_second == 100
    assert budget.connector_parallelism == 20
    assert budget.recovery_max_seconds == 900
    assert budget.data_loss_max_records == 0
    assert budget.duplicate_candidate_max_records == 0


def test_profile_rejects_publication(tmp_path: Path) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["governance"]["load_test_may_publish"] = True
    candidate = tmp_path / "profile.json"
    candidate.write_text(json.dumps(profile), encoding="utf-8")
    with pytest.raises(ValueError, match="forbid publication"):
        load_degraded_dependency_budget(candidate)


def test_profile_rejects_production_personal_data(tmp_path: Path) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["privacy"]["production_personal_data_allowed"] = True
    candidate = tmp_path / "profile.json"
    candidate.write_text(json.dumps(profile), encoding="utf-8")
    with pytest.raises(ValueError, match="forbid production personal data"):
        load_degraded_dependency_budget(candidate)


def test_degraded_dependency_buffers_and_recovers_without_loss() -> None:
    budget = DegradedDependencyBudget(50, 4, 5, 0, 0)
    result = asyncio.run(
        run_degraded_dependency_harness(
            budget=budget,
            duration_seconds=0.2,
            outage_seconds=0.08,
            delivery_records_per_second=50,
            retry_interval_seconds=0.005,
            queue_capacity=4,
        )
    )
    assert result.decision == "pass"
    assert result.submitted_records == 10
    assert result.delivered_records == 10
    assert result.buffered_during_outage > 0
    assert result.dependency_failure_events > 0
    assert result.dependency_unavailability_observed is True
    assert result.data_loss_records == 0
    assert result.duplicate_candidate_records == 0
    assert result.provenance_preserved is True
    assert result.publication_state_preserved is True


def test_degraded_dependency_fails_closed_when_recovery_budget_is_exceeded() -> None:
    budget = DegradedDependencyBudget(20, 1, 0.001, 0, 0)
    result = asyncio.run(
        run_degraded_dependency_harness(
            budget=budget,
            duration_seconds=0.2,
            outage_seconds=0.05,
            delivery_records_per_second=10,
            retry_interval_seconds=0.005,
            queue_capacity=2,
        )
    )
    assert result.recovery_seconds_after_dependency > budget.recovery_max_seconds
    assert result.decision == "fail"


def test_degraded_dependency_requires_positive_outage() -> None:
    budget = load_degraded_dependency_budget(PROFILE)
    with pytest.raises(ValueError, match="outage_seconds must be positive"):
        asyncio.run(
            run_degraded_dependency_harness(
                budget=budget,
                duration_seconds=0.1,
                outage_seconds=0,
            )
        )
