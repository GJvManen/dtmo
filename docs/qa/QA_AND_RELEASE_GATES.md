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
- RC6.3 OpenSearch Recovery Gate #5 and RC4 Quality Gate #253: `PASS`

Every new branch still requires its own exact-head execution.

## Phase 2 — Application security, identity and privacy

RC5.1 through RC5.12 are evidenced and merged. Least-privilege RBAC, trusted principals, asymmetric key rotation, revocation/replay controls, separation of duties, tamper-evident auditing, privacy minimization, legal hold and bounded retention purge are enforced.

**Phase 2 completion: `PASS`.**

## Phase 3 — Data integrity, backup and recovery

### RC6.1 PostgreSQL — `PASS`

Clean-target logical backup and restore, canonical intelligence, provenance, review/share state, Alembic revision and cryptographic audit-chain verification succeeded through Quality Gate #229.

### RC6.2 MinIO — `PASS`

Quality Gate #243 proved isolated source/target MinIO recovery, verified-empty target state, backup and object SHA-256 digests, exact object manifests, provenance references, recovery timing and retained evidence. PR #24 is merged.

### RC6.3 OpenSearch — `PASS`

OpenSearch Recovery Gate #5, run `31111652425`, and RC4 Quality Gate #253, run `31111652503`, succeeded on exact head `fbe3924d202d81ab59ebbcd10889a9a75b146941`.

Evidence proves:

- PostgreSQL is the canonical normalized source;
- the target index did not exist before reconstruction;
- root and provenance mappings are explicitly `dynamic: strict`;
- canonical content hash, governance state and provenance references are retained;
- source and target manifests are deterministically sorted and SHA-256 hashed;
- complete manifest digests and document counts match exactly;
- reconstruction duration and quiesced-source RPO basis are retained;
- the independent recovery gate fails closed unless reconstruction succeeds.

Retained artifacts:

- `opensearch-reconstruction-evidence` — `8971961873`;
- `release-gate-evidence` — `8971960034`;
- `postgres-restore-evidence` — `8971952797`;
- `minio-restore-evidence` — `8971939713`;
- `workflow-contract-evidence` — `8971929978`;
- `dependency-audit-evidence` — `8971928709`.

PR #25 merged as `4b08640e612801898307b065f7f2413c34a090c2`.

**RC6.3: `PASS`.**

Phase 3 remains `IN PROGRESS`: PostgreSQL, MinIO and OpenSearch are individually evidenced, but one combined multi-store recovery acceptance run with a consistent recovery point, cross-store provenance integrity and end-to-end RTO/RPO is still required.

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

`RUN-20260806-042` is `PASS`. The exact-head recovery and aggregate release gates succeeded, evidence is retained and PR #25 is merged.

## Exactly one next priority

Implement combined multi-store recovery acceptance for PostgreSQL, MinIO and OpenSearch with one consistent recovery point, cross-store provenance verification and measured end-to-end RTO/RPO.
