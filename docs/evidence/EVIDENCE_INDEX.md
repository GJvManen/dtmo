# DTMO Evidence Index

Last updated: 2026-08-10

## Purpose

This index provides the top-level map from roadmap phases to QA records, workflows, artifacts, run records, pull requests and authoritative issues. It does not replace the detailed evidence files.

## Authoritative sources

- Roadmap: `docs/roadmap/PRODUCTION_ROADMAP.md`
- Current state: `docs/project/CURRENT_STATE.md`
- Run audit trail: `docs/development/RUN_LOG.md` and `docs/development/runs/`
- QA decisions: `docs/qa/`
- External gates: issue #1
- Continuous development coordination: issue #2
- Production roadmap tracking: issue #3

## Phase evidence map

### Phase 1 — CI and workflow integrity

Status: `PASS`.

Evidence classes: exact-head workflow execution, regression protection, workflow-contract validation, quality gate execution and retained CI evidence.

### Phase 2 — Application security and identity

Status: `PASS` internally.

Evidence classes: RBAC, authentication/authorization, token/session behavior, separation of duties, auditability, security headers and human approval controls.

### Phase 3 — Data integrity and recovery

Status: `PASS` internally.

Evidence classes: migrations, object-storage migration, OpenSearch recovery, multi-store recovery, storage integrity and controlled recovery behavior.

### Phase 4 — Connector reliability and provenance

Status: `PASS` internally.

Evidence classes: connector contracts, state, retry, timeout, replay, freshness, failure isolation, live canary execution and payload provenance. Provider credential/rate-limit/licence/terms acceptance is separately recorded in issue #1.

### Phase 5 — Performance and scalability

Status: `PASS` internally.

Evidence classes: ingestion performance, queue burst behavior, API reads, OpenSearch reads, degraded dependencies and concurrency saturation.

### Phase 6 — Accessibility and operational UX

Status: `BLOCKED_EXTERNAL`.

Accepted: bounded automated/browser accessibility evidence.

Missing: genuine VoiceOver/NVDA execution on supported real combinations.

### Phase 7 — Observability and incident operations

Status: `PASS`.

Evidence classes: request observability, distributed trace context, queue backlog alerting, connector failure alerting, storage integrity alerting, API/search health alerting, dashboards, runbooks, exercises and on-call handover.

### Phase 8 — Staging acceptance

Status: `BLOCKED_EXTERNAL`.

Accepted bounded evidence:
- staging-emulator configuration contract;
- application-container runtime smoke.

Key accepted PRs/artifacts:
- PR #104, final head `93d1a659b7b136546ffcf73102890f5d2d00ba84`, 47/47 workflows, artifact `9045039742`;
- PR #107, final head `52d7a37660c9bb1c9f8468f11010f36d17bd1fba`, 48/48 workflows, artifact `9057259246`;
- PR #108 lifecycle remediation and documentation finalization, 48/48 exact-head workflow evidence before merge;
- PR #109 RUN-158 documentation/evidence recheck, 48/48 workflows before merge.

Missing: one real approved staging deployment and the ten deployment-parity classes documented in `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`.

### Phase 9 — External assurance

Status: `NOT COMPLETE`.

Evidence contract: `docs/qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md`.

Required independent classes: penetration test, representative load/stress, full restoration, platform hardening, secrets-management acceptance, operational/stakeholder acceptance and deployment acceptance.

### Phase 10 — Production go/no-go

Status: `NOT STARTED`.

Required inputs: all prior phase evidence, all issue #1 blocking gates, immutable release/deployment identity, SBOM/release manifest, rollback/recovery proof, findings disposition and required approvals.

## Evidence handling rules

- Evidence must be attributable and reviewable.
- Exact-head CI evidence must match the commit being accepted.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not PASS.
- Evidence must not contain secret values, credentials, tokens or unnecessary personal data.
- Threat-intelligence/CVE/vendor-advisory evidence must preserve source provenance, review time, applicability and confidence.
- Human share approval remains separate from technical execution and review.
