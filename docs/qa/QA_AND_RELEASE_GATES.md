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
- a focused regression test simulates a naive persisted isolation deadline and verifies active and expired decisions against UTC-aware inputs;
- new or updated parent runtime-state rows are explicitly flushed before health-event children are inserted.

Connector State Gate #13, run `31129850744`, provided independently observable PostgreSQL-backed execution on exact head `1fea5a9b07fa21cf16476a723bb1ddd656d0b39e`:

- Alembic upgrade through `0005_connector_state`: `PASS`;
- targeted connector-state and migration tests: `5 passed`;
- Quality Gate #288: `PASS`;
- Live Connector Canary Gate #21: `PASS`;
- OpenSearch Recovery Gate #40: `PASS`;
- Multi-store Recovery Gate #30: `PASS`;
- connector-state evidence fixture: `FAIL` with a PostgreSQL foreign-key violation because a health-event child was flushed before its newly created runtime-state parent;
- retained connector-state evidence artifact: absent because the primary job failed before upload;
- independent connector-state gate: correctly `FAIL` closed on missing evidence.

The bounded remediation is committed as `407fd75e149b50d28bb2830a17d26a877b09d9c4`. The parent `ConnectorRuntimeState` is now explicitly flushed before adding `ConnectorHealthEvent` children. This does not alter RBAC, separation of duties, privacy, provenance, quarantine decisions or human share approval.

The remediation commit is not acceptance evidence. RC7.2 remains `CI_VALIDATION_PENDING` until the exact current head executes the Quality Gate, Connector State Gate and required regression gates successfully and retains the required connector-state evidence artifact.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- publication requires explicit human approval by a principal different from the reviewer;
- service accounts and connectors may not review or approve sharing;
- connector success, isolation recovery or quarantine release never implies publication approval;
- provenance and confidence may not be silently discarded;
- missing, queued, cancelled or unexecuted CI and connector evidence may not be reported as successful.

## Current run decision

`RUN-20260807-047` is `CI_VALIDATION_PENDING`. Real PostgreSQL execution exposed and bounded a parent-before-child persistence-ordering defect; exact-head validation of the remediation and retained evidence are still required.

## Exactly one next priority

Inspect the RC7 Connector State Gate for the current exact head and remediate only its earliest deterministic failure, or merge PR #29 after all exact-head gates and retained evidence succeed.