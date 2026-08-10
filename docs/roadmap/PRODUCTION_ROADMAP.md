# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3. No phase is complete without objective evidence; missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks the corresponding claim.

## Current status — 2026-08-10

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — Application security and identity: `PASS` for internal gates.
- Phase 3 — Data integrity and recovery: `PASS` for internal gates.
- Phase 4 — Live connector reliability and provenance: `PASS` for the accepted built-in and governed registered-source execution baseline through rc9.
- Phase 5 — Performance and scalability: `PASS` for internal gates.
- Phase 6 — Frontend accessibility and operational UX: rc6 role-workspace, rc8 source-admin, RC10.1 unified Operations Workspace and RC10.2 live operational dashboards are accepted. RUN-178 / RC10.3 is `CI_VALIDATION_PENDING`. Genuine VoiceOver/NVDA remains `BLOCKED_EXTERNAL`.
- Phase 7 — Observability and incident operations: `PASS` for internal gates.
- Phase 8 — Staging acceptance: `BLOCKED_EXTERNAL` for real deployment-parity evidence.
- Phase 9 — External assurance: `NOT COMPLETE`.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Accepted recent release baselines

- RC6 / PR #112 — professional role workspaces: `PASS`.
- RC7 / PR #113 — search and live-intelligence remediation: `PASS`.
- RC8 / PR #114 — governed Admin Configuration & Source Registry: `PASS`.
- RC9 / PR #115 — safe registered-source execution and curated catalog: `PASS`.
- RC10.1 / PR #116 — unified Operations Workspace shell: `PASS`.
- RC10.2 / PR #117 — live unified operational dashboards: `PASS`; exact head `d4e35a5fa0c463438299d6cdd3638de162a69026`, merge `db9e72d871fb1c4d536912419ffbb4d68ad680c2`.

## RC10 staged workspace programme

1. **RC10.1 Operations Workspace shell** — `PASS`.
2. **RC10.2 Unified graphical dashboards** — `PASS`.
3. **RC10.3 Threat Intelligence Workspace** — current RUN-178, `CI_VALIDATION_PENDING`: governed search plus canonical investigation detail, confidence, CVE/KEV/vendor context where stored, and provenance.
4. **RC10.4 Source Center refinement** — integrate source catalog, execution health, scheduling and provenance into the unified shell.
5. **RC10.5 Administration consolidation** — bring governed configuration surfaces into one admin center without weakening RBAC/separation of duties.
6. **RC10.6 UX polish** — saved views, keyboard workflows, theme and density controls where evidence supports them.

Each step must independently pass the full registered workflow matrix before the next begins.

## RC10.3 claim boundary

The workspace may derive explicit CVE identifiers from stored canonical text/tags and identify CISA KEV records by stored source identity. Vendor/product context is displayed only when explicitly stored. The presentation layer must not fabricate absent enrichment, bypass `READ_INTELLIGENCE`, expose raw sensitive metadata, or perform review/share/admin/security mutations.

## Phase 8 — Staging acceptance

No approved real staging deployment and no complete ten-class deployment-parity package are yet evidenced against one immutable release identity. Required classes remain: approved environment/owner; reachable endpoint; immutable release/image identity; infrastructure/runtime/configuration parity; approved secrets-manager and least-privilege identities; TLS/network restrictions; staging data/no-production-credential confirmation; deployment/change record; rollback target/procedure; and deployment-time security/CVE/vendor-advisory review.

## Phase 9 — External assurance

Phase 9 requires independently observable evidence for independent penetration testing, representative load/stress testing, full backup/restoration, production platform hardening, approved secrets management, operational/stakeholder acceptance and staging/production deployment acceptance. Repository-controlled readiness evidence does not substitute for those external gates.

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

Complete exact-head CI validation for RUN-178 / RC10.3. Merge only on complete success. If any workflow fails, remediate only the first concrete root cause before re-running the full exact-head matrix.
