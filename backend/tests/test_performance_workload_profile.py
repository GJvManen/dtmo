from __future__ import annotations

import json
from pathlib import Path


PROFILE_PATH = Path("config/performance/phase5_workload_profile.json")


def _profile() -> dict[str, object]:
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def test_phase5_profile_is_synthetic_and_fail_closed_for_publication() -> None:
    profile = _profile()
    privacy = profile["privacy"]
    governance = profile["governance"]

    assert isinstance(privacy, dict)
    assert privacy["synthetic_only"] is True
    assert privacy["production_personal_data_allowed"] is False

    assert isinstance(governance, dict)
    assert governance["load_test_may_publish"] is False
    assert governance["human_review_required"] is True
    assert governance["share_approval_separate_from_review"] is True
    assert governance["service_accounts_may_approve_share"] is False


def test_phase5_profile_has_representative_positive_dataset_and_traffic() -> None:
    profile = _profile()
    dataset = profile["dataset"]
    traffic = profile["traffic"]

    assert isinstance(dataset, dict)
    assert isinstance(traffic, dict)
    assert all(isinstance(value, int) and value > 0 for value in dataset.values())
    assert all(isinstance(value, int) and value > 0 for value in traffic.values())
    assert traffic["ingestion_burst_records_per_second"] >= traffic[
        "ingestion_sustained_records_per_second"
    ]


def test_phase5_profile_defines_measurable_fail_closed_budgets() -> None:
    profile = _profile()
    budgets = profile["budgets"]

    assert isinstance(budgets, dict)
    positive_budget_names = {
        "api_read_p95_ms",
        "api_read_p99_ms",
        "api_write_p95_ms",
        "search_p95_ms",
        "search_p99_ms",
        "dashboard_p95_ms",
        "ingestion_min_sustained_records_per_second",
        "ingestion_min_burst_records_per_second",
        "error_rate_max_percent",
        "api_cpu_avg_max_percent",
        "api_memory_avg_max_percent",
        "postgres_cpu_avg_max_percent",
        "opensearch_heap_avg_max_percent",
        "queue_recovery_max_seconds_after_burst",
    }
    assert all(float(budgets[name]) > 0 for name in positive_budget_names)
    assert budgets["data_loss_max_records"] == 0
    assert budgets["duplicate_candidate_max_records"] == 0
    assert budgets["api_read_p99_ms"] >= budgets["api_read_p95_ms"]
    assert budgets["search_p99_ms"] >= budgets["search_p95_ms"]
    assert budgets["ingestion_min_burst_records_per_second"] >= budgets[
        "ingestion_min_sustained_records_per_second"
    ]
