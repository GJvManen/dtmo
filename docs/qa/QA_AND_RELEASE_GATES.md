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
| Connector reliability | Live canary, persistent state, health history, isolation, provenance and quarantine recovery are evidenced |
| Release | All release-critical jobs and retained evidence artifacts succeed |

## Completed exact-head gates

- RC5.1 #177 through RC5.12 #224: `PASS`
- RC6.1 #229 through RC6.4 Multi-store Gate #4: `PASS`
- RC7.1 Canary Gate #3 and Quality Gate #270: `PASS`

## Phase status

- Phase 2 — application security, identity and privacy: `PASS`.
- Phase 3 — data integrity, backup and recovery: `PASS`.
- Phase 4 — live connector reliability and provenance: `IN PROGRESS`.

## RC7.1 governed live connector canary — `PASS`

Exact head `c82e20c110354c1163b58ac8b9820756f829a4ae` passed required gates with retained canary evidence artifact `8973407243`.

## RC7.2 persistent connector state and failure isolation — `CI_VALIDATION_PENDING`

Committed controls:

- PostgreSQL-backed runtime state per connector;
- durable health events bound to unique connector/run identifiers;
- connector-scoped isolation after a bounded consecutive-failure threshold;
- successful runs reset failure state and close isolation;
- quarantined raw evidence retains SHA-256 and reason;
- quarantine recovery requires a named human reviewer and review reference;
- recovery may only become `released_to_candidate` or `rejected`;
- health and quarantine records are database-constrained to `publish_approved = false`;
- migration `0005_connector_state` is reversible;
- `RC7 Connector State Gate` executes migration, persistence and recovery verification on PostgreSQL 17;
- retained evidence upload uses `if-no-files-found: error`;
- a separate `always()` gate fails closed unless connector-state evidence succeeds;
- persisted and supplied timestamps are normalized to UTC before isolation decisions;
- a focused regression test simulates a naive persisted isolation deadline and verifies active and expired decisions against UTC-aware inputs.

Connector State Gate #12 reached PostgreSQL-backed project execution and exposed an offset-naive versus offset-aware comparison defect after migrations succeeded. The runtime normalization remediation is committed as `6fab8341e8123664bc3456eaba8daf8d603a0933`; direct regression protection is committed as `52e3d37f119547637571d77a33636ffb996281c6`.

The subsequent exact head `d489a60bcc2492b0a7dc0423bdf91c32211a07ed` had no GitHub Actions workflow run registered when checked. PR #29 was mergeable and `.github/workflows/connector-state.yml` contained an applicable `pull_request` trigger without path exclusions. No Quality Gate, Connector State Gate, regression execution or retained artifact existed for that head. This is an external execution-evidence blocker and not a test pass.

These commits are not acceptance evidence. RC7.2 remains `CI_VALIDATION_PENDING` until the exact current head executes the Quality Gate, Connector State Gate and required regression gates successfully and retains the required evidence artifacts.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- publication requires explicit human approval by a principal different from the reviewer;
- service accounts and connectors may not review or approve sharing;
- connector success, isolation recovery or quarantine release never implies publication approval;
- provenance and confidence may not be silently discarded;
- missing, queued, cancelled or unexecuted CI and connector evidence may not be reported as successful.

## Current run decision

`RUN-20260807-046` is `CI_VALIDATION_PENDING`. Workflow triggers are configured and PR #29 is mergeable, but GitHub Actions did not register exact-head execution or retained evidence for the inspected head.

## Exactly one next priority

Inspect the first RC7 Connector State Gate registered for the current exact head and remediate only its earliest deterministic failure, or merge after all exact-head gates and retained evidence succeed.