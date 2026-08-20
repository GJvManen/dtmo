# DTMO Evidence Index

Last updated: **2026-08-20**

## Purpose

This index maps current lifecycle stages to authoritative evidence classes and repository evidence chains. It is not a CI chronology. Historical run records, pull-request discussions and workflow artifacts remain immutable at their original candidate and moment.

## Current lifecycle

Phases 1–7 remain `PASS`; RC13 remains `PASS / OWNER_ACCEPTED`; **E8.1–E8.10 remain `PASS / REPOSITORY_COMPLETE`**. Phase 8 remains `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE`; Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`; Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. Phase 11.1–11.9 and Phase 11.10a–11.10e are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 remains **`IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`** with **Phase 11.10f OpenCTI graph/entity workspace** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 11.10g, Phase 11.10p, Phase 11.11 and Phase 12 are `NOT STARTED`. DTMO is **not production authorized**.

## Evidence hierarchy

1. **Repository-controlled engineering evidence** — exact-head CI, contracts, builds, browser tests, migrations and runtime contracts.
2. **Supply-chain evidence** — artifact hashes, SBOM/provenance/signing for the exact release subject.
3. **Accountable functional evidence** — explicit owner acceptance of product behavior.
4. **Real-environment evidence** — production-equivalent exercise bound to one immutable deployment identity.
5. **Independent assurance** — assessment independent from repository CI.
6. **Formal production authorization** — accountable GO/NO-GO for a specific candidate.

These classes are not interchangeable. Repository CI **does not prove** production-equivalent operation or production authorization.

## Accepted Phase 11 integration evidence

The accepted service integrations remain `PASS / REPOSITORY_COMPLETE` and separate service/licensing boundaries:

- Taranis AI — architecture, adapter and exact-head integration gates;
- IntelOwl — governed enrichment and immutable history;
- **Phase 11.4 OpenCTI** — `docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md`, `docs/integrations/OPENCTI_INTEGRATION.md`, `docs/operations/OPENCTI_INTEGRATION_RUNBOOK.md`, `docs/qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md`, `docs/qa/PHASE11_4_OPENCTI_PERSISTENCE_GATE.md`;
- **Phase 11.5 MISP** — governed consolidation/read/export evidence with human sharing authority retained by DTMO;
- TheHive — governed handoff evidence with case authority distinct from sharing authority;
- Cortex historical decision plus 11.7b analyzer-only connector evidence.

No enrichment, graph, correlation, MISP or TheHive integration grants autonomous DTMO publication/share authority or proves local compromise.

## Accepted Phase 11.8 / 11.9 evidence

Phase 11.8 is `PASS / REPOSITORY_COMPLETE` across runtime foundation, workload identity/external secret delivery, ingress/TLS/network segmentation, HA/disruption hardening, observability, backup/restore/recovery, software supply-chain hardening, capacity/resource planning and exercised upgrade/rollback. Phase 11.9 is `PASS / REPOSITORY_COMPLETE` for the connected migration graph and forward-first compatibility model.

Rollback requires exact prior immutable identity and post-rollback health. Application rollback does not authorize automatic database down migration. Repository acceptance is not live-cluster or production-equivalent evidence.

## Phase 11.10 candidate-completion evidence

### 11.10a frontend architecture/design

**Status:** `PASS / REPOSITORY_COMPLETE`.

Authoritative evidence includes `docs/architecture/FRONTEND_ARCHITECTURE.md`, `docs/architecture/UI_API_CONTRACT.md`, `docs/ux/UNIFIED_OPERATIONS_WORKBENCH.md`, `docs/ux/INFORMATION_ARCHITECTURE.md`, `docs/ux/DESIGN_SYSTEM.md`, `docs/qa/PHASE11_10A_FRONTEND_ARCHITECTURE_GATE.md`, `backend/tests/test_phase11_10a_frontend_architecture_contract.py` and `.github/workflows/phase11-frontend-architecture.yml`.

### 11.10b canonical application shell

**Status:** `PASS / REPOSITORY_COMPLETE`.

The accepted trust path is **browser → DTMO API → governed integration adapter → upstream service**. `/ui/console` remains a migration **compatibility path**. **Server-side RBAC** remains authoritative.

### 11.10c Command Center

**Status:** `PASS / REPOSITORY_COMPLETE`.

The Command Center is a read-only canonical projection. Missing canonical-store evidence produces unavailable/null state rather than synthetic zero values. Integration configuration is not promoted to general runtime health.

### 11.10d Unified Intelligence Workspace

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted evidence includes `docs/architecture/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE.md`, `docs/user/UNIFIED_INTELLIGENCE_WORKSPACE.md`, `docs/qa/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE_GATE.md`, `frontend/src/UnifiedIntelligenceWorkspace.tsx`, its contract/browser tests and `.github/workflows/phase11-unified-intelligence-workspace.yml`.

Search hits are discovery projections; canonical object detail comes separately from DTMO persistence. Dependency failures **fail closed**.

### 11.10e IntelOwl/Cortex integrated analysis

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted evidence chain:

- `backend/dtmo/intelowl_execution.py`;
- `backend/dtmo/persistence/cortex.py`;
- `database/migrations/versions/0015_cortex_analysis_history.py`;
- `frontend/src/AnalysisWorkspace.tsx`;
- `frontend/src/analysis-workspace.css`;
- `docs/architecture/PHASE11_10E_INTEGRATED_ANALYSIS_WORKSPACE.md`;
- `docs/user/INTEGRATED_ANALYSIS_WORKSPACE.md`;
- `docs/qa/PHASE11_10E_INTEGRATED_ANALYSIS_GATE.md`;
- `backend/tests/test_phase11_10e_integrated_analysis_contract.py`;
- `backend/tests/test_phase11_10e_integrated_analysis_browser.py`;
- `.github/workflows/phase11-integrated-analysis-workspace.yml`.

IntelOwl/Cortex output remains evidence rather than a verdict. It does not prove local compromise and grants no external-share/publication/case authority.

### 11.10f OpenCTI graph/entity workspace

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

Authoritative active chain:

- `backend/dtmo/opencti_workspace.py`;
- `backend/dtmo/persistence/opencti.py`;
- `frontend/src/OpenCTIGraphWorkspace.tsx`;
- `frontend/src/opencti-graph.css`;
- `docs/architecture/PHASE11_10F_OPENCTI_GRAPH_ENTITY_WORKSPACE.md`;
- `docs/user/OPENCTI_GRAPH_ENTITY_WORKSPACE.md`;
- `docs/qa/PHASE11_10F_OPENCTI_GRAPH_ENTITY_GATE.md`;
- `backend/tests/test_phase11_10f_opencti_graph_contract.py`;
- `backend/tests/test_phase11_10f_opencti_graph_browser.py`;
- `.github/workflows/phase11-opencti-graph-workspace.yml`.

11.10f reuses the accepted Phase 11.4 OpenCTI mapping and immutable-revision persistence. The browser consumes only DTMO APIs protected by `read:intelligence`.

The persisted boundary does not contain general OpenCTI entity-to-entity relationship topology. The graph therefore renders only proven DTMO canonical-item → OpenCTI mapping edges (`canonical-mapping`). Missing relationship evidence must **fail closed** and must not be inferred from display names, entity types, OpenCTI presence or graph layout.

An empty mapping result means only that no persisted mapping evidence exists for that canonical DTMO item. It does not prove upstream absence. Configuration does not establish runtime health. OpenCTI identity, confidence, markings, graph presence or revisions do **not prove** local exposure, exploitability, compromise, attribution certainty or remediation state and grant no external-share/publication authority.

Repository/browser evidence does not prove live OpenCTI connectivity/health, completeness of OpenCTI knowledge, production-equivalent operation, independent assurance or production authorization.

### Candidate-completion order

11.10g MISP, 11.10h TheHive, 11.10i Vulnerability & Exposure, 11.10j Sources & Collection, 11.10k Automation & Playbooks, 11.10l Governance & Evidence, 11.10m Operations & Administration, 11.10n role-aware UX/accessibility and 11.10o consolidation/full functional acceptance remain `NOT STARTED`.

## Phase 11.10p production-equivalent evidence

**Status:** `NOT STARTED / CANDIDATE FREEZE REQUIRED`.

After 11.10o, one immutable integrated candidate is frozen. Fresh evidence must cover candidate identity, migration/compatibility, upgrade, rollback to the exact prior immutable digest plus post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity.

Authoritative external execution package:

- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `backend/tests/test_phase11_10_production_equivalent_validation.py`;
- `tools/phase11_production_equivalent_validation.py`;
- `.github/workflows/phase11-production-equivalent-validation.yml`.

Every accepted item must bind to the **same immutable** candidate and production-equivalent environment. Historical Phase 8/9 evidence is audit history only. Missing, inaccessible, placeholder, historical-only or mixed-candidate evidence must **fail closed**.

## Phase 11.11 and Phase 12

Phase 11.11 independent external assurance is `NOT STARTED` and remains blocked until Phase 11.10 is explicitly `PASS / OWNER_ACCEPTED`. Phase 12 is `NOT STARTED`; only a formal accountable decision can authorize production.
