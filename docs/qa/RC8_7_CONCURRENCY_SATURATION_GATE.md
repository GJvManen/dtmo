# RC8.7 — Concurrency Saturation Performance Gate

Status: `PASS`

## Objective

Provide one bounded, reviewable CI gate that exercises sustained concurrent synthetic read and ingest work against the Phase-5 workload contract. This remains an internal regression/scalability signal only and does not satisfy issue #1's independent representative production load/stress gate.

## Contract

The harness reads `config/performance/phase5_workload_profile.json` and fails closed unless privacy and governance invariants remain enabled. CI runs a scaled fixture at concurrency 20, 40 read requests/s and 40 ingest records/s for one second while retaining the planning contract of 50 peak concurrent users, 100 API read requests/s and 100 sustained ingest records/s.

Acceptance requires observed concurrency, latency/error compliance, zero ingest loss, synthetic-only fixtures, preserved non-publication, human review/share separation, successful focused regressions, retained exact-head evidence and successful repository-required workflows.

## Accepted exact-head evidence

PR #46 final exact head: `ba99df99ccfa2afba940a410b301bda0b493d0b2`.

All 19 registered workflows completed successfully on that head. Retained artifact `9032891744`, digest `sha256:01b07d36a4c9ae86f9e5361c6f2b7735cfaa29693adbf44aa62b12544132b1aa`, was independently inspected and explicitly bound to the same head.

Observed evidence:

- requested concurrency: 20;
- maximum inflight operations: 20;
- 40 synthetic read requests;
- 40 synthetic ingest records / 40 unique records;
- read p95: 5.876 ms against the 300 ms planning budget;
- error rate: 0.0% against the 1.0% budget;
- data loss: 0 records;
- publication disabled and publication state preserved;
- JUnit: 6 tests, 0 failures, 0 errors, 0 skipped.

The artifact explicitly records `external_load_gate_satisfied=false` and `representative_production_saturation_satisfied=false`.

PR #46 was merged with expected-head protection to `main` as `7ecd1bf88d0577074390a173847186c8a92e48b6`.

## External assurance boundary

RC8.7 does not close issue #1's independent load/stress test, production OpenSearch hardening, staging/deployment acceptance, external assurance or production go/no-go.

## Current decision

`PASS` for the bounded RC8.7 gate. Phase 5 proceeds to RC8.8 capacity limits and scaling guidance.
