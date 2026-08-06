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

Current state after `RUN-20260806-020`:

- workflow-contract job in run `31090145413`: `PASS`;
- test, lint, type check and compile jobs in run `31090145413`: `PASS`;
- migrations upgrade, revision validation, downgrade and re-upgrade in run `31090145413`: `PASS`;
- container build and smoke test in run `31090145413`: `PASS`;
- dependency-review in run `31090145413`: `FAIL` because `pytest 8.4.2` matched `PYSEC-2026-1845`, `CVE-2025-71176`, `GHSA-6w46-j5rx-g56g`;
- dependency audit evidence artifact: ID `8963074009`, SHA-256 `b00f5410873b384e62c6f0c79b9fa95192d450a7cf51b6a0cac6fc7aa2158e5e`;
- required fixed pytest version: `9.0.3`;
- repository constraint: updated to `pytest>=9.0.3,<10`;
- replacement exact-head CI execution: `PENDING`;
- successful observer evidence for the replacement run: `PENDING`;
- Phase 1 completion: `BLOCKED` until the replacement run is successful and evidence is matched.

A previously successful numbered run does not override a later failed run on the current exact head. Phase 1 may advance only after one successful current-head `RC4 Quality Gate` run and matching observer evidence pass deterministic verification.

## Phase 3 — Data integrity and recovery evidence

Current state after `RUN-20260806-022`:

- canonical intelligence ORM and persistence model: implemented;
- explicit RC4-to-RC5 Alembic revision: implemented as `0002_rc5_canonical`;
- legacy intelligence and provenance confidence backfill: implemented before legacy-column removal;
- confidence and education-relevance range constraints: implemented;
- provenance uniqueness and reliability fields: implemented;
- immutable intelligence revision table and uniqueness controls: implemented;
- downgrade path restoring representable RC4 confidence values: implemented;
- migration contract regression tests: committed, execution `PENDING`;
- actual exact-head upgrade/current-revision/downgrade/re-upgrade evidence: `PENDING`;
- clean-environment backup and restoration evidence: `ABSENT`;
- tested RPO and RTO: `ABSENT`;
- Phase 3 completion: `BLOCKED`.

Phase 3 may not pass until the exact-head migration workflow succeeds and a clean-environment restore proves that database content, object evidence, provenance and checksums remain intact.

## Security and publication invariants

These are always blocking:

- ingestion must not create reviewed or share-approved intelligence;
- `reviewed` must remain separate from `share approved`;
- external publication requires explicit human approval;
- reports require evidence;
- source provenance and confidence may not be silently discarded;
- missing CI or scan results may not be reported as successful;
- production secrets may not be committed to the repository;
- privileged actions require explicit authorization.

## Per-run QA record

Every run file under `docs/development/runs/` must include a QA plan, QA results, actual commands or workflow names, commit identifiers, unresolved defects, release decision and exactly one next action.

## Release-level gates

A release may be marked `RC_READY` only when all release-blocking automated checks are successful, no critical or high unresolved security defect remains, migrations and recovery are validated, required API/integration/UI/accessibility tests pass, documentation is complete, governance invariants are verified and external acceptance requirements remain explicit.

`RC_READY` does not mean production accepted. Production acceptance additionally requires the external gates tracked in issue #1, including independent penetration testing, load testing, restoration testing and deployment acceptance.
