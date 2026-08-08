# DTMO QA and Release Gates

## Purpose

Every DTMO development step defines and evaluates explicit quality gates. A configured, queued, cancelled or committed test that has not executed is `PENDING`, never `PASS`.

## Baseline blocking gates

| Domain | Blocking evidence |
|---|---|
| Build | Source compiles and required packages resolve |
| Unit and regression tests | New and affected logic executes successfully |
| Security | Authentication, authorization, secrets and input controls are verified |
| Governance | Human review, share approval and separation of duties are preserved |
| Data integrity | Provenance, confidence, constraints and migrations are verified |
| Privacy | Direct identifiers, purpose limitation, retention and legal holds are verified |
| Recovery | Clean targets restore or reconstruct successfully with integrity and timing evidence |
| Connector reliability | Live canary, persistent state, health history, isolation, provenance, governed contracts, retry, timeout, replay and quarantine recovery are evidenced |
| Performance | Accepted workload profile plus executed latency, throughput, error, integrity and resource evidence |
| Release | All release-critical jobs and retained evidence artifacts succeed |

## Current phase status

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS`.
- Phase 3 — data integrity, backup and recovery: `PASS`.
- Phase 4 — live connector reliability and provenance: `PASS`.
- Phase 5 — performance and scalability: `IN PROGRESS`.
- Phases 6–9: `NOT ACCEPTED`.
- Phase 10 — production go/no-go: `BLOCKED`.

## Phase 5 accepted gates

### RC8.1 workload profile — `PASS`

Representative synthetic education-sector CTI volumes and measurable latency, throughput, error-rate, correctness and resource budgets are defined in the machine-readable Phase 5 workload profile.

### RC8.2 API-read performance — `PASS`

Accepted exact-head evidence recorded:

- 500/500 successful bounded requests;
- 100.142 requests/s;
- 0% errors;
- p95 1.878 ms;
- p99 11.059 ms;
- limits p95 <= 300 ms, p99 <= 750 ms, errors <= 1%;
- authentication/RBAC and mandatory human-publication governance preserved.

### RC8.3 OpenSearch search-read performance — `PASS`

Accepted exact-head evidence recorded:

- 200/200 successful searches;
- 40.161 searches/s;
- 0% errors;
- p95 7.700 ms;
- p99 12.131 ms;
- limits p95 <= 800 ms, p99 <= 1500 ms, errors <= 1%;
- source provenance and non-publication state preserved.

### RC8.4 ingestion throughput — `PASS`

Accepted exact-head evidence recorded:

- 500/500 accepted synthetic records;
- zero data loss;
- zero duplicate candidate creation;
- identical second pass quarantined as replay;
- 0% errors;
- measured bounded CI throughput 108081.257 records/s against minimum 100 records/s;
- provenance and `publish_approved=false` preserved.

### RC8.5 queue pressure and connector burst — `CI_VALIDATION_PENDING`

RC8.5 is implemented only in open PR #42. It is not yet an accepted `main` capability and must not be reported as PASS until its exact-head workflows and retained queue-burst evidence are independently verified and merged.

## Workflow presence versus workflow evidence

The following Phase 5 workflow files were directly verified on `main` during RUN-20260808-077:

- `.github/workflows/api-read-performance.yml`;
- `.github/workflows/search-read-performance.yml`;
- `.github/workflows/ingestion-performance.yml`.

Presence of a workflow file is not execution evidence. The current-state reconciliation itself remains `CI_VALIDATION_PENDING` until its exact-head required workflows run successfully.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- publication requires explicit human approval by a principal different from the reviewer;
- service accounts and connectors may not review or approve sharing;
- connector success, isolation recovery, quarantine release, contract validation, normalization, retry, timeout or performance success never implies publication approval;
- provenance and confidence may not be silently discarded;
- secret values may not be emitted into evidence;
- performance fixtures must be synthetic or approved public fixtures;
- missing, queued, cancelled or unexecuted CI/evidence may not be reported as successful.

## External assurance boundary

The independent representative load/stress gate in issue #1 remains open. Bounded internal CI performance results do not satisfy that external gate. Other remaining issue #1 gates also require their own evidence.

## Current reconciliation gate

`RUN-20260808-077` is `CI_VALIDATION_PENDING`. It corrects stale README/current-state documentation, adds workflow inventory and Mermaid graphs, and explicitly distinguishes accepted `main` capabilities from RC8.5 work still in PR #42.

## Exactly one next priority

Inspect exact-head CI for the current-state reconciliation PR. Merge only after every required workflow succeeds; otherwise remediate only the earliest deterministic failure. Do not advance RC8.5 within this documentation-only run.