# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's current release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3.

The release rule is strict: no phase is complete without objective evidence. Missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks production readiness.

## Current status — 2026-08-09

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — Application security and identity: `PASS` for internal gates.
- Phase 3 — Data integrity and recovery: `PASS` for internal gates.
- Phase 4 — Live connector reliability and provenance: `PASS` for internal gates.
- Phase 5 — Performance and scalability: `PASS` for internal gates.
- Phase 6 — Frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA execution on supported real hosts.
- Phase 7 — Observability and incident operations: `BLOCKED_EXTERNAL`; RC10.1–RC10.11 internal engineering gates are accepted, but human operational ownership/handover acceptance is not evidenced.
- Phase 8 — Staging acceptance: `NOT STARTED`.
- Phase 9 — External assurance: `NOT COMPLETE`; tracked in issue #1.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Accepted Phase 7 evidence

- RC10.1 request observability: `PASS` — PR #80.
- RC10.2 connector-failure alerting: `PASS` — PR #82.
- RC10.3 queue-backlog alerting: `PASS` — PR #84.
- RC10.4 storage-integrity alerting: `PASS` — PR #86.
- RC10.5 API-error alerting: `PASS` — PR #92.
- RC10.6 search-health alerting: `PASS` — PR #93.
- RC10.7 distributed trace-context baseline: `PASS` — PR #94.
- RC10.8 operational dashboard: `PASS` — PR #95.
- RC10.9 operational incident runbooks: `PASS` — PR #96.
- RC10.10 controlled synthetic operational runbook exercise: `PASS` — PR #97.
- RC10.11 on-call ownership and escalation handover baseline: `PASS` — PR #98 exact head `8574995796dd1d54cc6411227cdae83219f82122`, 45/45 workflows, artifact `9043200727`, digest `sha256:a33797bc61c6d08ba5fedc8010db4ebd0ded741153167fbd0fec163ceab675ac`, JUnit 5/5, merge `1e4e6a0a3fbe43ffcec5d421f0760467e3a53b4f`.

## Object-storage remediation — internal gate accepted

RUN-131 through RUN-134 established and implemented the supported object-storage contract. Commercial entitlement/support, production topology, deployment-time image digest verification, TLS/SSE/KMS, secrets-manager acceptance and production deployment remain external/open.

## Phase 1 — CI and workflow integrity

Current decision: `PASS`.

## Phase 2 — Application security and identity

Current decision: `PASS` for internal gates.

## Phase 3 — Data integrity and recovery

Current decision: `PASS` for internal gates; full representative external restore acceptance remains in issue #1.

## Phase 4 — Live connector reliability and provenance

Current decision: `PASS` for internal gates.

## Phase 5 — Performance and scalability

Current decision: `PASS` for bounded internal gates; representative production load/stress remains external.

## Phase 6 — Frontend accessibility and operational UX

Current decision: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA evidence on supported real host/browser/screen-reader combinations. Browser/DOM automation is not a substitute.

## Phase 7 — Observability and incident operations

Internal engineering objectives are complete and accepted through RC10.11: metrics/logs/trace context, alerting, dashboards, runbooks, controlled technical exercise, and a source-controlled ownership/escalation/handover contract.

Phase 7 is nevertheless `BLOCKED_EXTERNAL` because the following cannot be proven by repository CI:
- real staffed primary/secondary coverage;
- tested primary/fallback contact and escalation paths;
- real-participant handover with incoming acknowledgement;
- human exercise/walkthrough of the escalation and handover process;
- explicit ownership of unresolved operational gaps;
- service-owner and operational-owner sign-off.

These requirements must be retained as external human evidence. Named contact data and credentials remain outside the repository. CI success must not be interpreted as staffing/reachability/acceptance.

Exactly one next priority: obtain and retain external human operational-acceptance evidence for Phase 7. If unavailable, Phase 7 remains `BLOCKED_EXTERNAL` and production readiness remains blocked.

## Phase 8 — Staging acceptance

Objectives: production-equivalent deployment, smoke/integration/migration/connector/recovery/performance/accessibility tests, secrets/TLS/network restrictions.

Blocking gates: reproducible staging; all internal gates pass; no unresolved blockers; deployment evidence retained.

Phase 8 is `NOT STARTED`. RUN-145 deliberately does not begin Phase 8 because its single bounded objective is Phase 7 acceptance/blocker reconciliation.

## Phase 9 — External assurance

Tracked in issue #1: independent penetration test, representative load/stress, full backup/restoration exercise, production platform hardening, required secrets-management acceptance, operational/stakeholder approvals and production deployment acceptance.

## Phase 10 — Production go/no-go

Go requires every prior phase and external gate complete with retained evidence, green CI, release notes/SBOM/deployment manifest/rollback plan, proven recovery and required approvals. Any missing blocking evidence is `NO-GO`.

## PDCA execution order

1. Phase 1 — CI and workflow integrity.
2. Phase 2 — Application security and identity.
3. Phase 3 — Data integrity and recovery.
4. Phase 4 — Live connector reliability and provenance.
5. Phase 5 — Performance and scalability.
6. Phase 6 — Frontend accessibility and operational UX.
7. Phase 7 — Observability and incident operations.
8. Phase 8 — Staging acceptance.
9. Phase 9 — External assurance coordination.
10. Phase 10 — Production go/no-go.

Every run must document Plan, Do, Check and Act, update run/QA evidence, preserve claim boundaries, and leave exactly one next priority.