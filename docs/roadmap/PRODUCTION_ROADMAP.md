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
- Phase 7 — Observability and incident operations: `IN PROGRESS`; RC10.1–RC10.4 accepted and internal object-storage migration blocker cleared.
- Phase 8 — Staging acceptance: `NOT STARTED`.
- Phase 9 — External assurance: `NOT COMPLETE`; tracked in issue #1.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Accepted Phase 7 evidence

- RC10.1 request observability: `PASS` — PR #80.
- RC10.2 controlled connector-failure alerting: `PASS` — PR #82.
- RC10.3 bounded queue-backlog alerting: `PASS` — PR #84.
- RC10.4 bounded storage-integrity alerting: `PASS` — PR #86.

## Object-storage remediation — internal gate accepted

RUN-131 established that legacy MinIO was archived/unmaintained. RUN-132 accepted ADR-0001 and selected MinIO AIStor Enterprise Lite or Enterprise with active paid support. RUN-133 implemented the fail-closed migration contract.

PR #90 exact head `0fe5c5f0003211fe9df8535954d9276a2090af35` completed **38/38 workflows successfully** and merged as `383702bec6ba07cba065524efa451fd89cbd3b50`. Dedicated run `31326861369` retained artifact `9041774769`, digest `sha256:24e7241138dc0b293957f5e2cd06a4d3a6606b7ba68d688097795047f114ccf8`; independent inspection recorded JUnit 4/4, 0 failures/errors/skips.

Fresh CVE review in RUN-134 requires any production AIStor release selected after this repository migration to be at least `RELEASE.2026-04-14T21-32-45Z` and to undergo a fresh advisory review immediately before deployment. This is a deployment-time security floor, not a claim that production deployment is complete.

Commercial entitlement/support, production topology, registry-digest verification for the chosen release, TLS/network encryption, server-side encryption/KMS, secrets-manager acceptance, staging/production deployment acceptance and other issue #1 external gates remain open.

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

Current decision: `IN PROGRESS`. RC10.1–RC10.4 are accepted. The internal object-storage migration blocker is cleared for its bounded repository scope, so Phase 7 may resume.

Exactly one next priority: **RC10.5 bounded API-error alerting** with safe correlation, actionable evidence, controlled raise/clear behavior, no raw sensitive payload leakage and retained exact-head evidence.

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
