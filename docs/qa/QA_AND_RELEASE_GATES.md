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
| Recovery | A clean target restores successfully and integrity plus recovery timing are evidenced |
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
- RC5.12 Quality Gate #224: `PASS`.
- RC6.1 Quality Gate #229: `PASS`.
- Every new branch still requires its own exact-head execution.

## Phase 2 — Application security, identity and privacy

- RC5.1 through RC5.12 are evidenced and merged;
- least-privilege RBAC, trusted principals, asymmetric key rotation, revocation/replay controls and separation of duties are enforced;
- privileged authorization, review, share approval and revocation decisions are persisted in a tamper-evident append-only audit chain;
- privacy-minimized reporting projections use purpose-bound references, explicit retention and legal holds;
- storage-layer purge is bounded, scheduled and cannot remove immutable source audit records;
- Phase 2 completion: `PASS`.

## Phase 3 — Data integrity and recovery

Current state after `RUN-20260806-040`:

- canonical, append-only audit and privacy-projection migrations are evidenced;
- volatile token-revocation state can be reconciled from integrity-verified durable evidence;
- RC6.1 clean-target PostgreSQL logical backup and restoration is evidenced by Quality Gate #229 on exact head `d1d0e809ffcee6458cb8a8f31ad2d10d481fefb0`;
- a controlled source fixture contains canonical intelligence, authoritative provenance, review/share state and governed audit events;
- source and restored databases matched through deterministic manifests covering intelligence, provenance, audit records and Alembic revision state;
- the restored audit chain cryptographically verified and retained the same tail hash;
- provenance content hashes and canonical row counts matched exactly;
- the custom-format backup received a SHA-256 digest and was retained with machine-readable recovery evidence;
- measured restore duration and a quiesced-snapshot zero-second RPO basis were recorded;
- the `postgres-restore` job is included in the fail-closed aggregate release gate;
- retained artifacts: `postgres-restore-evidence` 8969397478, `release-gate-evidence` 8969403121, `workflow-contract-evidence` 8969379199 and `dependency-audit-evidence` 8969379447;
- PR #22 merged to `main` as `3441e5be486fd9bcca8ab1d8f531ca8e5d38958b`;
- MinIO object restoration, OpenSearch reconstruction and combined recovery objectives remain separate bounded runs;
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
- backup or restore completion without post-restore integrity verification may not be accepted;
- missing CI or recovery evidence may not be reported as successful.

## Current run decision

`RUN-20260806-040` is `PASS`. Quality Gate #229 and the clean-target PostgreSQL restore evidence succeeded on the exact PR head, and PR #22 is merged.

## Exactly one next priority

Implement clean-environment MinIO object backup and restore evidence with object digest and provenance-reference verification.
