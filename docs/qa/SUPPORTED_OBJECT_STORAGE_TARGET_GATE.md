# Supported Object Storage Target Gate

## Decision

`TARGET_ACCEPTED; MIGRATION_NOT_YET_ACCEPTED`

## Scope

This gate evaluates only whether DTMO has an explicit, supportable object-storage target with a documented lifecycle, deployment model and entitlement boundary. It does not accept the runtime migration itself.

## Accepted target

MinIO AIStor Enterprise Lite or AIStor Enterprise, with an active paid support entitlement. For Enterprise Lite, DTMO requires the separately purchased direct-to-engineer support option for production acceptance.

Production deployments must use a vendor-supported production topology. Single-host distributed Docker Compose is retained only for development/test/staging where appropriate and is not production evidence.

The migration implementation must pin the then-current stable `quay.io/minio/aistor/minio` release by immutable release tag and digest. `latest` is prohibited in the accepted production manifest.

## Evidence

First-party evidence reviewed 2026-08-09:

- MinIO AIStor documentation and server reference: maintained AIStor Server; native S3 API; server documented as a drop-in successor.
- MinIO container/distributed guidance: Docker Compose single-host distributed topology is not suitable for production; supported production deployment requires an appropriate production topology.
- MinIO release artifact and upgrade documentation: maintained release feed and pinned-container upgrade guidance.
- MinIO licensing documentation: AIStor Free has no SLA/SLO/service agreement and lacks distributed/replication/support capabilities required by this production-readiness design.
- MinIO subscription and support terms: Enterprise Lite/Enterprise are paid production tiers; Enterprise Lite engineer support is a separately purchased support service; Enterprise includes the stronger support profile.
- Repository `pyproject.toml`: current application dependency is `minio>=7.2,<8`, which reduces protocol-change risk but does not substitute for migration testing.

## Security and entitlement boundary

- AIStor license/SUBNET material is infrastructure entitlement data and must not be stored in Git.
- Administrative/root credentials must remain separate from application S3 credentials.
- Application S3 credentials must be least privilege and must not grant publication/share approval.
- TLS/network encryption and server-side encryption remain production acceptance requirements.
- Issue #1's secrets-manager, deployment acceptance and other external gates remain open.
- No raw evidence, object key, digest, license token, API key or credential may enter observability artifacts.

## Rejected production targets

- Legacy `minio/minio`: archived/unmaintained runtime.
- Patched community/source build without maintained vendor lifecycle: unsupported.
- AIStor Free: no SLA/SLO/service agreement and insufficient HA/support profile for DTMO production acceptance.

## Claim boundary

This QA gate does not claim that AIStor is deployed, licensed, configured, hardened, recoverable, performant or production accepted. Those claims require the bounded migration run, exact-head security/recovery/storage-integrity/full-regression evidence and remaining external gates.

## Exactly one next priority

Implement the bounded migration to the accepted AIStor target using an immutable supported release plus external license/secret injection, then rerun the required security, recovery, storage-integrity and full regression gates with retained exact-head evidence.