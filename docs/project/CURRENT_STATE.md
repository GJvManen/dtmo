# DTMO Current Project State

Last reconciled: 2026-08-10 — PR #111 / 16.0.0rc5 accepted; RUN-20260810-162 / 16.0.0rc6 professional UX overhaul is `CI_VALIDATION_PENDING`.

## Executive status

- Phase 1 — CI/workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: `PASS` for internal roadmap gates.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates.
- Phase 6 — frontend accessibility and operational UX: repository-controlled browser/accessibility gates are accepted historically; genuine VoiceOver/NVDA behavior remains `BLOCKED_EXTERNAL`.
- Phase 7 — observability and incident operations: `PASS`.
- Phase 8 — staging acceptance: `BLOCKED_EXTERNAL` for one approved real staging deployment and the ten deployment-parity evidence classes. Repository-controlled emulator configuration and bounded application-container runtime smoke are `PASS` only for their explicit scopes.
- Phase 9 — external assurance: `NOT COMPLETE`; the repository-controlled external-assurance intake/readiness contract is accepted on `main`.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is **not production ready**. Issue #1 remains authoritative for external production-acceptance gates.

## Accepted rc5 frontend baseline

PR #111 exact head `1e59cd6f02bd5b853d0e8bf66a09c90d46d89467` completed all 48 registered workflows successfully, including RC4, browser/accessibility gates and all Phase 8 repository gates, and merged as `05e72443b132e0e0c162d2a07b1578e84daaa25c`.

16.0.0rc5 therefore established a governed, discoverable web console and corrected the local OpenSearch bootstrap contract. This acceptance is bounded to repository-controlled evidence and does not close genuine VoiceOver/NVDA, real staging or external-assurance gates.

## 16.0.0rc6 professional frontend candidate

RUN-162 upgrades the operator experience without moving authorization into the browser. The primary Threat Operations Console is organized into five stable task areas: Overview, Intelligence, Governance, Audit and Security. The release adds persistent navigation, professional KPI/status presentation, structured analyst results, explicit two-step review/share decision presentation, read-only audit tables, isolated privileged security actions, responsive behavior and a per-tab test-identity dialog.

The specialized Analyst, Share Approval, Auditor and CISO workspaces now use the same visual/interaction language. `docs/ux/FRONTEND_UX.md` documents the UX architecture and `docs/qa/FRONTEND_UX_RELEASE_GATE.md` defines the rc6 acceptance contract.

The browser remains an experience layer only. Server-side RBAC is authoritative. Review and external share approval remain separate permissions/actions. Audit evidence remains read-only. Test identity data remains scoped to `sessionStorage`; production authentication remains the configured bearer-token/identity-provider path.

RUN-162 remains `CI_VALIDATION_PENDING` until every registered workflow succeeds on the final exact PR head.

## Phase 8 blocker

No approved real staging endpoint/environment identity and no complete ten-class deployment-parity package tied to one immutable staged release are available. Required classes remain: approved environment/owner; reachable endpoint; immutable deployed release/image identity; infrastructure/runtime/configuration parity; approved secrets-manager and least-privilege identities; TLS/network restrictions; staging data-class/sanitization and explicit no-production-credential confirmation; deployment/change record; rollback target/procedure; and deployment-time security/CVE/vendor-advisory review.

No staging acceptance result may be credited until those classes are complete against the same immutable identity.

## Phase 9 external assurance

The accepted Phase 9 intake contract requires independently observable evidence for independent penetration testing, representative load/stress testing, full backup/restoration, production platform hardening, secrets-management acceptance, operational/stakeholder acceptance and staging/production deployment acceptance. Evidence must be attributable, dated and tied to immutable target identities where applicable. Findings require explicit disposition.

## Security and governance invariants

RBAC, separation of duties, privacy, provenance, auditability and human share approval remain unchanged. Technical environment access cannot grant publication or share approval. Missing, stale, inaccessible, inferred, failed, cancelled, skipped or contradictory evidence is never PASS.

## Exactly one current priority

Complete exact-head CI and browser/accessibility validation for the 16.0.0rc6 professional frontend release candidate. Merge only if every registered workflow succeeds; otherwise remediate the first concrete failing gate.
