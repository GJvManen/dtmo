# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's current release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3.

The release rule is strict: no phase is complete without objective evidence. Missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks production readiness.

## Current status — 2026-08-09

- Phase 1 — CI and workflow integrity: `PASS` for accepted mainline evidence; PR #97 has an active exact-head acceptance blocker until RUN-143's remediated full matrix passes.
- Phase 2 — Application security and identity: `PASS` for internal gates.
- Phase 3 — Data integrity and recovery: `PASS` for internal gates.
- Phase 4 — Live connector reliability and provenance: `PASS` for internal gates.
- Phase 5 — Performance and scalability: `PASS` for internal gates.
- Phase 6 — Frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA execution on supported real hosts.
- Phase 7 — Observability and incident operations: `IN PROGRESS`; RC10.1–RC10.9 are accepted. RC10.10 remains `CI_VALIDATION_PENDING` after RUN-143 evidence-validator remediation.
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
- RC10.9 operational incident runbooks: `PASS` — PR #96 exact head `625757de118878d7c7b7b60847959c17d3c7c844`, 43/43 workflows, artifact `9042812326`, merge `28ffdc1d0c510ab57ea42751eb74261192899438`.

RUN-141 is accepted as the Phase-1 CI-integrity remediation that fixed the initial RC10.9 governance-text regression without weakening tests or policy.

## Object-storage remediation — internal gate accepted

RUN-131 through RUN-134 established and implemented the supported object-storage contract. Commercial entitlement/support, production topology, deployment-time image digest verification, TLS/SSE/KMS, secrets-manager acceptance and production deployment remain external/open.

## Phase 1 — CI and workflow integrity

Objectives: regression-protect release-critical workflows, validate triggers/jobs/permissions/services/artifacts, make execution observable, and fail closed on missing/malformed gates.

Blocking gates: workflow contract tests pass; required jobs/triggers are validated; workflow evidence is observable; failed/absent workflows cannot be interpreted as success.

RUN-143 is an active bounded Phase-1 remediation discovered during RC10.10 acceptance. PR #97 exact head `1862b1c4e9e768da82baef3470464845cadf3967` completed 43/44 workflows. The dedicated `RC10 Operational Runbook Exercise Gate` failed after its scenario tests passed 5/5 because its evidence validator used `assert all(e["controls"].values())`, which incorrectly rejected the intentionally false safety controls `production_data_used=false` and `production_credentials_used=false`.

The validator is corrected without weakening the gate: required-positive controls are asserted `True`; required-negative safety controls are asserted `False`; all claim-boundary values must remain false. A complete fresh exact-head matrix and regenerated retained artifact are mandatory. The failed prior head is not accepted.

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
- operational ownership/escalation documented.

### RC10.10 controlled synthetic operational runbook exercise — `CI_VALIDATION_PENDING`

RUN-142 adds a scenario-driven technical exercise over the accepted runbooks for API elevated-5xx, connector/source degradation, search red/unreachable, and storage-integrity failure. Each scenario requires severity/scope classification, evidence preservation, reversible containment, security/privacy branching, known-good recovery, objective validation, human communication/share approval and residual-risk handoff. No production data, production credentials, destructive remediation or external communication is used.

The first PR #97 exact head is not accepted: 43/44 workflows succeeded, while the dedicated exercise gate failed only in its evidence validator. RUN-143 fixes that validator logic; every workflow and retained `operational-runbook-exercise-evidence` must regenerate on one new exact final head.

The exercise remains a **controlled synthetic technical exercise** and does not claim human tabletop participation, response-time evidence, on-call handover or operational ownership acceptance.

Phase 7 will remain incomplete after RC10.10 until operational ownership/escalation and on-call handover are evidenced. Any production observability-platform deployment acceptance remains staging/external work.

Exactly one next priority: verify all 44 workflows on the new exact PR #97 head and independently inspect regenerated `operational-runbook-exercise-evidence`; merge only after all registered workflows succeed and retained evidence is exact-head bound.

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
