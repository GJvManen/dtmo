# RC8.7 — Concurrency Saturation Performance Gate

Status: `CI_VALIDATION_PENDING`

## Objective

Provide one bounded, reviewable CI gate that exercises sustained concurrent synthetic read and ingest work against the Phase-5 workload contract. This is an internal regression and scalability signal only; it does not satisfy the independent representative production load/stress gate in issue #1.

## Contract

The harness reads `config/performance/phase5_workload_profile.json` and fail-closes unless privacy and governance invariants remain enabled. CI runs a scaled fixture at concurrency 20, 40 read requests/s and 40 ingest records/s for one second while retaining the production contract of 50 peak concurrent users, 100 API read requests/s and 100 sustained ingest records/s.

Acceptance requires:

- observed concurrent execution at the requested bound;
- API-read p95 within the profile budget;
- error rate within the profile budget;
- zero ingest data loss;
- synthetic-only fixtures;
- publication remains disabled and human review/share separation remains required;
- focused regression tests execute successfully;
- retained JSON and JUnit evidence exists for the exact PR head;
- all repository-required workflows for that exact head succeed.

## Evidence boundary

The evidence output explicitly records:

- `external_load_gate_satisfied=false`;
- `representative_production_saturation_satisfied=false`.

Therefore this gate cannot close issue #1's independent load/stress test, production OpenSearch hardening, staging acceptance, external assurance, or production go/no-go.

## Inspected evidence

PR #46 implementation head `adf18135e91c0e28c151f8255563aba69b8df008` executed all 19 registered workflows successfully. Dedicated workflow run `31293634918` retained artifact `9032235183`, digest `sha256:66099a09e34099c3befc63918bdea0a8d0baf2302368138303eb6c96ccc1852d`, explicitly bound to that same head.

Independent artifact inspection recorded:

- requested concurrency: 20;
- maximum inflight operations: 20;
- 40 synthetic read requests;
- 40 synthetic ingest records and 40 unique ingested records;
- read p95: 5.734 ms against a 300 ms production-contract budget;
- error rate: 0.0% against a 1.0% budget;
- data loss: 0 records;
- publication disabled and publication state preserved;
- JUnit: 6 tests, 0 failures, 0 errors, 0 skipped.

The artifact correctly records `external_load_gate_satisfied=false` and `representative_production_saturation_satisfied=false`.

## Current decision

The implementation evidence satisfies the bounded RC8.7 contract, but the acceptance audit update itself changes PR #46's exact head. Therefore the gate remains `CI_VALIDATION_PENDING` until every registered workflow succeeds again on the final documentation head. Historical successful evidence is retained for audit but is not reused as final-head merge authorization.
