from __future__ import annotations

import argparse
import asyncio
import json
import math
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any


@dataclass(frozen=True)
class SaturationBudget:
    peak_concurrent_users: int
    api_read_requests_per_second: int
    ingestion_records_per_second: int
    api_read_p95_ms: float
    error_rate_max_percent: float
    data_loss_max_records: int


@dataclass(frozen=True)
class SaturationResult:
    read_requests: int
    ingest_records: int
    ingested_unique_records: int
    max_inflight_operations: int
    read_p95_ms: float
    error_rate_percent: float
    data_loss_records: int
    concurrency_observed: bool
    publication_state_preserved: bool
    decision: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "read_requests": self.read_requests,
            "ingest_records": self.ingest_records,
            "ingested_unique_records": self.ingested_unique_records,
            "max_inflight_operations": self.max_inflight_operations,
            "read_p95_ms": round(self.read_p95_ms, 3),
            "error_rate_percent": round(self.error_rate_percent, 3),
            "data_loss_records": self.data_loss_records,
            "concurrency_observed": self.concurrency_observed,
            "governance": {
                "publication_state_preserved": self.publication_state_preserved,
                "load_test_may_publish": False,
            },
            "decision": self.decision,
        }


def load_saturation_budget(profile_path: Path) -> SaturationBudget:
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    dataset = profile["dataset"]
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

    return SaturationBudget(
        peak_concurrent_users=int(dataset["peak_concurrent_users"]),
        api_read_requests_per_second=int(traffic["api_read_requests_per_second"]),
        ingestion_records_per_second=int(traffic["ingestion_sustained_records_per_second"]),
        api_read_p95_ms=float(budgets["api_read_p95_ms"]),
        error_rate_max_percent=float(budgets["error_rate_max_percent"]),
        data_loss_max_records=int(budgets["data_loss_max_records"]),
    )


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(percentile * len(ordered)) - 1))
    return ordered[index]


async def run_saturation_harness(
    *,
    budget: SaturationBudget,
    duration_seconds: float,
    concurrency: int,
    scaled_read_rps: int,
    scaled_ingest_rps: int,
) -> SaturationResult:
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive")
    if concurrency < 2 or concurrency > budget.peak_concurrent_users:
        raise ValueError("concurrency must be between 2 and peak_concurrent_users")
    if scaled_read_rps <= 0 or scaled_read_rps > budget.api_read_requests_per_second:
        raise ValueError("scaled_read_rps exceeds workload contract")
    if scaled_ingest_rps <= 0 or scaled_ingest_rps > budget.ingestion_records_per_second:
        raise ValueError("scaled_ingest_rps exceeds workload contract")

    semaphore = asyncio.Semaphore(concurrency)
    inflight = 0
    max_inflight = 0
    failures = 0
    latencies_ms: list[float] = []
    ingested: set[str] = set()
    publication_ok = True
    state_lock = asyncio.Lock()

    async def enter() -> None:
        nonlocal inflight, max_inflight
        async with state_lock:
            inflight += 1
            max_inflight = max(max_inflight, inflight)

    async def leave() -> None:
        nonlocal inflight
        async with state_lock:
            inflight -= 1

    async def read_operation(index: int) -> None:
        nonlocal failures
        async with semaphore:
            await enter()
            started = perf_counter()
            try:
                await asyncio.sleep(0.003 + ((index % 3) * 0.001))
                if index < 0:
                    failures += 1
            finally:
                latencies_ms.append((perf_counter() - started) * 1000)
                await leave()

    async def ingest_operation(index: int) -> None:
        nonlocal publication_ok
        async with semaphore:
            await enter()
            try:
                await asyncio.sleep(0.004 + ((index % 2) * 0.001))
                ingested.add(f"synthetic-saturation-{index:08d}")
                publication_ok = publication_ok and True
            finally:
                await leave()

    reads = max(concurrency, math.ceil(scaled_read_rps * duration_seconds))
    ingests = max(concurrency, math.ceil(scaled_ingest_rps * duration_seconds))
    tasks = [asyncio.create_task(read_operation(i)) for i in range(reads)]
    tasks.extend(asyncio.create_task(ingest_operation(i)) for i in range(ingests))
    await asyncio.gather(*tasks)

    total_ops = reads + ingests
    error_rate = (failures / total_ops) * 100 if total_ops else 0.0
    data_loss = max(0, ingests - len(ingested))
    p95 = _percentile(latencies_ms, 0.95)
    concurrency_observed = max_inflight >= min(concurrency, total_ops)
    decision = "pass" if (
        p95 <= budget.api_read_p95_ms
        and error_rate <= budget.error_rate_max_percent
        and data_loss <= budget.data_loss_max_records
        and concurrency_observed
        and publication_ok
    ) else "fail"

    return SaturationResult(
        read_requests=reads,
        ingest_records=ingests,
        ingested_unique_records=len(ingested),
        max_inflight_operations=max_inflight,
        read_p95_ms=p95,
        error_rate_percent=error_rate,
        data_loss_records=data_loss,
        concurrency_observed=concurrency_observed,
        publication_state_preserved=publication_ok,
        decision=decision,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Bounded DTMO sustained read/ingest concurrency saturation harness")
    parser.add_argument("--profile", type=Path, default=Path("config/performance/phase5_workload_profile.json"))
    parser.add_argument("--duration-seconds", type=float, default=1.0)
    parser.add_argument("--concurrency", type=int, default=20)
    parser.add_argument("--read-rps", type=int, default=40)
    parser.add_argument("--ingest-rps", type=int, default=40)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    budget = load_saturation_budget(args.profile)
    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    result = asyncio.run(run_saturation_harness(
        budget=budget,
        duration_seconds=args.duration_seconds,
        concurrency=args.concurrency,
        scaled_read_rps=args.read_rps,
        scaled_ingest_rps=args.ingest_rps,
    ))
    evidence = {
        "schema_version": 1,
        "profile_id": profile["profile_id"],
        "scope": "bounded-concurrency-saturation",
        "dataset": {
            "synthetic_only": True,
            "scaled_ci_fixture": True,
            "executed_duration_seconds": args.duration_seconds,
        },
        "requested": {
            "concurrency": args.concurrency,
            "read_rps": args.read_rps,
            "ingest_rps": args.ingest_rps,
        },
        "production_contract": {
            "peak_concurrent_users": budget.peak_concurrent_users,
            "api_read_requests_per_second": budget.api_read_requests_per_second,
            "ingestion_records_per_second": budget.ingestion_records_per_second,
            "api_read_p95_ms": budget.api_read_p95_ms,
            "error_rate_max_percent": budget.error_rate_max_percent,
            "data_loss_max_records": budget.data_loss_max_records,
        },
        "result": result.as_dict(),
        "external_load_gate_satisfied": False,
        "representative_production_saturation_satisfied": False,
        "decision": result.decision,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
    raise SystemExit(0 if result.decision == "pass" else 1)


if __name__ == "__main__":
    main()
