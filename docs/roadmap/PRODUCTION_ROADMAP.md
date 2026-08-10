# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3. No phase is complete without objective evidence; missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks the corresponding claim.

## Current status — 2026-08-10

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — Application security and identity: `PASS` for internal gates.
- Phase 3 — Data integrity and recovery: `PASS` for internal gates.
- Phase 4 — Live connector reliability and provenance: `PASS` for internal gates.
- Phase 5 — Performance and scalability: `PASS` for internal gates.
- Phase 6 — Frontend accessibility and operational UX: repository-controlled browser/accessibility evidence is historically accepted; genuine VoiceOver/NVDA execution remains `BLOCKED_EXTERNAL`. PR #111 / rc5 is accepted; RUN-162 / rc6 professional UX is `CI_VALIDATION_PENDING`.
- Phase 7 — Observability and incident operations: `PASS`.
- Phase 8 — Staging acceptance: `BLOCKED_EXTERNAL` for real deployment-parity evidence. Repository-controlled emulator configuration and bounded application-container runtime smoke are `PASS` only for their explicit scopes.
- Phase 9 — External assurance: `NOT COMPLETE`; the repository-controlled intake/readiness baseline is accepted from PR #110 exact-head evidence.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Phase 6 — Frontend accessibility and operational UX

Repository-controlled critical journeys, responsive layout, keyboard navigation, contrast, reflow, focus order, text spacing/resize and share-approval controls have historical accepted evidence. Genuine assistive-technology execution on supported VoiceOver/NVDA host/browser combinations remains externally required.

### RUN-161 — 16.0.0rc5 frontend productionization — `PASS`

PR #111 exact head `1e59cd6f02bd5b853d0e8bf66a09c90d46d89467` completed all 48 registered workflows successfully and merged as `05e72443b132e0e0c162d2a07b1578e84daaa25c`. rc5 established the discoverable root console and repaired the OpenSearch local bootstrap contract.

### RUN-162 — 16.0.0rc6 professional frontend UX overhaul — `CI_VALIDATION_PENDING`

rc6 keeps the rc5 governance boundary but upgrades the operator experience into one coherent task-oriented system. The primary console uses five work areas: Overview, Intelligence, Governance, Audit and Security. Specialized Analyst, Share Approval, Auditor and CISO views are retained and use the same visual/interaction language.

The release adds persistent navigation, KPI/status presentation, professional search/results, explicit review/share workflow, read-only audit tables, isolated privileged security actions, responsive behavior and a per-tab test-identity dialog. `docs/ux/FRONTEND_UX.md` documents the architecture and `docs/qa/FRONTEND_UX_RELEASE_GATE.md` defines the acceptance contract.

Server-side RBAC remains authoritative. Browser permission visibility is convenience only. Review and share approval remain separate. Audit evidence remains read-only. Local/dev/staging identity values remain limited to browser-tab `sessionStorage`. No external accessibility, staging, penetration-test or production claim is created by this release.

## Phase 8 — Staging acceptance

Objectives: production-equivalent deployment, smoke/integration/migration/connector/recovery/performance/accessibility tests, secrets/TLS/network restrictions and retained deployment evidence.

Blocking gates:
- reproducible production-equivalent staging deployment;
- immutable application/container/dependency identity and configuration-parity evidence;
- approved secret-management path, least privilege and no production credentials in staging;
- TLS and network restrictions validated with no unintended public exposure;
- smoke/integration, migration, connector, recovery, performance, accessibility and observability tests executed against the deployed staging environment;
- rollback/recovery proven and evidence retained;
- no unresolved blocker interpreted as PASS.

Accepted repository-controlled evidence includes RUN-147 readiness, RUN-151/152 emulator configuration, RUN-153/154 lifecycle reconciliation, RUN-155 bounded application-container runtime smoke and RUN-157 lifecycle remediation. RUN-148, RUN-150, RUN-156 and RUN-158 found no approved real staging environment/deployment identity and no complete ten-class deployment-parity package.

Required classes remain: approved environment/owner; reachable endpoint; immutable deployed release/image identity; infrastructure/runtime/configuration parity; approved secrets-manager and least-privilege identities; TLS/network restrictions; staging data-class/sanitization and no-production-credential confirmation; deployment/change record; rollback target/procedure; and deployment-time security/CVE/vendor-advisory review.

No staging acceptance result is credited until all ten classes are complete against the same deployment identity.

## Phase 9 — External assurance

Phase 9 requires independently observable evidence for independent penetration testing, representative load/stress testing, full backup/restoration, production platform hardening, approved secrets management, operational/stakeholder acceptance and staging/production deployment acceptance.

RUN-159's external-assurance intake baseline is `PASS` only for the readiness contract. No external assurance execution is implied.

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

Verify every registered workflow on the final 16.0.0rc6 frontend PR head and merge only on complete success. After acceptance, use rc6 as the external UX/accessibility/staging test baseline.
