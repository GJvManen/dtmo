# DTMO Evidence Index

Last updated: **2026-08-15**

## Purpose

This index maps DTMO lifecycle stages to their evidence classes and authoritative professional documentation. It is not a CI chronology or incident log. Exact workflow/job/commit history remains under `docs/development/`, GitHub issues/pull requests and CI artifacts.

**Production readiness:** Phase 8 is `PASS / OWNER_ACCEPTED`; Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`; Phase 10 is `IN PROGRESS / DECISION REQUIRED`. DTMO is not production authorized until an accountable Phase 10 `GO` is recorded.

## Authoritative current-state sources

- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PRODUCTION_ROADMAP.md`
- `docs/project/PRODUCTION_READINESS_REPORT.md`
- `docs/project/PRODUCTION_CHECKLIST.md`
- `docs/project/EXECUTIVE_STATUS.md`
- `docs/project/DOCUMENTATION_STATUS.md`
- `docs/qa/QA_AND_RELEASE_GATES.md`
- `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`
- `docs/traceability/TRACEABILITY_MATRIX.md`

## Evidence hierarchy

DTMO distinguishes five non-interchangeable evidence classes:

1. **Repository-controlled engineering evidence** — exact-head CI, contracts, browser tests and repository recovery/performance/observability evidence.
2. **Accountable functional evidence** — explicit project-owner acceptance of product behavior.
3. **Real-environment evidence** — production-equivalent staging deployment/validation tied to its accepted identity.
4. **Independent assurance evidence** — external security/resilience/operational assessment independent from repository CI or project self-attestation.
5. **Formal production authorization** — accountable Phase 10 go/no-go decision.

## Lifecycle evidence map

### Phases 1–7 — engineering baseline

**Status:** `PASS`.

### RC13 — functional product acceptance

**Status:** `PASS / OWNER_ACCEPTED`.

### E8.1–E8.10 — vulnerability and CTI evolution

**Status:** `PASS / REPOSITORY_COMPLETE`.

Repository evidence covers OpenCVE, Vulnerability-Lookup, vulnerability prioritization, vendor/product relevance, vulnerability analytics, governed MISP read/export, governed AIL read/enrichment/correlation and vulnerability-management governance evidence mapping. Repository completion does not create external sharing authority or production authorization.

### Phase 8 — production-equivalent staging acceptance

**Status:** `PASS / OWNER_ACCEPTED`.

The accountable owner reports Phase 8.2 platform/identity, Phase 8.3 source-to-intelligence, Phase 8.4 operations/recovery/rollback and Phase 8.5 accountable staging acceptance complete. Detailed sensitive staging evidence may remain in approved restricted evidence storage and be referenced rather than reproduced here.

Repository CI, Docker Compose and staging emulators remain supporting engineering evidence and are not represented as the source of external Phase 8 acceptance.

### Phase 9 — independent external assurance

**Status:** `PASS / EXTERNAL_ASSURANCE_ACCEPTED`.

Independent assurance is reported complete and accepted. The detailed independent evidence package remains a distinct evidence class; repository CI or owner self-attestation cannot substitute for it. Relevant restricted penetration-test, hardening, IAM/secrets, resilience, load, monitoring/IR, privacy/legal and dependency/CVE details should remain under approved evidence handling.

### Phase 10 — production go/no-go

**Status:** `IN PROGRESS / DECISION REQUIRED`.

Required production decision evidence includes:

- accepted Phase 8 and Phase 9 evidence references;
- production environment, accountable owner and support model approval;
- immutable production release identity and image digests;
- IAM/service identities, secrets-management and network approval;
- backup/restore/recovery/rollback approval;
- monitoring/alerting/on-call/escalation and incident-response handover;
- privacy/data/legal/governance approval;
- open-finding statement and accountable residual-risk disposition;
- production release/change authorization;
- go-live window and rollback authority;
- final accountable `GO` or `NO-GO / BLOCKED` decision.

Primary decision record: `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`.

## Governance evidence

Framework claims are governed by `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`. The current model includes explicit versioned/provenance-backed relationships and E8.10 vulnerability-management evidence mapping, including Normenkader IBP SM.07 and semantic boundaries for CVSS, EPSS, KEV, MITRE ATT&CK, MISP and AIL.

A mapping is not a blanket compliance, maturity, certification, exposure or remediation claim.

## Evidence handling rules

- Evidence must be attributable, scoped and reviewable.
- Exact-head automated evidence belongs to the exact state tested.
- Deployment-bound evidence belongs to the deployment identity it actually covered.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Raw credentials/tokens and unnecessary personal data must not be stored in repository evidence.
- Human review/share approval remains separate from technical execution and production authorization.
- Historical immutable run records are never rewritten to manufacture a later acceptance state.