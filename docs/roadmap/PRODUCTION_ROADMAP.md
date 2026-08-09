# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's current release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3.

The release rule is strict: no phase is complete without objective evidence. Missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks production readiness.

## Current status — 2026-08-09

- Phase 1 — CI and workflow integrity: `PASS` for accepted mainline evidence; PR #96 has an active exact-head acceptance blocker until the remediated full matrix passes.
- Phase 2 — Application security and identity: `PASS` for internal gates.
- Phase 3 — Data integrity and recovery: `PASS` for internal gates.
- Phase 4 — Live connector reliability and provenance: `PASS` for internal gates.
- Phase 5 — Performance and scalability: `PASS` for internal gates.
- Phase 6 — Frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA execution on supported real hosts.
- Phase 7 — Observability and incident operations: `IN PROGRESS`; RC10.1–RC10.8 and bounded object-storage remediation are accepted; RC10.9 operational runbooks remain `CI_VALIDATION_PENDING` after RUN-141 quality-gate remediation and are not yet exercised.
- Phase 8 — Staging acceptance: `NOT STARTED`.
- Phase 9 — External assurance: `NOT COMPLETE`; tracked in issue #1.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Accepted Phase 7 evidence

- RC10.1 request observability: `PASS` — PR #80.
- RC10.2 controlled connector-failure alerting: `PASS` — PR #82.
- RC10.3 bounded queue-backlog alerting: `PASS` — PR #84.
- RC10.4 bounded storage-integrity alerting: `PASS` — PR #86.
- RC10.5 bounded API-error alerting: `PASS` — PR #92, 39/39 workflows, artifact `9041987610`.
- RC10.6 bounded search-health alerting: `PASS` — PR #93, 40/40 workflows, artifact `9042097760`.
- RC10.7 bounded distributed trace-context baseline: `PASS` — PR #94 exact head `5a2f60749f6eaf6ece9dcfcc3b70c866887c6cb8`, 41/41 workflows, artifact `9042398103`, JUnit 10/10, merge `e52af08204d212cdfba0e9338bacb7a1c5fcfac7`.
- RC10.8 bounded operational dashboard: `PASS` — PR #95 exact head `602c316e5dca2b17787523c70e8eb8e327e78b0d`, 42/42 workflows, artifact `9042548010`, digest `sha256:11125b626f0f6431bc40a9700333bdba8f5c07175981e427f87f62b279a4fddf`, JUnit 5/5, merge `2726adeed0762b38f3ce03817bcb68aea688e356`.

## Object-storage remediation — internal gate accepted

RUN-131 established that legacy MinIO was archived/unmaintained. RUN-132 accepted ADR-0001 and selected MinIO AIStor Enterprise Lite or Enterprise with active paid support. RUN-133 implemented the fail-closed migration contract; RUN-134 reconciled security/recovery/storage-integrity evidence.

Production AIStor selection remains subject to the RUN-134 release/advisory floor and fresh deployment-time advisory review. Commercial entitlement/support, production topology, registry-digest verification, TLS/network encryption, server-side encryption/KMS, secrets-manager acceptance, staging/production deployment acceptance and other issue #1 external gates remain open.

## Phase 1 — CI and workflow integrity

Objectives: regression-protect release-critical workflows, validate triggers/jobs/permissions/services/artifacts, make execution observable, and fail closed on missing/malformed gates.

Blocking gates: workflow contract tests pass; required jobs/triggers are validated; workflow evidence is observable; failed/absent workflows cannot be interpreted as success.

RUN-141 is an active bounded Phase-1 remediation discovered during RC10.9 acceptance. PR #96 exact head `42d7104915a5e424e9cebc2e4f0a093cf7948f94` completed 42/43 workflows. The `RC4 Quality Gate` failed in the full pytest step because the runbook index omitted the canonical machine-checked governance phrase `human share approval`, although it contained near-equivalent wording. The documentation contract was corrected without weakening the test, workflow, RBAC or separation-of-duties requirement. A complete fresh exact-head matrix is mandatory.

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

### RC10.9 bounded operational incident runbooks — `CI_VALIDATION_PENDING`

RUN-140 adds:

- common incident roles and SEV-1/2/3 severity guidance;
- evidence/privacy rules and a universal acknowledge/correlate/preserve/contain/recover/validate/communicate/close sequence;
- API outage/elevated-5xx runbook bound to `dtmo_api_error_alert_active`;
- connector failure/source-degradation runbook bound to `dtmo_connector_alert_active`, preserving provenance, freshness, quarantine and human approval;
- search-health degradation runbook bound to `dtmo_search_health_alert_active`, with explicit incomplete-result handling;
- storage-integrity/recovery runbook bound to `dtmo_storage_integrity_alert_active`, quarantine and known-good restoration;
- controlled regression tests and a dedicated retained `RC10 Operational Runbooks Gate`.

Fresh authoritative threat/historical review uses CISA education-sector ransomware material, the CISA #StopRansomware Guide and CISA/FBI PaperCut CVE-2023-27350 reporting. Those sources document education-sector disruption, student-data theft/extortion, credential/system compromise, exfiltration and encryption, supporting evidence preservation, account review, containment and known-good recovery. They do not imply any current DTMO compromise or future attribution.

The first PR #96 exact head is not accepted: 42/43 workflows succeeded, but the aggregate `RC4 Quality Gate` failed on the canonical governance-text assertion. RUN-141 updates the runbook index to state explicitly that **human share approval** is never granted to technical responders, connectors, observability components or service accounts by incident status alone. The dedicated runbook gate's prior-head success is insufficient after this change; every workflow and retained `operational-runbooks-evidence` must regenerate on one new exact final head.

Phase 7 remains incomplete because the runbooks must still be exercised and operational ownership/escalation/on-call handover must be evidenced. Any required production observability-platform deployment acceptance also remains external/staging work.

Exactly one next priority: verify the complete fresh exact-head workflow matrix and regenerated retained `operational-runbooks-evidence` artifact for PR #96; merge only after all registered workflows succeed and retained evidence is exact-head bound.

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
