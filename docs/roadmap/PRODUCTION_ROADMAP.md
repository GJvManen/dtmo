# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3. No phase is complete without objective evidence; missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks the corresponding claim.

## Current status — 2026-08-10

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — Application security and identity: `PASS` for internal gates.
- Phase 3 — Data integrity and recovery: `PASS` for internal gates.
- Phase 4 — Live connector reliability and provenance: `PASS` for the accepted built-in and governed registered-source execution baseline through rc9.
- Phase 5 — Performance and scalability: `PASS` for internal gates.
- Phase 6 — Frontend accessibility and operational UX: rc6 role-workspace, rc8 source-admin and RC10.1 unified Operations Workspace shell baselines are accepted. Genuine VoiceOver/NVDA remains `BLOCKED_EXTERNAL`.
- Phase 7 — Observability and incident operations: `PASS` for internal gates; RC10.2 will surface accepted operational building blocks as real-data dashboard widgets without changing evidence boundaries.
- Phase 8 — Staging acceptance: `BLOCKED_EXTERNAL` for real deployment-parity evidence.
- Phase 9 — External assurance: `NOT COMPLETE`.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Accepted recent release baselines

### RUN-168 — 16.0.0rc6 professional frontend baseline — `PASS`
PR #112 final exact head `e5e0d5e808d1f66c8f512fa35bd0ea3932fe8631` completed 48/48 registered workflows and merged as `5c2a9c9a5d0d936784597899c97bf5be253c2394`.

### RUN-169 — 16.0.0rc7 search and live-intelligence remediation — `PASS`
PR #113 final exact head `c2b7216d4777488768796a69b3e928571a824e33` completed 48/48 registered workflows and merged as `892d7e48e19109b45062acd272f84a31f6f33802`.

### RUN-170 / RUN-171 — 16.0.0rc8 governed Admin Configuration & Source Registry — `PASS`
PR #114 exact head `95fed1e663bdf256def58020f11529f383c8efe5` completed all 48 registered workflows and merged as `7351ae2ab984b6848969bc634c32e819ec413031`.

### RUN-172 / RUN-173 — 16.0.0rc9 safe registered-source execution — `PASS`
PR #115 final exact head `c01611a48648ec73e14975337dd549bef86abe88` completed the complete registered workflow matrix and merged as `66f5faecb95b80add4ed4d28a6769592b1a18ddb`.

### RUN-174 / RUN-175 — 16.0.0rc10 RC10.1 Unified Operations Workspace shell — `PASS`
PR #116 exact head `d41d9e60a4a67ddb30345eecee4042d1c19a6cf5` completed every registered workflow successfully and merged as `b000ef2275d52ff098d2d2bd8df76136cea3b051`. `/ui/operations` is now the accepted unified shell. It reads existing operational endpoints and introduces no privileged write path.

## RC10 staged workspace programme

RC10 is intentionally decomposed into reviewable objectives rather than delivered as one unbounded frontend rewrite:

1. **RC10.1 Operations Workspace shell** — `PASS` via RUN-175.
2. **RC10.2 Unified graphical dashboards** — current next priority: bind existing operational metrics/building blocks to accessible real-data widgets.
3. **RC10.3 Threat Intelligence Workspace** — search/investigation flow with related CVE, KEV, vendor and provenance context.
4. **RC10.4 Source Center refinement** — integrate source catalog, execution health, scheduling and provenance into the unified shell.
5. **RC10.5 Administration consolidation** — bring governed configuration surfaces into one admin center without weakening RBAC/separation of duties.
6. **RC10.6 UX polish** — saved views, keyboard workflows, theme and density controls where evidence supports them.

Each step must independently pass the full registered workflow matrix before the next begins.

## Phase 8 — Staging acceptance

Objectives remain a production-equivalent deployment, smoke/integration/migration/connector/recovery/performance/accessibility tests, secrets/TLS/network restrictions and retained deployment evidence. No approved real staging deployment and no complete ten-class deployment-parity package are yet evidenced against one immutable release identity.

Required classes remain: approved environment/owner; reachable endpoint; immutable deployed release/image identity; infrastructure/runtime/configuration parity; approved secrets-manager and least-privilege identities; TLS/network restrictions; staging data-class/sanitization and no-production-credential confirmation; deployment/change record; rollback target/procedure; and deployment-time security/CVE/vendor-advisory review.

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

RC10.2 — bind accepted operational metrics/building blocks to accessible real-data dashboard widgets inside `/ui/operations`; require complete exact-head CI before acceptance.
