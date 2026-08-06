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
| Release | All release-critical jobs and evidence artifacts succeed |

## Phase 1 — CI and workflow integrity

- RC5.1 Quality Gate #177: `PASS`.
- RC5.2 Quality Gate #179: `PASS`.
- RC5.3 Quality Gate #197: `PASS`.
- RC5.4 Quality Gate #203: `PASS`.
- RC5.5 Quality Gate #205: `PASS`.
- Every new branch still requires its own exact-head execution.

## Phase 2 — Application security and identity

Current state after `RUN-20260806-032`:

- least-privilege RBAC, trusted principals, JWKS rotation and tamper-evident in-memory audit-chain logic are evidenced;
- persistent audit records now have deterministic sequence numbers, unique event IDs and hashes, prior-hash continuity and provenance fields;
- transactional append locks the current chain tail and flushes the next record in the caller transaction;
- rollback leaves no persisted chain advancement;
- persisted chains can be reloaded and cryptographically verified;
- migration `0003_persistent_audit` adds the table and a PostgreSQL trigger rejecting UPDATE and DELETE;
- migration downgrade removes trigger, function, indexes and table reversibly;
- focused persistence, rollback, tamper-detection and migration-contract regressions are committed;
- exact-head CI evidence for this objective remains `PENDING`;
- runtime wiring of authorization and publication decisions remains a separate bounded objective;
- Phase 2 completion remains `BLOCKED` until remaining objectives are evidenced.

## Phase 3 — Data integrity and recovery

- canonical migrations are evidenced;
- clean-environment restoration, RPO and RTO evidence are not yet implemented;
- Phase 3 completion: `BLOCKED`.

## Security and publication invariants

- ingestion creates candidate intelligence only;
- reviewed and share-approved states remain distinct;
- external publication requires explicit human approval by a principal different from the reviewer;
- service accounts may not review or approve sharing;
- source provenance and confidence may not be silently discarded;
- production secrets may not be committed;
- missing CI or scan evidence may not be reported as successful.

## Current run decision

`RUN-20260806-032` is `CI_VALIDATION_PENDING` until the exact PR-head Quality Gate completes successfully.

## Exactly one next priority

Inspect the exact-head Quality Gate and either resolve only its earliest deterministic failure or merge after full success.
