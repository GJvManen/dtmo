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
class SearchReadBudget:
    requests_per_second: int
    p95_ms: float
    p99_ms: float
    error_rate_max_percent: float


@dataclass(frozen=True)
class SearchReadResult:
    total_requests: int
    successful_requests: int
    failed_requests: int
    achieved_requests_per_second: float
    p50_ms: float
    p95_ms: float
    p99_ms: float
    max_ms: float
    error_rate_percent: float
    provenance_preserved: bool
    publication_state_preserved: bool
    decision: str

    def as_dict(self) -> dict[str, Any]:
        return {
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
                "provenance_preserved": self.provenance_preserved,
                "publication_state_preserved": self.publication_state_preserved,
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


def load_search_read_budget(profile_path: Path) -> SearchReadBudget:
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

    return SearchReadBudget(
        requests_per_second=int(traffic["search_requests_per_second"]),
        p95_ms=float(budgets["search_p95_ms"]),
        p99_ms=float(budgets["search_p99_ms"]),
        error_rate_max_percent=float(budgets["error_rate_max_percent"]),
    )


def synthetic_document(index: int) -> dict[str, Any]:
    return {
        "external_id": f"synthetic-{index:08d}",
        "title": f"Synthetic education threat record {index}",
        "summary": f"Synthetic phishing malware vulnerability campaign school cohort {index % 100}",
        "source_uri": f"https://example.test/source/{index % 25}",
        "confidence": 70 + (index % 26),
        "publish_approved": False,
        "fixture_class": "synthetic-performance",
    }


async def seed_synthetic_corpus(
    *, endpoint: str, index_name: str, document_count: int, batch_size: int = 500
) -> None:
    if document_count <= 0:
        raise ValueError("document_count must be positive")
    if not endpoint.startswith(("http://", "https://")):
        raise ValueError("endpoint must be HTTP(S)")

    async with httpx.AsyncClient(timeout=30.0) as client:
        await client.delete(f"{endpoint}/{index_name}")
        create = await client.put(
            f"{endpoint}/{index_name}",
            json={
                "settings": {"number_of_shards": 1, "number_of_replicas": 0},
                "mappings": {
                    "properties": {
                        "external_id": {"type": "keyword"},
                        "title": {"type": "text"},
                        "summary": {"type": "text"},
                        "source_uri": {"type": "keyword"},
                        "confidence": {"type": "integer"},
                        "publish_approved": {"type": "boolean"},
                        "fixture_class": {"type": "keyword"},
                    }
                },
            },
        )
        create.raise_for_status()

        for start in range(0, document_count, batch_size):
            lines: list[str] = []
            for i in range(start, min(start + batch_size, document_count)):
                lines.append(json.dumps({"index": {"_index": index_name, "_id": str(i)}}))
                lines.append(json.dumps(synthetic_document(i)))
            response = await client.post(
                f"{endpoint}/_bulk",
                content="\n".join(lines) + "\n",
                headers={"content-type": "application/x-ndjson"},
            )
            response.raise_for_status()
            payload = response.json()
            if payload.get("errors") is True:
                raise RuntimeError("OpenSearch bulk seed returned item errors")

        refresh = await client.post(f"{endpoint}/{index_name}/_refresh")
        refresh.raise_for_status()


async def run_search_read_harness(
    *,
    endpoint: str,
    index_name: str,
    budget: SearchReadBudget,
    duration_seconds: float,
    concurrency: int,
    timeout_seconds: float = 5.0,
    transport: httpx.AsyncBaseTransport | None = None,
) -> SearchReadResult:
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive")
    if concurrency <= 0:
        raise ValueError("concurrency must be positive")
    if not endpoint.startswith(("http://", "https://")):
        raise ValueError("endpoint must be HTTP(S)")

    total_requests = max(1, math.ceil(budget.requests_per_second * duration_seconds))
    semaphore = asyncio.Semaphore(concurrency)
    latencies_ms: list[float] = []
    failed_requests = 0
    provenance_preserved = True
    publication_state_preserved = True
    started = perf_counter()

    async with httpx.AsyncClient(timeout=timeout_seconds, transport=transport) as client:
        async def execute(request_index: int) -> None:
            nonlocal failed_requests, provenance_preserved, publication_state_preserved
            scheduled_at = started + (request_index / budget.requests_per_second)
            delay = scheduled_at - perf_counter()
            if delay > 0:
                await asyncio.sleep(delay)

            async with semaphore:
                request_started = perf_counter()
                try:
                    response = await client.post(
                        f"{endpoint}/{index_name}/_search",
                        headers={"x-correlation-id": f"perf-search-{request_index:06d}"},
                        json={
                            "size": 10,
                            "query": {
                                "multi_match": {
                                    "query": ["phishing", "malware", "vulnerability"][request_index % 3],
                                    "fields": ["title", "summary"],
                                }
                            },
                        },
                    )
                    latencies_ms.append((perf_counter() - request_started) * 1000)
                    if response.status_code != 200:
                        failed_requests += 1
                        return
                    hits = response.json().get("hits", {}).get("hits", [])
                    for hit in hits:
                        source = hit.get("_source", {})
                        provenance_preserved = provenance_preserved and bool(
                            source.get("external_id") and source.get("source_uri")
                        )
                        publication_state_preserved = publication_state_preserved and (
                            source.get("publish_approved") is False
                        )
                except (httpx.HTTPError, ValueError):
                    latencies_ms.append((perf_counter() - request_started) * 1000)
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
        and provenance_preserved
        and publication_state_preserved
    ) else "fail"

    return SearchReadResult(
        total_requests=total_requests,
        successful_requests=successful_requests,
        failed_requests=failed_requests,
        achieved_requests_per_second=total_requests / elapsed,
        p50_ms=_percentile(latencies_ms, 0.50),
        p95_ms=p95_ms,
        p99_ms=p99_ms,
        max_ms=max(latencies_ms, default=math.inf),
        error_rate_percent=error_rate_percent,
        provenance_preserved=provenance_preserved,
        publication_state_preserved=publication_state_preserved,
        decision=decision,
    )


async def _main() -> int:
    parser = argparse.ArgumentParser(description="Bounded DTMO OpenSearch read performance harness")
    parser.add_argument("--endpoint", default="http://127.0.0.1:9200")
    parser.add_argument("--index-name", default="dtmo-performance")
    parser.add_argument("--profile", type=Path, default=Path("config/performance/phase5_workload_profile.json"))
    parser.add_argument("--duration-seconds", type=float, default=5.0)
    parser.add_argument("--concurrency", type=int, default=20)
    parser.add_argument("--documents", type=int, default=5000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    budget = load_search_read_budget(args.profile)
    await seed_synthetic_corpus(
        endpoint=args.endpoint, index_name=args.index_name, document_count=args.documents
    )
    result = await run_search_read_harness(
        endpoint=args.endpoint,
        index_name=args.index_name,
        budget=budget,
        duration_seconds=args.duration_seconds,
        concurrency=args.concurrency,
    )
    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    evidence = {
        "schema_version": 1,
        "profile_id": profile["profile_id"],
        "scope": "opensearch-search-read-only",
        "dataset": {
            "fixture_class": "synthetic-performance",
            "documents_loaded": args.documents,
            "representative_intelligence_records_target": profile["dataset"]["intelligence_records"],
            "scaled_ci_fixture": True,
        },
        "budget": {
            "requests_per_second": budget.requests_per_second,
            "p95_ms": budget.p95_ms,
            "p99_ms": budget.p99_ms,
            "error_rate_max_percent": budget.error_rate_max_percent,
        },
        "result": result.as_dict(),
        "external_load_gate_satisfied": False,
        "decision": result.decision,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
    return 0 if result.decision == "pass" else 1


def main() -> None:
    raise SystemExit(asyncio.run(_main()))


if __name__ == "__main__":
    main()
