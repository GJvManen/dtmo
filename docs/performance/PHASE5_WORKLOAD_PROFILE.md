# Phase 5 Workload Profile and Performance Budgets

Status: `DEFINED_NOT_YET_EVIDENCED`

## Objective

Define the representative education-sector workload and measurable acceptance thresholds that all Phase 5 load, stress, burst and degraded-dependency tests must use. This document is a test contract, not performance evidence.

## Workload model

The profile is intentionally synthetic and privacy-safe. No production personal data is permitted in performance fixtures.

### Dataset envelope

| Dimension | Phase 5 representative volume |
|---|---:|
| Education organisations | 250 |
| Analyst/CISO/audit users | 200 |
| Peak concurrent users | 50 |
| Intelligence records | 1,000,000 |
| Vulnerability records | 500,000 |
| IOC records | 5,000,000 |
| Knowledge-graph edges | 20,000,000 |
| Raw-evidence objects | 2,000,000 |
| Raw-evidence capacity | 500 GiB |

These are deliberately conservative synthetic capacity assumptions for DTMO production-readiness testing. They are not claims about actual school populations, actual incident counts or production data holdings.

### Traffic envelope

| Workload | Target |
|---|---:|
| API reads | 100 req/s |
| API writes | 25 req/s |
| Search | 40 req/s |
| Dashboard loads | 10 req/s |
| Sustained ingestion | 100 records/s |
| Burst ingestion | 250 records/s for 10 minutes |
| Concurrent connector executions | 20 |

## Acceptance budgets

| Measure | Budget |
|---|---:|
| API read p95 | <= 300 ms |
| API read p99 | <= 750 ms |
| API write p95 | <= 500 ms |
| Search p95 | <= 800 ms |
| Search p99 | <= 1,500 ms |
| Dashboard p95 | <= 1,500 ms |
| Sustained ingestion | >= 100 records/s |
| Burst ingestion | >= 250 records/s |
| Error rate | <= 1.0% |
| Data loss | 0 records |
| Duplicate candidate creation | 0 records |
| API average CPU | <= 70% |
| API average memory | <= 75% |
| PostgreSQL average CPU | <= 70% |
| OpenSearch average heap | <= 75% |
| Queue recovery after burst | <= 900 s |

Latency budgets apply after warm-up and must be reported with sample count, duration, concurrency, environment identity and exact commit SHA. Throughput PASS requires correctness at the same time: no data loss, no duplicate candidate creation, intact provenance, and no bypass of quarantine or human approval.

## Required Phase 5 scenarios

Subsequent bounded objectives must implement and execute, in roadmap order:

1. API and PostgreSQL representative read/write load;
2. OpenSearch query load against the defined corpus;
3. ingestion sustained-load and 10-minute burst tests;
4. queue pressure and connector-burst tests;
5. degraded PostgreSQL/OpenSearch/object-store dependency tests;
6. capacity and scaling guidance derived from measured results.

A later test may use a smaller developer fixture for fast regression checks, but release evidence must exercise the representative envelope or document an equivalent scaled methodology with a defensible extrapolation. No extrapolation alone may satisfy the external load/stress gate in issue #1.

## Evidence contract

A Phase 5 measurement is gate-eligible only when it records:

- exact commit SHA and test-tool version;
- environment CPU, memory and storage allocation;
- dataset cardinalities actually loaded;
- duration, concurrency and request/record rate;
- p50/p95/p99 latency where applicable;
- successful/error counts and error taxonomy;
- resource utilisation over the measurement window;
- queue depth and recovery time for burst/degradation scenarios;
- integrity reconciliation proving zero data loss and zero duplicate candidates;
- provenance and publication-state checks;
- machine-readable retained evidence.

Configured thresholds, dry runs, skipped tests, unavailable dependencies or missing artifacts are `PENDING`/`BLOCKED`, never `PASS`.

## Security, privacy and governance invariants

- performance fixtures are synthetic or approved public test fixtures only;
- no production personal data or secret value may be copied into load-test artifacts;
- RBAC remains active under load;
- review and share approval remain separate human decisions;
- connectors and service accounts cannot approve sharing;
- performance success never implies publication approval;
- provenance, confidence, raw-evidence integrity and quarantine semantics remain mandatory under load and degradation.

## Machine-readable source of truth

`config/performance/phase5_workload_profile.json` is the machine-readable contract. `backend/tests/test_performance_workload_profile.py` regression-protects its privacy, governance, cardinality and threshold invariants.

## Current decision

This workload profile is defined but not yet performance-evidenced. Phase 5 remains `IN PROGRESS`.
