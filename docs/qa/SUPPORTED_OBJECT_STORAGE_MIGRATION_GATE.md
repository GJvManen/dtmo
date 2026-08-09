# Supported Object Storage Migration Gate

## Decision

`CI_VALIDATION_PENDING`

## Objective

Validate the bounded repository migration from archived legacy `minio/minio` to the supported AIStor target selected in ADR-0001 without weakening credential, auditability, provenance or human-approval controls.

## Required evidence

Acceptance requires all of the following on one exact PR head:

- legacy `minio/minio` absent from the supported Compose path;
- AIStor image input fail-closed and explicitly requiring an immutable `@sha256` digest-pinned vendor image reference;
- no use of `latest` in the migrated Compose contract;
- AIStor license supplied through an external file/secret boundary;
- administrative user/password supplied externally with no runnable repository defaults;
- existing DTMO S3 service name, `minio:9000` endpoint and persistent volume contract preserved;
- human share approval invariant preserved;
- dedicated `Supported Object Storage Migration Gate` succeeds and retains JUnit evidence;
- complete registered workflow matrix succeeds on the final exact head;
- relevant existing recovery and storage-integrity workflows remain green.

## Current implementation evidence

The migration branch removes `minio/minio:RELEASE.2025-07-23T15-54-02Z` and introduces required external `AISTOR_IMAGE`, `AISTOR_LICENSE_FILE`, `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` inputs. The Compose service retains the internal service name `minio`, `minio_data:/data` and the application endpoint contract `DTMO_MINIO_ENDPOINT=minio:9000`.

`backend/tests/test_supported_object_storage_migration.py` provides bounded regression checks for legacy-image removal, digest-pinned fail-closed image configuration, secret/license boundaries, credential-default removal and S3/persistence/human-approval continuity.

## Claim boundary

This gate does **not** claim:

- a paid AIStor entitlement has been purchased;
- a production AIStor cluster is deployed;
- the external registry digest has been independently attested for a selected production release;
- production TLS/network encryption or server-side encryption is complete;
- production topology, secrets manager or staging acceptance is complete;
- issue #1 external gates are closed;
- RC10.5 or Phase 7 is complete.

The production digest is deliberately not fabricated. The deployer must resolve a vendor-supported release and verify its registry digest, then provide the complete release-tag-plus-digest image reference through the external deployment boundary.

## Exactly one next priority

Accept this gate only after the migration PR's complete exact-head workflow matrix and retained dedicated evidence succeed; otherwise record the precise failing or missing gate. After acceptance, perform one bounded post-migration security/recovery/storage-integrity reconciliation before RC10.5.
