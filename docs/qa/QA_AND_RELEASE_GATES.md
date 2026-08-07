# DTMO QA and Release Gates

## Purpose

Every DTMO development step defines and evaluates explicit quality gates. A configured, queued, cancelled or committed test that has not executed is `PENDING`, never `PASS`.

## Baseline blocking gates

| Domain | Blocking evidence |
|---|---|
| Build | Source compiles and required packages resolve |
| Unit and regression tests | New and affected logic executes successfully |
| Security | Authentication, authorization, secrets and input controls are verified |
| Governance | Human review, share approval and separation of duties are preserved |
| Data integrity | Provenance, confidence, constraints and migrations are verified |
| Privacy | Direct identifiers, purpose limitation, retention and legal holds are verified |
| Recovery | Clean targets restore or reconstruct successfully with integrity and timing evidence |
| Connector reliability | Live canary, persistent state, health history, isolation, provenance, governed contracts and quarantine recovery are evidenced |
| Release | All release-critical jobs and retained evidence artifacts succeed |

## Completed exact-head gates

- RC5.1 #177 through RC5.12 #224: `PASS`
- RC6.1 #229 through RC6.4 Multi-store Gate #4: `PASS`
- RC7.1 Canary Gate #3 and Quality Gate #270: `PASS`
- RC7.2 Connector State Gate #17 and Quality Gate #292: `PASS`

## Phase status

- Phase 2 — application security, identity and privacy: `PASS`.
- Phase 3 — data integrity, backup and recovery: `PASS`.
- Phase 4 — live connector reliability and provenance: `IN PROGRESS`.

## RC7.1 governed live connector canary — `PASS`

Exact head `c82e20c110354c1163b58ac8b9820756f829a4ae` passed required gates with retained canary evidence artifact `8973407243`.

## RC7.2 persistent connector state and failure isolation — `PASS`

Accepted controls:

- PostgreSQL-backed runtime state per connector;
- durable health events bound to unique connector/run identifiers;
- connector-scoped isolation after a bounded consecutive-failure threshold;
- successful runs reset failure state and close isolation;
- quarantined raw evidence retains SHA-256 and reason;
- quarantine recovery requires a named human reviewer and review reference;
- recovery may only become `released_to_candidate` or `rejected`;
- health and quarantine records are database-constrained to `publish_approved = false`;
- migration `0005_connector_state` is reversible;
- persisted and supplied timestamps are normalized to UTC before isolation decisions;
- parent runtime-state rows are flushed before health-event children are inserted;
- retained evidence upload fails closed when evidence is absent;
- connector recovery never implies publication approval.

Exact head `af4625b0f285da6e2b0d5135a623c418a9f3b9d4` produced complete evidence:

- RC7 Connector State Gate #17, run `31132196662`: `PASS`;
- Alembic upgrade through `0005_connector_state`: `PASS`;
- targeted connector-state and migration tests: `PASS`;
- PostgreSQL-backed persistence and isolation fixture: `PASS`;
- independent fail-closed aggregate gate: `PASS`;
- retained artifact `connector-state-evidence`, ID `8976473782`;
- artifact digest `sha256:a3f23e76eb550c058d942918582488aa9782b78b8845e4c76b5d9bdf5a9139b9`;
- RC7 Live Connector Canary Gate #25: `PASS`;
- RC4 Quality Gate #292: `PASS`;
- RC6 OpenSearch Recovery Gate #44: `PASS`;
- RC6 Multi-store Recovery Gate #34: `PASS`.

PR #29 was merged from that exact head as squash commit `ac31b9d4409b97d6db734791365a3dd814255c9d`.

## RC7.3 governed connector contract validation — `CI_VALIDATION_PENDING`

Implemented controls:

- connector IDs must be unique and explicitly approved before live execution;
- source and terms endpoints require HTTPS and licence provenance is mandatory;
- source reliability and confidence are bounded;
- environment-backed credentials are validated for presence without serializing secret values;
- timeout, attempts, minimum request interval, maximum backoff and record-volume limits are bounded;
- malformed and duplicate records must be governed for quarantine;
- human review is mandatory and automatic publication is forbidden;
- evidence includes deterministic SHA-256 contract digests and always records `publish_approved = false`;
- approved CISA KEV contract preserves authoritative-source, feed and terms provenance;
- dedicated `RC7 Connector Contract Gate` runs focused regressions, retains `connector-contract-evidence` for 30 days and fails closed when its primary job is missing or unsuccessful;
- workflow structure itself is regression protected.

Observed pre-remediation evidence on exact head `b333d013d2b183d2678a7aaec04010bc6b1549d1`:

- RC7 Connector Contract Gate #1: `PASS`;
- RC7 Live Connector Canary Gate #30: `PASS`;
- RC7 Connector State Gate #18: `PASS`;
- RC6 OpenSearch Recovery Gate #49: `PASS`;
- RC6 Multi-store Recovery Gate #39: `PASS`;
- RC4 Quality Gate #297: `FAIL`;
- first deterministic RC4 failure: Ruff `S105` on a synthetic redaction-test fixture in `backend/tests/test_rc7_connector_contracts.py`;
- type check, tests and compile in the RC4 test job did not execute after lint failed.

RUN-20260807-050 remediated only that lint failure by making the fixture explicitly non-sensitive and applying a narrow line-level `S105` suppression. No repository-wide lint rule and no product control was weakened. New exact-head CI is required before acceptance.

The issue #1 external gate for validating real production credentials, rate limits, licences and terms for every live connector remains open; repository contract validation is not a substitute for external acceptance.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- publication requires explicit human approval by a principal different from the reviewer;
- service accounts and connectors may not review or approve sharing;
- connector success, isolation recovery, quarantine release or contract validation never implies publication approval;
- provenance and confidence may not be silently discarded;
- secret values may not be emitted into connector contract evidence;
- missing, queued, cancelled or unexecuted CI and connector evidence may not be reported as successful.

## Current run decision

`RUN-20260807-050` is `CI_VALIDATION_PENDING`. The first deterministic RC4 failure has been remediated, but the new exact head has not yet been accepted by GitHub Actions. Phase 4 remains `IN PROGRESS`.

## Exactly one next priority

Inspect the first RC4 Quality Gate registered for the current exact head; remediate only its earliest deterministic failure, or accept and merge RC7.3 only after the contract gate and required regression gates execute successfully with retained evidence.