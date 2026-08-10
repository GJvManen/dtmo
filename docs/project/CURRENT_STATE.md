# DTMO Current Project State

Last reconciled: 2026-08-10 — 16.0.0rc7 / PR #113 is accepted and merged. RUN-20260810-170 introduces the next bounded product objective: a governed Admin Configuration & Source Registry baseline in 16.0.0rc8.

## Executive status

- Phase 1 — CI/workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: `PASS` for the built-in CISA KEV pipeline after rc7 restored raw/canonical/provenance/search persistence and replay repair.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates.
- Phase 6 — frontend accessibility and operational UX: rc6 remains the accepted repository-controlled UX baseline; genuine VoiceOver/NVDA behavior remains `BLOCKED_EXTERNAL`. rc8 adds an admin workspace but does not supersede external AT evidence.
- Phase 7 — observability and incident operations: `PASS`.
- Phase 8 — staging acceptance: `BLOCKED_EXTERNAL` for one approved real staging deployment and the ten deployment-parity evidence classes.
- Phase 9 — external assurance: `NOT COMPLETE`; repository-controlled intake/readiness contract accepted.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is **not production ready**. Issue #1 remains authoritative for external production-acceptance gates.

## Accepted 16.0.0rc7 intelligence baseline

PR #113 final exact head `c2b7216d4777488768796a69b3e928571a824e33` completed all 48 registered workflows successfully and merged to `main` as `892d7e48e19109b45062acd272f84a31f6f33802`. Search now safely initializes its index, the strict mapping matches canonical confidence fields, CISA KEV records traverse the raw lake/canonical database/provenance/OpenSearch path, replay can repair derived search state and manual connector execution is permission-gated.

## RUN-170 / 16.0.0rc8 Admin Configuration & Source Registry

The next accepted-feedback gap is admin source lifecycle control. rc8 adds:

- persistent source definitions with Alembic revision `0007_source_registry`;
- `/api/v1/admin/sources` list/create/update/validate operations;
- a professional `/ui/admin-sources` workspace;
- human-admin plus `manage:connectors` authorization for mutations;
- service-account exclusion from the human admin surface;
- supported source types and explicit reliability/schedule/enabled metadata;
- first-line SSRF-safe URL shape validation;
- secret references instead of raw secret values;
- persistent audit-chain events for source create/update.

Generic `json-feed` entries are intentionally **registry-only** in this run. They are not fetched yet. Safe generic execution is a separate trust boundary requiring DNS/rebinding-safe destination validation, redirect policy, response bounds, content validation, provenance normalization, connector health/failure isolation and replay semantics.

RUN-170 remains `CI_VALIDATION_PENDING` until every registered workflow succeeds on one exact PR head.

## Deferred accepted-feedback backlog

After rc8 acceptance, the next bounded objective is the safe generic source execution adapter for enabled registered JSON feeds. Once the control/data plane is reliable, the next UI objective is graphical dashboard integration and broader framework/navigation consolidation so operational, connector and intelligence visualizations are first-class parts of the console rather than separate building blocks.

## Dependency/advisory observation

The recorded OpenSearch 2.19.1 patch-maintenance finding remains open: later 2.19 patch releases exist and require a separate compatibility/security maintenance run. This is not folded into rc8 because the current objective is source-registry governance.

## Phase 8 blocker

No approved real staging endpoint/environment identity and no complete ten-class deployment-parity package tied to one immutable staged release are available. Required classes remain: approved environment/owner; reachable endpoint; immutable deployed release/image identity; infrastructure/runtime/configuration parity; approved secrets-manager and least-privilege identities; TLS/network restrictions; staging data-class/sanitization and explicit no-production-credential confirmation; deployment/change record; rollback target/procedure; and deployment-time security/CVE/vendor-advisory review.

## Security and governance invariants

RBAC, separation of duties, privacy, provenance, auditability and human share approval remain mandatory. Missing, stale, inaccessible, inferred, failed, cancelled, skipped or contradictory evidence is never PASS. Connector execution is not publication approval. Registry membership is not source trust or execution approval.

## Exactly one current priority

Complete exact-head CI validation for RUN-170 / 16.0.0rc8. Merge only if every registered workflow succeeds; otherwise remediate the first concrete failure.
