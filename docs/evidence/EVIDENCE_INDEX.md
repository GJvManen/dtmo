# DTMO Evidence Index

Last updated: **2026-08-16**

## Purpose

This index maps DTMO lifecycle stages to evidence classes and authoritative professional documentation. It is not a CI chronology or incident log. Exact workflow/job/commit history remains under `docs/development/`, GitHub issues/pull requests and CI artifacts.

**Current lifecycle:** Phase 8 is `PASS / OWNER_ACCEPTED`; Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`; Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1–11.2 Taranis and Phase 11.3 IntelOwl are `PASS / REPOSITORY_COMPLETE`; Phase 11.4 OpenCTI contract is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`; Phase 12 is `NOT STARTED`. DTMO is not production authorized.

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
- `docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md`
- `docs/integrations/OPENCTI_INTEGRATION.md`
- `docs/operations/OPENCTI_INTEGRATION_RUNBOOK.md`
- `docs/qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md`
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
4. **Independent assurance evidence** — external security/resilience/operational assessment independent from repository CI or self-attestation.
5. **Formal production authorization** — accountable go/no-go decision for a specific candidate.
6. **Platform-integration evidence** — service contract, adapter, migration, trust-boundary, runtime and interoperability evidence for the Phase 11 composed platform; this does not become production authorization by itself.

## Lifecycle evidence map

### Phases 1–7

**Status:** `PASS`.

### RC13

**Status:** `PASS / OWNER_ACCEPTED`.

### E8.1–E8.10

**Status:** `PASS / REPOSITORY_COMPLETE`.

### Phase 8

**Status:** `PASS / OWNER_ACCEPTED` for the earlier candidate.

### Phase 9

**Status:** `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate.

### Phase 10

**Status:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.

Production authorization was not granted. The accountable decision remains in `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`.

### Phase 11.1–11.2 Taranis

**Status:** `PASS / REPOSITORY_COMPLETE`.

Evidence covers the Taranis service contract and canonical read adapter, durable pagination/checkpointing/reconciliation, detail/CTI retrieval, governed execution, canonical persistence/indexing and observability. It is repository evidence, not live production evidence.

### Phase 11.3 IntelOwl

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers the IntelOwl service/API/licensing contract, bounded analyzer adapter, runtime-secret/HTTPS/allowlist configuration, privacy/TLP fail-closed behavior, bounded polling/result validation, immutable job identity, partial-success semantics, human-authorized execution and durable enrichment history with explicit no-share/no-local-compromise authority markers.

The dedicated repository contract workflow remains `.github/workflows/phase11-intelowl-integration-contract.yml`. Its accepted exact-head results are repository-controlled engineering evidence only; they are not live-service, production-equivalent, independent-assurance or production-authorization evidence.

This does not prove live IntelOwl connectivity, deployed credentials, analyzer quality, privacy approval, production-equivalent behavior, independent assurance or production authorization.

### Phase 11.4 OpenCTI contract

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

The active repository evidence target covers:

- reviewed OpenCTI `7.260811.0` compatibility baseline;
- Community Edition Apache-2.0 and separate Enterprise Edition licensing distinction;
- separate service/API boundary with no OpenCTI source vendoring;
- GraphQL, STIX 2.1, TAXII 2.1 and access-controlled stream boundaries;
- dedicated least-privilege service identity and runtime-secret handling;
- explicit OpenCTI/STIX ↔ DTMO canonical identity mapping;
- marking/TLP/PAP, confidence and provenance preservation;
- fail-closed authorization/marking/STIX semantics;
- bounded, durable and idempotent pagination/stream replay requirements;
- exclusion of connector registration, MISP synchronization, enrichment, case creation and publication side effects;
- preservation of DTMO human publication/share authority and no-local-compromise semantics;
- synchronized architecture, integration, security, operations, QA, roadmap, README/docs portal and evidence documentation.

The exact acceptance definition is `docs/qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md`; the dedicated repository workflow is `.github/workflows/phase11-opencti-integration-contract.yml`.

This contract evidence does **not** prove live OpenCTI connectivity, deployed credentials or effective marking segregation, real STIX interoperability, graph quality/performance, privacy/data-processing approval, production HA/recovery, independent assurance or production authorization.

After protected acceptance, the next repository evidence class is the bounded read-only OpenCTI STIX/identity adapter with pagination/reconciliation and provenance preservation.

### Phase 11.5–11.9

Future evidence covers MISP consolidation, TheHive handoff, conditional Cortex disposition, integrated Kubernetes/Helm/GitOps runtime hardening and migration/compatibility in the fixed roadmap order.

### Phase 11.10–11.11

The materially changed integrated candidate requires fresh production-equivalent validation and fresh independent external assurance bound to the same immutable deployment identity. Historical Phase 8/9 evidence cannot satisfy these gates by itself.

### Phase 12

**Status:** `NOT STARTED`.

Phase 12 can start only after required Phase 11 validation/assurance is accepted. A `GO` must be explicitly accountable and bound to one immutable production release identity.

## Evidence transfer rule

Historical Phase 8 and Phase 9 acceptance is retained but candidate-bound. It cannot be automatically transferred to the materially changed Phase 11 integrated platform.

## Governance evidence

Framework claims are governed by `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`. A mapping is not a blanket compliance, maturity, certification, exposure or remediation claim. IntelOwl outputs and OpenCTI graph relationships are contextual evidence and do not establish local exploitability or compromise without separate attributable local evidence.

## Evidence handling rules

- Evidence must be attributable, scoped and reviewable.
- Exact-head automated evidence belongs to the exact state tested.
- Deployment-bound evidence belongs to the deployment identity it covered.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Raw credentials/tokens and unnecessary personal data must not be stored in repository evidence.
- Human review/share approval remains separate from technical execution and production authorization.
- OpenCTI graph confidence/relationships cannot silently become DTMO local-compromise or publication-authority claims.
- Historical immutable run records are never rewritten to manufacture a later acceptance state.
