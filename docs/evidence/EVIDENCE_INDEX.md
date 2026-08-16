# DTMO Evidence Index

Last updated: **2026-08-17**

## Purpose

This index maps lifecycle stages to evidence classes and authoritative professional documentation. It is not a CI chronology. Exact run/commit/job history remains in immutable operational records, pull requests and CI artifacts.

**Current lifecycle:** Phase 8 is `PASS / OWNER_ACCEPTED`; Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`; Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1–11.2 Taranis, Phase 11.3 IntelOwl and Phase 11.4 OpenCTI are `PASS / REPOSITORY_COMPLETE`; the Phase 11.5 MISP consolidation contract is `PASS / REPOSITORY_COMPLETE`; Phase 11.5 synchronization-state/persistence is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`; Phase 12 is `NOT STARTED`. DTMO is not production authorized.

## Authoritative current-state sources

- `README.md`
- `docs/README.md`
- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`
- `docs/architecture/MISP_DTMO_CONSOLIDATION_CONTRACT.md`
- `docs/integrations/MISP_READ_INTEGRATION.md`
- `docs/intelligence/MISP_GOVERNED_EXPORT.md`
- `docs/qa/PHASE11_5_MISP_CONSOLIDATION_CONTRACT_GATE.md`
- `docs/qa/PHASE11_5_MISP_CONSOLIDATION_STATE_GATE.md`
- `backend/tests/test_phase11_5_misp_consolidation_contract.py`
- `backend/tests/test_phase11_5_misp_consolidation_state.py`
- `.github/workflows/phase11-misp-consolidation-contract.yml`
- `.github/workflows/phase11-misp-consolidation-state.yml`
- `docs/security/SECURITY_OVERVIEW.md`
- `docs/qa/QA_AND_RELEASE_GATES.md`
- `docs/roadmap/PRODUCTION_ROADMAP.md`
- `docs/project/PRODUCTION_READINESS_REPORT.md`
- `docs/project/PRODUCTION_CHECKLIST.md`
- `docs/project/EXECUTIVE_STATUS.md`
- `docs/project/DOCUMENTATION_STATUS.md`
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

### Phase 11.4 OpenCTI

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers the OpenCTI service/API/licensing contract, bounded GraphQL/STIX adapter, stable identity/marking/provenance preservation, canonical mapping/revision persistence, database-enforced no-share/no-local-compromise invariants and PostgreSQL-before-checkpoint ordering. The accepted persistence contract is exercised by `backend/tests/test_phase11_4_opencti_persistence.py`, and the dedicated workflow remains `.github/workflows/phase11-opencti-integration-contract.yml`.

This evidence does **not** prove live OpenCTI connectivity, deployed service identity or marking segregation, production STIX interoperability, graph quality/performance, privacy approval, HA/recovery, independent assurance or production authorization.

### Phase 11.5 MISP consolidation contract

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers MISP v2.5.44, the separate AGPL-3.0 service/API boundary, one authority model spanning existing `events/restSearch` and human-approved unpublished `events/add` paths, preservation of UUID/distribution/sharing-group/TLP/provenance restrictions, no source vendoring, no implicit share authority, no automatic federation and no automatic OpenCTI↔MISP synchronization.

The accepted contract test/workflow remain `backend/tests/test_phase11_5_misp_consolidation_contract.py` and `.github/workflows/phase11-misp-consolidation-contract.yml`.

### Phase 11.5 MISP synchronization-state implementation

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

The active repository evidence target covers:

- durable `misp_synchronization_state` binding one DTMO canonical item to one stable MISP event UUID;
- event UUID identity remaining distinct from DTMO canonical identity;
- authoritative distribution, sharing-group and normalized TLP restrictions persisted with an attributable snapshot/hash;
- accepted source restrictions projected to canonical `metadata_json.misp_restrictions`, consumed by the existing governed export path;
- canonical MISP candidate persistence and state reconciliation occurring inside the same database transaction;
- failure on event UUID collision, DTMO-item identity drift, unknown distribution, missing sharing group for distribution `4`, malformed/non-authoritative restriction state or attempted inbound external-share authority;
- database-enforced `external_share_authorized=false` and sharing/distribution constraints;
- migration `0013_misp_synchronization_state` after `0012_opencti_mapping_persistence`, including upgrade/downgrade validation;
- existing MISP read/export gates staying green;
- tests in `backend/tests/test_phase11_5_misp_consolidation_state.py` and workflow `.github/workflows/phase11-misp-consolidation-state.yml`;
- professional lifecycle, security, integration, QA and evidence documentation synchronized to the same exact head.

Repository implementation evidence does **not** prove live MISP credentials, effective production roles, remote-server trust, lawful live-data sharing, production federation behavior, production-equivalent validation, independent assurance or production authorization.

Phase 11.6 remains blocked until this implementation is protected-merged and Phase 11.5 is reconciled to `PASS / REPOSITORY_COMPLETE`.

### Phase 11.6–11.9

Future evidence covers TheHive handoff, conditional Cortex disposition, Kubernetes/Helm/GitOps runtime hardening and migration/compatibility in fixed order.

### Phase 11.10–11.11

Fresh production-equivalent validation and fresh independent assurance must target the same immutable integrated candidate. Historical Phase 8/9 evidence cannot satisfy these gates.

### Phase 12

**Status:** `NOT STARTED`.

## Evidence transfer rule

Historical Phase 8/9 acceptance remains candidate-bound and cannot be transferred automatically to the materially changed Phase 11 platform.

## Governance and handling rules

Framework claims remain governed by explicit provenance-backed mappings. IntelOwl outputs, OpenCTI graph context and MISP event presence do not establish local exploitability, compromise or dissemination authority without separate attributable evidence.

- Exact-head evidence belongs only to the exact state tested.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Credentials/tokens and unnecessary personal data do not belong in repository evidence.
- Human review/share approval remains separate from technical execution.
- Historical immutable run records are never rewritten to manufacture later acceptance.
