# DTMO Evidence Index

Last updated: **2026-08-17**

## Purpose

This index maps lifecycle stages to evidence classes and authoritative professional documentation. It is not a CI chronology. Exact run/commit/job history remains in immutable operational records, pull requests and CI artifacts.

**Current lifecycle:** Phase 8 is `PASS / OWNER_ACCEPTED`; Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`; Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1–11.6 are `PASS / REPOSITORY_COMPLETE`; Phase 11.7 is an accepted historical Cortex decision baseline; Phase 11.7b Cortex analyzer connector is `IN PROGRESS / OWNER-REQUIRED EXACT-HEAD VALIDATION`; Phase 11.8 is blocked by 11.7b; Phase 12 is `NOT STARTED`. DTMO is not production authorized.

## Authoritative current-state sources

- `README.md`
- `docs/README.md`
- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`
- `docs/architecture/CORTEX_DECISION_GATE.md`
- `docs/architecture/CORTEX_DTMO_INTEGRATION_CONTRACT.md`
- `docs/integrations/CORTEX_ANALYZER_CONNECTOR.md`
- `docs/operations/CORTEX_ANALYZER_RUNBOOK.md`
- `docs/qa/PHASE11_7B_CORTEX_CONNECTOR_GATE.md`
- `backend/dtmo/integrations/cortex.py`
- `backend/tests/test_phase11_7b_cortex_connector.py`
- `.github/workflows/phase11-cortex-connector.yml`
- `docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md`
- `docs/integrations/THEHIVE_HANDOFF.md`
- `docs/operations/THEHIVE_HANDOFF_RUNBOOK.md`
- `docs/user/THEHIVE_CASE_HANDOFF.md`
- `docs/administration/THEHIVE_HANDOFF_CONFIGURATION.md`
- `docs/qa/PHASE11_6_THEHIVE_HANDOFF_CONTRACT_GATE.md`
- `docs/qa/PHASE11_6_THEHIVE_HANDOFF_IMPLEMENTATION_GATE.md`
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

### Phase 11.1–11.6

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers Taranis, IntelOwl, OpenCTI, MISP and TheHive service boundaries, identity/provenance preservation, durable reconciliation/state, fail-closed authority controls and human publication/share/case-handoff authority. These are repository engineering claims only.

The accepted TheHive implementation evidence includes `backend/tests/test_phase11_6_thehive_handoff_adapter.py`, `backend/tests/test_phase11_6_thehive_handoff_state.py` and `.github/workflows/phase11-thehive-handoff-implementation.yml`. A green gate does not prove live TheHive entitlement, permissions or production authorization.

### Phase 11.7 Cortex decision

**Status:** `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE`.

The accepted decision record concluded that Cortex was not adopted under the requirement set then available because no validated IntelOwl capability gap existed. That point-in-time claim remains preserved.

### Phase 11.7b Cortex analyzer connector

**Status:** `IN PROGRESS / OWNER-REQUIRED EXACT-HEAD VALIDATION`.

The accountable owner added Cortex connector integration as a new attributable requirement on 2026-08-17. The active repository evidence target covers:

- separate Cortex service/API identity boundary and no upstream source vendoring;
- API-key bearer authentication;
- production HTTPS/token/analyzer-allowlist guardrails;
- explicit observable datatype and analyzer allowlists;
- analyzer-only `POST /api/analyzer/{ANALYZER_ID}/run` execution;
- bounded `GET /api/job/{JOB_ID}/waitreport` retrieval;
- explicit Cortex TLP 0..3 validation before network I/O;
- stable job identity and analyzer-identity checks;
- bounded JSON report size and malformed-result fail-closed behavior;
- explicit `external_share_authorized=false` and `local_compromise_proven=false` result metadata;
- responder, external side-effect, administrative, file/attachment and automatic provider-fallback exclusions;
- synchronized architecture, integration, security, operations, QA, roadmap and documentation-portal material.

Dedicated repository evidence is:

- `backend/tests/test_phase11_7b_cortex_connector.py`;
- `.github/workflows/phase11-cortex-connector.yml`;
- `docs/qa/PHASE11_7B_CORTEX_CONNECTOR_GATE.md`.

A green connector gate does **not** prove live Cortex connectivity, effective organization/service-account permissions, enabled analyzer quality, provider subscriptions, lawful disclosure, runtime secrets, network policy, HA/recovery, production-equivalent validation, independent assurance or production authorization.

### Phase 11.8–11.9

After protected Phase 11.7b acceptance, evidence covers Kubernetes/Helm/GitOps runtime hardening and migration/compatibility in fixed order. Cortex must participate in the same secrets, network, observability, recovery and supply-chain controls if the connector is accepted.

### Phase 11.10–11.11

Fresh production-equivalent validation and fresh independent assurance must target the same immutable integrated candidate. Historical Phase 8/9 evidence cannot satisfy these gates.

### Phase 12

**Status:** `NOT STARTED`.

## Evidence transfer rule

Historical Phase 8/9 acceptance remains candidate-bound and cannot be transferred automatically to the materially changed Phase 11 platform. The historical Phase 11.7 Cortex decision is also not rewritten to manufacture a later requirement.

## Governance and handling rules

Framework claims remain governed by explicit provenance-backed mappings. External service state does not establish local exploitability, compromise, case necessity or dissemination authority without separate attributable evidence.

- Exact-head evidence belongs only to the exact state tested.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Credentials/tokens and unnecessary personal data do not belong in repository evidence.
- Human review/share approval and human case-handoff approval remain separate from technical execution.
- Cortex analyzer output is enrichment evidence only.
- Historical immutable run records are never rewritten to manufacture later acceptance.
