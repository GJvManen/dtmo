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

RC5.1 through RC5.12 are evidenced and merged. **Phase 2 completion: `PASS`.**

## Phase 3 — Data integrity, backup and recovery

### RC6.1 PostgreSQL — `PASS`

Clean-target logical backup and restore, canonical intelligence, provenance, review/share state, Alembic revision and cryptographic audit-chain verification succeeded through Quality Gate #229.

### RC6.2 MinIO — `PASS`

Quality Gate #243 proved isolated source/target MinIO recovery, exact object digests, provenance references, timing and retained evidence.

### RC6.3 OpenSearch — `PASS`

OpenSearch Recovery Gate #5 and RC4 Quality Gate #253 proved deterministic clean reconstruction from canonical PostgreSQL data with strict provenance mappings and retained evidence.

### RC6.4 combined multi-store recovery — `CI_VALIDATION_PENDING`

Committed controls:

- one recovery-point identifier and UTC start timestamp bind the complete acceptance run;
- PostgreSQL, MinIO and OpenSearch recovery execute sequentially within the same bounded workflow;
- the PostgreSQL audit chain and provenance hashes must remain valid;
- MinIO object digests and provenance references must remain valid;
- OpenSearch provenance and source/target manifest equality must remain valid;
- all three subsystem decisions must be `pass`;
- subsystem evidence files are SHA-256 bound into one combined artifact;
- a cross-store provenance envelope digest is recorded;
- zero-second quiesced-run RPO basis and measured end-to-end RTO are recorded;
- artifact upload uses `if-no-files-found: error`;
- a separate `always()` recovery gate fails closed unless the combined job succeeds;
- workflow contract tests protect these requirements.

No exact-head execution has completed successfully, so RC6.4 is not accepted as `PASS`.

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

`RUN-20260806-043` is `CI_VALIDATION_PENDING` until the exact-head multi-store workflow retains passing combined evidence and its fail-closed gate succeeds.

## Exactly one next priority

Inspect the exact-head RC6 Multi-store Recovery Gate and remediate only its earliest deterministic failure, or merge after complete success.
