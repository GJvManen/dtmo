# DTMO Evidence Index

Last updated: **2026-08-15**

## Purpose

This index maps DTMO lifecycle stages to their evidence classes and authoritative professional documentation. It is not a CI chronology or incident log.

Exact workflow/job/commit history remains under `docs/development/`, GitHub issues/pull requests and CI artifacts.

**Production readiness:** DTMO is **not production ready**. Phase 8 accountable external acceptance, Phase 9 independent external assurance and Phase 10 formal production authorization remain required.

## Authoritative current-state sources

- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PRODUCTION_ROADMAP.md`
- `docs/project/PRODUCTION_READINESS_REPORT.md`
- `docs/project/PRODUCTION_CHECKLIST.md`
- `docs/project/EXECUTIVE_STATUS.md`
- `docs/project/DOCUMENTATION_STATUS.md`
- `docs/qa/QA_AND_RELEASE_GATES.md`
- `docs/traceability/TRACEABILITY_MATRIX.md`

## Evidence hierarchy

DTMO distinguishes five non-interchangeable evidence classes:

1. **Repository-controlled engineering evidence** — exact-head CI, contracts, browser tests and repository recovery/performance/observability evidence.
2. **Accountable functional evidence** — explicit project-owner acceptance of product behavior.
3. **Real-environment evidence** — production-equivalent staging deployment and validation tied to an immutable identity.
4. **Independent assurance evidence** — external security/resilience/operational assessment independent from project self-attestation.
5. **Formal production authorization** — accountable Phase 10 go/no-go decision.

## Lifecycle evidence map

### Phases 1–7 — engineering baseline

**Status:** `PASS`.

Primary evidence includes release integrity, identity/security, persistence/recovery, connector provenance/reliability, performance, accessibility/browser UX, observability/operations and open-source governance.

### RC13 — functional product acceptance

**Status:** `PASS / OWNER_ACCEPTED`.

Primary current-state references:

- `docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`
- `docs/project/CURRENT_STATE.md`
- immutable owner-acceptance records under `docs/development/runs/`

### E8.1–E8.10 — vulnerability and CTI evolution

**Status:** `PASS / REPOSITORY_COMPLETE`.

Repository evidence covers OpenCVE, Vulnerability-Lookup, vulnerability prioritization, vendor/product relevance, vulnerability analytics, governed MISP read/export, governed AIL read/enrichment/correlation and vulnerability-management governance evidence mapping.

This is repository evidence only; it does not establish live-feed completeness, external-share authority, production deployment, independent assurance or production approval.

### Post-E8 staging deployment

**Status:** `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE` for the fact that the post-E8 candidate was externally deployed/tested in an owner-approved production-equivalent staging environment.

Formal Phase 8 closure remains incomplete until the accepted deployment is bound to one immutable technical identity and the required external Phase 8.2–8.5 evidence is accepted.

### Phase 8.2 — platform and identity validation

**Repository contract:** `COMPLETE`  
**External acceptance:** `REQUIRED`

Primary artifacts:

- `docs/staging/PHASE8_2_PLATFORM_IDENTITY_VALIDATION.md`
- step-specific Phase 8.2 runbooks/templates under `docs/staging/` and `docs/qa/`
- complete Phase 8.2 evidence-consolidation contract

Required external evidence includes health/readiness, PostgreSQL, OpenSearch, Redis, object storage, bearer trust, RBAC, human/service separation, privileged Administration, audit/correlation, Prometheus and Grafana, all tied to the same immutable staging identity.

### Phase 8.3 — source-to-intelligence validation

**Repository contract:** `COMPLETE`  
**External acceptance:** `REQUIRED`

Primary artifacts:

- `docs/qa/PHASE8_3_SOURCE_TO_INTELLIGENCE_VALIDATION.md`
- `docs/staging/PHASE8_3_SOURCE_INTELLIGENCE_EVIDENCE.template.json`

Required evidence must demonstrate a real approved staging source through retrieval, provenance, raw evidence, normalization, persistence/search, deduplication/idempotency, enrichment/correlation, vulnerability/CTI semantics, API/UI presentation, governance/classification, traceability and degraded behavior.

### Phase 8.4 — operations, recovery and rollback

**Repository contract:** `COMPLETE`  
**External acceptance:** `REQUIRED`

Primary artifacts:

- `docs/qa/PHASE8_4_OPERATIONS_RECOVERY_VALIDATION.md`
- `docs/staging/PHASE8_4_OPERATIONS_RECOVERY_EVIDENCE.template.json`

Required evidence includes service recovery, PostgreSQL/object-storage/OpenSearch/Redis recovery, application rollback, migration recovery, IAM/secrets continuity, observability continuity, degraded dependencies, RTO/RPO observations and change/rollback references.

### Phase 8.5 — accountable staging acceptance

**Repository contract:** `COMPLETE`  
**External decision:** `REQUIRED`

Primary artifacts:

- Phase 8.5 accountable staging acceptance runbook/template/validator
- `docs/project/PRODUCTION_CHECKLIST.md`

Phase 8 may be marked `PASS / OWNER_ACCEPTED` only when accepted Phase 8.2–8.4 evidence is bound to one immutable staging identity, deviations/residual risks are recorded, no unresolved release-blocking staging finding remains and an accountable owner decision is recorded.

### Phase 9 — independent external assurance

**Status:** `NOT COMPLETE`.

Primary contract: `docs/qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md`.

Expected evidence includes independent penetration testing, hardening/configuration, IAM/secrets, load/stress, resilience/recovery, monitoring/incident response, relevant privacy/legal/governance review, assurance-time vulnerability review, finding triage, remediation/retest and residual-risk disposition.

### Phase 10 — production go/no-go

**Status:** `NOT STARTED`.

Required inputs are accepted Phase 8 and Phase 9 evidence plus production environment/ownership, IAM/secrets/network, backup/recovery/rollback, monitoring/on-call/escalation, privacy/data/legal, open-finding/residual-risk and formal release/change decisions.

## Governance evidence

Framework claims are governed by `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`. The current model includes explicit versioned/provenance-backed relationships and E8.10 vulnerability-management evidence mapping, including Normenkader IBP SM.07 and explicit semantic boundaries for CVSS, EPSS, KEV, MITRE ATT&CK, MISP and AIL.

A mapping is not a blanket compliance, maturity, certification, exposure or remediation claim.

## Evidence handling rules

- Evidence must be attributable, scoped and reviewable.
- Exact-head automated evidence belongs to the exact state tested.
- Deployment-bound evidence belongs to the deployment identity it actually covered.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Raw credentials/tokens and unnecessary personal data must not be stored in repository evidence.
- Human review/share approval remains separate from technical execution.
- Historical immutable run records are never rewritten to manufacture a later acceptance state.
