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
- Phase 7 — Observability and incident operations: `IN PROGRESS`; RC10.1–RC10.5 and the bounded object-storage remediation are accepted; RC10.6 search-health alerting is `CI_VALIDATION_PENDING`.
- Phase 8 — Staging acceptance: `NOT STARTED`.
- Phase 9 — External assurance: `NOT COMPLETE`; tracked in issue #1.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Accepted Phase 7 evidence

- RC10.1 request observability: `PASS` — PR #80.
- RC10.2 controlled connector-failure alerting: `PASS` — PR #82.
- RC10.3 bounded queue-backlog alerting: `PASS` — PR #84.
- RC10.4 bounded storage-integrity alerting: `PASS` — PR #86.
- RC10.5 bounded API-error alerting: `PASS` — PR #92 exact head `659fa022840e01ed6db4ebeb6a5e703f58a6d259`, 39/39 workflows, artifact `9041987610`, digest `sha256:6a6f2aa5ea2b0b3fb081a0b376f8187a799af726ba950bcbf6fd8618c54e2eca`, JUnit 6/6, merge `8d6297e17c93150dacb39428ed3580e7c8cc1579`.

## Object-storage remediation — internal gate accepted

RUN-131 established that legacy MinIO was archived/unmaintained. RUN-132 accepted ADR-0001 and selected MinIO AIStor Enterprise Lite or Enterprise with active paid support. RUN-133 implemented the fail-closed migration contract; RUN-134 reconciled security/recovery/storage-integrity evidence.

Production AIStor selection remains subject to the RUN-134 release/advisory floor and fresh deployment-time advisory review. Commercial entitlement/support, production topology, registry-digest verification, TLS/network encryption, server-side encryption/KMS, secrets-manager acceptance, staging/production deployment acceptance and other issue #1 external gates remain open.

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

Current decision: `PASS` for bounded internal gates. Issue #1 retains independent representative production load/stress acceptance.

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

### RC10.6 bounded search-health alerting — `CI_VALIDATION_PENDING`

RUN-136 implements:

- cluster-health-only observation using a bounded cluster identifier plus `green|yellow|red|unreachable` status;
- raise after 2 consecutive `red`/`unreachable` observations;
- clear after 2 consecutive `green`/`yellow` observations while active;
- repeat-raise suppression;
- bounded health-check/streak/active-state/transition Prometheus metrics;
- `DTMOSearchHealthFailure` with actionable operator guidance;
- `probe_opensearch_health()` which consumes only `/_cluster/health` status and maps HTTP/parse failure to `unreachable` without exposing response bodies;
- structured correlation evidence with `publish_approved=false`;
- controlled failure/recovery/privacy tests;
- dedicated retained exact-head `RC10 Search Health Alerting Gate`.

Fresh first-party OpenSearch review confirms OpenSearch 2.19 remains in maintenance and 2.19.6 is the current 2.x maintenance release with security updates. This run does not close the separate issue #1 production OpenSearch hardening/version gate.

RC10.6 is not accepted until every registered workflow succeeds on its exact final head and retained `search-health-alerting-evidence` is independently verified.

Phase 7 remains incomplete after RC10.6 because distributed tracing, dashboards, runbooks, on-call handover and ownership/escalation evidence remain open.

Exactly one next priority: verify the complete exact-head workflow matrix and retained `search-health-alerting-evidence` artifact for RUN-136; merge only after all registered workflows succeed and retained evidence is exact-head bound.

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
