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
- RC5.6 Quality Gate #207: `PASS`.
- RC5.7 Quality Gate #209: `PASS`.
- RC5.8 Quality Gate #215: `PASS`.
- RC5.9 Quality Gate #217: `PASS`.
- Every new branch still requires its own exact-head execution.

## Phase 2 — Application security and identity

Current state after `RUN-20260806-037`:

- least-privilege RBAC, trusted principals, JWKS rotation, token-state enforcement, operational revocation and denial auditing are evidenced;
- RC5.10 records revocation expiry and rationale in versioned canonical JSON within the append-only audit event;
- reconciliation verifies the full persistent audit chain before using durable revocation evidence;
- missing active Redis revocation markers are restored with their original expiry boundary;
- existing markers are left unchanged and expired revocations are not recreated;
- malformed, incomplete or tampered durable evidence stops reconciliation rather than silently accepting drift;
- Redis inspection failures remain `TokenStateError` and therefore fail closed;
- focused restoration, idempotence, expiry and tamper regressions are committed;
- exact-head RC5.10 CI evidence remains `PENDING`;
- Phase 2 completion remains `BLOCKED` until RC5.10 and remaining privacy controls are evidenced.

## Phase 3 — Data integrity and recovery

- canonical and persistent-audit migrations are evidenced;
- RC5.10 adds deterministic recovery for volatile token-revocation state from integrity-verified durable evidence;
- clean-environment database/object restoration, RPO and RTO evidence are not yet implemented;
- Phase 3 completion: `BLOCKED`.

## Security and publication invariants

- ingestion creates candidate intelligence only;
- reviewed and share-approved states remain distinct;
- external publication requires explicit human approval by a principal different from the reviewer;
- service accounts may not review, approve sharing or revoke tokens;
- source provenance and confidence may not be silently discarded;
- production secrets may not be committed;
- production token-state failure must deny authentication;
- authorization-denial audit failure must never permit access;
- revocation recovery must never proceed from an invalid audit chain;
- missing CI or scan evidence may not be reported as successful.

## Current run decision

`RUN-20260806-037` is `CI_VALIDATION_PENDING` until the exact PR-head Quality Gate completes successfully.

## Exactly one next priority

Inspect the exact-head RC5.10 Quality Gate and either resolve only its earliest deterministic failure or merge after full success.
