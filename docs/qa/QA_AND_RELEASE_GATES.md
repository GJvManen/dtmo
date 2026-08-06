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
- Every new branch still requires its own exact-head execution.

## Phase 2 — Application security, identity and privacy

Current state after `RUN-20260806-038`:

- least-privilege RBAC, trusted principals, JWKS rotation, token-state enforcement, operational revocation, denial auditing and revocation reconciliation are evidenced;
- RC5.11 adds derived audit projections that replace direct principal, resource and request identifiers with purpose-bound HMAC-SHA-256 references;
- direct free-text provenance is excluded from minimized projections while the immutable source event hash is retained for integrity correlation;
- retention decisions are explicit, timezone-safe and deterministic;
- legal hold overrides ordinary expiry without mutating the source audit chain;
- production requires a dedicated pseudonymization secret of at least 32 characters;
- identity projection retention may not exceed audit projection retention;
- source audit records remain append-only and cryptographically verifiable;
- exact-head RC5.11 CI evidence remains `PENDING`;
- storage-layer enforcement and scheduled purge execution remain a separate bounded objective;
- Phase 2 completion remains `BLOCKED` until RC5.11 is evidenced.

## Phase 3 — Data integrity and recovery

- canonical and persistent-audit migrations are evidenced;
- RC5.10 adds deterministic recovery for volatile token-revocation state from integrity-verified durable evidence;
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
- legal holds must be explicit and may not silently bypass auditability;
- missing CI or scan evidence may not be reported as successful.

## Current run decision

`RUN-20260806-038` is `CI_VALIDATION_PENDING` until the exact PR-head Quality Gate completes successfully.

## Exactly one next priority

Inspect the exact-head RC5.11 Quality Gate and either resolve only its earliest deterministic failure or merge after full success.
