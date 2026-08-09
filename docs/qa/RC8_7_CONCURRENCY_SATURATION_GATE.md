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

## Current evidence

Implementation and dedicated workflow are present on branch `rc8-7-concurrency-saturation`. No CI result is claimed until GitHub Actions executes on the final exact PR head and the retained artifact is inspected.
