# DTMO Current Project State

Last reconciled: 2026-08-10 — PR #112 / 16.0.0rc6 remains the accepted repository-controlled frontend baseline. RUN-20260810-169 is a higher-severity functional remediation candidate for the search/live-intelligence pipeline after acceptance feedback exposed a user-visible OpenSearch error and a connector path that fetched but did not persist/index records.

## Executive status

- Phase 1 — CI/workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: previously accepted internal gate evidence remains historical; RUN-169 is correcting a newly observed end-to-end product integration defect before further staging acceptance.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates.
- Phase 6 — frontend accessibility and operational UX: rc6 is the accepted repository-controlled professional frontend baseline; genuine VoiceOver/NVDA behavior remains `BLOCKED_EXTERNAL`.
- Phase 7 — observability and incident operations: `PASS`.
- Phase 8 — staging acceptance: `BLOCKED_EXTERNAL` for one approved real staging deployment and the ten deployment-parity evidence classes; progression is additionally paused until RUN-169 completes exact-head CI.
- Phase 9 — external assurance: `NOT COMPLETE`; repository-controlled intake/readiness contract accepted.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is **not production ready**. Issue #1 remains authoritative for external production-acceptance gates.

## Accepted rc6 frontend baseline

PR #112 final exact head `e5e0d5e808d1f66c8f512fa35bd0ea3932fe8631` completed all 48 registered workflows successfully and merged as `5c2a9c9a5d0d936784597899c97bf5be253c2394`. That acceptance remains valid for its repository-controlled UX/accessibility scope.

## RUN-169 / 16.0.0rc7 functional remediation

Acceptance testing identified four product gaps: missing admin configuration/source management, insufficient framework/dashboard integration, no operational data path from previously identified live sources, and a search failure reporting `search backend unavailable: HTTPStatusError`.

RUN-169 deliberately addresses exactly one bounded objective: restore **search plus the existing CISA KEV live-source pipeline**. Repository inspection found:

- search queried an index without first ensuring it existed, turning the fresh/empty state into an OpenSearch HTTP error;
- the strict OpenSearch mapping declared `confidence`, while canonical ingestion wrote `confidence_score`, `confidence_level` and `confidence_rationale`, allowing strict mapping rejection;
- CISA KEV connector execution fetched and parsed records but never landed them in the raw lake, canonical database or search index;
- the manual connector-run endpoint was not permission-gated;
- replay only indexed newly inserted records, preventing repair of previously failed derived search documents.

16.0.0rc7 corrects these contracts and adds regression tests. Manual connector execution requires `manage:connectors`; connector/service ingestion remains candidate ingestion only and cannot review or approve external sharing. The final decision remains `CI_VALIDATION_PENDING` until every registered workflow succeeds on one exact PR head.

## Deferred accepted-feedback backlog

After RUN-169 passes, the next bounded product objective is a governed **Admin Configuration & Source Registry** workspace. It must provide admin-only connector/source lifecycle, scheduling and test execution, safe supported source types, explicit URL/network validation against SSRF, audit history, secrets references rather than secret values, and clear status/provenance. Arbitrary user-supplied URL execution must not be introduced.

Graphical dashboards and deeper framework/navigation integration are retained immediately behind that source-control plane so they can consume reliable operational data rather than decorative placeholder state.

## Dependency/advisory observation

The current deployment uses OpenSearch 2.19.1. OpenSearch official version history shows later 2.19 patch releases, including 2.19.6 dated 2026-07-02 with security updates. This is a high-confidence dependency-maintenance finding, not proof of a directly exploitable DTMO vulnerability. Upgrade/compatibility validation remains a separate bounded production-readiness item.

CISA KEV remains an authoritative high-confidence source for vulnerabilities known to be exploited in the wild, and the CISA-maintained `cisagov/kev-data` mirror documents that it follows the canonical CISA catalog.

## Phase 8 blocker

No approved real staging endpoint/environment identity and no complete ten-class deployment-parity package tied to one immutable staged release are available. Required classes remain: approved environment/owner; reachable endpoint; immutable deployed release/image identity; infrastructure/runtime/configuration parity; approved secrets-manager and least-privilege identities; TLS/network restrictions; staging data-class/sanitization and explicit no-production-credential confirmation; deployment/change record; rollback target/procedure; and deployment-time security/CVE/vendor-advisory review.

## Phase 9 external assurance

The accepted Phase 9 intake contract requires independently observable evidence for independent penetration testing, representative load/stress testing, full backup/restoration, production platform hardening, secrets-management acceptance, operational/stakeholder acceptance and staging/production deployment acceptance. RUN-169 advances none of those external claims.

## Security and governance invariants

RBAC, separation of duties, privacy, provenance, auditability and human share approval remain mandatory. Missing, stale, inaccessible, inferred, failed, cancelled, skipped or contradictory evidence is never PASS. Connector execution is not publication approval.

## Exactly one current priority

Complete exact-head CI validation for RUN-169 / 16.0.0rc7. If all registered workflows succeed, proceed to the governed Admin Configuration & Source Registry workspace; otherwise remediate only the first concrete CI failure.
