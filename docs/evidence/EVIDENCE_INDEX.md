# DTMO Evidence Index

Last updated: **2026-08-17**

## Purpose

This index maps lifecycle stages to evidence classes and authoritative professional documentation. It is not a CI chronology. Exact run/commit/job history remains in immutable operational records, pull requests and CI artifacts.

**Current lifecycle:** Phase 8 is `PASS / OWNER_ACCEPTED`; Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`; Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1–11.5 are `PASS / REPOSITORY_COMPLETE`; the Phase 11.6 TheHive contract is `PASS / REPOSITORY_COMPLETE`; the bounded Phase 11.6 TheHive handoff implementation is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`; Phase 12 is `NOT STARTED`. DTMO is not production authorized.

## Authoritative current-state sources

- `README.md`
- `docs/README.md`
- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`
- `docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md`
- `docs/integrations/THEHIVE_HANDOFF.md`
- `docs/operations/THEHIVE_HANDOFF_RUNBOOK.md`
- `docs/user/THEHIVE_CASE_HANDOFF.md`
- `docs/administration/THEHIVE_HANDOFF_CONFIGURATION.md`
- `docs/qa/PHASE11_6_THEHIVE_HANDOFF_CONTRACT_GATE.md`
- `docs/qa/PHASE11_6_THEHIVE_HANDOFF_IMPLEMENTATION_GATE.md`
- `backend/dtmo/integrations/thehive.py`
- `backend/dtmo/persistence/thehive.py`
- `backend/dtmo/thehive_handoff.py`
- `database/migrations/versions/0014_thehive_handoff_state.py`
- `backend/tests/test_thehive_handoff_contract.py`
- `backend/tests/test_phase11_6_thehive_handoff_adapter.py`
- `backend/tests/test_phase11_6_thehive_handoff_state.py`
- `.github/workflows/phase11-thehive-handoff-contract.yml`
- `.github/workflows/phase11-thehive-handoff-implementation.yml`
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

### Phase 11.1–11.5

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers Taranis, IntelOwl, OpenCTI and MISP service boundaries, identity/provenance preservation, durable reconciliation/state, fail-closed authority controls and human publication/share authority. These are repository engineering claims only.

### Phase 11.6 TheHive contract

**Status:** `PASS / REPOSITORY_COMPLETE`.

The accepted contract establishes TheHive 5.5.16/API v1, separate StrangeBee service/licensing boundary, dedicated human case-handoff authority distinct from publication/share authority, stable DTMO↔TheHive identity requirements, fail-closed TLP/PAP/access handling, data minimization and no-blind-replay semantics before runtime mutation code.

This remains repository engineering evidence only. It does not establish a live entitlement, tenant, credential, organization or production-ready integration.

### Phase 11.6 TheHive bounded handoff implementation

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

The active repository evidence target covers:

- the dedicated `handoff:case` permission and human/service identity separation;
- the only accepted external mutation being `POST /api/v1/case`;
- canonical item identity and repository provenance validation before handoff;
- deterministic severity/TLP/PAP mapping with unknown values failing closed;
- prevention of TLP broadening where authoritative TLP tags are known;
- fail-closed blocking when authoritative MISP distribution/sharing-group restrictions cannot yet be safely represented in the configured TheHive organization/access model;
- minimized payload fields and exclusion of attachments, raw source bodies, credentials, private enrichment and unrelated personal data;
- migration `0014_thehive_handoff_state` and durable PostgreSQL reservation before external mutation;
- unique request identity and unique confirmed TheHive case identity;
- `reserved`, `delivered`, `ambiguous` and `failed` state semantics;
- stable case identity being required for `delivered` status;
- timeout/network uncertainty or malformed success identity becoming `ambiguous` and blocking automatic replay;
- persisted upstream outcome being minimized to case identity, number and organization rather than arbitrary response content;
- database-enforced `external_share_authorized=false` and `local_compromise_proven=false` invariants;
- runtime feature being disabled by default and production configuration requiring HTTPS API base, secret token and explicit organization when enabled;
- synchronized architecture, integration, security, operations, user/admin, QA, evidence, roadmap and documentation-portal material.

The dedicated implementation tests/workflow are:

- `backend/tests/test_phase11_6_thehive_handoff_adapter.py`;
- `backend/tests/test_phase11_6_thehive_handoff_state.py`;
- `.github/workflows/phase11-thehive-handoff-implementation.yml`.

A green implementation gate does **not** prove live TheHive connectivity, deployed service-account permissions, activated license entitlement, organization/access configuration, privacy approval, correct TLP/PAP handling on real data, HA/recovery, production-equivalent validation, independent assurance or production authorization.

### Phase 11.7–11.9

Future evidence covers the conditional Cortex disposition, Kubernetes/Helm/GitOps runtime hardening and migration/compatibility in fixed order.

### Phase 11.10–11.11

Fresh production-equivalent validation and fresh independent assurance must target the same immutable integrated candidate. Historical Phase 8/9 evidence cannot satisfy these gates.

### Phase 12

**Status:** `NOT STARTED`.

## Evidence transfer rule

Historical Phase 8/9 acceptance remains candidate-bound and cannot be transferred automatically to the materially changed Phase 11 platform.

## Governance and handling rules

Framework claims remain governed by explicit provenance-backed mappings. External service state does not establish local exploitability, compromise, case necessity or dissemination authority without separate attributable evidence.

- Exact-head evidence belongs only to the exact state tested.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Credentials/tokens and unnecessary personal data do not belong in repository evidence.
- Human review/share approval and human case-handoff approval remain separate from technical execution.
- Historical immutable run records are never rewritten to manufacture later acceptance.
