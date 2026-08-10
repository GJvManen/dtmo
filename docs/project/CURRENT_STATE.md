# DTMO Current Project State

Last reconciled: 2026-08-10 — 16.0.0rc9 / PR #115 is accepted and merged. RUN-20260810-174 / 16.0.0rc10 starts the next bounded frontend objective: a unified professional Operations Workspace shell.

## Executive status

- Phase 1 — CI/workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: `PASS` for the accepted CISA KEV plus governed registered-source execution baseline from rc9.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates.
- Phase 6 — frontend accessibility and operational UX: rc6 is the accepted role-workspace baseline, rc8 the accepted admin source-management baseline, and rc10.1 now introduces the unified Operations Workspace shell under `CI_VALIDATION_PENDING`. Genuine VoiceOver/NVDA remains `BLOCKED_EXTERNAL`.
- Phase 7 — observability and incident operations: `PASS` for internal gates.
- Phase 8 — staging acceptance: `BLOCKED_EXTERNAL` for one approved real staging deployment and the ten deployment-parity evidence classes.
- Phase 9 — external assurance: `NOT COMPLETE`.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is **not production ready**. Issue #1 remains authoritative for external production-acceptance gates.

## Accepted rc9 baseline

PR #115 exact head `c01611a48648ec73e14975337dd549bef86abe88` completed the complete registered workflow matrix successfully and merged as `66f5faecb95b80add4ed4d28a6769592b1a18ddb`. The accepted baseline includes governed registered JSON-source execution, runtime SSRF controls, NVD and GitHub advisory normalizers, DTMO JSON v1 ingestion, connector health/failure isolation and the curated intelligence-source catalog. Human review and separate external share approval remain unchanged.

## RUN-174 / 16.0.0rc10

RC10.1 adds `/ui/operations` as a unified professional application shell. It consolidates operations navigation, command palette, notifications, workspace tabs, runtime/connector KPI cards, quick access to governed role workspaces and a responsive command-center layout.

The new shell reads existing `/health` and `/connectors` endpoints only. It adds no privileged write action and does not bypass admin, review, share-approval, audit or CISO authorization. A graphical ingestion placeholder is explicitly marked as a future real-metrics widget and is not claimed as live telemetry.

The application and package versions are now `16.0.0rc10`. Repository-controlled regression tests protect router wiring, version consistency, navigation, accessibility/responsive contracts and the absence of privileged writes from the shell.

## External blockers

No approved real staging endpoint/environment identity and no complete ten-class deployment-parity package tied to one immutable release are available. Genuine assistive-technology execution, independent penetration testing and remaining external assurance also remain absent. Missing external evidence is never inferred from repository CI.

## Exactly one current priority

Complete exact-head CI validation for RUN-174 / 16.0.0rc10. Merge only if every registered workflow succeeds. After acceptance, the next bounded priority is RC10.2: bind existing operational metrics/building blocks to real graphical dashboard widgets inside the Operations Workspace.
