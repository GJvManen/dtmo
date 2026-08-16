# DTMO Evidence Index

Last updated: **2026-08-16**

## Purpose

This index maps lifecycle stages to evidence classes and authoritative professional documentation. It is not a CI chronology. Exact run/commit/job history remains in immutable operational records, pull requests and CI artifacts.

**Current lifecycle:** Phase 8 is `PASS / OWNER_ACCEPTED`; Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`; Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1–11.2 Taranis and Phase 11.3 IntelOwl are `PASS / REPOSITORY_COMPLETE`; the Phase 11.4 OpenCTI contract and read-only adapter are `PASS / REPOSITORY_COMPLETE`; Phase 11.4 canonical mapping/persistence is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`; Phase 12 is `NOT STARTED`. DTMO is not production authorized.

## Authoritative current-state sources

- `README.md`
- `docs/README.md`
- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`
- `docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md`
- `docs/integrations/OPENCTI_INTEGRATION.md`
- `docs/operations/OPENCTI_INTEGRATION_RUNBOOK.md`
- `docs/qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md`
- `backend/tests/test_phase11_4_opencti_adapter.py`
- `backend/tests/test_phase11_4_opencti_persistence.py`
- `database/migrations/versions/0012_opencti_mapping_persistence.py`
- `docs/roadmap/PRODUCTION_ROADMAP.md`
- `docs/project/PRODUCTION_READINESS_REPORT.md`
- `docs/project/PRODUCTION_CHECKLIST.md`
- `docs/project/EXECUTIVE_STATUS.md`
- `docs/project/DOCUMENTATION_STATUS.md`
- `docs/qa/QA_AND_RELEASE_GATES.md`
- `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`

## Evidence hierarchy

1. **Repository-controlled engineering evidence** — exact-head CI, contracts, migrations and synthetic integration tests.
2. **Accountable functional evidence** — explicit owner acceptance of product behavior.
3. **Real-environment evidence** — production-equivalent validation bound to an immutable deployment identity.
4. **Independent assurance evidence** — external assessment independent from repository CI.
5. **Formal production authorization** — accountable GO/NO-GO for a specific candidate.
6. **Platform-integration evidence** — service contracts, adapters, mappings, migrations and interoperability evidence; never production authorization by itself.

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

### Phase 11.1–11.2 Taranis

**Status:** `PASS / REPOSITORY_COMPLETE`.

### Phase 11.3 IntelOwl

**Status:** `PASS / REPOSITORY_COMPLETE`.

The dedicated repository workflow remains `.github/workflows/phase11-intelowl-integration-contract.yml`. Its results are repository engineering evidence only.

### Phase 11.4 OpenCTI contract

**Status:** `PASS / REPOSITORY_COMPLETE`.

The accepted contract covers OpenCTI `7.260811.0`, licensing separation, service/API boundaries, STIX/TAXII/GraphQL semantics, least privilege, provenance/marking preservation and excluded side effects. The dedicated workflow remains `.github/workflows/phase11-opencti-integration-contract.yml`.

### Phase 11.4 OpenCTI read-only adapter

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers bounded GraphQL `stixCoreObjects` reads, stable OpenCTI/STIX identity preservation, entity allowlists, markings/confidence/external references, fail-closed malformed state, durable cursor loading and explicit post-persistence `commit_page(page)` semantics.

### Phase 11.4 OpenCTI canonical mapping/persistence

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

The active repository evidence target covers:

- `backend/dtmo/persistence/opencti.py` canonical mapping and reconciliation logic;
- `opencti_object_mappings` current attributed state;
- `opencti_mapping_revisions` immutable snapshot history;
- SHA-256 canonical snapshot hashes for replay idempotency;
- fail-closed OpenCTI-internal-ID/STIX-ID drift and ambiguous identity mapping;
- preserved entity type, parent types, markings, confidence, timestamps, external references and provenance;
- database-enforced `external_share_authorized=false` and `local_compromise_proven=false`;
- migration `0012_opencti_mapping_persistence` following `0011_intelowl_enrichment_history`;
- persistence coordinator ordering: PostgreSQL commit before checkpoint advance;
- no checkpoint advance when database commit fails;
- safe replay when database commit succeeds but checkpoint replacement fails;
- tests in `backend/tests/test_phase11_4_opencti_persistence.py`.

This evidence does **not** prove live OpenCTI connectivity, deployed service identity or marking segregation, production STIX interoperability, graph quality/performance, privacy approval, HA/recovery, independent assurance or production authorization.

### Phase 11.5–11.9

Future evidence covers MISP consolidation, TheHive handoff, conditional Cortex disposition, Kubernetes/Helm/GitOps runtime hardening and migration/compatibility in fixed order.

### Phase 11.10–11.11

Fresh production-equivalent validation and fresh independent assurance must target the same immutable integrated candidate. Historical Phase 8/9 evidence cannot satisfy these gates.

### Phase 12

**Status:** `NOT STARTED`.

## Evidence transfer rule

Historical Phase 8/9 acceptance remains candidate-bound and cannot be transferred automatically to the materially changed Phase 11 platform.

## Governance and handling rules

Framework claims remain governed by explicit provenance-backed mappings. IntelOwl outputs and OpenCTI graph context do not establish local exploitability, compromise or dissemination authority without separate attributable evidence.

- Exact-head evidence belongs only to the exact state tested.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Credentials/tokens and unnecessary personal data do not belong in repository evidence.
- Human review/share approval remains separate from technical execution.
- Historical immutable run records are never rewritten to manufacture later acceptance.
