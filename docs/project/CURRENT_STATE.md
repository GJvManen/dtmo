# DTMO Current Project State

Last reconciled: 2026-08-09 — RUN-20260809-133 (`CI_VALIDATION_PENDING`; supported object-storage migration implementation present, acceptance not yet claimed)

This document is the human-readable current-state view of DTMO. It complements the immutable run history in `docs/development/runs/`, the chronological `docs/development/RUN_LOG.md`, the production roadmap, QA gate records and GitHub issues #1–#3.

## Executive status

- Phase 1 — application CI/workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: `PASS` for internal roadmap gates.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates; representative production load/stress remains external in issue #1.
- Phase 6 — frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA behavior on supported real host/browser/screen-reader combinations.
- Phase 7 — observability and incident operations: `IN PROGRESS`; RC10.1–RC10.4 are accepted. RC10.5 is deferred until the higher-severity object-storage migration is accepted.
- Phase 8 — staging acceptance: `NOT STARTED`.
- Phase 9 — external assurance: `NOT COMPLETE`.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is **not production ready**. Issue #1 remains authoritative for external production-acceptance gates.

## Latest verified acceptance

PR #89 exact head `79c5684b7e65064efe480e6da7913fd437d52b6d` completed all 37 registered workflows successfully and merged as `83e880a289467151c6604e28cd4141118fb538a9`.

## Supported object-storage migration

ADR-0001 selects MinIO AIStor Enterprise Lite or AIStor Enterprise with active paid support as the supported successor to legacy `minio/minio`.

RUN-133 implements the repository migration contract:

- removes the legacy `minio/minio` image from `docker-compose.yml`;
- requires external `AISTOR_IMAGE` with a release-tag-plus-`@sha256` digest contract and no implicit runnable default;
- prohibits `latest` through regression testing;
- injects the AIStor license through a required external file and Compose secret;
- requires external administrative user/password inputs with no legacy default credentials;
- preserves the internal `minio` service name, `DTMO_MINIO_ENDPOINT=minio:9000`, `minio_data:/data` persistent volume and application S3 compatibility contract;
- preserves `DTMO_PUBLISH_REQUIRES_HUMAN_APPROVAL=true` and does not alter RBAC, provenance or publication authority;
- adds a dedicated `Supported Object Storage Migration Gate` with retained JUnit evidence.

The migration remains `CI_VALIDATION_PENDING`. No unexecuted workflow is treated as PASS.

## Security and governance invariants

- RBAC remains enforced.
- Review and share approval remain separate human actions.
- Connectors and service accounts cannot approve publication.
- Storage or observability success never implies publication approval.
- Provenance, confidence and raw evidence controls remain unchanged.
- License, API keys, administrative credentials and application credentials must not enter source control or telemetry.
- Missing, queued, cancelled, failed or unexecuted CI is never `PASS`.

## External gates still open

Issue #1 remains authoritative for independently executed production gates, including penetration testing, representative load/stress, full backup/restoration, production OpenSearch hardening, secrets-manager acceptance, deployment acceptance and operational/stakeholder approvals. AIStor commercial entitlement/support purchase, production topology, TLS/network encryption, server-side encryption and independent registry-digest attestation also remain outside this repository-only migration claim.

## Exactly one current priority

Verify the complete exact-head CI matrix and retained evidence for the RUN-133 migration PR; merge only after every registered workflow succeeds. After acceptance, perform one bounded post-migration security/recovery/storage-integrity reconciliation before resuming Phase 7 / RC10.5 API-error alerting.