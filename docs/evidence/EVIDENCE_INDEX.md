# DTMO Evidence Index

Last updated: **2026-08-16**

## Purpose

This index maps DTMO lifecycle stages to their evidence classes and authoritative professional documentation. It is not a CI chronology or incident log. Exact workflow/job/commit history remains under `docs/development/`, GitHub issues/pull requests and CI artifacts.

**Current lifecycle:** Phase 8 is `PASS / OWNER_ACCEPTED`; Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`; Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1 and 11.2 are `PASS / REPOSITORY_COMPLETE`; the Phase 11.3 IntelOwl contract and bounded adapter are `PASS / REPOSITORY_COMPLETE`; Phase 11.3 governed execution/persistence is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`; Phase 12 is `NOT STARTED`. DTMO is not production authorized.

## Authoritative current-state sources

- `README.md`
- `docs/README.md`
- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`
- `docs/architecture/TARANIS_PLATFORM_INTEGRATION_ASSESSMENT.md`
- `docs/architecture/TARANIS_DTMO_INTEGRATION_CONTRACT.md`
- `docs/integrations/TARANIS_ADAPTER.md`
- `docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md`
- `docs/integrations/INTELOWL_INTEGRATION.md`
- `docs/user/INTELOWL_ENRICHMENT_WORKFLOW.md`
- `docs/operations/INTELOWL_ENRICHMENT_RUNBOOK.md`
- `docs/qa/PHASE11_3_INTELOWL_GOVERNED_EXECUTION_GATE.md`
- `docs/roadmap/PRODUCTION_ROADMAP.md`
- `docs/project/PRODUCTION_READINESS_REPORT.md`
- `docs/project/PRODUCTION_CHECKLIST.md`
- `docs/project/EXECUTIVE_STATUS.md`
- `docs/project/DOCUMENTATION_STATUS.md`
- `docs/qa/QA_AND_RELEASE_GATES.md`
- `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`
- `docs/traceability/TRACEABILITY_MATRIX.md`

## Evidence hierarchy

DTMO distinguishes six non-interchangeable evidence classes:

1. **Repository-controlled engineering evidence** — exact-head CI, contracts, synthetic integration tests and repository recovery/performance/observability evidence.
2. **Accountable functional evidence** — explicit project-owner acceptance of product behavior.
3. **Real-environment evidence** — production-equivalent staging deployment/validation tied to its accepted identity.
4. **Independent assurance evidence** — external security/resilience/operational assessment independent from repository CI or project self-attestation.
5. **Formal production authorization** — accountable go/no-go decision for a specific candidate.
6. **Platform-integration evidence** — service contract, adapter, migration, trust-boundary, runtime and interoperability evidence for the Phase 11 composed platform; this does not become production authorization by itself.

## Lifecycle evidence map

### Phases 1–7 — engineering baseline

**Status:** `PASS`.

### RC13 — functional product acceptance

**Status:** `PASS / OWNER_ACCEPTED`.

### E8.1–E8.10 — vulnerability and CTI evolution

**Status:** `PASS / REPOSITORY_COMPLETE`.

### Phase 8 — production-equivalent staging acceptance

**Status:** `PASS / OWNER_ACCEPTED`.

Accepted historical evidence remains attributable to the prior candidate. Repository CI, Docker Compose and staging emulators are not represented as the source of accountable Phase 8 acceptance.

### Phase 9 — independent external assurance

**Status:** `PASS / EXTERNAL_ASSURANCE_ACCEPTED`.

Accepted historical assurance remains a distinct evidence class for the prior candidate. Repository CI or owner self-attestation cannot substitute for it.

### Phase 10 — production go/no-go

**Status:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.

Production authorization was not granted. The accountable decision is recorded in `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`.

### Phase 11 — platform industrialisation

**Status:** `IN PROGRESS / ACTIVE`.

Phase 11.1 Taranis architecture/contract and Phase 11.2 Taranis→DTMO canonical adapter are repository-complete. Their evidence remains repository-controlled integration evidence rather than proof of live production behavior.

#### Phase 11.3 IntelOwl contract

**Status:** `PASS / REPOSITORY_COMPLETE`.

`docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md` is the accepted v6.7-compatible service/API/security/licensing baseline. The exact-head contract gate is `.github/workflows/phase11-intelowl-integration-contract.yml`. Acceptance proves contract/test synchronization only; it does not prove live IntelOwl connectivity, deployed identity or provider credentials.

#### Phase 11.3 IntelOwl adapter

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers runtime-secret IntelOwl API token configuration, production HTTPS and explicit analyzer allowlisting, approved observable classes, fail-closed privacy/TLP checks, `connectors_requested=[]`, bounded submission/polling, immutable job identity, result-size bounds, unknown-analyzer rejection, partial-success semantics and explicit no-share/no-compromise authority markers.

Adapter acceptance does not prove live connectivity, provider credentials, analyzer quality, privacy approval, production-equivalent behavior, independent assurance or production authorization.

#### Phase 11.3 governed execution/persistence

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

The active repository evidence target covers:

- a human-authorized `POST /api/v1/intelowl/items/{item_id}/enrich` boundary requiring `REVIEW_INTELLIGENCE`;
- no autonomous service-account execution through that endpoint under the current RBAC model;
- conservative treatment of every requested analyzer as an external service disclosure boundary, causing restricted handling to fail closed before network disclosure;
- migration `0011_intelowl_enrichment_history` and durable `intelowl_enrichment_records` linked to canonical intelligence;
- immutable `(item_id, job_id)` uniqueness and idempotent replay persistence;
- preserved observable/handling decision inputs, analyzer identities, requesting human subject, terminal/partial status and raw normalized result;
- database-enforced `external_share_authorized=false` and `local_compromise_proven=false`;
- `GET /api/v1/intelowl/items/{item_id}/history` as a read-only contextual evidence surface requiring `READ_INTELLIGENCE`;
- operations, user and QA documentation synchronized to the implementation.

The exact acceptance definition is `docs/qa/PHASE11_3_INTELOWL_GOVERNED_EXECUTION_GATE.md`.

This evidence does **not** prove live IntelOwl connectivity, provider credentials, analyzer quality, privacy/data-processing approval, production-equivalent PostgreSQL durability/recovery, deployed network trust, independent assurance or production authorization. No historical Phase 8/9 evidence is transferred to this materially changed candidate.

OpenCTI evidence does not begin until Phase 11.3 is repository-complete.

Required Phase 11 evidence subsequently includes OpenCTI interoperability, MISP consolidation, TheHive handoff, conditional Cortex disposition, Kubernetes/Helm/GitOps runtime hardening, migration/compatibility, a new production-equivalent validation package bound to one immutable integrated identity and a new independent external-assurance package for that same candidate.

### Phase 12 — production go/no-go

**Status:** `NOT STARTED`.

Phase 12 can start only after Phase 11 production-equivalent validation and independent external assurance are accepted for the integrated candidate. A Phase 12 `GO` must be explicitly accountable and bound to one immutable production release identity.

## Evidence transfer rule

Historical Phase 8 and Phase 9 acceptance is not discarded. It is candidate-bound and cannot be automatically transferred to the materially changed Phase 11 integrated platform. Material component, trust-boundary or deployment changes require explicit impact assessment and appropriate revalidation.

## Governance evidence

Framework claims are governed by `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`. A mapping is not a blanket compliance, maturity, certification, exposure or remediation claim. IntelOwl analyzer outputs are likewise contextual enrichment evidence and do not establish local exploitability or compromise without separate attributable local evidence.

## Evidence handling rules

- Evidence must be attributable, scoped and reviewable.
- Exact-head automated evidence belongs to the exact state tested.
- Deployment-bound evidence belongs to the deployment identity it covered.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Raw credentials/tokens and unnecessary personal data must not be stored in repository evidence.
- Human review/share approval remains separate from technical execution and production authorization.
- IntelOwl provider/analyzer verdicts remain attributed context and cannot silently become DTMO local-compromise claims.
- Durable IntelOwl history may not be edited to manufacture a later or stronger authority state.
- Historical immutable run records are never rewritten to manufacture a later acceptance state.
