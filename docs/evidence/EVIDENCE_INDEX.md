# DTMO Evidence Index

Last updated: **2026-08-16**

## Purpose

This index maps lifecycle stages to evidence classes and authoritative professional documentation. It is not a CI chronology. Exact run/commit/job history remains in immutable operational records, pull requests and CI artifacts.

**Current lifecycle:** Phase 8 is `PASS / OWNER_ACCEPTED`; Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`; Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1–11.2 Taranis, Phase 11.3 IntelOwl and Phase 11.4 OpenCTI are `PASS / REPOSITORY_COMPLETE`; Phase 11.5 MISP consolidation is `IN PROGRESS / CONTRACT EXACT-HEAD VALIDATION REQUIRED`; Phase 12 is `NOT STARTED`. DTMO is not production authorized.

## Authoritative current-state sources

- `README.md`
- `docs/README.md`
- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`
- `docs/architecture/MISP_DTMO_CONSOLIDATION_CONTRACT.md`
- `docs/integrations/MISP_READ_INTEGRATION.md`
- `docs/intelligence/MISP_GOVERNED_EXPORT.md`
- `docs/qa/PHASE11_5_MISP_CONSOLIDATION_CONTRACT_GATE.md`
- `backend/tests/test_phase11_5_misp_consolidation_contract.py`
- `.github/workflows/phase11-misp-consolidation-contract.yml`
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

Accepted repository evidence covers the OpenCTI service/API/licensing contract, bounded GraphQL/STIX adapter, stable identity/marking/provenance preservation, canonical mapping/revision persistence, database-enforced no-share/no-local-compromise invariants and PostgreSQL-before-checkpoint ordering. The dedicated workflow remains `.github/workflows/phase11-opencti-integration-contract.yml`.

This evidence does **not** prove live OpenCTI connectivity, deployed service identity or marking segregation, production STIX interoperability, graph quality/performance, privacy approval, HA/recovery, independent assurance or production authorization.

### Phase 11.5 MISP consolidation contract

**Status:** `IN PROGRESS / CONTRACT EXACT-HEAD VALIDATION REQUIRED`.

The active repository evidence target covers:

- reviewed upstream baseline **MISP v2.5.44**;
- separate **AGPL-3.0** service/API boundary with no MISP core source vendoring;
- consolidation of existing inbound `POST /events/restSearch` and governed outbound `POST /events/add` paths rather than duplication;
- preservation of event/attribute/object UUID identity, distribution, sharing-group, TLP/tag and provenance context;
- DTMO canonical UUID identity remaining separate from MISP identities;
- import never granting `share_approved`, publication authority or local-compromise proof;
- human DTMO review/share approval remaining mandatory for outbound delivery;
- service accounts, collectors, schedulers, IntelOwl, OpenCTI and MISP not gaining DTMO sharing authority;
- source restrictions not being broadened on re-export;
- unpublished destination events, deterministic replay reservations and fail-closed uncertain-delivery handling;
- automatic MISP server push/pull synchronization and OpenCTI↔MISP synchronization excluded from this first boundary;
- runtime-secret, production HTTPS and least-privilege requirements;
- tests in `backend/tests/test_phase11_5_misp_consolidation_contract.py` and workflow `.github/workflows/phase11-misp-consolidation-contract.yml`.

Repository contract evidence does **not** prove live MISP credentials, effective production roles, remote-server trust, lawful live-data sharing, production federation behavior, staging acceptance, independent assurance or production authorization.

### Phase 11.5 next implementation slice

Only after protected acceptance of the contract may DTMO implement the single reconciled MISP synchronization-state/persistence and authority-enforcement model. Phase 11.6 remains blocked until Phase 11.5 is repository-complete.

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
