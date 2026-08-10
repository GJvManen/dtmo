# DTMO Current Project State

Last reconciled: 2026-08-10 — 16.0.0rc8 / PR #114 is accepted and merged. The current bounded product priority is safe generic registered-source execution for governed `json-feed` source definitions.

## Executive status

- Phase 1 — CI/workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: `PASS` for the built-in CISA KEV path; the generic registered-source path is not yet executable and remains the current bounded product objective.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates.
- Phase 6 — frontend accessibility and operational UX: rc6 remains the accepted repository-controlled professional UX baseline; rc8 adds the accepted admin source-management workspace. Genuine VoiceOver/NVDA behavior remains `BLOCKED_EXTERNAL`.
- Phase 7 — observability and incident operations: `PASS`.
- Phase 8 — staging acceptance: `BLOCKED_EXTERNAL` for one approved real staging deployment and the ten deployment-parity evidence classes.
- Phase 9 — external assurance: `NOT COMPLETE`; repository-controlled intake/readiness contract accepted.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is **not production ready**. Issue #1 remains authoritative for external production-acceptance gates.

## Accepted 16.0.0rc8 Admin Configuration & Source Registry baseline

PR #114 final exact head `95fed1e663bdf256def58020f11529f383c8efe5` completed all 48 registered workflows successfully and merged to `main` as `7351ae2ab984b6848969bc634c32e819ec413031`.

Accepted rc8 capabilities include:

- persistent source definitions with Alembic revision `0007_source_registry`;
- `/api/v1/admin/sources` list/create/update/validate operations;
- professional `/ui/admin-sources` workspace;
- human-admin plus `manage:connectors` authorization for mutations;
- service-account exclusion from the human admin surface;
- supported source types and explicit reliability/schedule/enabled metadata;
- registration-time SSRF-safe URL shape validation;
- secret references instead of raw secret values;
- persistent audit-chain events for source create/update.

Generic `json-feed` entries remain **registry-only**. Registration is not execution approval and does not establish source trust. Safe execution requires a separate runtime trust boundary with DNS/rebinding protection, redirect policy, response/content limits, provenance normalization, connector health/failure isolation and replay/idempotency semantics.

## Deferred accepted-feedback backlog

The next bounded objective is the safe generic source execution adapter for enabled registered JSON feeds. Once that control/data plane is accepted, graphical dashboard integration and broader framework/navigation consolidation become the next UI objective so operational, connector and intelligence visualizations are first-class parts of the console rather than separate building blocks.

## Dependency/advisory observation

The recorded OpenSearch 2.19.1 patch-maintenance finding remains open: later 2.19 patch releases exist and require a separate compatibility/security maintenance run. This is not folded into the generic-source execution objective unless a higher-severity advisory makes it blocking.

## Phase 8 blocker

No approved real staging endpoint/environment identity and no complete ten-class deployment-parity package tied to one immutable staged release are available. Required classes remain: approved environment/owner; reachable endpoint; immutable deployed release/image identity; infrastructure/runtime/configuration parity; approved secrets-manager and least-privilege identities; TLS/network restrictions; staging data-class/sanitization and explicit no-production-credential confirmation; deployment/change record; rollback target/procedure; and deployment-time security/CVE/vendor-advisory review.

## Security and governance invariants

RBAC, separation of duties, privacy, provenance, auditability and human share approval remain mandatory. Missing, stale, inaccessible, inferred, failed, cancelled, skipped or contradictory evidence is never PASS. Connector execution is not publication approval. Registry membership is not source trust or execution approval.

## Exactly one current priority

Implement and independently test one safe generic registered-source execution adapter for enabled `json-feed` source definitions. Do not begin dashboard integration until this data-plane objective is accepted on complete exact-head CI.
