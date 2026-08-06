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

Implementation must include the appropriate combination of:

- source code;
- database migrations;
- automated tests;
- documentation;
- configuration examples;
- monitoring or audit evidence;
- release notes.

### 3. Verify

A gate may be marked `PASS` only when its evidence is observable and linked or recorded. Examples include:

- successful GitHub Actions check;
- test output or workflow artifact;
- migration output;
- verified API contract;
- reviewed security scan;
- browser accessibility report;
- checksum or data-quality report;
- documented human review.

A configured test that has not run is `PENDING`, not `PASS`.

### 4. Decide the bounded run gate

Every run receives exactly one outcome:

- `PASS`: the bounded objective is implemented and all run-specific blocking gates have evidence;
- `BLOCKED`: implementation or required validation is incomplete, failed or unsafe;
- `NO-CHANGE`: no justified safe change was made; the reason and next action are recorded.

The overall release may remain `CI VALIDATION PENDING` or `BLOCKED` even if a bounded documentation or implementation objective passes.

## Baseline blocking gates

The following gates apply whenever relevant.

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
3. the job produces machine-readable evidence, currently JUnit XML;
4. the evidence is retained as the named `workflow-contract-evidence` artifact;
5. a separate observer control records completion, conclusion, head SHA, run ID and URL;
6. observer evidence is retained as the named `ci-observation-evidence` artifact;
7. both the quality-gate run and observer result are independently observable for the same commit;
8. manual observer execution must explicitly identify a real upstream `RC4 Quality Gate` run and may not self-attest with the observer's own metadata;
9. absent, skipped, cancelled or failed execution may not be interpreted as success.

Current state after `RUN-20260806-007`:

- structural workflow contract: implemented;
- dedicated observable contract job: implemented;
- retained workflow-contract artifact design: implemented;
- independent observer workflow: implemented;
- observer regression protection: implemented;
- manual observer evidence inputs and validation: implemented;
- observer permissions: structurally limited to `actions: read` and `contents: read`;
- successful quality-gate execution evidence: `PENDING`;
- successful observer execution evidence: `PENDING`;
- matching artifacts for one head SHA: `PENDING`;
- likely external control to verify: repository Actions permissions and workflow enablement;
- Phase 1 completion: `BLOCKED`.

Phase 1 may only advance after an administrator permits or validates Actions execution and one completed `RC4 Quality Gate` run exposes its run ID, job results and `workflow-contract-evidence` artifact, followed by a matching `RC4 CI Observer` run with `ci-observation-evidence` for the same head SHA.

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

Every run file under `docs/development/runs/` must include:

```markdown
## QA plan

| Gate | Method | Blocking |
|---|---|---:|
| ... | ... | Yes/No |

## QA results

| Gate | Result | Evidence |
|---|---|---|
| ... | PASS/BLOCKED/PENDING/NOT-APPLICABLE | ... |
```

It must also include:

- actual test commands or workflow names;
- commit identifiers;
- unresolved defects;
- release decision;
- one next action.

## Release-level gates

A release may be marked `RC_READY` only when:

1. all release-blocking automated checks are successful;
2. no critical or high unresolved security defect remains;
3. migrations and recovery procedures are validated;
4. required API, integration, UI and accessibility tests pass;
5. documentation and known limitations are complete;
6. governance invariants are verified;
7. external acceptance requirements are either passed or explicitly keep the release non-production.

`RC_READY` does not mean production accepted. Production acceptance additionally requires the external gates tracked in issue #1, including independent penetration testing, load testing, restoration testing and deployment acceptance.
