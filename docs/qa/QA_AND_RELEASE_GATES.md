# DTMO QA and Release Gates

## Purpose

Every DTMO development step defines and evaluates explicit quality gates. A configured or committed test that has not executed is `PENDING`, never `PASS`.

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
- a separate `always()` gate fails closed unless connector-state evidence succeeds.

Connector State Gate #6, run `31118437816`, did not execute product tests because its primary job was cancelled. No connector-state artifact was retained. The independent aggregate gate failed as designed on missing evidence. This is not a product-test failure and is not accepted as `PASS`; a complete exact-head execution remains mandatory.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- publication requires explicit human approval by a principal different from the reviewer;
- service accounts and connectors may not review or approve sharing;
- connector success, isolation recovery or quarantine release never implies publication approval;
- provenance and confidence may not be silently discarded;
- missing, cancelled or unexecuted CI and connector evidence may not be reported as successful.

## Current run decision

`RUN-20260806-045` is `CI_VALIDATION_PENDING` until the exact-head Quality Gate and RC7 Connector State Gate complete successfully and retain evidence.

## Exactly one next priority

Inspect the exact-head RC7 Connector State Gate and remediate only its earliest deterministic failure, or merge after all exact-head gates and retained evidence succeed.
