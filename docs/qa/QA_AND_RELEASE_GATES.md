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
| Recovery | Separate clean targets restore or reconstruct successfully and integrity plus timing are evidenced |
| Release | All release-critical jobs and retained evidence artifacts succeed |

## Completed exact-head gates

- RC5.1 #177 through RC5.12 #224: `PASS`
- RC6.1 #229: `PASS`
- RC6.2 #243: `PASS`

Every new branch still requires its own exact-head execution.

## Phase 2 — Application security, identity and privacy

RC5.1 through RC5.12 are evidenced and merged. Least-privilege RBAC, trusted principals, asymmetric key rotation, revocation/replay controls, separation of duties, tamper-evident auditing, privacy minimization, legal hold and bounded retention purge are enforced.

**Phase 2 completion: `PASS`.**

## Phase 3 — Data integrity, backup and recovery

### RC6.1 PostgreSQL — `PASS`

Clean-target logical backup and restore, canonical intelligence, provenance, review/share state, Alembic revision and cryptographic audit-chain verification succeeded through Quality Gate #229.

### RC6.2 MinIO — `PASS`

Quality Gate #243 proved isolated source/target MinIO recovery, verified-empty target state, backup and object SHA-256 digests, exact object manifests, provenance references, recovery timing and retained evidence. PR #24 is merged.

### RC6.3 OpenSearch — `CI_VALIDATION_PENDING`

Committed controls:

- PostgreSQL is the canonical normalized source;
- recovery uses a clean OpenSearch target where the index must not pre-exist;
- index mapping is explicit and dynamically strict;
- canonical documents retain content hash, governance state and provenance references;
- source and target manifests are sorted deterministically and SHA-256 hashed;
- document count and complete manifest digest must match exactly;
- reconstruction duration and quiesced-source RPO basis are retained;
- `opensearch-reconstruction-evidence` is uploaded with `if-no-files-found: error`;
- a separate `recovery-gate` executes with `always()` and fails closed unless reconstruction succeeds;
- workflow regression tests protect service isolation, evidence upload and fail-closed behavior.

No exact-head execution has completed, so no OpenSearch reconstruction result is accepted yet.

Open Phase 3 objective after RC6.3 is combined multi-store recovery acceptance. Phase 3 remains `BLOCKED` until all recovery controls are evidenced.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- reviewed and share-approved states remain distinct;
- external publication requires explicit human approval by a principal different from the reviewer;
- service accounts may not review, approve sharing or revoke tokens;
- source provenance and confidence may not be silently discarded;
- immutable source audit records may not be deleted by retention processing;
- search state is derived and may only be accepted after deterministic reconstruction from canonical data;
- backup, restore or reconstruction without post-recovery integrity verification may not be accepted;
- missing CI or recovery evidence may not be reported as successful.

## Current run decision

`RUN-20260806-042` is `CI_VALIDATION_PENDING` until the exact branch-head OpenSearch Recovery Gate reconstructs the index, verifies deterministic manifests and retains the required evidence.

## Exactly one next priority

Inspect the exact-head RC6.3 OpenSearch Recovery Gate and remediate only its earliest deterministic failure, or merge after complete success.
