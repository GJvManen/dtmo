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
- Phase 7 — Observability and incident operations: `IN PROGRESS`; RC10.1–RC10.4 and the bounded object-storage remediation are accepted; RC10.5 API-error alerting is `CI_VALIDATION_PENDING`.
- Phase 8 — Staging acceptance: `NOT STARTED`.
- Phase 9 — External assurance: `NOT COMPLETE`; tracked in issue #1.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Accepted Phase 7 evidence

- RC10.1 request observability: `PASS` — PR #80.
- RC10.2 controlled connector-failure alerting: `PASS` — PR #82.
- RC10.3 bounded queue-backlog alerting: `PASS` — PR #84.
- RC10.4 bounded storage-integrity alerting: `PASS` — PR #86.

## Object-storage remediation — internal gate accepted

RUN-131 established that legacy MinIO was archived/unmaintained. RUN-132 accepted ADR-0001 and selected MinIO AIStor Enterprise Lite or Enterprise with active paid support. RUN-133 implemented the fail-closed migration contract; RUN-134 reconciled security/recovery/storage-integrity evidence.

PR #90 exact head `0fe5c5f0003211fe9df8535954d9276a2090af35` completed 38/38 workflows and merged as `383702bec6ba07cba065524efa451fd89cbd3b50`. Dedicated artifact `9041774769`, digest `sha256:24e7241138dc0b293957f5e2cd06a4d3a6606b7ba68d688097795047f114ccf8`, independently recorded JUnit 4/4. PR #91 exact head `d81caaa372b0cf3e079023eb255a57fd4892d6e0` subsequently completed 38/38 workflows and merged as `23af430c041e3f0e203b7a7f7a6c69f3eea79055`.

Production AIStor selection remains subject to the RUN-134 release/advisory floor and fresh deployment-time advisory review. Commercial entitlement/support, production topology, registry-digest verification, TLS/network encryption, server-side encryption/KMS, secrets-manager acceptance, staging/production deployment acceptance and other issue #1 external gates remain open.

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
- operational ownership/escalation documented.

### RC10.5 bounded API-error alerting — `CI_VALIDATION_PENDING`

RUN-135 implements a bounded API-error observer integrated with existing request middleware:

- route-template-only alert labels; raw request URL/query/body/header/identity data are outside the observer contract;
- raise after 3 consecutive HTTP 5xx outcomes for one route template;
- clear after 2 consecutive non-5xx outcomes while active;
- repeat-raise suppression;
- request-result/streak/active-state/transition Prometheus metrics;
- structured correlation evidence, actionable guidance and `publish_approved=false`;
- `DTMOApiServerErrors` Prometheus rule;
- controlled middleware integration tests and dedicated retained-evidence workflow.

Fresh dependency review recorded Starlette CVE-2026-48817 and CVE-2026-48818 as affecting versions through 1.0.1 and fixed in 1.1.0. DTMO does not directly pin Starlette, so exploitability is not asserted; the resolved dependency set remains governed by the existing security/dependency CI gates.

RC10.5 is not accepted until every registered workflow succeeds on its exact final head and the retained `api-error-alerting-evidence` artifact is independently verified.

Phase 7 remains incomplete after RC10.5 because search-health alerting, distributed tracing, dashboards, runbooks, on-call handover and ownership/escalation evidence remain open.

Exactly one next priority: verify the complete exact-head workflow matrix and retained `api-error-alerting-evidence` artifact for RUN-135; merge only after all registered workflows succeed and retained evidence is exact-head bound.

## Phase 8 — Staging acceptance

Objectives: production-equivalent deployment, smoke/integration/migration/connector/recovery/performance/accessibility tests, secrets/TLS/network restrictions.

Blocking gates: reproducible staging; all internal gates pass; no unresolved blockers; deployment evidence retained.

## Phase 9 — External assurance

Tracked in issue #1: independent penetration test, representative load/stress, full backup/restoration exercise, production OpenSearch hardening, required secrets-management acceptance, operational/stakeholder approvals and production deployment acceptance.

## Phase 10 — Production go/no-go

Go requires every prior phase and external gate complete with retained evidence, green CI, release notes/SBOM/deployment manifest/rollback plan, proven recovery and required approvals. Any missing blocking evidence is `NO-GO`.

## PDCA execution order

Each run performs exactly one bounded objective in roadmap order unless a higher-severity blocker is discovered or an earlier phase is blocked only by an explicitly external dependency that cannot be executed in the current environment.

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
