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
- Phase 7 — Observability and incident operations: `IN PROGRESS`; RC10.1–RC10.10 are accepted. RC10.11 on-call ownership/escalation handover baseline is `CI_VALIDATION_PENDING`.
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
- RC10.10 controlled synthetic operational runbook exercise: `PASS` — PR #97 exact head `a332453e0ed9c2f413107cdadfed316b4ac6c2ce`, 44/44 workflows, artifact `9043082726`, digest `sha256:dd095787ed6624f628d0f030ac9af0ccc56d46e9a59ff840ac64ab261dace154`, JUnit 5/5, merge `788daad06879c1c99f22625569bd1b74abe9249f`.

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

Objectives:
- service-level metrics, structured logs and traces;
- alerting for connector failures, queue backlog, storage integrity, API errors and search health;
- incident/outage/recovery/connector-failure runbooks;
- dashboards and on-call handover guidance.

Blocking gates:
- alerts tested with controlled failures;
- logs/metrics provide correlation IDs and actionable evidence;
- runbooks complete and exercised;
- operational ownership/escalation documented and human handover accepted.

### RC10.11 on-call ownership and escalation handover baseline — `CI_VALIDATION_PENDING`

RUN-144 defines the source-controlled handover contract:

- primary/secondary responder, Incident Commander, security lead, service owner, communications approver and business/stakeholder owner responsibilities;
- severity escalation matrix and coverage requirements;
- shift-handover checklist with explicit incoming acknowledgement;
- privacy-safe incident/handover evidence rules;
- RBAC and human share approval remain unchanged;
- named people/contact details remain outside the repository;
- human acceptance requires staffed coverage, tested paging/contact and escalation paths, real-participant handover, a human exercise/walkthrough, unresolved-gap ownership and service/operational-owner sign-off.

CI validates only the documentation/governance contract. It does not prove staffing, reachability, training, tested contacts or human acceptance.

Phase 7 remains incomplete until RC10.11 exact-head evidence is accepted and the external/human operational ownership/handover evidence is supplied. If that human evidence cannot be produced in the repository workflow, Phase 7 becomes `BLOCKED_EXTERNAL` at that point rather than being falsely marked complete.

Exactly one next priority: verify the complete exact-head workflow matrix and retained `oncall-handover-evidence` for RUN-144; merge only after all registered workflows succeed and retained evidence is exact-head bound.

## Phase 8 — Staging acceptance

Objectives: production-equivalent deployment, smoke/integration/migration/connector/recovery/performance/accessibility tests, secrets/TLS/network restrictions.

Blocking gates: reproducible staging; all internal gates pass; no unresolved blockers; deployment evidence retained.

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
