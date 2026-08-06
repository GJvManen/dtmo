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
| Recovery | Separate clean targets restore successfully and integrity plus recovery timing are evidenced |
| Release | All release-critical jobs and retained evidence artifacts succeed |

## Completed exact-head gates

- RC5.1 #177: `PASS`
- RC5.2 #179: `PASS`
- RC5.3 #197: `PASS`
- RC5.4 #203: `PASS`
- RC5.5 #205: `PASS`
- RC5.6 #207: `PASS`
- RC5.7 #209: `PASS`
- RC5.8 #215: `PASS`
- RC5.9 #217: `PASS`
- RC5.10 #219: `PASS`
- RC5.11 #221: `PASS`
- RC5.12 #224: `PASS`
- RC6.1 #229: `PASS`
- RC6.2 #243: `PASS`

Every new branch still requires its own exact-head execution.

## Phase 2 — Application security, identity and privacy

RC5.1 through RC5.12 are evidenced and merged. Least-privilege RBAC, trusted principals, asymmetric key rotation, revocation/replay controls, separation of duties, tamper-evident auditing, privacy minimization, legal hold and bounded retention purge are enforced.

**Phase 2 completion: `PASS`.**

## Phase 3 — Data integrity, backup and recovery

### RC6.1 PostgreSQL

- clean-target logical backup and restore succeeded through Quality Gate #229;
- canonical intelligence, provenance, review/share state, Alembic revision and append-only auditrecords matched;
- the restored audit chain cryptographically verified;
- backup digest, recovery timing and machine-readable evidence were retained;
- PR #22 is merged.

**RC6.1: `PASS`.**

### RC6.2 MinIO

Quality Gate #243 succeeded on exact head `bd2fa4f16d09e924ae3aa0cfb40946aba1fc9084` (run ID `31110100789`). Evidence proves:

- separate source and target MinIO instances;
- verified-empty target bucket before restore;
- deterministic raw intelligence objects with explicit provenance references;
- manifest-bound compressed backup archive;
- SHA-256 digest for backup and every object;
- exact comparison of object name, size, content type, digest and provenance reference;
- measured restore duration and explicit quiesced-fixture RPO basis;
- release-critical `minio-restore` job included in the aggregate gate.

Retained artifacts:

- `minio-restore-evidence` — `8971294887`;
- `postgres-restore-evidence` — `8971307002`;
- `release-gate-evidence` — `8971313962`;
- `dependency-audit-evidence` — `8971291122`;
- `workflow-contract-evidence` — `8971287078`.

PR #24 merged to `main` as `2b623ada2d5dc2faa5d04414da719fe6b9ff6509`.

**RC6.2: `PASS`.**

Open Phase 3 objectives are OpenSearch reconstruction and combined multi-store recovery acceptance. Phase 3 remains `BLOCKED` until those required recovery controls are evidenced.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- reviewed and share-approved states remain distinct;
- external publication requires explicit human approval by a principal different from the reviewer;
- service accounts may not review, approve sharing or revoke tokens;
- source provenance and confidence may not be silently discarded;
- production secrets may not be committed;
- production token-state failure must deny authentication;
- authorization-denial audit failure must never permit access;
- privacy reporting projections must not expose direct identifiers;
- legal holds must block purge;
- immutable source audit records may not be deleted by retention processing;
- backup or restore completion without post-restore integrity verification may not be accepted;
- missing CI or recovery evidence may not be reported as successful.

## Current run decision

`RUN-20260806-041` is `PASS`. Quality Gate #243 executed the isolated MinIO backup and clean-target restore successfully on the exact PR head, retained all required evidence and PR #24 is merged.

## Exactly one next priority

Implement clean-environment OpenSearch reconstruction from canonical PostgreSQL and immutable MinIO evidence, with deterministic index-manifest verification.
