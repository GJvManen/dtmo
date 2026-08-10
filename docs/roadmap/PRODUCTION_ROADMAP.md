# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3. No phase is complete without objective evidence; missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks the corresponding claim.

## Current status — 2026-08-10

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — Application security and identity: `PASS` for internal gates.
- Phase 3 — Data integrity and recovery: `PASS` for internal gates.
- Phase 4 — Live connector reliability and provenance: `PASS` for the built-in CISA KEV path; rc7 restored end-to-end persistence/indexing and replay repair.
- Phase 5 — Performance and scalability: `PASS` for internal gates.
- Phase 6 — Frontend accessibility and operational UX: rc6 is the accepted repository-controlled professional UX baseline; genuine VoiceOver/NVDA execution remains `BLOCKED_EXTERNAL`. rc8 adds an admin source-management workspace under the same external AT claim boundary.
- Phase 7 — Observability and incident operations: `PASS`.
- Phase 8 — Staging acceptance: `BLOCKED_EXTERNAL` for real deployment-parity evidence.
- Phase 9 — External assurance: `NOT COMPLETE`; repository-controlled intake/readiness baseline accepted.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Accepted recent release baselines

### RUN-168 — 16.0.0rc6 professional frontend baseline — `PASS`

PR #112 final exact head `e5e0d5e808d1f66c8f512fa35bd0ea3932fe8631` completed 48/48 registered workflows and merged as `5c2a9c9a5d0d936784597899c97bf5be253c2394`.

### RUN-169 — 16.0.0rc7 search and live-intelligence remediation — `PASS`

PR #113 final exact head `c2b7216d4777488768796a69b3e928571a824e33` completed 48/48 registered workflows and merged as `892d7e48e19109b45062acd272f84a31f6f33802`. Search fresh-index behavior, strict canonical confidence mapping, CISA KEV raw/canonical/provenance/search ingestion, replay-repair and permission-gated manual connector execution are accepted within repository-controlled scope.

### RUN-170 — 16.0.0rc8 governed Admin Configuration & Source Registry — `CI_VALIDATION_PENDING`

Current bounded objective: persistent source lifecycle management with human-admin authorization, service-account separation, secret references, audit-chain events, safe supported source types, explicit reliability/schedule/enabled metadata and first-line SSRF-safe endpoint validation. The admin workspace is `/ui/admin-sources` and the control API is `/api/v1/admin/sources`.

Generic `json-feed` definitions are registry-only in this run. They are not executed. Safe generic source execution remains the next bounded objective after rc8 acceptance and must add DNS/rebinding-safe egress validation, redirect controls, bounded response/content validation, provenance normalization, health/failure isolation and replay integration before any arbitrary registered endpoint is fetched.

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

Complete exact-head CI for RUN-170 / 16.0.0rc8. Merge only on complete success. If accepted, proceed to one safe generic registered-source execution adapter; otherwise remediate only the first concrete failure.
