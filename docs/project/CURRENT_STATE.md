# DTMO Current Project State

Last reconciled: 2026-08-09 — RUN-20260809-132 (`CI_VALIDATION_PENDING` for this documentation head; supported object-storage target selected, migration not yet executed)

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

PR #88 exact head `e10eba331fca40b95bd3800fa1be93c9474ece2f` completed all 37 registered workflows successfully and was merged as `c11e37f5c166d698b0edf05ec1969dcfb3b0fe2d`.

## Supported object-storage decision

ADR-0001 selects **MinIO AIStor Enterprise Lite or AIStor Enterprise with an active paid support entitlement** as the supported successor to legacy `minio/minio`.

Production acceptance requires:

- vendor-supported production deployment topology;
- current supported AIStor release pinned by immutable release tag and image digest;
- no `latest` tag in accepted production manifests;
- active license supplied outside source control;
- separation of AIStor license/SUBNET, administrative/root and least-privilege application S3 credentials;
- TLS/network encryption and server-side encryption before production acceptance;
- retained security, recovery, storage-integrity and full-regression evidence.

AIStor Free is not accepted for DTMO production because first-party documentation states it has no SLA/SLO/service agreement and does not provide the required distributed/support profile. The archived legacy `minio/minio` runtime and unsupported source builds remain rejected.

This decision removes the target-selection ambiguity only. It does **not** claim that AIStor is deployed, licensed, hardened, recoverable or production accepted.

## Security and governance invariants

- RBAC remains enforced.
- Review and share approval remain separate human actions.
- Connectors and service accounts cannot approve publication.
- Storage or observability success never implies publication approval.
- Provenance, confidence and raw evidence controls remain unchanged.
- License, API keys, administrative credentials and application credentials must not enter source control or telemetry.
- Missing, queued, cancelled, failed or unexecuted CI is never `PASS`.

## External gates still open

Issue #1 remains authoritative for independently executed production gates, including penetration testing, representative load/stress, full backup/restoration, production OpenSearch hardening, secrets-manager acceptance, deployment acceptance and operational/stakeholder approvals. The AIStor commercial entitlement/support purchase is also an external prerequisite for production deployment and does not close any issue #1 gate by itself.

## Exactly one current priority

Implement the bounded migration from legacy `minio/minio` to the accepted AIStor target using an immutable supported release and external license/secret boundary, then execute relevant security, recovery, storage-integrity and full regression gates with retained exact-head evidence before resuming Phase 7 / RC10.5 API-error alerting.