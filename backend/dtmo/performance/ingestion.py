from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any
from uuid import UUID, uuid4

from dtmo.connectors.provenance import IngestionContext, normalize_connector_records


@dataclass(frozen=True)
class IngestionBudget:
    min_sustained_records_per_second: int
    data_loss_max_records: int
    duplicate_candidate_max_records: int
    error_rate_max_percent: float


@dataclass(frozen=True)
class IngestionResult:
    submitted_records: int
    accepted_candidates: int
    quarantined_records: int
    replayed_records: int
    duplicate_candidate_records: int
    data_loss_records: int
    achieved_records_per_second: float
    error_rate_percent: float
    provenance_preserved: bool
    publication_state_preserved: bool
    decision: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "submitted_records": self.submitted_records,
            "accepted_candidates": self.accepted_candidates,
            "quarantined_records": self.quarantined_records,
            "replayed_records": self.replayed_records,
            "duplicate_candidate_records": self.duplicate_candidate_records,
            "data_loss_records": self.data_loss_records,
            "achieved_records_per_second": round(self.achieved_records_per_second, 3),
            "error_rate_percent": round(self.error_rate_percent, 3),
            "governance": {
                "provenance_preserved": self.provenance_preserved,
                "publication_state_preserved": self.publication_state_preserved,
                "load_test_may_publish": False,
            },
            "decision": self.decision,
        }


class InMemoryReplayRegistry:
    """Deterministic replay registry for the bounded synthetic performance fixture."""

    def __init__(self) -> None:
        self._claims: set[tuple[str, str, str]] = set()

    def claim(
        self,
        *,
        connector_id: str,
        external_id: str,
        payload_digest: str,
        run_id: UUID,
        source_uri: str,
        observed_at: datetime | None = None,
    ) -> bool:
        del run_id, source_uri, observed_at
        key = (connector_id, external_id, payload_digest)
        if key in self._claims:
            return False
        self._claims.add(key)
        return True


def load_ingestion_budget(profile_path: Path) -> IngestionBudget:
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    traffic = profile["traffic"]
    budgets = profile["budgets"]
    governance = profile["governance"]
    privacy = profile["privacy"]

    if governance["load_test_may_publish"] is not False:
        raise ValueError("performance profile must forbid publication")
    if governance["human_review_required"] is not True:
        raise ValueError("performance profile must preserve human review")
    if governance["share_approval_separate_from_review"] is not True:
        raise ValueError("performance profile must preserve separation of duties")
    if governance["service_accounts_may_approve_share"] is not False:
        raise ValueError("performance profile must forbid service-account share approval")
    if privacy["synthetic_only"] is not True:
        raise ValueError("performance profile must require synthetic fixtures")
    if privacy["production_personal_data_allowed"] is not False:
        raise ValueError("performance profile must forbid production personal data")

    sustained = int(traffic["ingestion_sustained_records_per_second"])
    minimum = int(budgets["ingestion_min_sustained_records_per_second"])
    if sustained < minimum:
        raise ValueError("configured sustained ingestion rate is below the acceptance budget")

    return IngestionBudget(
        min_sustained_records_per_second=minimum,
        data_loss_max_records=int(budgets["data_loss_max_records"]),
        duplicate_candidate_max_records=int(budgets["duplicate_candidate_max_records"]),
        error_rate_max_percent=float(budgets["error_rate_max_percent"]),
    )


def synthetic_records(count: int) -> list[dict[str, Any]]:
    if count <= 0:
        raise ValueError("count must be positive")
    return [
        {
            "external_id": f"synthetic-ingest-{index:08d}",
            "title": f"Synthetic education-sector intelligence record {index}",
            "category": ["phishing", "malware", "vulnerability"][index % 3],
            "fixture_class": "synthetic-performance",
        }
        for index in range(count)
    ]


def run_ingestion_harness(
    *,
    budget: IngestionBudget,
    record_count: int,
    replay_registry: InMemoryReplayRegistry | Any | None = None,
) -> IngestionResult:
    records = synthetic_records(record_count)
    registry = replay_registry or InMemoryReplayRegistry()
    source_uri = "https://example.test/performance/ingestion"

    started = perf_counter()
    first = normalize_connector_records(
        records,
        context=IngestionContext(
            connector_id="synthetic-performance-ingestion",
            run_id=uuid4(),
            source_uri=source_uri,
            fetched_at=datetime.now(UTC),
            confidence=80,
        ),
        external_id_field="external_id",
        replay_registry=registry,
    )
    elapsed = max(perf_counter() - started, 1e-9)

    replay = normalize_connector_records(
        records,
        context=IngestionContext(
            connector_id="synthetic-performance-ingestion",
            run_id=uuid4(),
            source_uri=source_uri,
            fetched_at=datetime.now(UTC),
            confidence=80,
        ),
        external_id_field="external_id",
        replay_registry=registry,
    )

    accepted_candidates = len(first.candidates)
    first_quarantine = len(first.quarantined)
    replayed_records = sum(item.reason == "replayed_record" for item in replay.quarantined)
    duplicate_candidate_records = len(replay.candidates)
    data_loss_records = max(0, record_count - accepted_candidates - first_quarantine)
    error_rate_percent = (first_quarantine / record_count) * 100
    achieved = record_count / elapsed

    provenance_preserved = all(
        candidate.external_id
        and candidate.source_uri == source_uri
        and candidate.payload_digest
        and candidate.confidence == 80
        and candidate.raw_evidence.get("fixture_class") == "synthetic-performance"
        for candidate in first.candidates
    )
    publication_state_preserved = (
        first.publish_approved is False
        and replay.publish_approved is False
        and all(candidate.publish_approved is False for candidate in first.candidates)
        and all(item.publish_approved is False for item in replay.quarantined)
    )

    decision = "pass" if (
        accepted_candidates == record_count
        and first_quarantine == 0
        and replayed_records == record_count
        and achieved >= budget.min_sustained_records_per_second
        and data_loss_records <= budget.data_loss_max_records
        and duplicate_candidate_records <= budget.duplicate_candidate_max_records
        and error_rate_percent <= budget.error_rate_max_percent
        and provenance_preserved
        and publication_state_preserved
    ) else "fail"

    return IngestionResult(
        submitted_records=record_count,
        accepted_candidates=accepted_candidates,
        quarantined_records=first_quarantine,
        replayed_records=replayed_records,
        duplicate_candidate_records=duplicate_candidate_records,
        data_loss_records=data_loss_records,
        achieved_records_per_second=achieved,
        error_rate_percent=error_rate_percent,
        provenance_preserved=provenance_preserved,
        publication_state_preserved=publication_state_preserved,
        decision=decision,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Bounded DTMO ingestion throughput harness")
    parser.add_argument(
        "--profile", type=Path, default=Path("config/performance/phase5_workload_profile.json")
    )
    parser.add_argument("--duration-seconds", type=float, default=5.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.duration_seconds <= 0:
        raise SystemExit("duration-seconds must be positive")

    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    budget = load_ingestion_budget(args.profile)
    target_rate = int(profile["traffic"]["ingestion_sustained_records_per_second"])
    record_count = max(1, math.ceil(target_rate * args.duration_seconds))
    result = run_ingestion_harness(budget=budget, record_count=record_count)

    evidence = {
        "schema_version": 1,
        "profile_id": profile["profile_id"],
        "scope": "governed-ingestion-normalization-and-replay",
        "dataset": {
            "fixture_class": "synthetic-performance",
            "submitted_records": record_count,
            "representative_intelligence_records_target": profile["dataset"]["intelligence_records"],
            "scaled_ci_fixture": True,
        },
        "budget": {
            "min_sustained_records_per_second": budget.min_sustained_records_per_second,
            "data_loss_max_records": budget.data_loss_max_records,
            "duplicate_candidate_max_records": budget.duplicate_candidate_max_records,
            "error_rate_max_percent": budget.error_rate_max_percent,
        },
        "result": result.as_dict(),
        "external_load_gate_satisfied": False,
        "decision": result.decision,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
    raise SystemExit(0 if result.decision == "pass" else 1)


if __name__ == "__main__":
    main()
