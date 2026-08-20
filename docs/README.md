# DTMO Documentation Portal

This directory contains the authoritative professional documentation for Dutch Threat Monitoring for Education (DTMO). Current product, architecture, security, governance, operations and readiness documentation is separated from immutable historical evidence and prior-candidate assurance records.

## Current controlled baseline

| Area | Current state |
|---|---|
| Software baseline | `16.0.0rc12` plus accepted post-RC13/E8/Phase-11 repository enhancements |
| Phases 1–7 | `PASS` |
| RC13 functional product acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 production-equivalent staging | `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 9 independent assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 10 production go/no-go | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11.1–11.9 | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10 candidate completion + production-equivalent validation | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` |
| Phase 11.10a frontend architecture/design contract | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10b canonical application shell | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10c Command Center | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.10d–11.10o candidate completion | `NOT STARTED` |
| Phase 11.10p fresh production-equivalent validation | `NOT STARTED / CANDIDATE FREEZE REQUIRED` |
| Phase 11.11 independent external assurance | `NOT STARTED` |
| Phase 12 production go/no-go | `NOT STARTED` |
| Production readiness | **not production authorized** |

The active bounded programme step is **Phase 11.10c Command Center**. Phase 11.10a and 11.10b are accepted repository baselines. The Unified Operations Workbench materially changes the integrated candidate, so fresh external production-equivalent execution remains 11.10p after 11.10a–11.10o candidate completion and immutable candidate freeze. Earlier Phase 8/9 evidence remains historical and candidate-bound and cannot be reused.

## Start here

| Audience | Primary documents |
|---|---|
| Executive / sponsor | [Current State](project/CURRENT_STATE.md), [Executive Status](project/EXECUTIVE_STATUS.md), [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md) |
| Product / delivery | [Product Guide](product/PRODUCT_GUIDE.md), [Unified Operations Workbench](ux/UNIFIED_OPERATIONS_WORKBENCH.md), [Platform Industrialisation Roadmap](roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md) |
| Analyst / reviewer | [User Guide](user/USER_GUIDE.md), [Information Architecture](ux/INFORMATION_ARCHITECTURE.md), [System Workflows](architecture/SYSTEM_WORKFLOWS.md), [Screenshot Catalogue](visual/screenshots/README.md) |
| Administrator | [Administrator Guide](administration/ADMINISTRATOR_GUIDE.md), [Kubernetes Runtime Configuration](administration/KUBERNETES_RUNTIME_CONFIGURATION.md), [Security Overview](security/SECURITY_OVERVIEW.md) |
| Architecture / engineering | [Frontend Architecture](architecture/FRONTEND_ARCHITECTURE.md), [UI/API Contract](architecture/UI_API_CONTRACT.md), [Phase 11.10b Application Shell](architecture/PHASE11_10B_APPLICATION_SHELL.md), [Phase 11.10c Command Center](architecture/PHASE11_10C_COMMAND_CENTER.md), [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) |
| UX / frontend | [Unified Operations Workbench](ux/UNIFIED_OPERATIONS_WORKBENCH.md), [Information Architecture](ux/INFORMATION_ARCHITECTURE.md), [Design System](ux/DESIGN_SYSTEM.md), [Frontend UX](ux/FRONTEND_UX.md), [`frontend/README.md`](../frontend/README.md) |
| Security / CISO | [Security Overview](security/SECURITY_OVERVIEW.md), [Threat Model](security/THREAT_MODEL.md), [Risk Register](security/RISK_REGISTER.md), [Phase 11.10 Validation Gate](qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md) |
| Governance / compliance | [Governance Mapping Registry](governance/GOVERNANCE_MAPPING_REGISTRY.md), [Data Classification & Retention](governance/DATA_CLASSIFICATION_RETENTION.md) |
| QA / release | [Phase 11.10c Command Center Gate](qa/PHASE11_10C_COMMAND_CENTER_GATE.md), [Phase 11.10b Application Shell Gate](qa/PHASE11_10B_APPLICATION_SHELL_GATE.md), [QA and Release Gates](qa/QA_AND_RELEASE_GATES.md), [Evidence Index](evidence/EVIDENCE_INDEX.md) |
| Operations | [Phase 11.10 Production-Equivalent Validation Runbook](operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md), [Operating Model](operations/OPERATING_MODEL.md), [Operations Manual](operations/OPERATIONS_MANUAL.md) |

## Unified Operations Workbench programme

Phase 11.10a established the frontend architecture/design contract. Phase 11.10b implemented the separately built React/TypeScript/Vite canonical shell under `/workbench/`. Phase 11.10c is the first functional workspace and implements a governed operational Command Center.

The canonical frontend trust path remains:

**browser → DTMO API → governed integration adapter → upstream service**

The browser does not become a privileged upstream client. **Server-side RBAC**, provenance, human publication/share authority and separate TheHive case authority remain authoritative. `/ui/console` is a temporary migration **compatibility path**, not a parallel target for new feature development.

### Accepted Phase 11.10a / 11.10b package

- `architecture/FRONTEND_ARCHITECTURE.md`
- `architecture/UI_API_CONTRACT.md`
- `ux/UNIFIED_OPERATIONS_WORKBENCH.md`
- `ux/INFORMATION_ARCHITECTURE.md`
- `ux/DESIGN_SYSTEM.md`
- `architecture/PHASE11_10B_APPLICATION_SHELL.md`
- `qa/PHASE11_10A_FRONTEND_ARCHITECTURE_GATE.md`
- `qa/PHASE11_10B_APPLICATION_SHELL_GATE.md`
- `.github/workflows/phase11-frontend-architecture.yml`
- `.github/workflows/phase11-application-shell.yml`
- `frontend/package.json`, `frontend/package-lock.json`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/styles.css`

### Active Phase 11.10c Command Center package

- `architecture/PHASE11_10C_COMMAND_CENTER.md`
- `qa/PHASE11_10C_COMMAND_CENTER_GATE.md`
- `backend/dtmo/command_center.py`
- `backend/dtmo/api_command_center.py`
- `frontend/src/command-center.css`
- `backend/tests/test_phase11_10c_command_center_contract.py`
- `backend/tests/test_phase11_10c_command_center_browser.py`
- `.github/workflows/phase11-command-center.yml`

The Command Center uses attributable canonical read models. If the canonical datastore is unavailable, values are reported as unavailable rather than converted to zero. Integration configuration is not promoted to a runtime-health claim. Role-aware quick-action visibility never substitutes for server-side authorization. Repository CI **does not prove** live upstream health, production-equivalent execution, independent assurance or production authorization.

After exact-head acceptance and merge of 11.10c, the only next bounded priority is **Phase 11.10d Unified Intelligence Workspace**.

## Accepted Phase 11 service integration baseline

- Phase 11.3 IntelOwl remains `PASS / REPOSITORY_COMPLETE`. Analyst workflow: `user/INTELOWL_ENRICHMENT_WORKFLOW.md`; operations: `operations/INTELOWL_ENRICHMENT_RUNBOOK.md`. Enrichment grants no publication/share authority and proves no local compromise.
- **Phase 11.4 OpenCTI** remains `PASS / REPOSITORY_COMPLETE`. Authoritative material: `architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md`, `integrations/OPENCTI_INTEGRATION.md`, `operations/OPENCTI_INTEGRATION_RUNBOOK.md`, `qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md`.
- Phase 11.5 MISP remains `PASS / REPOSITORY_COMPLETE`; governed exchange remains subject to DTMO human sharing approval and handling restrictions.
- TheHive implementation remains accepted through `integrations/THEHIVE_HANDOFF.md`, `architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md`, `operations/THEHIVE_HANDOFF_RUNBOOK.md`, `administration/THEHIVE_HANDOFF_CONFIGURATION.md` and the **Phase 11.6 TheHive Handoff Implementation Gate**.
- Historical Cortex decision: `qa/PHASE11_7_CORTEX_DECISION_GATE.md` (`CORTEX_DECISION_GATE.md`). The historical decision is not rewritten by later connector work.
- Cortex 11.7b analyzer connector: `integrations/CORTEX_ANALYZER_CONNECTOR.md` and `qa/PHASE11_7B_CORTEX_CONNECTOR_GATE.md`.

## Accepted Phase 11.8 / 11.9 industrialisation baseline

- `architecture/PHASE11_8_RUNTIME_FOUNDATION.md` and `administration/KUBERNETES_RUNTIME_CONFIGURATION.md`
- `architecture/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS.md` and `administration/WORKLOAD_IDENTITY_EXTERNAL_SECRETS.md`
- `architecture/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION.md` and `administration/INGRESS_TLS_NETWORK_SEGMENTATION.md`
- `architecture/PHASE11_8D_HA_DISRUPTION.md`
- `architecture/PHASE11_8E_OBSERVABILITY_HARDENING.md`
- `architecture/PHASE11_8F_RECOVERY_HARDENING.md`
- `security/PHASE11_8G_SUPPLY_CHAIN_HARDENING.md`
- `architecture/PHASE11_8H_CAPACITY_RESOURCE_PLANNING.md`
- `architecture/PHASE11_8I_UPGRADE_ROLLBACK.md`
- `architecture/PHASE11_9_MIGRATION_COMPATIBILITY.md`
- `operations/PHASE11_9_MIGRATION_COMPATIBILITY_RUNBOOK.md`
- `qa/PHASE11_9_MIGRATION_COMPATIBILITY_GATE.md`

Phase 11.8 and 11.9 remain `PASS / REPOSITORY_COMPLETE`; repository controls do not by themselves establish production-equivalent behavior or production authorization.

The governed screenshot catalogue now contains UI-01 through UI-10. These are documentation illustrations rather than proof of live-source connectivity, staging acceptance or production readiness.

## Phase 11.10 external validation package

The existing execution package remains authoritative for 11.10p:

- `qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`
- `operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`
- `evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`
- `tools/phase11_production_equivalent_validation.py`
- `backend/tests/test_phase11_10_production_equivalent_validation.py`
- `.github/workflows/phase11-production-equivalent-validation.yml`

11.10p requires fresh candidate identity, migration/compatibility, upgrade, rollback, health, saturation and recovery evidence for the **same immutable** candidate and one production-equivalent environment. Historical Phase 8/9 evidence cannot satisfy this gate. Missing, ambiguous, inaccessible, historical-only or mixed-candidate evidence must **fail closed**.

Repository CI validates repository-controlled contracts only. It does not prove production-equivalent operation and does not authorize production. Phase 11.11 remains `NOT STARTED` until Phase 11.10 is explicitly `PASS / OWNER_ACCEPTED`; Phase 12 remains `NOT STARTED` until fresh independent assurance is accepted.

## Documentation maintenance rule

Whenever lifecycle state, architecture, security boundary, product scope or governance claims materially change, affected professional documents and documentation-contract tests must be reconciled in the same bounded PR. Historical evidence is preserved rather than rewritten to support a new candidate.
