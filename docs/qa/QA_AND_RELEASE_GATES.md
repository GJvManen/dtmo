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
- Every new branch still requires its own exact-head execution.

## Phase 2 — Application security and identity

Current state after `RUN-20260806-034`:

- least-privilege RBAC, trusted principals, JWKS rotation and governed decision auditing are evidenced;
- persistent append-only audit state and transactional review/share approval are evidenced through Quality Gates #205, #207 and #209;
- RC5.8 introduces shared Redis token state for production bearer authentication;
- revocation markers remain effective until the token expiry boundary;
- every JTI is bound to issuer, subject, principal type and roles, preventing identifier reuse for another principal;
- tokens explicitly marked `one_time=true` are consumed atomically through `SET NX` and replay is rejected;
- token-state backend failure denies production authentication rather than bypassing state checks;
- reusable access tokens remain reusable while their identity binding is unchanged and they are not revoked;
- focused revocation, replay, rebinding and validation regressions are committed;
- exact-head RC5.8 CI evidence remains `PENDING`;
- broader authorization-denial audit coverage and operational revocation administration remain separate bounded objectives;
- Phase 2 completion remains `BLOCKED` until remaining objectives are evidenced.

## Phase 3 — Data integrity and recovery

- canonical and persistent-audit migrations are evidenced;
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

`RUN-20260806-034` is `CI_VALIDATION_PENDING` until the exact PR-head Quality Gate completes successfully.

## Exactly one next priority

Inspect the exact-head RC5.8 Quality Gate and either resolve only its earliest deterministic failure or merge after full success.
