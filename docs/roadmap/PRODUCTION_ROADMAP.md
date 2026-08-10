# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3. No phase is complete without objective evidence; missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks the corresponding claim.

## Current status — 2026-08-10

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — Application security and identity: `PASS` for internal gates.
- Phase 3 — Data integrity and recovery: `PASS` for internal gates.
- Phase 4 — Live connector reliability and provenance: `PASS` for the built-in CISA KEV path; RUN-172 / rc9 extends this with safe registered JSON-source execution and remains `CI_VALIDATION_PENDING`.
- Phase 5 — Performance and scalability: `PASS` for internal gates.
- Phase 6 — Frontend accessibility and operational UX: rc6 is the accepted professional UX baseline; rc8 adds the accepted admin source-management workspace. Genuine VoiceOver/NVDA remains `BLOCKED_EXTERNAL`.
- Phase 7 — Observability and incident operations: `PASS`.
- Phase 8 — Staging acceptance: `BLOCKED_EXTERNAL` for real deployment-parity evidence.
- Phase 9 — External assurance: `NOT COMPLETE`.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Accepted recent release baselines

### RUN-168 — 16.0.0rc6 professional frontend baseline — `PASS`

PR #112 final exact head `e5e0d5e808d1f66c8f512fa35bd0ea3932fe8631` completed 48/48 registered workflows and merged as `5c2a9c9a5d0d936784597899c97bf5be253c2394`.

### RUN-169 — 16.0.0rc7 search and live-intelligence remediation — `PASS`

PR #113 final exact head `c2b7216d4777488768796a69b3e928571a824e33` completed 48/48 registered workflows and merged as `892d7e48e19109b45062acd272f84a31f6f33802`.

### RUN-170 / RUN-171 — 16.0.0rc8 governed Admin Configuration & Source Registry — `PASS`

PR #114 exact head `95fed1e663bdf256def58020f11529f383c8efe5` completed all 48 registered workflows and merged as `7351ae2ab984b6848969bc634c32e819ec413031`. Human-admin source lifecycle, secret references, audit events, reliability/schedule/enabled metadata and registration-time URL validation are accepted.

### RUN-172 — 16.0.0rc9 safe registered-source execution — `CI_VALIDATION_PENDING`

Current bounded scope adds a runtime trust boundary for enabled registered `json-feed` sources: fresh DNS resolution, complete-answer rejection of non-global destinations, transport pinning to a validated IP with original-hostname TLS verification, no redirects, no environment proxy path, JSON-only content, 5 MiB response bounds, supported NVD/GitHub normalizers, canonical DTMO JSON v1 fallback, connector health/failure isolation, alert integration and replay-safe canonical/search ingestion.

The curated catalog covers major authoritative/public-sector/vendor sources and explicitly distinguishes supported execution profiles from planned parser or research/reference sources. Education-sector School-CERT/Kennisnet and SURF/SURFcert material is tracked as high-value onboarding context subject to approved interfaces and distribution conditions.

Source execution remains candidate ingestion only. It does not change review or separate human share approval.

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

Verify every registered workflow on the final RUN-172 / rc9 exact head. Merge only on complete success; otherwise remediate the first concrete failure. If accepted, the next product objective is integration of existing graphical/operational dashboard building blocks into the professional console.
