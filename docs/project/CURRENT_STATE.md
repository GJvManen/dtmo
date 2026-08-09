# DTMO Current Project State

Last reconciled: 2026-08-09 — RUN-20260809-131 (`BLOCKED_EXTERNAL` for the supported object-storage remediation objective; documentation PR remains CI-gated)

This document is the human-readable current-state view of DTMO. It complements the immutable run history in `docs/development/runs/`, the chronological `docs/development/RUN_LOG.md`, the production roadmap, QA gate records and GitHub issues #1–#3.

## Executive status

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: `PASS` for internal roadmap gates.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates. External representative production load/stress remains separate in issue #1.
- Phase 6 — frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA behavior on supported real host/browser/screen-reader combinations. Browser/DOM automation is not accepted as a substitute.
- Phase 7 — observability and incident operations: `IN PROGRESS`.
  - RC10.1 request observability: `PASS`.
  - RC10.2 controlled connector-failure alerting: `PASS`.
  - RC10.3 bounded queue-backlog alerting: `PASS`.
  - RC10.4 bounded storage-integrity alerting: `PASS`.
  - normal next item RC10.5 API-error alerting is deferred behind the higher-severity supported object-storage remediation blocker.
- Phase 8 — staging acceptance: `NOT STARTED`.
- Phase 9 — external assurance: `NOT COMPLETE`.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is therefore **not production ready**. Issue #1 remains the source of truth for external production-acceptance gates.

## Latest accepted evidence

PR #87 reconciliation exact head `036e3a6035794bb115d578919327f0d87fa1c596` completed all 37 registered workflows successfully and was squash-merged with expected-head protection as `4af2f1ceb24ead103690584473118db738f169d3`.

RC10.4 remains accepted from PR #86 exact head `8aa56dacd64583de5e96c0fda188ba954437ffda`, 37/37 workflows, retained artifact `9041327884`, digest `sha256:456b09902727552d62fa7e1c96f119c6050a692d2519e0f8cecdd160e8b1dab3`, JUnit 5/5, merge `4d7494e8b8fcdcddb73349bf87157d8c16763c33`.

## Higher-severity security/lifecycle blocker

The repository still pins `minio/minio:RELEASE.2025-07-23T15-54-02Z`. Fresh public advisory review places that version within affected ranges for later MinIO vulnerabilities. RUN-20260809-131 additionally verified that upstream `minio/minio` is archived and explicitly no longer maintained and that legacy binary/container releases are unmaintained.

The remediation objective is therefore `BLOCKED_EXTERNAL`: a newer legacy image or patched-but-unsupported community source build is not sufficient production lifecycle evidence. Upstream points to successor offerings, but DTMO currently has no repository-evidenced supported target, deployment contract, entitlement boundary or support lifecycle source accepted for migration.

Affected-version and upstream-maintenance-status confidence are high. Configuration-specific exploitability of individual advisories and successor suitability are not overstated or claimed without evidence.

## Phase 6 external accessibility boundary

RC9.1–RC9.15 contain accepted bounded browser/accessibility evidence. RC9.16 defines the remaining real-assistive-technology evidence contract. Phase 6 remains `BLOCKED_EXTERNAL` until genuine VoiceOver and NVDA execution is retained from supported real host/browser/screen-reader combinations.

## External gates still open

Issue #1 remains authoritative for externally executed production gates, including independent penetration testing, representative load/stress, full backup/restoration exercise, production OpenSearch hardening, secrets-manager replacement where required, staging/production deployment acceptance and operational/stakeholder approval.

## Security and governance invariants

- RBAC remains enforced.
- Review and share approval remain separate human actions.
- Connectors and service accounts cannot approve publication.
- Ingestion, connector, queue, storage, replay, retry, recovery, timeout, performance or observability success never implies publication approval.
- Provenance, confidence and raw evidence remain retained according to their controls.
- Missing, queued, cancelled, failed or unexecuted CI is never `PASS`.

## Exactly one current priority

Obtain and record an explicit supported object-storage target for DTMO, including supported product/image or deployment method, lifecycle/support source, and required entitlement/credential boundary. Once that evidence exists, perform one bounded migration implementation and rerun security, recovery, storage-integrity and full regression gates before resuming Phase 7 / RC10.5 API-error alerting.
