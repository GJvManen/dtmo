# DTMO Current Project State

Last reconciled: 2026-08-10 — PR #111 / 16.0.0rc5 accepted; PR #112 / 16.0.0rc6 is under RUN-20260810-163 remediation after failed first exact-head CI.

## Executive status

- Phase 1 — CI/workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: `PASS` for internal roadmap gates.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates.
- Phase 6 — frontend accessibility and operational UX: rc5 remains the last accepted repository-controlled frontend baseline; genuine VoiceOver/NVDA behavior remains `BLOCKED_EXTERNAL`. rc6 is not accepted while RUN-163 exact-head validation is pending.
- Phase 7 — observability and incident operations: `PASS`.
- Phase 8 — staging acceptance: `BLOCKED_EXTERNAL` for one approved real staging deployment and the ten deployment-parity evidence classes.
- Phase 9 — external assurance: `NOT COMPLETE`; repository-controlled intake/readiness contract accepted.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is **not production ready**. Issue #1 remains authoritative for external production-acceptance gates.

## Accepted rc5 frontend baseline

PR #111 exact head `1e59cd6f02bd5b853d0e8bf66a09c90d46d89467` completed all 48 registered workflows successfully and merged as `05e72443b132e0e0c162d2a07b1578e84daaa25c`. rc5 therefore remains the current accepted repository-controlled UI baseline.

## 16.0.0rc6 professional frontend candidate

RUN-162 introduced the professional Threat Operations Console and unified Analyst, Share Approval, Auditor and CISO workspaces, but its first exact head `0e6bc86b425b4e6511520bd6734f79baf7413d97` is **not accepted**. Eleven RC9 workflows failed (22 checks including fail-closed aggregate jobs).

RUN-163 inspected actual job logs and grouped the failures into shared regressions rather than treating them as unrelated defects. Observed failures included lost semantic `empty`/`forbidden` states, missing `aria-atomic=true`, missing audit-row `data-event-id`, absent visible focus, 360 px horizontal overflow and decorative backgrounds that made contrast measurement fail closed.

The remediation restores those accepted RC9 contracts while retaining the rc6 professional information architecture. A compatibility stylesheet provides explicit focus, reflow/mobile and contrast-measurability safeguards; role scripts restore semantic states and evidence identifiers. Server-side RBAC, separation of duties, privacy, append-only auditability and human share approval are unchanged.

PR #112 remains `CI_VALIDATION_PENDING` until every registered workflow succeeds on the final remediation head.

## Phase 8 blocker

No approved real staging endpoint/environment identity and no complete ten-class deployment-parity package tied to one immutable staged release are available. Required classes remain: approved environment/owner; reachable endpoint; immutable deployed release/image identity; infrastructure/runtime/configuration parity; approved secrets-manager and least-privilege identities; TLS/network restrictions; staging data-class/sanitization and explicit no-production-credential confirmation; deployment/change record; rollback target/procedure; and deployment-time security/CVE/vendor-advisory review.

## Phase 9 external assurance

The accepted Phase 9 intake contract requires independently observable evidence for independent penetration testing, representative load/stress testing, full backup/restoration, production platform hardening, secrets-management acceptance, operational/stakeholder acceptance and staging/production deployment acceptance. No such external activity is advanced by RUN-163.

## Security and governance invariants

RBAC, separation of duties, privacy, provenance, auditability and human share approval remain unchanged. Missing, stale, inaccessible, inferred, failed, cancelled, skipped or contradictory evidence is never PASS.

## Exactly one current priority

Verify the complete registered workflow matrix on the final RUN-163 remediation head of PR #112. Merge only on complete exact-head success; otherwise remediate the first concrete remaining failure.
