# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3. No phase is complete without objective evidence; missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks the corresponding claim.

## Current status — 2026-08-10

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — Application security and identity: `PASS` for internal gates.
- Phase 3 — Data integrity and recovery: `PASS` for internal gates.
- Phase 4 — Live connector reliability and provenance: `PASS` for internal gates.
- Phase 5 — Performance and scalability: `PASS` for internal gates.
- Phase 6 — Frontend accessibility and operational UX: rc5 is the accepted repository-controlled baseline; genuine VoiceOver/NVDA execution remains `BLOCKED_EXTERNAL`. rc6 PR #112 is under RUN-163 remediation after its first exact-head CI failed.
- Phase 7 — Observability and incident operations: `PASS`.
- Phase 8 — Staging acceptance: `BLOCKED_EXTERNAL` for real deployment-parity evidence.
- Phase 9 — External assurance: `NOT COMPLETE`; repository-controlled intake/readiness baseline accepted.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Phase 6 — Frontend accessibility and operational UX

Repository-controlled critical journeys, responsive layout, keyboard navigation, contrast, reflow, focus order, text spacing/resize and share-approval controls have historical accepted evidence. Genuine assistive-technology execution on supported VoiceOver/NVDA host/browser combinations remains externally required.

### RUN-161 — 16.0.0rc5 frontend productionization — `PASS`

PR #111 exact head `1e59cd6f02bd5b853d0e8bf66a09c90d46d89467` completed all 48 registered workflows successfully and merged as `05e72443b132e0e0c162d2a07b1578e84daaa25c`. rc5 remains the accepted frontend baseline.

### RUN-162 — 16.0.0rc6 professional frontend UX overhaul — `FAILED_CI`

rc6 introduced a coherent task-oriented Threat Operations Console and unified Analyst, Share Approval, Auditor and CISO workspaces. Server-side RBAC, separation of duties, privacy, auditability and human share approval remained unchanged.

The first exact head `0e6bc86b425b4e6511520bd6734f79baf7413d97` is not accepted. Eleven RC9 workflow-level gates failed, represented by 22 failing checks when their fail-closed aggregate jobs are counted.

### RUN-163 — RC6 RC9 acceptance-contract regression remediation — `CI_VALIDATION_PENDING`

Actual workflow logs identified a shared regression cluster: lost semantic `empty`/`forbidden` states, missing `aria-atomic=true` on critical principal live regions, missing `data-event-id` on rendered audit evidence, absent visible focus on the analyst search field, mobile/reflow horizontal overflow and decorative backgrounds that made contrast evidence fail closed.

RUN-163 restores these already accepted RC9 contracts without reverting the professional rc6 information architecture. A shared role-workspace compatibility layer provides explicit visible focus, minimum-width/reflow safeguards, mobile grid collapse and solid contrast-measurable surfaces. Role scripts restore semantic state identifiers and audit-event row identity. Repository regression tests lock the corrected contracts.

No prior failed-head result is reusable as PASS evidence. PR #112 requires a complete fresh workflow matrix on its final exact head.

## Phase 8 — Staging acceptance

Objectives remain a production-equivalent deployment, smoke/integration/migration/connector/recovery/performance/accessibility tests, secrets/TLS/network restrictions and retained deployment evidence. No approved real staging deployment and no complete ten-class deployment-parity package are yet evidenced against one immutable release identity.

Required classes remain: approved environment/owner; reachable endpoint; immutable deployed release/image identity; infrastructure/runtime/configuration parity; approved secrets-manager and least-privilege identities; TLS/network restrictions; staging data-class/sanitization and no-production-credential confirmation; deployment/change record; rollback target/procedure; and deployment-time security/CVE/vendor-advisory review.

## Phase 9 — External assurance

Phase 9 requires independently observable evidence for independent penetration testing, representative load/stress testing, full backup/restoration, production platform hardening, approved secrets management, operational/stakeholder acceptance and staging/production deployment acceptance. RUN-159's intake baseline is accepted only as a readiness contract.

## Phase 10 — Production go/no-go

Go requires every prior phase and external gate complete with retained evidence, green CI, release notes/SBOM/deployment manifest/rollback plan, proven recovery and required approvals. Any missing blocking evidence is `NO-GO`.

## PDCA execution order

1. CI and workflow integrity.
2. Application security and identity.
3. Data integrity and recovery.
4. Live connector reliability and provenance.
5. Performance and scalability.
6. Frontend accessibility and operational UX.
7. Observability and incident operations.
8. Staging acceptance.
9. External assurance coordination.
10. Production go/no-go.

Every run must document Plan, Do, Check and Act, update run/QA evidence, preserve claim boundaries, and leave exactly one next priority.

## Exactly one next priority

Verify every registered workflow on the final RUN-163 remediation head of PR #112. Merge only on complete exact-head success; otherwise remediate the first concrete remaining failure.
