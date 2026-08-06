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
- Every new branch still requires its own exact-head execution.

## Phase 2 — Application security and identity

Current state after `RUN-20260806-036`:

- least-privilege RBAC, trusted principals, JWKS rotation, token-state enforcement and governed decision auditing are evidenced;
- only CISO and administrator roles receive `revoke:tokens`;
- the revocation API requires a JTI, future expiry, human rationale and request correlation;
- successful revocation writes expiry-bounded Redis state and appends an immutable allow event with reason provenance;
- permission denials append principal, permission, route and correlation evidence before returning 403;
- inability to persist denial evidence remains fail closed and returns 503 rather than allowing access;
- service accounts receive no revocation permission;
- focused revocation and denial-audit regressions are committed;
- exact-head RC5.9 CI evidence remains `PENDING`;
- cross-system revocation/audit reconciliation is recorded as a future resilience objective;
- Phase 2 completion remains `BLOCKED` until RC5.9 and remaining privacy controls are evidenced.

## Phase 3 — Data integrity and recovery

- canonical and persistent-audit migrations are evidenced;
- clean-environment restoration, RPO and RTO evidence are not yet implemented;
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
- missing CI or scan evidence may not be reported as successful.

## Current run decision

`RUN-20260806-036` is `CI_VALIDATION_PENDING` until the exact PR-head Quality Gate completes successfully.

## Exactly one next priority

Inspect the exact-head RC5.9 Quality Gate and either resolve only its earliest deterministic failure or merge after full success.
