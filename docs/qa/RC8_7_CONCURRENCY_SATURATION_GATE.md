# RC8.7 — Concurrency Saturation Performance Gate

Status: `PASS`

## Objective

Provide one bounded, reviewable CI gate that exercises sustained concurrent synthetic read and ingest work against the Phase-5 workload contract. This is an internal regression and scalability signal only; it does not satisfy the independent representative production load/stress gate in issue #1.

## Contract

The harness reads `config/performance/phase5_workload_profile.json` and fail-closes unless privacy and governance invariants remain enabled. CI runs a scaled fixture at concurrency 20, 40 read requests/s and 40 ingest records/s for one second while retaining the production contract of 50 peak concurrent users, 100 API read requests/s and 100 sustained ingest records/s.

Acceptance requires observed concurrency, p95/error budgets, zero ingest data loss, synthetic-only fixtures, publication disabled, human review/share separation, successful focused regressions, retained JSON/JUnit evidence for the exact PR head, and all registered workflows successful for that exact head.

## Final exact-head evidence

PR #46 exact head `ba99df99ccfa2afba940a410b301bda0b493d0b2` executed all 19 registered workflows successfully. Dedicated workflow run `31295730826` retained artifact `9032891744`, digest `sha256:01b07d36a4c9ae86f9e5361c6f2b7735cfaa29693adbf44aa62b12544132b1aa`, explicitly bound to that head.

Independent artifact inspection recorded:

- requested concurrency: 20;
- maximum inflight operations: 20;
- 40 synthetic read requests;
- 40 synthetic ingest records and 40 unique ingested records;
- read p95: 5.876 ms against a 300 ms production-contract budget;
- error rate: 0.0% against a 1.0% budget;
- data loss: 0 records;
- publication disabled and publication state preserved;
- JUnit: 6 tests, 0 failures, 0 errors, 0 skipped.

The artifact correctly records `external_load_gate_satisfied=false` and `representative_production_saturation_satisfied=false`.

## Acceptance

Immediately before merge, PR #46 was re-read and confirmed open, mergeable, non-draft and unchanged at exact head `ba99df99ccfa2afba940a410b301bda0b493d0b2`. All 19 registered workflows were re-fetched and remained `completed/success`.

An expected-head squash merge with that SHA succeeded. GitHub returned `merged=true` and merge commit `7ecd1bf88d0577074390a173847186c8a92e48b6`.

RC8.7 is therefore accepted on `main`. This PASS is scoped only to the bounded internal concurrency-saturation contract. It does not close issue #1's independent representative production load/stress gate or any staging/external-assurance gate.

## Exactly one next priority

RC8.8 — produce one bounded capacity-limits and scaling-guidance gate from the accepted Phase-5 evidence, with explicit observed-vs-representative boundaries and fail-closed wording. Do not claim the issue #1 independent representative production load/stress gate from internal synthetic CI evidence.