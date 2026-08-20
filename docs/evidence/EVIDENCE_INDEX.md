# DTMO Evidence Index

Last updated: **2026-08-20**

## Purpose

This index maps current lifecycle stages to authoritative evidence classes and repository evidence chains. It is not a CI chronology. Historical run records, pull-request discussions and workflow artifacts remain immutable at their original candidate and moment.

## Current lifecycle

Phases 1–7 remain `PASS`; RC13 remains `PASS / OWNER_ACCEPTED`; **E8.1–E8.10 remain `PASS / REPOSITORY_COMPLETE`**. Phase 8 remains `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE`; Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`; Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. Phase 11.1–11.9 and Phase 11.10a–11.10d are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 remains **`IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`** with **Phase 11.10e IntelOwl/Cortex integrated analysis** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 11.10f, Phase 11.10p, Phase 11.11 and Phase 12 are `NOT STARTED`. DTMO is **not production authorized**.

## Evidence hierarchy

1. **Repository-controlled engineering evidence** — exact-head CI, contracts, builds, browser tests, migrations and synthetic/runtime contracts.
2. **Supply-chain evidence** — artifact hashes, SBOM/provenance/signing for the exact release subject.
3. **Accountable functional evidence** — explicit owner acceptance of product behavior.
4. **Real-environment evidence** — production-equivalent exercise bound to one immutable deployment identity.
5. **Independent assurance** — assessment independent from repository CI.
6. **Formal production authorization** — accountable GO/NO-GO for a specific candidate.

These classes are not interchangeable. Repository CI **does not prove** production-equivalent operation or production authorization.

## Accepted Phase 11 integration evidence

The accepted service integrations remain `PASS / REPOSITORY_COMPLETE` and separate service/licensing boundaries:

- Taranis AI — architecture, adapter and exact-head integration gates;
- IntelOwl — `docs/user/INTELOWL_ENRICHMENT_WORKFLOW.md`, integration/runbook/gate evidence;
- **Phase 11.4 OpenCTI** — `docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md`, `docs/integrations/OPENCTI_INTEGRATION.md`, `docs/operations/OPENCTI_INTEGRATION_RUNBOOK.md`, `docs/qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md`;
- **Phase 11.5 MISP** — governed consolidation/read/export evidence with human sharing authority retained by DTMO;
- TheHive — `docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md`, `docs/integrations/THEHIVE_HANDOFF.md`, `docs/operations/THEHIVE_HANDOFF_RUNBOOK.md`, `docs/qa/PHASE11_6_THEHIVE_HANDOFF_IMPLEMENTATION_GATE.md`, `.github/workflows/phase11-thehive-handoff-implementation.yml`;
- Cortex historical decision — `docs/qa/PHASE11_7_CORTEX_DECISION_GATE.md` / `CORTEX_DECISION_GATE.md`;
- Cortex 11.7b analyzer connector — `docs/integrations/CORTEX_ANALYZER_CONNECTOR.md`, `docs/qa/PHASE11_7B_CORTEX_CONNECTOR_GATE.md`.

No enrichment, graph, correlation, MISP or TheHive integration grants autonomous DTMO publication/share authority or proves local compromise.

## Accepted Phase 11.8 runtime evidence

Phase 11.8 is `PASS / REPOSITORY_COMPLETE` across runtime foundation, workload identity/external secret delivery, ingress/TLS/network segmentation, HA/disruption hardening, observability, backup/restore/recovery, software supply-chain hardening, capacity/resource planning and exercised upgrade/rollback.

Key workflow references include `.github/workflows/phase11-workload-identity-secrets.yml`, `.github/workflows/phase11-ingress-tls-network.yml`, `.github/workflows/phase11-ha-disruption.yml`, `.github/workflows/phase11-supply-chain-hardening.yml`, `.github/workflows/release-artifact-attestation.yml` and `.github/workflows/phase11-upgrade-rollback.yml`.

11.8i requires immutable baseline/candidate/rollback digests, finite rollout controls, exact prior-digest rollback and post-rollback health. Application rollback does not authorize automatic database down migration. Repository acceptance is not live-cluster or production-equivalent evidence.

## Accepted Phase 11.9 migration/compatibility evidence

Phase 11.9 is `PASS / REPOSITORY_COMPLETE`.

Authoritative chain:

- `backend/tests/test_phase11_9_migration_compatibility.py`;
- `tools/phase11_migration_compatibility.py`;
- `.github/workflows/phase11-migration-compatibility.yml`;
- `docs/architecture/PHASE11_9_MIGRATION_COMPATIBILITY.md`;
- `docs/operations/PHASE11_9_MIGRATION_COMPATIBILITY_RUNBOOK.md`;
- `docs/qa/PHASE11_9_MIGRATION_COMPATIBILITY_GATE.md`.

The contract requires one connected single-root/single-head Alembic graph, forward-first sequencing, compatible rolling overlap and expand/migrate/contract for destructive changes. Ambiguity must **fail closed**.

## Phase 11.10 candidate-completion evidence

### 11.10a frontend architecture/design

**Status:** `PASS / REPOSITORY_COMPLETE`.

- `docs/architecture/FRONTEND_ARCHITECTURE.md`;
- `docs/architecture/UI_API_CONTRACT.md`;
- `docs/ux/UNIFIED_OPERATIONS_WORKBENCH.md`;
- `docs/ux/INFORMATION_ARCHITECTURE.md`;
- `docs/ux/DESIGN_SYSTEM.md`;
- `docs/qa/PHASE11_10A_FRONTEND_ARCHITECTURE_GATE.md`;
- `backend/tests/test_phase11_10a_frontend_architecture_contract.py`;
- `.github/workflows/phase11-frontend-architecture.yml`.

### 11.10b canonical application shell

**Status:** `PASS / REPOSITORY_COMPLETE`.

- `docs/architecture/PHASE11_10B_APPLICATION_SHELL.md`;
- `docs/qa/PHASE11_10B_APPLICATION_SHELL_GATE.md`;
- `frontend/package.json` and `frontend/package-lock.json`;
- `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/styles.css`;
- `backend/dtmo/workbench_frontend.py`;
- `backend/tests/test_phase11_10b_application_shell_contract.py`;
- `backend/tests/test_phase11_10b_application_shell_browser.py`;
- `.github/workflows/phase11-application-shell.yml`.

The accepted trust path is **browser → DTMO API → governed integration adapter → upstream service**. `/ui/console` remains a temporary **compatibility path**. **Server-side RBAC** remains authoritative.

### 11.10c Command Center

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted chain:

- `backend/dtmo/command_center.py`;
- `backend/dtmo/api_command_center.py`;
- `frontend/src/App.tsx`;
- `frontend/src/command-center.css`;
- `docs/architecture/PHASE11_10C_COMMAND_CENTER.md`;
- `docs/qa/PHASE11_10C_COMMAND_CENTER_GATE.md`;
- `backend/tests/test_phase11_10c_command_center_contract.py`;
- `backend/tests/test_phase11_10c_command_center_browser.py`;
- `.github/workflows/phase11-command-center.yml`.

The Command Center is a read-only canonical projection. Missing canonical-store evidence produces `unavailable`/`null`, not synthetic zero values. Configured integrations are never promoted to a general `healthy` claim. Role-aware visibility does not replace server-side authorization. Repository acceptance does not prove live upstream health, production-equivalent execution, independent assurance or production authorization.

### 11.10d Unified Intelligence Workspace

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted chain:

- `frontend/src/UnifiedIntelligenceWorkspace.tsx`;
- `frontend/src/unified-intelligence.css`;
- `docs/architecture/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE.md`;
- `docs/user/UNIFIED_INTELLIGENCE_WORKSPACE.md`;
- `docs/qa/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE_GATE.md`;
- `backend/tests/test_phase11_10d_unified_intelligence_workspace_contract.py`;
- `backend/tests/test_phase11_10d_unified_intelligence_workspace_browser.py`;
- `.github/workflows/phase11-unified-intelligence-workspace.yml`.

11.10d reuses the governed `/api/v1/intelligence/search` discovery contract and `/api/v1/intelligence/{item_id}/workspace` canonical-detail/provenance contract. Search hits are index projections. Search or detail dependency failure is unavailable and must **fail closed**. `read:intelligence` remains server-authoritative and no review, sharing, publication, analyzer/connector execution, case mutation or administration authority is granted.

### 11.10e IntelOwl/Cortex integrated analysis

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

Authoritative active chain:

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

The workspace preserves the existing governed IntelOwl execution/history contract and adds a DTMO Cortex analyzer-only execution/history path with durable immutable persistence. `read:intelligence` authorizes capability/history reads; `review:intelligence` is required for execution. Cortex responders, automatic analyzer discovery and automatic IntelOwl fallback remain prohibited. Persisted analyzer evidence is constrained to `external_share_authorized=false` and `local_compromise_proven=false`.

The workflow must **fail closed** on missing canonical data, policy rejection or upstream failure. Configuration is not a runtime-health claim. IntelOwl/Cortex output **does not prove** local compromise, grants no external-share/publication/case authority, and repository/browser evidence does not prove live analyzer availability, production-equivalent operation, independent assurance or production authorization.

### Candidate-completion order

11.10f OpenCTI, 11.10g MISP, 11.10h TheHive, 11.10i Vulnerability & Exposure, 11.10j Sources & Collection, 11.10k Automation & Playbooks, 11.10l Governance & Evidence, 11.10m Operations & Administration, 11.10n role-aware UX/accessibility and 11.10o consolidation/full functional acceptance remain `NOT STARTED`.

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

Every accepted item must bind to the **same immutable** candidate and production-equivalent environment. Historical Phase 8/9 evidence is audit history only. Missing, inaccessible, placeholder, historical-only or mixed-candidate evidence must **fail closed**. A valid repository manifest validates metadata consistency only.

## Phase 11.11 and Phase 12

Phase 11.11 independent external assurance is `NOT STARTED` and remains blocked until Phase 11.10 is explicitly `PASS / OWNER_ACCEPTED`. Phase 12 is `NOT STARTED`; only a formal accountable decision can authorize production.
