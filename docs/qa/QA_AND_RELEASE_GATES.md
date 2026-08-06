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
| Connector reliability | Live canary execution, provenance, licensing, timeout, rate limiting, bounded retries and quarantine are evidenced |
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

RC6.1 through RC6.4 are evidenced and merged. **Phase 3 completion: `PASS`.**

## Phase 4 — Live connector reliability and provenance

### RC7.1 governed live connector canary — `CI_VALIDATION_PENDING`

Committed controls:

- approved authoritative CISA KEV HTTPS source;
- explicit public-domain licence and terms URL;
- fixed timeout and maximum three attempts;
- bounded exponential retry/backoff and minimum request interval;
- no redirects and a dedicated user agent;
- source URL, timestamp, reliability, confidence and raw-evidence SHA-256 on accepted records;
- duplicate and malformed records are quarantined;
- maximum record count is bounded and overflow is quarantined;
- canary evidence is machine-readable and retained for 30 days;
- `publish_approved` is always false and prevents the canary from being treated as publication approval;
- a separate `always()` gate fails closed unless the live canary succeeds;
- positive and negative regression tests protect these controls.

No exact-head execution has completed successfully, so RC7.1 is not accepted as `PASS`.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- reviewed and share-approved states remain distinct;
- external publication requires explicit human approval by a principal different from the reviewer;
- service accounts and connectors may not review or approve sharing;
- live connector success never implies publication approval;
- source provenance and confidence may not be silently discarded;
- immutable source audit records may not be deleted by retention processing;
- missing CI, recovery or connector evidence may not be reported as successful.

## Current run decision

`RUN-20260806-044` is `CI_VALIDATION_PENDING` until the exact-head regular Quality Gate and RC7 Live Connector Canary Gate succeed and retain canary evidence.

## Exactly one next priority

Inspect the exact-head RC7 Live Connector Canary Gate and remediate only its earliest deterministic failure, or merge after all exact-head gates and retained evidence succeed.
