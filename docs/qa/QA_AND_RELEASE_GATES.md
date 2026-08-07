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
- RC7.3 Connector Contract Gate #5 and Quality Gate #301: `PASS`

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

## RC7.3 governed connector contract validation — `PASS`

Accepted controls:

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

Exact head `54ad16cd6694ba17aa2ab28d56c9beaeaf7b789f` produced complete release evidence:

- RC4 Quality Gate #301, run `31145386886`: `PASS`;
- RC7 Live Connector Canary Gate #34, run `31145386892`: `PASS`;
- RC7 Connector Contract Gate #5, run `31145386898`: `PASS`;
- RC7 Connector State Gate #22, run `31145386874`: `PASS`;
- RC6 Multi-store Recovery Gate #43, run `31145386891`: `PASS`;
- RC6 OpenSearch Recovery Gate #53, run `31145386961`: `PASS`;
- retained artifact `connector-contract-evidence`, ID `8981283640`, not expired;
- artifact digest `sha256:e5be71c0a30ebe4249877a3a990abc8726375293dd0c20b43411ea2e0af13733`;
- downloaded evidence aggregate decision: `pass`;
- duplicate connector IDs: none;
- evidence records `publish_approved = false` at connector and aggregate levels;
- deterministic CISA contract digest: `b55692915fe4ad450355c48139371240c330bc997411f0f5ab39df86c56b09ef`.

PR #30 was re-read immediately before merge and remained open, mergeable and unchanged at that exact head. It was merged with expected-head protection as squash commit `0e1d4d370aff0a1e340a10fe1fd373d282864abc`.

The issue #1 external gate for validating real production credentials, provider rate limits, licences and terms for every live connector remains open; repository contract validation is not a substitute for external acceptance.

## RC7.4 payload provenance and normalization enforcement — `CI_VALIDATION_PENDING`

Implemented controls:

- immutable ingestion context binds connector ID, run ID, HTTPS source URI, fetch timestamp and confidence before record acceptance;
- accepted candidates retain optional source timestamp, canonical SHA-256 raw-payload digest and raw evidence;
- naive fetch timestamps are normalized to UTC;
- malformed non-object records, missing external IDs, malformed supplied source timestamps and duplicate external IDs fail closed to quarantine;
- duplicate detection occurs before candidate creation;
- candidate, quarantine and aggregate normalization outputs always record `publish_approved = false`;
- deterministic canonical JSON hashing prevents dictionary key ordering from changing payload identity;
- dedicated `RC7 Payload Provenance Gate` runs focused regressions and emits retained machine-readable `payload-provenance-evidence`;
- the independent aggregate gate fails closed when the provenance job is missing or unsuccessful;
- workflow structure is regression protected.

The previous exact head `7d96a25cab1fff0fc6cf1d1235efd251618213a8` executed all required RC4/RC6/RC7 workflows successfully, but independent retained-artifact inspection found a release-evidence defect: `quarantine_publish_approved` was emitted as `true` even though every quarantined object itself had `publish_approved = false`. The evidence generator had inverted the meaning by storing `all(item.publish_approved is False ...)` under a positively named approval field, and the workflow asserted the misleading value as true.

RUN-20260807-053 corrected this evidence contract so `quarantine_publish_approved` represents actual approval state and must be `false`; the dedicated workflow now asserts false and a regression test protects aggregate, candidate and quarantine approval evidence. The old green exact-head executions are not accepted as RC7.4 release evidence because their retained artifact was semantically unsafe.

No RC7.4 `PASS` is claimed until fresh exact-head CI executes the dedicated gate, existing RC4/RC6/RC7 regressions complete successfully, and the retained artifact is independently verified to report aggregate, candidate and quarantine publication approval as false.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- publication requires explicit human approval by a principal different from the reviewer;
- service accounts and connectors may not review or approve sharing;
- connector success, isolation recovery, quarantine release, contract validation or normalization never implies publication approval;
- provenance and confidence may not be silently discarded;
- secret values may not be emitted into connector contract evidence;
- retained evidence must use literal, non-inverted publication-approval semantics;
- missing, queued, cancelled or unexecuted CI and connector evidence may not be reported as successful.

## Current run decision

`RUN-20260807-053` is `CI_VALIDATION_PENDING`. A higher-severity retained-evidence semantics defect was corrected before merge. Fresh exact-head workflow execution and retained artifact verification are required before RC7.4 acceptance. Phase 4 remains `IN PROGRESS`; external production connector and assurance gates remain tracked in issue #1.

## Exactly one next priority

Inspect the fresh exact-head RC7 Payload Provenance Gate and remediate only its earliest deterministic failure; if all required exact-head RC4/RC6/RC7 gates succeed and retained evidence records aggregate, candidate and quarantine publication approval as false, accept and merge RC7.4.