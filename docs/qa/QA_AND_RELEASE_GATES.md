# DTMO QA and Release Gates

## Purpose

Every DTMO development step must define and evaluate explicit quality gates. A configured or committed test that has not executed is `PENDING`, never `PASS`.

## Baseline blocking gates

| Domain | Blocking evidence |
|---|---|
| Build | Source compiles and required packages resolve |
| Unit and regression tests | New and affected logic executes successfully |
| Security | Authentication, authorization, secrets and input controls are verified |
| Governance | Human review, share approval and separation of duties are preserved |
| Data integrity | Provenance, confidence, constraints and migrations are verified |
| Privacy | Direct identifiers, purpose limitation, retention and legal holds are verified |
| Release | All release-critical jobs and evidence artifacts succeed |

## Phase 1 — CI and workflow integrity

- RC5.1 Quality Gate #177: `PASS`.
- RC5.2 Quality Gate #179: `PASS`.
- RC5.3 Quality Gate #197: `PASS`.
- RC5.4 Quality Gate #203: `PASS`.
- RC5.5 Quality Gate #205: `PASS`.
- RC5.6 Quality Gate #207: `PASS`.
- RC5.7 Quality Gate #209: `PASS`.
- RC5.8 Quality Gate #215: `PASS`.
- RC5.9 Quality Gate #217: `PASS`.
- RC5.10 Quality Gate #219: `PASS`.
- RC5.11 Quality Gate #221: `PASS`.
- Every new branch still requires its own exact-head execution.

## Phase 2 — Application security, identity and privacy

Current state after `RUN-20260806-039`:

- RC5.1 through RC5.11 are evidenced and merged;
- RC5.12 adds persistent privacy-minimized audit projections linked by restrictive foreign key to immutable source events;
- projection storage contains purpose-bound references rather than direct principal, token/resource or request identifiers;
- retention expiry is stored explicitly and legal hold requires an auditable reference;
- bounded purge batches select only expired, non-held projections and never delete source audit events;
- a credential-free daily schedule invokes the purge command through secret-backed `DTMO_DATABASE_URL` configuration;
- migration lineage, projection minimization, source preservation, legal hold, batch limiting and schedule safety have regressions committed;
- exact-head RC5.12 CI evidence remains `PENDING`;
- Phase 2 completion remains `BLOCKED` until RC5.12 is evidenced.

## Phase 3 — Data integrity and recovery

- canonical and persistent-audit migrations are evidenced;
- deterministic recovery for volatile token-revocation state is evidenced;
- clean-environment database/object restoration, RPO and RTO evidence are not yet implemented;
- Phase 3 completion: `BLOCKED`.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- reviewed and share-approved states remain distinct;
- external publication requires explicit human approval by a principal different from the reviewer;
- service accounts may not review, approve sharing or revoke tokens;
- source provenance and confidence may not be silently discarded;
- production secrets may not be committed;
- production token-state failure must deny authentication;
- authorization-denial audit failure must never permit access;
- revocation recovery must never proceed from an invalid audit chain;
- privacy reporting projections must not expose direct identity, token or request identifiers;
- legal holds must be explicit and must block purge;
- immutable source audit records may not be deleted by privacy-retention processing;
- missing CI or scan evidence may not be reported as successful.

## Current run decision

`RUN-20260806-039` is `CI_VALIDATION_PENDING` until the exact PR-head Quality Gate completes successfully.

## Exactly one next priority

Inspect the exact-head RC5.12 Quality Gate and either resolve only its earliest deterministic failure or merge after full success.
