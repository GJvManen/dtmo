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
| Phase 11.10c Command Center | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10d Unified Intelligence Workspace | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10e IntelOwl/Cortex integrated analysis | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10f OpenCTI graph/entity workspace | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10g MISP Sharing & Exchange | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.10h–11.10o candidate completion | `NOT STARTED` |
| Phase 11.10p fresh production-equivalent validation | `NOT STARTED / CANDIDATE FREEZE REQUIRED` |
| Phase 11.11 independent external assurance | `NOT STARTED` |
| Phase 12 production go/no-go | `NOT STARTED` |
| Production readiness | **not production authorized** |

The active bounded programme step is **Phase 11.10g MISP Sharing & Exchange**. Phase 11.10a–11.10f are accepted repository baselines. The Unified Operations Workbench materially changes the integrated candidate, so fresh external production-equivalent execution remains 11.10p after 11.10a–11.10o completion and immutable candidate freeze. Earlier Phase 8/9 evidence remains historical and candidate-bound and cannot be reused.

## Start here

| Audience | Primary documents |
|---|---|
| Executive / sponsor | [Current State](project/CURRENT_STATE.md), [Executive Status](project/EXECUTIVE_STATUS.md), [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md) |
| Product / delivery | [Product Guide](product/PRODUCT_GUIDE.md), [Unified Operations Workbench](ux/UNIFIED_OPERATIONS_WORKBENCH.md), [Platform Industrialisation Roadmap](roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md) |
| Analyst / reviewer | [MISP Sharing & Exchange](user/MISP_SHARING_EXCHANGE_WORKSPACE.md), [OpenCTI Graph / Entity Workspace](user/OPENCTI_GRAPH_ENTITY_WORKSPACE.md), [Integrated Analysis Workspace](user/INTEGRATED_ANALYSIS_WORKSPACE.md), [Unified Intelligence Workspace](user/UNIFIED_INTELLIGENCE_WORKSPACE.md), [IntelOwl Enrichment Workflow](user/INTELOWL_ENRICHMENT_WORKFLOW.md), [User Guide](user/USER_GUIDE.md) |
| Administrator | [Administrator Guide](administration/ADMINISTRATOR_GUIDE.md), [Kubernetes Runtime Configuration](administration/KUBERNETES_RUNTIME_CONFIGURATION.md), [Security Overview](security/SECURITY_OVERVIEW.md) |
| Architecture / engineering | [Phase 11.10g MISP Sharing & Exchange](architecture/PHASE11_10G_MISP_SHARING_EXCHANGE.md), [Frontend Architecture](architecture/FRONTEND_ARCHITECTURE.md), [UI/API Contract](architecture/UI_API_CONTRACT.md), [Phase 11.10f OpenCTI Graph / Entity Workspace](architecture/PHASE11_10F_OPENCTI_GRAPH_ENTITY_WORKSPACE.md), [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) |
| UX / frontend | [Unified Operations Workbench](ux/UNIFIED_OPERATIONS_WORKBENCH.md), [Information Architecture](ux/INFORMATION_ARCHITECTURE.md), [Design System](ux/DESIGN_SYSTEM.md), [Frontend UX](ux/FRONTEND_UX.md), [`frontend/README.md`](../frontend/README.md) |
| Security / CISO | [Security Overview](security/SECURITY_OVERVIEW.md), [Threat Model](security/THREAT_MODEL.md), [Risk Register](security/RISK_REGISTER.md), [Phase 11.10 Validation Gate](qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md) |
| Governance / compliance | [MISP Sharing & Exchange](architecture/PHASE11_10G_MISP_SHARING_EXCHANGE.md), [Governance Mapping Registry](governance/GOVERNANCE_MAPPING_REGISTRY.md), [Data Classification & Retention](governance/DATA_CLASSIFICATION_RETENTION.md) |
| QA / release | [Phase 11.10g MISP Sharing Gate](qa/PHASE11_10G_MISP_SHARING_EXCHANGE_GATE.md), [Phase 11.10f OpenCTI Graph Gate](qa/PHASE11_10F_OPENCTI_GRAPH_ENTITY_GATE.md), [QA and Release Gates](qa/QA_AND_RELEASE_GATES.md), [Evidence Index](evidence/EVIDENCE_INDEX.md) |
| Operations | [Phase 11.10 Production-Equivalent Validation Runbook](operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md), [OpenCTI Integration Runbook](operations/OPENCTI_INTEGRATION_RUNBOOK.md), [IntelOwl Enrichment Runbook](operations/INTELOWL_ENRICHMENT_RUNBOOK.md), [Operations Manual](operations/OPERATIONS_MANUAL.md) |

## Unified Operations Workbench programme

Phase 11.10a established the frontend architecture/design contract. Phase 11.10b implemented the React/TypeScript/Vite canonical shell under `/workbench/`. Phase 11.10c delivered the governed Command Center. Phase 11.10d delivered governed intelligence discovery and canonical object detail/provenance. Phase 11.10e delivered the human-governed IntelOwl/Cortex analysis workspace. Phase 11.10f delivered the OpenCTI graph/entity workspace. **Phase 11.10g is active** and makes `/workbench/sharing` a human-governed MISP review, approval and unpublished-export workspace.

The canonical frontend trust path remains:

**browser → DTMO API → governed integration adapter → upstream service**

The browser does not become a privileged upstream client. **Server-side RBAC**, provenance, human publication/share authority and separate TheHive case authority remain authoritative. `/ui/console`, `/ui/intelligence-workspace` and `/ui/misp-workspace` are migration **compatibility paths**, not parallel feature-development targets.

### Accepted Phase 11.10a–11.10f packages

Accepted workbench evidence remains discoverable through:

- `architecture/FRONTEND_ARCHITECTURE.md`, `architecture/UI_API_CONTRACT.md`, `ux/UNIFIED_OPERATIONS_WORKBENCH.md`, `ux/INFORMATION_ARCHITECTURE.md`, `ux/DESIGN_SYSTEM.md`;
- `architecture/PHASE11_10B_APPLICATION_SHELL.md` and `qa/PHASE11_10B_APPLICATION_SHELL_GATE.md`;
- `architecture/PHASE11_10C_COMMAND_CENTER.md` and `qa/PHASE11_10C_COMMAND_CENTER_GATE.md`;
- `architecture/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE.md`, `user/UNIFIED_INTELLIGENCE_WORKSPACE.md`, `qa/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE_GATE.md`;
- `architecture/PHASE11_10E_INTEGRATED_ANALYSIS_WORKSPACE.md`, `user/INTEGRATED_ANALYSIS_WORKSPACE.md`, `qa/PHASE11_10E_INTEGRATED_ANALYSIS_GATE.md`;
- `architecture/PHASE11_10F_OPENCTI_GRAPH_ENTITY_WORKSPACE.md`, `user/OPENCTI_GRAPH_ENTITY_WORKSPACE.md`, `qa/PHASE11_10F_OPENCTI_GRAPH_ENTITY_GATE.md`;
- `.github/workflows/phase11-frontend-architecture.yml`, `.github/workflows/phase11-application-shell.yml`, `.github/workflows/phase11-command-center.yml`, `.github/workflows/phase11-unified-intelligence-workspace.yml`, `.github/workflows/phase11-integrated-analysis-workspace.yml` and `.github/workflows/phase11-opencti-graph-workspace.yml`.

These accepted slices preserve fail-closed behavior. Search projections are not canonical truth; configuration is not runtime health; IntelOwl/Cortex output is evidence rather than a compromise verdict; OpenCTI topology is not inferred beyond persisted evidence; UI visibility never replaces server-side authorization.

### Active Phase 11.10g MISP Sharing & Exchange package

- `architecture/PHASE11_10G_MISP_SHARING_EXCHANGE.md`
- `user/MISP_SHARING_EXCHANGE_WORKSPACE.md`
- `qa/PHASE11_10G_MISP_SHARING_EXCHANGE_GATE.md`
- `backend/dtmo/misp_sharing_workspace.py`
- `backend/dtmo/misp_export_api.py`
- `backend/dtmo/governance/misp_export.py`
- `frontend/src/MispSharingWorkspace.tsx`
- `frontend/src/misp-sharing.css`
- `backend/tests/test_phase11_10g_misp_sharing_contract.py`
- `backend/tests/test_phase11_10g_misp_sharing_browser.py`
- `.github/workflows/phase11-misp-sharing-exchange.yml`

The workspace reads canonical sharing state with `read:intelligence`, records review only through the existing `review:intelligence` endpoint, requires a **different human principal** with `approve:share` for sharing approval, and invokes the accepted MISP export only for already reviewed/share-approved canonical revisions. Service accounts cannot substitute for human review/share authority.

MISP-origin intelligence retains authoritative distribution, sharing-group and TLP restrictions. Replay evidence for the deterministic current revision fails closed on `pending`, `success` or `uncertain` states. The export creates an event with `published=false`. Phase 11.10g exposes **no Publish or Synchronize action**.

MISP configuration is not live-service health. A successful transfer does not prove publication, synchronization, downstream consumption, local compromise, production-equivalent operation, independent assurance or production authorization.

After exact-head acceptance and merge of 11.10g, the only next bounded priority is **Phase 11.10h TheHive Investigations & Cases**.

## Accepted Phase 11 service integration baseline

- Phase 11.3 IntelOwl remains `PASS / REPOSITORY_COMPLETE`. Operator documentation remains explicitly exposed through `user/INTELOWL_ENRICHMENT_WORKFLOW.md` and `operations/INTELOWL_ENRICHMENT_RUNBOOK.md`; enrichment grants no publication/share authority and proves no local compromise.
- Phase 11.4 OpenCTI remains `PASS / REPOSITORY_COMPLETE`; authoritative service-boundary material includes `architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md`, `integrations/OPENCTI_INTEGRATION.md`, `operations/OPENCTI_INTEGRATION_RUNBOOK.md`, `qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md` and `qa/PHASE11_4_OPENCTI_PERSISTENCE_GATE.md`.
- Phase 11.5 MISP remains `PASS / REPOSITORY_COMPLETE`; governed exchange remains subject to DTMO human sharing approval and handling restrictions. Accepted baseline material includes `architecture/MISP_DTMO_CONSOLIDATION_CONTRACT.md`, `integrations/MISP_READ_INTEGRATION.md` and `intelligence/MISP_GOVERNED_EXPORT.md`.
- **Phase 11.6 TheHive Handoff Implementation Gate** remains accepted through `architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md`, `integrations/THEHIVE_HANDOFF.md`, `operations/THEHIVE_HANDOFF_RUNBOOK.md`, `user/THEHIVE_CASE_HANDOFF.md`, `administration/THEHIVE_HANDOFF_CONFIGURATION.md` and `qa/PHASE11_6_THEHIVE_HANDOFF_IMPLEMENTATION_GATE.md`.
- Phase 11.7 historical Cortex decision remains accepted through `qa/PHASE11_7_CORTEX_DECISION_GATE.md`; the 11.7b analyzer connector remains exposed through `integrations/CORTEX_ANALYZER_CONNECTOR.md`, `operations/CORTEX_ANALYZER_RUNBOOK.md` and `qa/PHASE11_7B_CORTEX_CONNECTOR_GATE.md`. Responders remain outside the accepted analyzer boundary.

## Accepted Phase 11.8 / 11.9 industrialisation baseline

Phase 11.8 and 11.9 remain `PASS / REPOSITORY_COMPLETE` across runtime, identity/secrets, ingress/network, HA, observability, recovery, supply chain, capacity, upgrade/rollback and forward-first migration compatibility. Application rollback does not authorize automatic database down migration. Repository controls do not by themselves establish production-equivalent behavior or production authorization.

The accepted runtime and migration documentation remains explicitly discoverable:

- `architecture/PHASE11_8_RUNTIME_FOUNDATION.md` and `administration/KUBERNETES_RUNTIME_CONFIGURATION.md`;
- `architecture/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS.md`, `administration/WORKLOAD_IDENTITY_EXTERNAL_SECRETS.md`, `operations/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_RUNBOOK.md` and `qa/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_GATE.md`;
- `architecture/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION.md`, `administration/INGRESS_TLS_NETWORK_SEGMENTATION.md`, `operations/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION_RUNBOOK.md` and `qa/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION_GATE.md`;
- `architecture/PHASE11_8D_HA_DISRUPTION.md`, `operations/PHASE11_8D_HA_DISRUPTION_RUNBOOK.md` and `qa/PHASE11_8D_HA_DISRUPTION_GATE.md`;
- `architecture/PHASE11_8E_OBSERVABILITY_HARDENING.md`, `operations/PHASE11_8E_OBSERVABILITY_RUNBOOK.md` and `qa/PHASE11_8E_OBSERVABILITY_GATE.md`;
- `architecture/PHASE11_8F_RECOVERY_HARDENING.md`, `operations/PHASE11_8F_RECOVERY_RUNBOOK.md` and `qa/PHASE11_8F_RECOVERY_GATE.md`;
- `security/PHASE11_8G_SUPPLY_CHAIN_HARDENING.md`, `operations/PHASE11_8G_SUPPLY_CHAIN_RUNBOOK.md` and `qa/PHASE11_8G_SUPPLY_CHAIN_GATE.md`;
- `architecture/PHASE11_9_MIGRATION_COMPATIBILITY.md`, `operations/PHASE11_9_MIGRATION_COMPATIBILITY_RUNBOOK.md` and `qa/PHASE11_9_MIGRATION_COMPATIBILITY_GATE.md`.

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

## Governed visual evidence boundary

The governed screenshot catalogue now contains UI-01 through UI-10. These are **documentation illustrations rather than proof of live-source connectivity, staging acceptance or production readiness**. No synthetic screenshot is promoted as operational, staging, assurance or production evidence.

## Documentation maintenance rule

Whenever lifecycle state, architecture, security boundary, product scope or governance claims materially change, affected professional documents and documentation-contract tests are reconciled in the same bounded PR. Historical evidence is preserved rather than rewritten to support a new candidate.
