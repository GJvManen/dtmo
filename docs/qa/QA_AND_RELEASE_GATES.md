# DTMO QA and Release Gates

## Purpose

Every DTMO development step, automated run, sprint and release must define and evaluate explicit quality gates. A change is not complete merely because files were committed.

## Mandatory lifecycle for every run

### 1. Plan the gates before implementation

Each run record must define:

- bounded objective;
- affected components and data flows;
- security, privacy and governance impact;
- tests to add or execute;
- blocking release gates;
- rollback or recovery consideration;
- expected evidence.

### 2. Implement

Implementation must include the appropriate combination of source code, migrations, automated tests, documentation, configuration, monitoring evidence and release notes.

### 3. Verify

A gate may be marked `PASS` only when its evidence is observable and linked or recorded. A configured test that has not run is `PENDING`, not `PASS`.

### 4. Decide the bounded run gate

Every run receives exactly one outcome: `PASS`, `BLOCKED` or `NO-CHANGE`. The overall release may remain `CI VALIDATION PENDING` or `BLOCKED` even if a bounded implementation objective passes.

## Baseline blocking gates

| Domain | Blocking evidence |
|---|---|
| Build | Source compiles and required packages resolve |
| Unit tests | New and affected logic is covered and tests pass |
| Integration | Connected services and data flows are tested |
| Regression | Existing critical controls remain functional |
| Security | Authentication, authorization, secrets and input controls are verified |
| Privacy | Data minimisation, purpose, retention and access implications are reviewed |
| Governance | Human review, share approval and separation of duties are preserved |
| Data quality | Provenance, confidence, deduplication, lineage and checksums are verified |
| Database | Migrations upgrade, downgrade where supported, and re-upgrade successfully |
| API | OpenAPI contract and failure behaviour are tested |
| Frontend | Responsive behaviour and critical user journeys are tested |
| Accessibility | WCAG checks and keyboard behaviour are validated |
| Performance | Applicable response-time, throughput or resource thresholds are met |
| Resilience | Retry, rollback, recovery or degraded behaviour is tested |
| Documentation | User, API, operational and architecture documents are updated |
| Release | Known limitations, blockers and next action are explicit |

## Phase 1 — CI and workflow integrity evidence

The committed presence of a workflow file is not release evidence. Phase 1 requires all of the following:

1. structural regression tests parse the workflow and verify required triggers, permissions, jobs, services, conditions and release-blocking commands;
2. the workflow contract runs as a dedicated job;
3. the primary artifact contains JUnit output plus an identity-bound JSON manifest;
4. that manifest records workflow, run ID, run attempt, repository, head SHA, event, conclusion and canonical run URL;
5. the evidence is retained as the named `workflow-contract-evidence` artifact;
6. a separate observer control records completion, conclusion, head SHA, run ID and URL;
7. observer evidence is retained as the named `ci-observation-evidence` artifact;
8. both artifacts are independently observable and their immutable identifiers match;
9. manual observer execution must explicitly identify a real upstream `RC4 Quality Gate` run and may not self-attest;
10. a deterministic verifier must reject failed, malformed, incomplete or mismatched evidence pairs;
11. a repository-side execution-readiness preflight must distinguish configuration readiness from actual workflow execution and must mark its own report as non-gate-eligible;
12. absent, skipped, cancelled or failed execution may not be interpreted as success.

Current state after `RUN-20260806-024`:

- RC5.1 exact-head Quality Gate #177 / run `31095343102`: `PASS`;
- test, lint, strict MyPy and compile jobs: `PASS`;
- migrations upgrade, current revision, downgrade and re-upgrade: `PASS`;
- dependency audit: `PASS`;
- container build and smoke test: `PASS`;
- workflow contract and aggregate release gate: `PASS`;
- evidence artifacts: `release-gate-evidence`, `workflow-contract-evidence`, `dependency-audit-evidence`;
- PR #9 merged into `main` as `e7d745a37b09076fe5e50bc408120e58b98bde7c`;
- merge commit status contexts observed during RUN-024: none;
- RC5.2 exact-head CI execution: `PENDING`.

Phase 1 CI integrity is evidenced by Quality Gate #177 for the merged RC5.1 head. New RC5.2 changes require their own exact-head execution before acceptance.

## Phase 2 — Application security and identity evidence

Current state after `RUN-20260806-024`:

- authenticated principal resolution and route-level RBAC: implemented previously;
- dedicated ingestion permission separate from review authority: implemented;
- explicit analyst, senior analyst, reviewer, publisher and service-account roles: implemented;
- service-account role mixing with human or administrator roles: denied;
- service accounts cannot review intelligence or approve sharing;
- share approval requires an authorized principal different from the reviewer;
- ingestion route now requires `ingest:intelligence`, not `review:intelligence`;
- positive and negative RBAC regression tests: committed, execution `PENDING`;
- enterprise identity or hardened trusted-proxy boundary: not yet evidenced;
- privileged-operation audit logging: not yet complete;
- secrets and static-analysis gates: not yet complete;
- Phase 2 completion: `BLOCKED`.

Phase 2 may not pass until the RC5.2 exact-head quality gate succeeds and the remaining identity, audit and security-scan objectives are evidenced.

## Phase 3 — Data integrity and recovery evidence

Current state after `RUN-20260806-024`:

- canonical intelligence ORM and persistence model: implemented;
- explicit RC4-to-RC5 Alembic revision: implemented as `0002_rc5_canonical`;
- legacy intelligence and provenance confidence backfill: implemented before legacy-column removal;
- confidence and education-relevance range constraints: implemented;
- provenance uniqueness and reliability fields: implemented;
- immutable intelligence revision table and uniqueness controls: implemented;
- downgrade path restoring representable RC4 confidence values: implemented;
- exact-head upgrade/current-revision/downgrade/re-upgrade in Quality Gate #177: `PASS`;
- migration contract tests in Quality Gate #177: `PASS`;
- clean-environment backup and restoration evidence: `ABSENT`;
- tested RPO and RTO: `ABSENT`;
- Phase 3 completion: `BLOCKED`.

Phase 3 may not pass until a clean-environment restore proves that database content, object evidence, provenance and checksums remain intact.

## Security and publication invariants

These are always blocking:

- ingestion must not create reviewed or share-approved intelligence;
- `reviewed` must remain separate from `share approved`;
- external publication requires explicit human approval by a principal different from the reviewer;
- service accounts may not review intelligence or approve external sharing;
- reports require evidence;
- source provenance and confidence may not be silently discarded;
- missing CI or scan results may not be reported as successful;
- production secrets may not be committed to the repository;
- privileged actions require explicit authorization.

## Per-run QA record

Every run file under `docs/development/runs/` must include a QA plan, QA results, actual commands or workflow names, commit identifiers, unresolved defects, release decision and exactly one next action.

## Release-level gates

A release may be marked `RC_READY` only when all release-blocking automated checks are successful, no critical or high unresolved security defect remains, migrations and recovery are validated, required API/integration/UI/accessibility tests pass, documentation is complete and governance invariants are verified.
