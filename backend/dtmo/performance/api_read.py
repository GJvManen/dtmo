from __future__ import annotations

import argparse
import asyncio
import json
import math
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any

import httpx


@dataclass(frozen=True)
class ApiReadBudget:
    requests_per_second: int
    p95_ms: float
    p99_ms: float
    error_rate_max_percent: float


@dataclass(frozen=True)
class ApiReadResult:
    target_url: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    achieved_requests_per_second: float
    p50_ms: float
    p95_ms: float
    p99_ms: float
    max_ms: float
    error_rate_percent: float
    publication_gate_preserved: bool
    authentication_boundary_reported: bool
    decision: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "target_url": self.target_url,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "achieved_requests_per_second": round(self.achieved_requests_per_second, 3),
            "latency_ms": {
                "p50": round(self.p50_ms, 3),
                "p95": round(self.p95_ms, 3),
                "p99": round(self.p99_ms, 3),
                "max": round(self.max_ms, 3),
            },
            "error_rate_percent": round(self.error_rate_percent, 3),
            "governance": {
                "publication_gate_preserved": self.publication_gate_preserved,
                "authentication_boundary_reported": self.authentication_boundary_reported,
                "load_test_may_publish": False,
            },
            "decision": self.decision,
        }


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return math.inf
    ordered = sorted(values)
    index = max(0, math.ceil(percentile * len(ordered)) - 1)
    return ordered[index]


def load_api_read_budget(profile_path: Path) -> ApiReadBudget:
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
    if privacy["synthetic_only"] is not True:
        raise ValueError("performance profile must require synthetic fixtures")
    if privacy["production_personal_data_allowed"] is not False:
        raise ValueError("performance profile must forbid production personal data")

    return ApiReadBudget(
        requests_per_second=int(traffic["api_read_requests_per_second"]),
        p95_ms=float(budgets["api_read_p95_ms"]),
        p99_ms=float(budgets["api_read_p99_ms"]),
        error_rate_max_percent=float(budgets["error_rate_max_percent"]),
    )


async def run_api_read_harness(
    *,
    target_url: str,
    budget: ApiReadBudget,
    duration_seconds: float,
    concurrency: int,
    timeout_seconds: float = 5.0,
    transport: httpx.AsyncBaseTransport | None = None,
) -> ApiReadResult:
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive")
    if concurrency <= 0:
        raise ValueError("concurrency must be positive")
    if not target_url.startswith(("http://", "https://")):
        raise ValueError("target_url must be HTTP(S)")

    total_requests = max(1, math.ceil(budget.requests_per_second * duration_seconds))
    semaphore = asyncio.Semaphore(concurrency)
    latencies_ms: list[float] = []
    failed_requests = 0
    publication_gate_preserved = True
    authentication_boundary_reported = True
    started = perf_counter()

    async with httpx.AsyncClient(timeout=timeout_seconds, transport=transport) as client:
        async def execute(index: int) -> None:
            nonlocal failed_requests, publication_gate_preserved, authentication_boundary_reported
            scheduled_at = started + (index / budget.requests_per_second)
            delay = scheduled_at - perf_counter()
            if delay > 0:
                await asyncio.sleep(delay)

            async with semaphore:
                request_started = perf_counter()
                try:
                    response = await client.get(
                        target_url,
                        headers={"x-correlation-id": f"perf-api-read-{index:06d}"},
                    )
                    latency_ms = (perf_counter() - request_started) * 1000
                    latencies_ms.append(latency_ms)
                    if response.status_code != 200:
                        failed_requests += 1
                        return
                    payload = response.json()
                    publication_gate_preserved = publication_gate_preserved and (
                        payload.get("publication_gate") == "human-approval-required"
                    )
                    authentication_boundary_reported = authentication_boundary_reported and (
                        payload.get("authentication") == "api-key-and-rbac"
                    )
                except (httpx.HTTPError, ValueError):
                    latency_ms = (perf_counter() - request_started) * 1000
                    latencies_ms.append(latency_ms)
                    failed_requests += 1

        await asyncio.gather(*(execute(index) for index in range(total_requests)))

    elapsed = perf_counter() - started
    successful_requests = total_requests - failed_requests
    error_rate_percent = (failed_requests / total_requests) * 100
    p95_ms = _percentile(latencies_ms, 0.95)
    p99_ms = _percentile(latencies_ms, 0.99)
    decision = "pass" if (
        p95_ms <= budget.p95_ms
        and p99_ms <= budget.p99_ms
        and error_rate_percent <= budget.error_rate_max_percent
        and publication_gate_preserved
        and authentication_boundary_reported
    ) else "fail"

    return ApiReadResult(
        target_url=target_url,
        total_requests=total_requests,
        successful_requests=successful_requests,
        failed_requests=failed_requests,
        achieved_requests_per_second=total_requests / elapsed,
        p50_ms=_percentile(latencies_ms, 0.50),
        p95_ms=p95_ms,
        p99_ms=p99_ms,
        max_ms=max(latencies_ms, default=math.inf),
        error_rate_percent=error_rate_percent,
        publication_gate_preserved=publication_gate_preserved,
        authentication_boundary_reported=authentication_boundary_reported,
        decision=decision,
    )


async def _main() -> int:
    parser = argparse.ArgumentParser(description="Bounded DTMO API-read performance harness")
    parser.add_argument("--target-url", required=True)
    parser.add_argument(
        "--profile",
        default="config/performance/phase5_workload_profile.json",
        type=Path,
    )
    parser.add_argument("--duration-seconds", type=float, default=5.0)
    parser.add_argument("--concurrency", type=int, default=50)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    budget = load_api_read_budget(args.profile)
    result = await run_api_read_harness(
        target_url=args.target_url,
        budget=budget,
        duration_seconds=args.duration_seconds,
        concurrency=args.concurrency,
    )
    evidence = {
        "schema_version": 1,
        "profile_id": json.loads(args.profile.read_text(encoding="utf-8"))["profile_id"],
        "scope": "api-read-only",
        "budget": {
            "requests_per_second": budget.requests_per_second,
            "p95_ms": budget.p95_ms,
            "p99_ms": budget.p99_ms,
            "error_rate_max_percent": budget.error_rate_max_percent,
        },
        "result": result.as_dict(),
        "decision": result.decision,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
    return 0 if result.decision == "pass" else 1


def main() -> None:
    raise SystemExit(asyncio.run(_main()))


if __name__ == "__main__":
    main()
