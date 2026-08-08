from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

from dtmo.performance.queue_burst import QueueBurstBudget, load_queue_burst_budget, run_queue_burst_harness


PROFILE = Path("config/performance/phase5_workload_profile.json")


def test_profile_loads_queue_burst_budget() -> None:
    budget = load_queue_burst_budget(PROFILE)
    assert budget.burst_records_per_second == 250
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
        load_queue_burst_budget(candidate)


def test_profile_rejects_production_personal_data(tmp_path: Path) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["privacy"]["production_personal_data_allowed"] = True
    candidate = tmp_path / "profile.json"
    candidate.write_text(json.dumps(profile), encoding="utf-8")
    with pytest.raises(ValueError, match="forbid production personal data"):
        load_queue_burst_budget(candidate)


def test_queue_burst_applies_backpressure_without_loss() -> None:
    budget = QueueBurstBudget(250, 4, 10, 0, 0)
    result = asyncio.run(run_queue_burst_harness(budget=budget, duration_seconds=0.2, consumer_records_per_second=20, queue_capacity=4))
    assert result.decision == "pass"
    assert result.submitted_records == 50
    assert result.accepted_candidates == 50
    assert result.data_loss_records == 0
    assert result.duplicate_candidate_records == 0
    assert result.backpressure_events > 0
    assert result.max_queue_depth <= result.queue_capacity
    assert result.provenance_preserved is True
    assert result.publication_state_preserved is True


def test_queue_burst_fails_closed_when_recovery_budget_is_impossible() -> None:
    budget = QueueBurstBudget(100, 2, 0.001, 0, 0)
    result = asyncio.run(run_queue_burst_harness(budget=budget, duration_seconds=0.1, consumer_records_per_second=10, queue_capacity=2))
    assert result.recovery_seconds_after_producer > budget.recovery_max_seconds
    assert result.decision == "fail"


def test_queue_burst_requires_positive_duration() -> None:
    budget = load_queue_burst_budget(PROFILE)
    with pytest.raises(ValueError, match="duration_seconds must be positive"):
        asyncio.run(run_queue_burst_harness(budget=budget, duration_seconds=0))
