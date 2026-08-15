# Phase 8.2.5 — Object-storage read/write validation

**Status:** `IN PROGRESS / REPOSITORY_CONTRACT`

## Objective

Validate DTMO object-storage read/write behavior against the owner-approved post-E8 production-equivalent staging deployment and bind accepted evidence to the same immutable Phase 8.2 deployment identity.

## Required external validation

1. Confirm the application reaches object storage using the intended staging endpoint, bucket/container and service identity.
2. Confirm no production credentials or production bucket/container are used.
3. Write a uniquely named disposable test object through the same application/service path used by DTMO.
4. Read the object back and verify expected size/content or checksum integrity.
5. Delete the test object and confirm cleanup completed without unintended residue.
6. Confirm the staging identity cannot read/write outside the intended staging bucket/container/prefix boundary.
7. Observe storage-unavailable/degraded behavior and confirm the application fails safely and surfaces the condition operationally.

## Evidence requirements

Record the validation timestamp, accountable reviewer, restricted evidence reference and deployment fingerprint. Do not store raw credentials, secrets or sensitive payloads in the repository.

Use the Phase 8.2 step-scoped validator after populating the restricted evidence manifest:

```bash
python3 tools/phase8_platform_validation.py <manifest.json> --check object_storage_read_write
```

The step result may be accepted only when `checks.object_storage_read_write.result` is `PASS`, the evidence reference is present, immutable identity fields are complete and the fingerprint matches the approved staging deployment.

## Evidence boundary

Repository CI, local MinIO/object-store tests and migration gates are supporting evidence only. They do not substitute for observation on the owner-approved staging deployment.

## Acceptance

`PASS` only when write, read-back integrity, cleanup, least-privilege scope and safe degradation are evidenced against the same immutable staging deployment identity used by the other Phase 8.2 checks.

Related: #219, #217, #214, #211, #210, #158.
