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
| Recovery | Clean targets restore or reconstruct successfully with integrity and timing evidence |
| Connector reliability | Live canary, provenance, licensing, timeout, rate limiting, bounded retries and quarantine are evidenced |
| Release | All release-critical jobs and retained evidence artifacts succeed |

## Completed exact-head gates

- RC5.1 #177 through RC5.12 #224: `PASS`
- RC6.1 #229: `PASS`
- RC6.2 #243: `PASS`
- RC6.3 OpenSearch Gate #5 and Quality Gate #253: `PASS`
- RC6.4 Multi-store Gate #4, Quality Gate #262 and OpenSearch Gate #14: `PASS`
- RC7.1 Canary Gate #3, Quality Gate #270, OpenSearch Gate #22 and Multi-store Gate #12: `PASS`

## Phase status

- Phase 2 — application security, identity and privacy: `PASS`.
- Phase 3 — data integrity, backup and recovery: `PASS`.
- Phase 4 — live connector reliability and provenance: `IN PROGRESS`.

## RC7.1 governed live connector canary — `PASS`

Exact head `c82e20c110354c1163b58ac8b9820756f829a4ae` passed all required gates. Evidenced controls include HTTPS-only CISA KEV ingestion, licence and terms metadata, timeout, maximum three attempts, bounded exponential backoff, minimum request interval, disabled redirects, provenance retention, deduplication, quarantine of malformed/duplicate/overflow records, bounded record volume and `publish_approved: false`.

Retained artifacts:

- `live-connector-canary-evidence` — `8973407243`, digest `sha256:437b09bf13746fecf4e929921e1a63ac74bdbba1f1ecb08e0d04b99f763a3f53`;
- `release-gate-evidence` — `8973424158`;
- `postgres-restore-evidence` — `8973421161`;
- `dependency-audit-evidence` — `8973411040`;
- `minio-restore-evidence` — `8973409186`;
- `workflow-contract-evidence` — `8973408182`.

PR #28 merged as `aeeb0709a26ecb1f20620d7ac21f823fec35e98f`.

One successful canary does not yet prove persistent run-state, long-term source health, failure isolation across runs or broader approved connector coverage.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- reviewed and share-approved states remain distinct;
- publication requires explicit human approval by a principal different from the reviewer;
- service accounts and connectors may not review or approve sharing;
- live connector success never implies publication approval;
- provenance and confidence may not be silently discarded;
- missing CI, recovery or connector evidence may not be reported as successful.

## Current run decision

`RUN-20260806-044` is `PASS`.

## Exactly one next priority

RC7.2 — persistent connector-run state, source-health history and failure isolation with quarantined recovery and no automatic publication.
