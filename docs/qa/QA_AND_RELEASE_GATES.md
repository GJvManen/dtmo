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

Current state after `RUN-20260806-035`:

- least-privilege RBAC, trusted principals, JWKS rotation and governed decision auditing are evidenced;
- persistent append-only audit state and transactional review/share approval are evidenced through Quality Gates #205, #207 and #209;
- RC5.8 introduces shared Redis token state for production bearer authentication;
- revocation markers remain effective until the token expiry boundary;
- every JTI is bound to issuer, subject, principal type and roles, preventing identifier reuse for another principal;
- tokens explicitly marked `one_time=true` are consumed atomically through `SET NX` and replay is rejected;
- token-state backend failure denies production authentication rather than bypassing state checks;
- Quality Gate #211 reached 90 passing tests before a legacy production-JWKS unit test attempted to contact undeclared Redis infrastructure;
- that test now supplies a controlled active token-state double and asserts the validated JTI reaches state enforcement;
- product fail-closed behavior is unchanged and remains covered by dedicated token-state failure regressions;
- a new exact-head Quality Gate is required; RC5.8 remains `BLOCKED`;
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
- production token-state failure must deny authentication;
- missing CI or scan evidence may not be reported as successful.

## Current run decision

`RUN-20260806-035` is `BLOCKED` until the updated exact PR #16 head completes its Quality Gate successfully.

## Exactly one next priority

Inspect the first exact-head Quality Gate after the Redis-isolated regression correction and either resolve only its earliest deterministic failure or merge after full success.
