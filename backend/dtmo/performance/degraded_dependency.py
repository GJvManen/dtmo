from __future__ import annotations

import argparse
import asyncio
import json
import math
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any
from uuid import uuid4

from dtmo.connectors.provenance import IngestionContext, normalize_connector_records
from dtmo.performance.ingestion import InMemoryReplayRegistry


@dataclass(frozen=True)
class DegradedDependencyBudget:
    ingestion_records_per_second: int
    connector_parallelism: int
    recovery_max_seconds: float
    data_loss_max_records: int
    duplicate_candidate_max_records: int


@dataclass(frozen=True)
class DegradedDependencyResult:
    submitted_records: int
    delivered_records: int
    buffered_during_outage: int
    dependency_failure_events: int
    duplicate_candidate_records: int
    data_loss_records: int
    outage_seconds: float
    recovery_seconds_after_dependency: float
    dependency_unavailability_observed: bool
    provenance_preserved: bool
    publication_state_preserved: bool
    decision: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "submitted_records": self.submitted_records,
            "delivered_records": self.delivered_records,
            "buffered_during_outage": self.buffered_during_outage,
            "dependency_failure_events": self.dependency_failure_events,
            "duplicate_candidate_records": self.duplicate_candidate_records,
            "data_loss_records": self.data_loss_records,
            "outage_seconds": round(self.outage_seconds, 3),
            "recovery_seconds_after_dependency": round(self.recovery_seconds_after_dependency, 3),
            "dependency_unavailability_observed": self.dependency_unavailability_observed,
            "governance": {
                "provenance_preserved": self.provenance_preserved,
                "publication_state_preserved": self.publication_state_preserved,
                "load_test_may_publish": False,
            },
            "decision": self.decision,
        }


def load_degraded_dependency_budget(profile_path: Path) -> DegradedDependencyBudget:
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

    return DegradedDependencyBudget(
        ingestion_records_per_second=int(traffic["ingestion_sustained_records_per_second"]),
        connector_parallelism=int(traffic["connector_parallelism"]),
        recovery_max_seconds=float(budgets["queue_recovery_max_seconds_after_burst"]),
        data_loss_max_records=int(budgets["data_loss_max_records"]),
        duplicate_candidate_max_records=int(budgets["duplicate_candidate_max_records"]),
    )


def _synthetic_record(index: int) -> dict[str, Any]:
    return {
        "external_id": f"synthetic-degraded-{index:08d}",
        "title": f"Synthetic degraded-dependency intelligence record {index}",
        "fixture_class": "synthetic-degraded-dependency",
    }


async def run_degraded_dependency_harness(
    *,
    budget: DegradedDependencyBudget,
    duration_seconds: float,
    outage_seconds: float,
    delivery_records_per_second: int = 100,
    retry_interval_seconds: float = 0.01,
    queue_capacity: int | None = None,
) -> DegradedDependencyResult:
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive")
    if outage_seconds <= 0:
        raise ValueError("outage_seconds must be positive")
    if delivery_records_per_second <= 0:
        raise ValueError("delivery_records_per_second must be positive")
    if retry_interval_seconds <= 0:
        raise ValueError("retry_interval_seconds must be positive")
    if budget.connector_parallelism <= 0:
        raise ValueError("connector_parallelism must be positive")

    capacity = queue_capacity or max(1, budget.connector_parallelism * 2)
    queue: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue(maxsize=capacity)
    registry = InMemoryReplayRegistry()
    source_uri = "https://example.test/performance/degraded-dependency"
    dependency_name = "opensearch-index-sink"
    total = max(1, math.ceil(budget.ingestion_records_per_second * duration_seconds))
    delivery_delay = budget.connector_parallelism / delivery_records_per_second

    delivered_ids: list[str] = []
    buffered_ids: set[str] = set()
    dependency_failure_events = 0
    provenance_ok = True
    publication_ok = True

    started = perf_counter()
    dependency_available_at = started + outage_seconds

    async def consumer() -> None:
        nonlocal dependency_failure_events, provenance_ok, publication_ok
        while True:
            record = await queue.get()
            try:
                if record is None:
                    return

                normalized = normalize_connector_records(
                    [record],
                    context=IngestionContext(
                        connector_id="synthetic-degraded-dependency",
                        run_id=uuid4(),
                        source_uri=source_uri,
                        fetched_at=datetime.now(UTC),
                        confidence=80,
                    ),
                    external_id_field="external_id",
                    replay_registry=registry,
                )
                publication_ok = publication_ok and normalized.publish_approved is False
                if len(normalized.candidates) != 1 or normalized.quarantined:
                    continue

                candidate = normalized.candidates[0]
                provenance_ok = provenance_ok and (
                    candidate.source_uri == source_uri
                    and bool(candidate.payload_digest)
                    and candidate.confidence == 80
                    and candidate.raw_evidence.get("fixture_class") == "synthetic-degraded-dependency"
                )
                publication_ok = publication_ok and candidate.publish_approved is False

                while perf_counter() < dependency_available_at:
                    dependency_failure_events += 1
                    buffered_ids.add(candidate.external_id)
                    await asyncio.sleep(retry_interval_seconds)

                await asyncio.sleep(delivery_delay)
                delivered_ids.append(candidate.external_id)
            finally:
                queue.task_done()

    consumers = [asyncio.create_task(consumer()) for _ in range(budget.connector_parallelism)]
    producer_interval = 1.0 / budget.ingestion_records_per_second

    for index in range(total):
        target = started + (index * producer_interval)
        delay = target - perf_counter()
        if delay > 0:
            await asyncio.sleep(delay)
        await queue.put(_synthetic_record(index))

    await queue.join()
    recovered_at = perf_counter()

    for _ in consumers:
        await queue.put(None)
    await asyncio.gather(*consumers)

    delivered = len(delivered_ids)
    unique_delivered = len(set(delivered_ids))
    duplicate_candidates = delivered - unique_delivered
    data_loss = max(0, total - unique_delivered)
    recovery = max(0.0, recovered_at - dependency_available_at)
    dependency_unavailable = dependency_failure_events > 0 and bool(buffered_ids)

    decision = "pass" if (
        delivered == total
        and data_loss <= budget.data_loss_max_records
        and duplicate_candidates <= budget.duplicate_candidate_max_records
        and dependency_unavailable
        and recovery <= budget.recovery_max_seconds
        and provenance_ok
        and publication_ok
    ) else "fail"

    return DegradedDependencyResult(
        submitted_records=total,
        delivered_records=delivered,
        buffered_during_outage=len(buffered_ids),
        dependency_failure_events=dependency_failure_events,
        duplicate_candidate_records=duplicate_candidates,
        data_loss_records=data_loss,
        outage_seconds=outage_seconds,
        recovery_seconds_after_dependency=recovery,
        dependency_unavailability_observed=dependency_unavailable,
        provenance_preserved=provenance_ok,
        publication_state_preserved=publication_ok,
        decision=decision,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Bounded DTMO degraded-dependency performance/correctness harness")
    parser.add_argument("--profile", type=Path, default=Path("config/performance/phase5_workload_profile.json"))
    parser.add_argument("--duration-seconds", type=float, default=1.0)
    parser.add_argument("--outage-seconds", type=float, default=0.25)
    parser.add_argument("--delivery-records-per-second", type=int, default=100)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    budget = load_degraded_dependency_budget(args.profile)
    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    result = asyncio.run(
        run_degraded_dependency_harness(
            budget=budget,
            duration_seconds=args.duration_seconds,
            outage_seconds=args.outage_seconds,
            delivery_records_per_second=args.delivery_records_per_second,
        )
    )

    evidence = {
        "schema_version": 1,
        "profile_id": profile["profile_id"],
        "scope": "degraded-dependency-performance-correctness",
        "dependency": {
            "name": "opensearch-index-sink",
            "fault_model": "temporary-unavailable",
            "fault_injection": "in-process synthetic dependency gate",
            "production_opensearch_hardening_satisfied": False,
        },
        "dataset": {
            "fixture_class": "synthetic-degraded-dependency",
            "scaled_ci_fixture": True,
            "executed_duration_seconds": args.duration_seconds,
            "injected_outage_seconds": args.outage_seconds,
        },
        "budget": {
            "ingestion_records_per_second": budget.ingestion_records_per_second,
            "connector_parallelism": budget.connector_parallelism,
            "recovery_max_seconds": budget.recovery_max_seconds,
            "data_loss_max_records": budget.data_loss_max_records,
            "duplicate_candidate_max_records": budget.duplicate_candidate_max_records,
        },
        "result": result.as_dict(),
        "external_load_gate_satisfied": False,
        "degraded_dependency_tested": True,
        "decision": result.decision,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
    raise SystemExit(0 if result.decision == "pass" else 1)


if __name__ == "__main__":
    main()
