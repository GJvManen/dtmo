from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from dtmo.performance.ingestion import (
    IngestionBudget,
    load_ingestion_budget,
    run_ingestion_harness,
    synthetic_records,
)


PROFILE = Path("config/performance/phase5_workload_profile.json")


def test_profile_budget_preserves_governance_and_zero_loss() -> None:
    budget = load_ingestion_budget(PROFILE)
    assert budget.min_sustained_records_per_second == 100
    assert budget.data_loss_max_records == 0
    assert budget.duplicate_candidate_max_records == 0


def test_synthetic_fixture_contains_no_personal_data_fields() -> None:
    records = synthetic_records(3)
    assert len(records) == 3
    assert all(record["fixture_class"] == "synthetic-performance" for record in records)
    assert all("name" not in record and "email" not in record for record in records)


def test_harness_accepts_unique_records_and_quarantines_replay() -> None:
    result = run_ingestion_harness(
        budget=IngestionBudget(
            min_sustained_records_per_second=1,
            data_loss_max_records=0,
            duplicate_candidate_max_records=0,
            error_rate_max_percent=0,
        ),
        record_count=100,
    )
    assert result.decision == "pass"
    assert result.accepted_candidates == 100
    assert result.data_loss_records == 0
    assert result.replayed_records == 100
    assert result.duplicate_candidate_records == 0
    assert result.provenance_preserved is True
    assert result.publication_state_preserved is True


class AlwaysAcceptReplayRegistry:
    def claim(self, **kwargs: Any) -> bool:
        return True


def test_duplicate_candidate_creation_fails_closed() -> None:
    result = run_ingestion_harness(
        budget=IngestionBudget(
            min_sustained_records_per_second=1,
            data_loss_max_records=0,
            duplicate_candidate_max_records=0,
            error_rate_max_percent=0,
        ),
        record_count=25,
        replay_registry=AlwaysAcceptReplayRegistry(),
    )
    assert result.decision == "fail"
    assert result.duplicate_candidate_records == 25


def test_profile_rejects_publication_permission(tmp_path: Path) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["governance"]["load_test_may_publish"] = True
    mutated = tmp_path / "profile.json"
    mutated.write_text(json.dumps(profile), encoding="utf-8")
    with pytest.raises(ValueError, match="forbid publication"):
        load_ingestion_budget(mutated)


def test_profile_rejects_production_personal_data(tmp_path: Path) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["privacy"]["production_personal_data_allowed"] = True
    mutated = tmp_path / "profile.json"
    mutated.write_text(json.dumps(profile), encoding="utf-8")
    with pytest.raises(ValueError, match="forbid production personal data"):
        load_ingestion_budget(mutated)
