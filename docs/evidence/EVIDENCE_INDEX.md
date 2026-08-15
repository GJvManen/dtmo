# DTMO Evidence Index

Last updated: **2026-08-15**

## Purpose

This index maps DTMO lifecycle stages to their evidence classes and authoritative professional documentation. It is not a CI chronology or incident log. Exact workflow/job/commit history remains under `docs/development/`, GitHub issues/pull requests and CI artifacts.

**Current lifecycle:** Phase 8 is `PASS / OWNER_ACCEPTED`; Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`; Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11 is `IN PROGRESS / ACTIVE`; Phase 12 is `NOT STARTED`. DTMO is not production authorized.

## Authoritative current-state sources

- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`
- `docs/architecture/TARANIS_PLATFORM_INTEGRATION_ASSESSMENT.md`
- `docs/architecture/TARANIS_DTMO_INTEGRATION_CONTRACT.md`
- `docs/integrations/TARANIS_ADAPTER.md`
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

1. **Repository-controlled engineering evidence** — exact-head CI, contracts, browser tests and repository recovery/performance/observability evidence.
2. **Accountable functional evidence** — explicit project-owner acceptance of product behavior.
3. **Real-environment evidence** — production-equivalent staging deployment/validation tied to its accepted identity.
4. **Independent assurance evidence** — external security/resilience/operational assessment independent from repository CI or project self-attestation.
5. **Formal production authorization** — accountable go/no-go decision for a specific candidate.
6. **Platform-integration evidence** — service contract, migration, trust-boundary, runtime and interoperability evidence for the Phase 11 composed platform; this does not become production authorization by itself.

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

Accepted historical evidence remains attributable to the prior candidate. Repository CI, Docker Compose and staging emulators remain supporting engineering evidence and are not represented as the source of external Phase 8 acceptance.

### Phase 9 — independent external assurance

**Status:** `PASS / EXTERNAL_ASSURANCE_ACCEPTED`.

Accepted historical assurance remains a distinct evidence class for the prior candidate. Repository CI or owner self-attestation cannot substitute for it.

### Phase 10 — production go/no-go

**Status:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.

Production authorization was not granted. The accountable decision is recorded in `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`.

### Phase 11 — platform industrialisation

**Status:** `IN PROGRESS / ACTIVE`.

Phase 11.1 Taranis architecture/contract work is repository-complete. Phase 11.2 now has repository evidence for the read-only canonical adapter, fail-closed handling, stable identity, deterministic replay, durable atomic checkpointing, bounded pagination/reconciliation, bounded detail/CTI retrieval and governed connector execution. This evidence is repository-controlled only and does not prove live Taranis permissions, persistent-volume deployment or production-equivalent behavior.

Required evidence classes progressively include:

- Taranis API/data-model/identity/licensing assessment;
- service-to-service adapter contracts and interoperability tests;
- provenance/classification/replay/deduplication evidence;
- Taranis detail/CTI and governed scheduler/manual execution evidence;
- IntelOwl enrichment contract/runtime evidence;
- OpenCTI STIX/entity/relationship interoperability evidence;
- consolidated MISP authority/synchronization evidence;
- TheHive handoff evidence and conditional Cortex decision evidence;
- Kubernetes/Helm/GitOps runtime, secrets, identity, network, HA/recovery, observability and supply-chain evidence;
- migration/compatibility and rollback evidence;
- a new production-equivalent validation package bound to one immutable integrated deployment identity;
- a new independent external assurance package for that same integrated candidate.

Primary Phase 11 documents:

- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`;
- `docs/architecture/TARANIS_PLATFORM_INTEGRATION_ASSESSMENT.md`;
- `docs/architecture/TARANIS_DTMO_INTEGRATION_CONTRACT.md`;
- `docs/integrations/TARANIS_ADAPTER.md`.

### Phase 12 — production go/no-go

**Status:** `NOT STARTED`.

Phase 12 can start only after Phase 11 production-equivalent validation and independent external assurance are accepted for the integrated candidate. A Phase 12 `GO` must be explicitly accountable and bound to one immutable production release identity.

## Evidence transfer rule

Historical Phase 8 and Phase 9 acceptance is not discarded. However, it is candidate-bound and cannot be automatically transferred to the materially changed Phase 11 integrated platform. Any material component, trust-boundary or deployment change requires explicit impact assessment and appropriate revalidation.

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