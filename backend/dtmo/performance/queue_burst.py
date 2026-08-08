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
class QueueBurstBudget:
    burst_records_per_second: int
    connector_parallelism: int
    recovery_max_seconds: float
    data_loss_max_records: int
    duplicate_candidate_max_records: int


@dataclass(frozen=True)
class QueueBurstResult:
    submitted_records: int
    accepted_candidates: int
    quarantined_records: int
    duplicate_candidate_records: int
    data_loss_records: int
    queue_capacity: int
    max_queue_depth: int
    backpressure_events: int
    recovery_seconds_after_producer: float
    provenance_preserved: bool
    publication_state_preserved: bool
    decision: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "submitted_records": self.submitted_records,
            "accepted_candidates": self.accepted_candidates,
            "quarantined_records": self.quarantined_records,
            "duplicate_candidate_records": self.duplicate_candidate_records,
            "data_loss_records": self.data_loss_records,
            "queue_capacity": self.queue_capacity,
            "max_queue_depth": self.max_queue_depth,
            "backpressure_events": self.backpressure_events,
            "recovery_seconds_after_producer": round(self.recovery_seconds_after_producer, 3),
            "governance": {
                "provenance_preserved": self.provenance_preserved,
                "publication_state_preserved": self.publication_state_preserved,
                "load_test_may_publish": False,
            },
            "decision": self.decision,
        }


def load_queue_burst_budget(profile_path: Path) -> QueueBurstBudget:
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

    return QueueBurstBudget(
        burst_records_per_second=int(traffic["ingestion_burst_records_per_second"]),
        connector_parallelism=int(traffic["connector_parallelism"]),
        recovery_max_seconds=float(budgets["queue_recovery_max_seconds_after_burst"]),
        data_loss_max_records=int(budgets["data_loss_max_records"]),
        duplicate_candidate_max_records=int(budgets["duplicate_candidate_max_records"]),
    )


def _synthetic_record(index: int) -> dict[str, Any]:
    return {
        "external_id": f"synthetic-burst-{index:08d}",
        "title": f"Synthetic burst intelligence record {index}",
        "fixture_class": "synthetic-queue-burst",
    }


async def run_queue_burst_harness(
    *,
    budget: QueueBurstBudget,
    duration_seconds: float,
    consumer_records_per_second: int = 100,
    queue_capacity: int | None = None,
) -> QueueBurstResult:
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive")
    if consumer_records_per_second <= 0:
        raise ValueError("consumer_records_per_second must be positive")
    if budget.connector_parallelism <= 0:
        raise ValueError("connector_parallelism must be positive")

    capacity = queue_capacity or max(1, budget.connector_parallelism * 2)
    queue: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue(maxsize=capacity)
    registry = InMemoryReplayRegistry()
    source_uri = "https://example.test/performance/queue-burst"
    total = max(1, math.ceil(budget.burst_records_per_second * duration_seconds))
    consumer_delay = budget.connector_parallelism / consumer_records_per_second

    accepted_ids: list[str] = []
    quarantined = 0
    provenance_ok = True
    publication_ok = True
    max_depth = 0
    backpressure_events = 0

    async def consumer() -> None:
        nonlocal quarantined, provenance_ok, publication_ok
        while True:
            record = await queue.get()
            try:
                if record is None:
                    return
                await asyncio.sleep(consumer_delay)
                normalized = normalize_connector_records(
                    [record],
                    context=IngestionContext(
                        connector_id="synthetic-performance-burst",
                        run_id=uuid4(),
                        source_uri=source_uri,
                        fetched_at=datetime.now(UTC),
                        confidence=80,
                    ),
                    external_id_field="external_id",
                    replay_registry=registry,
                )
                quarantined += len(normalized.quarantined)
                publication_ok = publication_ok and normalized.publish_approved is False
                for candidate in normalized.candidates:
                    accepted_ids.append(candidate.external_id)
                    provenance_ok = provenance_ok and (
                        candidate.source_uri == source_uri
                        and bool(candidate.payload_digest)
                        and candidate.confidence == 80
                        and candidate.raw_evidence.get("fixture_class") == "synthetic-queue-burst"
                    )
                    publication_ok = publication_ok and candidate.publish_approved is False
            finally:
                queue.task_done()

    consumers = [asyncio.create_task(consumer()) for _ in range(budget.connector_parallelism)]
    interval = 1.0 / budget.burst_records_per_second
    producer_started = perf_counter()

    for index in range(total):
        target = producer_started + (index * interval)
        delay = target - perf_counter()
        if delay > 0:
            await asyncio.sleep(delay)
        record = _synthetic_record(index)
        try:
            queue.put_nowait(record)
        except asyncio.QueueFull:
            backpressure_events += 1
            await queue.put(record)
        max_depth = max(max_depth, queue.qsize())

    producer_finished = perf_counter()
    await queue.join()
    recovered_at = perf_counter()

    for _ in consumers:
        await queue.put(None)
    await asyncio.gather(*consumers)

    accepted = len(accepted_ids)
    unique_accepted = len(set(accepted_ids))
    duplicate_candidates = accepted - unique_accepted
    accounted = accepted + quarantined
    data_loss = max(0, total - accounted)
    recovery = recovered_at - producer_finished

    decision = "pass" if (
        accepted == total
        and quarantined == 0
        and data_loss <= budget.data_loss_max_records
        and duplicate_candidates <= budget.duplicate_candidate_max_records
        and max_depth <= capacity
        and backpressure_events > 0
        and recovery <= budget.recovery_max_seconds
        and provenance_ok
        and publication_ok
    ) else "fail"

    return QueueBurstResult(
        submitted_records=total,
        accepted_candidates=accepted,
        quarantined_records=quarantined,
        duplicate_candidate_records=duplicate_candidates,
        data_loss_records=data_loss,
        queue_capacity=capacity,
        max_queue_depth=max_depth,
        backpressure_events=backpressure_events,
        recovery_seconds_after_producer=recovery,
        provenance_preserved=provenance_ok,
        publication_state_preserved=publication_ok,
        decision=decision,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Bounded DTMO queue-pressure and connector-burst harness")
    parser.add_argument(
        "--profile", type=Path, default=Path("config/performance/phase5_workload_profile.json")
    )
    parser.add_argument("--duration-seconds", type=float, default=1.0)
    parser.add_argument("--consumer-records-per-second", type=int, default=100)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    budget = load_queue_burst_budget(args.profile)
    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    result = asyncio.run(
        run_queue_burst_harness(
            budget=budget,
            duration_seconds=args.duration_seconds,
            consumer_records_per_second=args.consumer_records_per_second,
        )
    )

    evidence = {
        "schema_version": 1,
        "profile_id": profile["profile_id"],
        "scope": "queue-pressure-and-connector-burst",
        "dataset": {
            "fixture_class": "synthetic-queue-burst",
            "scaled_ci_fixture": True,
            "configured_burst_duration_seconds": profile["traffic"]["ingestion_burst_duration_seconds"],
            "executed_burst_duration_seconds": args.duration_seconds,
        },
        "budget": {
            "burst_records_per_second": budget.burst_records_per_second,
            "connector_parallelism": budget.connector_parallelism,
            "queue_recovery_max_seconds_after_burst": budget.recovery_max_seconds,
            "data_loss_max_records": budget.data_loss_max_records,
            "duplicate_candidate_max_records": budget.duplicate_candidate_max_records,
        },
        "result": result.as_dict(),
        "external_load_gate_satisfied": False,
        "degraded_dependency_tested": False,
        "decision": result.decision,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
    raise SystemExit(0 if result.decision == "pass" else 1)


if __name__ == "__main__":
    main()
