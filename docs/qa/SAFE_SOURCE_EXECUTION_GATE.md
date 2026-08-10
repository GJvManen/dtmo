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

## Fail-closed conditions

Any missing CI run, failing/cancelled/skipped required workflow, private/non-global DNS resolution, redirect, invalid TLS identity, unsupported content type, oversized response, malformed payload, disabled source or authorization failure blocks a PASS claim for the affected operation.

## External claim boundary

A green rc9 gate proves only the repository-controlled implementation and CI contracts above. It does not prove real staging network policy, enterprise egress controls, external service availability, VoiceOver/NVDA behavior, independent penetration-test results, vendor contractual permission to automate restricted feeds, or production go/no-go readiness.
