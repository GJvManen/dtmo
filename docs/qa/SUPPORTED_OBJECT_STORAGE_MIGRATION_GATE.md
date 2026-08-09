# Supported Object Storage Migration Gate

## Decision

`PASS`

## Accepted exact-head evidence

PR #90 exact head `0fe5c5f0003211fe9df8535954d9276a2090af35` completed **38/38 registered workflows successfully** and was squash-merged with expected-head protection as `383702bec6ba07cba065524efa451fd89cbd3b50`.

Dedicated workflow run `31326861369` (`Supported Object Storage Migration Gate`) succeeded. Retained artifact `9041774769`, digest `sha256:24e7241138dc0b293957f5e2cd06a4d3a6606b7ba68d688097795047f114ccf8`, is bound to the exact head. Independent inspection of `supported-object-storage-migration-junit.xml` recorded **4 tests, 0 failures, 0 errors and 0 skips**.

Evidence proves the bounded repository contract:

- archived legacy `minio/minio` is absent from the supported Compose path;
- `AISTOR_IMAGE` fails closed and requires a release-tag-plus-`@sha256` digest reference;
- `latest` is prohibited by regression protection;
- AIStor license is injected through an external file/Compose-secret boundary;
- administrative credentials have no runnable repository defaults;
- internal S3 endpoint `minio:9000`, `minio_data:/data` persistence and application S3 compatibility are preserved;
- human share approval remains required;
- recovery and storage-integrity workflows remained green on the same exact head.

## Fresh vulnerability boundary

Post-merge public CVE review on 2026-08-09 found relevant MinIO/AIStor fixes through `RELEASE.2026-04-14T21-32-45Z`. Therefore any production deployment must select a vendor-supported release **at or after that threshold** and repeat advisory/CVE review immediately before deployment. The repository intentionally does not fabricate or freeze a production digest.

## Claim boundary

This PASS does **not** claim a paid entitlement has been purchased, a production AIStor cluster is deployed, production TLS/SSE is complete, a secrets manager is accepted, the deployment-time registry digest is externally attested, staging is accepted, or issue #1 external gates are closed.

## Exactly one next priority

Complete RUN-134 post-migration security/recovery/storage-integrity reconciliation. If no new internal blocker is found and the reconciliation exact-head CI succeeds, resume Phase 7 with RC10.5 API-error alerting.
