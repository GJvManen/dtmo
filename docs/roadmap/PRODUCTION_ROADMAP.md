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
- Phase 7 — Observability and incident operations: `IN PROGRESS`.
- Phase 8 — Staging acceptance: `NOT STARTED`.
- Phase 9 — External assurance: `NOT COMPLETE`; tracked in issue #1.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Accepted Phase 7 evidence

### RC10.1 request observability — `PASS`
PR #80 exact head `01a175e12da7c8af8566178a2d7e6b34a57d58bc`; 34/34 workflows; artifact `9040196394`, digest `sha256:6792020994d94b0484cb84140d202433303eceb82565f8598ffd5937940531d6`; JUnit 5/5; merge `1675d88bb24dcd50e20545f49b26dd7cc2810d97`.

### RC10.2 controlled connector-failure alerting — `PASS`
PR #82 exact head `b38aeae44588e39e35339f4c4d9667947804b243`; 35/35 workflows; artifact `9040485255`, digest `sha256:96883158cfd790c3c6b21c2db819acbcbc03d431d4dd79bb32038b6ff258de25`; JUnit 4/4; merge `f6680423860389288d9feced34592294d774bf4a`.

### RC10.3 bounded queue-backlog alerting — `PASS`
PR #84 exact head `8058b476298eee4bcd2942d9cca54384ec12aa74`; 36/36 workflows; artifact `9040996591`, digest `sha256:42aaad1424d7c1ad40accd056b4746ea6fb328a561b24df5ebc293c0425b1910`; 80% raise/50% clear hysteresis, bounded queue metrics, correlated actionable evidence and RC8 queue-pressure reuse; JUnit 5/5; merge `42ccbe04cbc1081f93e4a155243627b5a3038573`.

Phase 7 remains incomplete because distributed tracing, storage-integrity/API-error/search-health alerting, dashboards, runbooks, on-call handover and ownership/escalation evidence remain open. RC10.2/RC10.3 do not claim external notification delivery; RC10.3 does not claim a separate deployed durable queue service.

## Phase 1 — CI and workflow integrity

Objectives: regression-protect release-critical workflows, validate triggers/jobs/permissions/services/artifacts, make execution observable, and fail closed on missing/malformed gates.

Blocking gates: workflow contract tests pass; required jobs/triggers are validated; workflow evidence is observable; failed/absent workflows cannot be interpreted as success.

## Phase 2 — Application security and identity

Objectives: enterprise identity or hardened trust boundary, strong RBAC/separation of duties, privileged audit logging, SAST/dependency/secrets/container scanning.

Blocking gates: authentication/authorization and negative RBAC tests pass; no hardcoded production secrets; no unresolved critical security-scan findings.

## Phase 3 — Data integrity and recovery

Objectives: validate PostgreSQL migrations/constraints, raw-object immutability/checksums, backup/retention/restoration, and full clean restoration.

Blocking gates: migration cycle succeeds; restore test succeeds; provenance/checksum integrity survives; RTO/RPO are documented and tested.

## Phase 4 — Live connector reliability and provenance

Objectives: controlled live canaries, credentials/rate limits/licences/terms validation, retry/backoff/dedup/source health/failure isolation, retained source/timestamp/confidence/raw evidence.

Blocking gates: connector contracts pass; canaries repeat; malformed/duplicate records quarantine; connectors cannot publish without human review.

## Phase 5 — Performance and scalability

Objectives: representative education-sector volumes, API/PostgreSQL/OpenSearch/ingestion load tests, latency/throughput/resource budgets, queue pressure and degraded dependencies.

Current decision: `PASS` for bounded internal gates. RC8.8 capacity guidance does not close issue #1's independent representative production load/stress gate.

## Phase 6 — Frontend accessibility and operational UX

Objectives: browser E2E, critical analyst/CISO/audit workflows, responsive/keyboard behavior, bounded WCAG evidence and separately genuine assistive-technology behavior.

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
- operational ownership/escalation documented.

Current decision: `IN PROGRESS`. RC10.1, RC10.2 and RC10.3 are accepted. Exactly one next priority is RC10.4 bounded storage-integrity alerting with controlled integrity-failure/recovery evidence, actionable correlation, no raw sensitive payload leakage and retained exact-head evidence. API-error and search-health alerting remain later objectives.

## Phase 8 — Staging acceptance

Objectives: production-equivalent deployment, smoke/integration/migration/connector/recovery/performance/accessibility tests, secrets/TLS/network restrictions.

Blocking gates: reproducible staging; all internal gates pass; no unresolved blockers; deployment evidence retained.

## Phase 9 — External assurance

Tracked in issue #1: independent penetration test, representative load/stress, full backup/restoration exercise, production OpenSearch hardening, required secrets-management acceptance, operational/stakeholder approvals.

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
