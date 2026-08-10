# Safe Registered-Source Execution QA Gate

Release candidate: 16.0.0rc9

Status: `CI_VALIDATION_PENDING`

## Gate scope

This gate covers the registered `json-feed` execution trust boundary and curated source catalog. It does not convert external staging, assistive-technology testing, penetration testing or production acceptance into repository-controlled evidence.

## Required evidence

- human-admin + `manage:connectors` authorization remains required for manual source runs;
- disabled sources cannot execute;
- URL validation permits only direct HTTPS on the default port;
- DNS is freshly resolved immediately before outbound connection;
- execution fails closed if any resolved destination is non-global/private/local/reserved;
- the outbound TLS connection is pinned to a validated resolved IP while the configured hostname is retained for SNI/certificate verification;
- redirects are rejected rather than followed;
- environment proxy settings cannot redirect this execution path;
- only JSON responses are accepted and the response body is capped at 5 MiB;
- NVD and GitHub supported profiles normalize to `ConnectorRecord` with source provenance and reliability;
- uncatalogued JSON feeds require the DTMO JSON v1 `items[]` contract;
- normalized records pass through raw-object storage, canonical persistence, provenance and OpenSearch indexing;
- repeat execution remains idempotent and can repair a previously failed derived search index document;
- source execution feeds connector health/failure isolation and operational alerting;
- source execution never grants review or external share approval;
- curated catalog distinguishes `supported`, `planned-parser`, `research-reference` and built-in execution states;
- complete registered GitHub workflow matrix succeeds on one final exact PR head.

## Latest CI evidence

PR #115 exact head `d7b51cc9aace6f87cfe34b8aeb50be59e15b800a` completed 47 of 48 registered workflows successfully. The sole workflow failure was RC4 Quality Gate. Its lint and mypy steps succeeded; pytest stopped on one stale rc8 regression assertion that required the global application version to remain `16.0.0rc8`. The RC4 aggregate `release-gate` then failed as consequence of the red `test` job.

RUN-20260810-173 narrows that earlier feature test back to the admin wiring/accessibility contract it was intended to protect. Production code and security controls are unchanged. Because this change creates a new exact head, the previous 47/48 result is not reusable as final acceptance evidence. A fresh complete matrix is required.

## Fail-closed conditions

Any missing CI run, failing/cancelled/skipped required workflow, private/non-global DNS resolution, redirect, invalid TLS identity, unsupported content type, oversized response, malformed payload, disabled source or authorization failure blocks a PASS claim for the affected operation.

## External claim boundary

A green rc9 gate proves only the repository-controlled implementation and CI contracts above. It does not prove real staging network policy, enterprise egress controls, external service availability, VoiceOver/NVDA behavior, independent penetration-test results, vendor contractual permission to automate restricted feeds, or production go/no-go readiness.
