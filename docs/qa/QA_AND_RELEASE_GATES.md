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
- RC6.4 Multi-store Recovery Gate #4, RC4 Quality Gate #262 and OpenSearch Recovery Gate #14: `PASS`

Every new branch still requires its own exact-head execution.

## Phase 2 — Application security, identity and privacy

RC5.1 through RC5.12 are evidenced and merged. **Phase 2 completion: `PASS`.**

## Phase 3 — Data integrity, backup and recovery

### RC6.1 PostgreSQL — `PASS`

Clean-target logical backup and restore, canonical intelligence, provenance, review/share state, Alembic revision and cryptographic audit-chain verification succeeded through Quality Gate #229.

### RC6.2 MinIO — `PASS`

Quality Gate #243 proved isolated source/target MinIO recovery, exact object digests, provenance references, timing and retained evidence.

### RC6.3 OpenSearch — `PASS`

OpenSearch Recovery Gate #5 and RC4 Quality Gate #253 proved deterministic clean reconstruction from canonical PostgreSQL data with strict provenance mappings and retained evidence.

### RC6.4 combined multi-store recovery — `PASS`

Exact head `ba3389613341c84aa21b591b706b7819981b7a4b` passed:

- RC6 Multi-store Recovery Gate #4, run `31113680268`;
- RC4 Quality Gate #262, run `31113681659`;
- RC6 OpenSearch Recovery Gate #14, run `31113680720`.

Evidence proves:

- one recovery-point identifier and UTC start timestamp bind the complete acceptance run;
- PostgreSQL, MinIO and OpenSearch recovery execute sequentially within the same bounded workflow;
- the PostgreSQL audit chain and provenance hashes remain valid;
- MinIO object digests and provenance references remain valid;
- OpenSearch provenance and deterministic source/target manifests match;
- all three subsystem decisions are `pass`;
- subsystem evidence files are SHA-256 bound into one combined artifact;
- a cross-store provenance-envelope digest is retained;
- zero-second quiesced-run RPO basis and measured end-to-end RTO are retained;
- the independent `always()` recovery gate fails closed unless combined recovery succeeds.

Retained artifacts:

- `multistore-recovery-evidence` — `8972811292`, digest `sha256:7739c8667acb87ab7d5377c0473586fce5959a3424432e0a78f04cf3ecd70502`;
- `release-gate-evidence` — `8972794627`;
- `postgres-restore-evidence` — `8972788335`;
- `minio-restore-evidence` — `8972774036`;
- `workflow-contract-evidence` — `8972771621`;
- `dependency-audit-evidence` — `8972771222`.

PR #26 merged as `d25c2e4a9c5e5869071020a109ddf57638779a02`.

**Phase 3 completion: `PASS`.**

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- reviewed and share-approved states remain distinct;
- external publication requires explicit human approval by a principal different from the reviewer;
- service accounts may not review, approve sharing or revoke tokens;
- source provenance and confidence may not be silently discarded;
- immutable source audit records may not be deleted by retention processing;
- search state is derived and may only be accepted after deterministic reconstruction from canonical data;
- missing CI or recovery evidence may not be reported as successful.

## Current run decision

`RUN-20260806-043` is `PASS`. Phase 3 recovery acceptance is complete and evidenced.

## Exactly one next priority

Start Phase 4 with one controlled live connector canary including source provenance, timeout, rate limiting, retry/backoff, quarantine and fail-closed human share approval.
