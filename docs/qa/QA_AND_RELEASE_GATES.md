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

Current state after `RUN-20260806-017`:

- structural workflow contract: implemented;
- dedicated observable contract job: implemented;
- JUnit artifact design: implemented;
- identity-bound primary evidence manifest: implemented;
- manifest regression protection: implemented;
- independent observer workflow: implemented;
- observer regression protection: implemented;
- manual observer evidence validation: implemented;
- deterministic evidence-pair verifier: implemented;
- verifier positive and negative tests: implemented, execution `PENDING`;
- repository-side execution-readiness preflight: implemented;
- preflight positive and negative tests: implemented, execution `PENDING`;
- preflight output release-gate eligibility: explicitly `false`;
- historical quality-gate run `31075045431`: executed but `failure`, not gate-eligible;
- PR #7 quality-gate run `31082165346`: executed but `failure`, not gate-eligible;
- PR #7 quality-gate run `31082453008`: executed but `failure`, not gate-eligible;
- dependency installation, migrations and workflow-contracts in run `31082453008`: `PASS`;
- lint in run `31082453008`: `FAIL` with 41 findings; type checking and tests skipped;
- targeted Ruff repository/framework/test policy alignment: committed as `87089002f835e1bb2d076f924f1cd684984a3d79`;
- dependency review and container smoke test in run `31082453008`: `FAIL`, not addressed in this bounded run;
- replacement quality-gate execution for the lint-policy head: `PENDING`;
- successful quality-gate execution evidence: `PENDING`;
- successful observer execution evidence: `PENDING`;
- matching artifacts for one head SHA and run ID: `PENDING`;
- Phase 1 completion: `BLOCKED`.

Phase 1 may only advance after one completed `RC4 Quality Gate` run exposes its run ID, job results and a `workflow-contract-evidence` artifact containing both XML and JSON, followed by a matching `RC4 CI Observer` run for the same head SHA, and the downloaded pair passes `tools/verify_ci_evidence.py`.

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
