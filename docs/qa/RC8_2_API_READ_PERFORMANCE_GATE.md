# RC8.2 API Read Performance Gate

Status: `CI_VALIDATION_PENDING`

## Control objective

Execute a bounded, synthetic API-read performance test against the accepted RC8.1 workload profile without broadening this run into search, ingestion or degraded-dependency testing.

## Scope

- target: DTMO `/health` read endpoint served by the real FastAPI application process;
- target request rate: 100 requests/second from `config/performance/phase5_workload_profile.json`;
- bounded duration: 5 seconds;
- bounded request count: 500;
- concurrency ceiling: 50;
- acceptance budgets: p95 <= 300 ms, p99 <= 750 ms, error rate <= 1%;
- retained evidence: JSON latency/error/governance evidence, JUnit regressions and API server log.

## Governance invariants

The harness reads its security/privacy requirements from the accepted workload profile and fails closed if publication is permitted, human review is not mandatory, review/share approval separation is removed, synthetic-only fixture policy is removed, or production personal data becomes permitted.

Runtime evidence also requires the tested DTMO endpoint to report `publication_gate=human-approval-required` and `authentication=api-key-and-rbac`. Load execution never grants publication approval, does not use production personal data and does not exercise mutating review/share-approval routes.

## Evidence rule

`PASS` requires actual exact-head execution of the dedicated `RC8 API Read Performance Gate` plus all release-critical regression workflows. Configured, queued, skipped, missing or unexecuted jobs are never PASS. The retained machine-readable evidence must report `decision=pass` and remain tied to the exact PR head.

## External assurance boundary

This CI harness is an internal bounded performance control. It does not close issue #1's independent representative load/stress test gate and does not establish production-scale search, ingestion, queue-pressure or degraded-dependency capacity.

## Current decision

`CI_VALIDATION_PENDING` until exact-head GitHub Actions execute and retained evidence is independently inspected.

## Exactly one next priority

Inspect all exact-head workflows for this PR. Remediate only the earliest deterministic failure, or accept and merge RC8.2 only if every required gate succeeds and retained API-read evidence satisfies the accepted profile budgets and governance invariants.
