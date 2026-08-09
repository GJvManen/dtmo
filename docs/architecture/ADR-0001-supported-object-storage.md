# ADR-0001 — Supported object storage for DTMO

- Status: `ACCEPTED_FOR_MIGRATION`
- Date: 2026-08-09
- Decision owner: DTMO production-readiness program
- Scope: object-storage runtime only; this ADR does not deploy, purchase, configure production credentials, or close external assurance gates.

## Context

DTMO currently uses the Python `minio>=7.2,<8` client and a legacy `minio/minio:RELEASE.2025-07-23T15-54-02Z` server in `docker-compose.yml`. Fresh threat-intelligence review placed that server release inside affected ranges for later advisories. RUN-20260809-131 further established that the former community server repository is archived/no longer maintained, so moving to another legacy image or an unsupported source build cannot satisfy the production lifecycle gate.

## Decision

DTMO selects **MinIO AIStor Enterprise Lite or AIStor Enterprise, with an active paid support entitlement, as the supported object-storage successor**.

The minimum production acceptance profile is:

1. AIStor Enterprise Lite subscription or higher.
2. Direct-to-engineer support purchased for Enterprise Lite, or the standard Enterprise support package.
3. Production deployment on a vendor-documented supported platform. Docker Compose may remain a development/test/staging convenience but is not accepted as a production distributed topology on a single host.
4. Container source `quay.io/minio/aistor/minio` (or an organization-controlled private mirror of that vendor image).
5. The migration implementation must resolve the then-current stable AIStor release from MinIO's official release feed, pin an immutable release tag and image digest, and must not use `latest` for an accepted production manifest.
6. An active AIStor license must be supplied through a secret/file boundary. No license key, API key, root credential or object identity may be committed to the repository.
7. Existing DTMO application credentials remain least-privilege S3 credentials and remain separate from AIStor licensing/SUBNET credentials and administrative root credentials.
8. TLS/network encryption and server-side encryption must be enabled before production acceptance; secrets-manager replacement remains coordinated with issue #1.

## Why this target

- MinIO documents AIStor Server as a drop-in replacement for the former community server and documents native S3 API support. This minimizes application-protocol change while removing dependence on the archived runtime.
- MinIO publishes maintained AIStor release artifacts and an upgrade path for pinned containers.
- AIStor Enterprise Lite provides the distributed feature set; paid support is available as an add-on. AIStor Enterprise includes 24x7 direct-to-engineer support. DTMO requires a paid support entitlement because the Free tier explicitly has no SLA/SLO/service agreement and lacks production HA features used by the production-readiness design.
- MinIO's container documentation states that single-host distributed Docker Compose is development/test/staging only; production must use a supported production topology across separate hosts or a supported Kubernetes/Linux deployment.

## Rejected alternatives for this migration

### Legacy `minio/minio` community image
Rejected because the upstream repository/runtime is archived and unmaintained. A patched community build would still fail the supported-lifecycle gate.

### AIStor Free
Rejected for DTMO production because MinIO documents no SLA/SLO/service agreement for the Free license and limits distributed/replication/support functionality.

### Immediate switch to a different S3 provider
Not selected in this bounded run. Amazon S3 and other maintained S3 services are viable strategic alternatives, but changing provider would introduce a larger operational, identity, networking and data-residency decision surface than necessary to remove the immediate unsupported-runtime blocker. This ADR can be superseded later if platform strategy requires it.

## Lifecycle and provenance sources

Primary vendor sources reviewed 2026-08-09:

- MinIO AIStor documentation: https://docs.min.io/aistor/
- AIStor Server reference/drop-in statement: https://docs.min.io/aistor/reference/aistor-server/
- AIStor container deployment guidance: https://docs.min.io/aistor/installation/container/
- Distributed Docker Compose production boundary: https://docs.min.io/aistor/installation/container/distributed/
- AIStor upgrade guidance/current pinned release mechanism: https://docs.min.io/aistor/upgrade-aistor-server/
- AIStor release artifacts/feed: https://docs.min.io/aistor/operations/release-artifacts/
- AIStor license capabilities: https://docs.min.io/aistor/operations/licenses/
- AIStor subscriptions/pricing: https://www.min.io/pricing
- AIStor support terms: https://www.min.io/legal/aistor-support-services

Confidence: **high** for vendor lifecycle/support/product statements because the decision is based on current first-party documentation and legal/support terms. Suitability is still conditional on migration/recovery/security regression evidence.

## Security and governance invariants

This decision does not change DTMO RBAC, review/share separation, human share approval, provenance/confidence retention, immutable evidence controls, audit logging, or service-account publication restrictions. AIStor license/SUBNET credentials are infrastructure credentials and must never grant application-level publication authority.

## Migration acceptance criteria

The subsequent migration run may be accepted only when it proves, on one exact head:

- legacy `minio/minio` is removed from the supported deployment path;
- a current supported AIStor release is immutably pinned;
- license and administrative credentials are injected outside source control;
- application storage operations and checksum verification remain correct;
- clean recovery/restore succeeds;
- storage-integrity alerting still raises and clears correctly;
- security/dependency/container checks pass;
- the full registered regression matrix completes successfully;
- no raw evidence, object key, digest, credential or license material leaks into telemetry/artifacts;
- issue #1 external gates remain independently open unless separately evidenced.

## Exactly one next priority

Implement the bounded migration from the legacy MinIO server runtime to the accepted AIStor target, using an immutable supported release and external license/secret boundary, then execute the relevant security, recovery, storage-integrity and full regression gates with retained exact-head evidence.