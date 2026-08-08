# RC8.1 Performance Workload Profile Gate

Status: `CI_VALIDATION_PENDING`

## Control objective

Establish one reviewable, machine-readable workload contract for Phase 5 before any load generation is implemented. The contract must define representative synthetic education-sector CTI volumes, traffic rates, latency/throughput/resource budgets, integrity constraints and governance invariants.

## Required evidence for acceptance

- `config/performance/phase5_workload_profile.json` exists and is machine-readable;
- `docs/performance/PHASE5_WORKLOAD_PROFILE.md` documents the rationale, scenarios and evidence contract;
- regression tests execute successfully and prove synthetic-only fixtures, no publication under load, separation of review/share approval, positive representative volumes and measurable budgets;
- exact-head RC4 quality/regression CI is observable and successful;
- no configured, queued, skipped or absent test is treated as PASS.

## Defined budgets

The profile defines 1,000,000 intelligence records, 500,000 vulnerabilities, 5,000,000 IOCs, 20,000,000 graph edges and 500 GiB of raw-evidence capacity, with peak traffic including 100 API reads/s, 40 searches/s and 100 records/s sustained ingestion plus a 250 records/s ten-minute burst.

Primary user-facing latency budgets are API-read p95 <= 300 ms / p99 <= 750 ms, search p95 <= 800 ms / p99 <= 1,500 ms, and dashboard p95 <= 1,500 ms. Correctness is fail-closed: maximum data loss and duplicate candidate creation are both zero.

These are acceptance targets only; they are not measured results.

## Governance invariants

- only synthetic or approved public fixtures are permitted;
- production personal data is forbidden in performance fixtures;
- RBAC remains active under load;
- human review remains mandatory;
- share approval remains separate from review;
- service accounts may not approve sharing;
- performance or ingestion success never implies publication approval;
- provenance and integrity must survive burst and degraded-dependency scenarios.

## Current decision

`CI_VALIDATION_PENDING`. The workload contract is committed for review, but RC8.1 cannot be accepted until exact-head CI executes successfully. Phase 5 remains `IN PROGRESS`.

## Exactly one next priority

Inspect exact-head CI for the RC8.1 PR. If all required regression gates succeed, accept and merge the workload contract; if any gate fails, remediate only the earliest deterministic failure.
