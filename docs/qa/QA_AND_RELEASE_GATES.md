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

OpenSearch Recovery Gate #5 and RC4 Quality Gate #253 succeeded on exact head `fbe3924d202d81ab59ebbcd10889a9a75b146941`. Deterministic reconstruction evidence and aggregate release evidence are retained. PR #25 is merged.

### RC6.4 Combined multi-store acceptance — `CI_VALIDATION_PENDING`

Committed blocking controls:

- PostgreSQL, MinIO and OpenSearch execute in one isolated recovery workflow;
- all component evidence is bound to one `commit:${GITHUB_SHA}` recovery-point identifier;
- PostgreSQL requires clean-target restore, exact manifest equality, valid audit chain and retained provenance hashes;
- MinIO requires clean-target restore, exact object manifest equality, object SHA-256 and valid provenance references;
- OpenSearch requires clean-target reconstruction, exact manifest equality and preserved provenance references;
- every store must expose a bounded RPO;
- component timings are aggregated into a measured end-to-end RTO;
- the effective RPO is the maximum accepted component RPO;
- a deterministic SHA-256 binds all store manifests, audit evidence and provenance evidence;
- missing or non-pass component evidence fails closed;
- `multistore-recovery-evidence` uploads aggregate and component evidence with `if-no-files-found: error`;
- a separate `recovery-acceptance-gate` runs with `always()` and fails unless the recovery job succeeds;
- regression tests protect successful binding, missing provenance rejection, unbounded RPO rejection and workflow observability.

No exact-head RC6.4 execution or retained aggregate artifact has completed. RC6.4 and Phase 3 therefore remain pending.

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

`RUN-20260806-043` is `CI_VALIDATION_PENDING`. Code, tests, workflow and documentation are committed, but exact-head GitHub Actions and retained evidence are not yet successful.

## Exactly one next priority

Inspect the exact-head RC6 Multi-Store Recovery Gate and remediate only its earliest deterministic failure, or merge after all required gates and retained artifacts succeed.
