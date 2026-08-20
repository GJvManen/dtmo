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
| Phase 11.10f OpenCTI graph/entity workspace | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.10g–11.10o candidate completion | `NOT STARTED` |
| Phase 11.10p fresh production-equivalent validation | `NOT STARTED / CANDIDATE FREEZE REQUIRED` |
| Phase 11.11 independent external assurance | `NOT STARTED` |
| Phase 12 production go/no-go | `NOT STARTED` |
| Production readiness | **not production authorized** |

The active bounded programme step is **Phase 11.10f OpenCTI graph/entity workspace**. Phase 11.10a–11.10e are accepted repository baselines. The Unified Operations Workbench materially changes the integrated candidate, so fresh external production-equivalent execution remains 11.10p after 11.10a–11.10o completion and immutable candidate freeze. Earlier Phase 8/9 evidence remains historical and candidate-bound and cannot be reused.

## Start here

| Audience | Primary documents |
|---|---|
| Executive / sponsor | [Current State](project/CURRENT_STATE.md), [Executive Status](project/EXECUTIVE_STATUS.md), [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md) |
| Product / delivery | [Product Guide](product/PRODUCT_GUIDE.md), [Unified Operations Workbench](ux/UNIFIED_OPERATIONS_WORKBENCH.md), [Platform Industrialisation Roadmap](roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md) |
| Analyst / reviewer | [OpenCTI Graph / Entity Workspace](user/OPENCTI_GRAPH_ENTITY_WORKSPACE.md), [Integrated Analysis Workspace](user/INTEGRATED_ANALYSIS_WORKSPACE.md), [Unified Intelligence Workspace](user/UNIFIED_INTELLIGENCE_WORKSPACE.md), [User Guide](user/USER_GUIDE.md) |
| Administrator | [Administrator Guide](administration/ADMINISTRATOR_GUIDE.md), [Kubernetes Runtime Configuration](administration/KUBERNETES_RUNTIME_CONFIGURATION.md), [Security Overview](security/SECURITY_OVERVIEW.md) |
| Architecture / engineering | [Frontend Architecture](architecture/FRONTEND_ARCHITECTURE.md), [UI/API Contract](architecture/UI_API_CONTRACT.md), [Phase 11.10f OpenCTI Graph / Entity Workspace](architecture/PHASE11_10F_OPENCTI_GRAPH_ENTITY_WORKSPACE.md), [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) |
| UX / frontend | [Unified Operations Workbench](ux/UNIFIED_OPERATIONS_WORKBENCH.md), [Information Architecture](ux/INFORMATION_ARCHITECTURE.md), [Design System](ux/DESIGN_SYSTEM.md), [Frontend UX](ux/FRONTEND_UX.md), [`frontend/README.md`](../frontend/README.md) |
| Security / CISO | [Security Overview](security/SECURITY_OVERVIEW.md), [Threat Model](security/THREAT_MODEL.md), [Risk Register](security/RISK_REGISTER.md), [Phase 11.10 Validation Gate](qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md) |
| Governance / compliance | [Governance Mapping Registry](governance/GOVERNANCE_MAPPING_REGISTRY.md), [Data Classification & Retention](governance/DATA_CLASSIFICATION_RETENTION.md) |
| QA / release | [Phase 11.10f OpenCTI Graph Gate](qa/PHASE11_10F_OPENCTI_GRAPH_ENTITY_GATE.md), [Phase 11.10e Integrated Analysis Gate](qa/PHASE11_10E_INTEGRATED_ANALYSIS_GATE.md), [QA and Release Gates](qa/QA_AND_RELEASE_GATES.md), [Evidence Index](evidence/EVIDENCE_INDEX.md) |
| Operations | [Phase 11.10 Production-Equivalent Validation Runbook](operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md), [OpenCTI Integration Runbook](operations/OPENCTI_INTEGRATION_RUNBOOK.md), [Operations Manual](operations/OPERATIONS_MANUAL.md) |

## Unified Operations Workbench programme

Phase 11.10a established the frontend architecture/design contract. Phase 11.10b implemented the React/TypeScript/Vite canonical shell under `/workbench/`. Phase 11.10c delivered the governed Command Center. Phase 11.10d delivered governed intelligence discovery and canonical object detail/provenance. Phase 11.10e delivered the human-governed IntelOwl/Cortex analysis workspace. **Phase 11.10f is active** and makes the OpenCTI graph/entity route functional over persisted DTMO evidence.

The canonical frontend trust path remains:

**browser → DTMO API → governed integration adapter → upstream service**

The browser does not become a privileged upstream client. **Server-side RBAC**, provenance, human publication/share authority and separate TheHive case authority remain authoritative. `/ui/console` and `/ui/intelligence-workspace` are migration **compatibility paths**, not parallel feature-development targets.

### Accepted Phase 11.10a–11.10e packages

Accepted workbench evidence remains discoverable through:

- `architecture/FRONTEND_ARCHITECTURE.md`, `architecture/UI_API_CONTRACT.md`, `ux/UNIFIED_OPERATIONS_WORKBENCH.md`, `ux/INFORMATION_ARCHITECTURE.md`, `ux/DESIGN_SYSTEM.md`;
- `architecture/PHASE11_10B_APPLICATION_SHELL.md` and `qa/PHASE11_10B_APPLICATION_SHELL_GATE.md`;
- `architecture/PHASE11_10C_COMMAND_CENTER.md` and `qa/PHASE11_10C_COMMAND_CENTER_GATE.md`;
- `architecture/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE.md`, `user/UNIFIED_INTELLIGENCE_WORKSPACE.md`, `qa/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE_GATE.md`;
- `architecture/PHASE11_10E_INTEGRATED_ANALYSIS_WORKSPACE.md`, `user/INTEGRATED_ANALYSIS_WORKSPACE.md`, `qa/PHASE11_10E_INTEGRATED_ANALYSIS_GATE.md`;
- `.github/workflows/phase11-frontend-architecture.yml`, `.github/workflows/phase11-application-shell.yml`, `.github/workflows/phase11-command-center.yml`, `.github/workflows/phase11-unified-intelligence-workspace.yml` and `.github/workflows/phase11-integrated-analysis-workspace.yml`.

These accepted slices preserve fail-closed behavior. Search projections are not canonical truth; configuration is not runtime health; IntelOwl/Cortex output is evidence rather than a compromise verdict; UI visibility never replaces server-side authorization.

### Active Phase 11.10f OpenCTI Graph / Entity package

- `architecture/PHASE11_10F_OPENCTI_GRAPH_ENTITY_WORKSPACE.md`
- `user/OPENCTI_GRAPH_ENTITY_WORKSPACE.md`
- `qa/PHASE11_10F_OPENCTI_GRAPH_ENTITY_GATE.md`
- `backend/dtmo/opencti_workspace.py`
- `backend/dtmo/persistence/opencti.py`
- `frontend/src/OpenCTIGraphWorkspace.tsx`
- `frontend/src/opencti-graph.css`
- `backend/tests/test_phase11_10f_opencti_graph_contract.py`
- `backend/tests/test_phase11_10f_opencti_graph_browser.py`
- `.github/workflows/phase11-opencti-graph-workspace.yml`

The active workspace is read-only and requires `read:intelligence`. It renders a canonical DTMO intelligence root and persisted OpenCTI/STIX mapping nodes. The accepted Phase 11.4 persistence boundary does not durably store general OpenCTI entity-to-entity relationship topology, so 11.10f renders only attributable `canonical-mapping` edges and must **fail closed** rather than infer missing upstream relationships.

An empty mapping graph is not evidence that OpenCTI has no related knowledge. OpenCTI configuration is not live-service health. Graph/entity presence does not prove local exposure, exploitability, compromise or attribution, and it grants no external-share/publication authority.

Repository/browser CI for 11.10f **does not prove** live OpenCTI health or completeness, production-equivalent operation, independent assurance or production authorization.

After exact-head acceptance and merge of 11.10f, the only next bounded priority is **Phase 11.10g MISP Sharing & Exchange**.

## Accepted Phase 11 service integration baseline

- Phase 11.3 IntelOwl remains `PASS / REPOSITORY_COMPLETE` and grants no publication/share authority or compromise proof.
- Phase 11.4 OpenCTI remains `PASS / REPOSITORY_COMPLETE`; authoritative service-boundary material includes `architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md`, `integrations/OPENCTI_INTEGRATION.md`, `operations/OPENCTI_INTEGRATION_RUNBOOK.md`, `qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md` and `qa/PHASE11_4_OPENCTI_PERSISTENCE_GATE.md`.
- Phase 11.5 MISP remains `PASS / REPOSITORY_COMPLETE`; governed exchange remains subject to DTMO human sharing approval and handling restrictions.
- Phase 11.6 TheHive remains `PASS / REPOSITORY_COMPLETE`; case-handoff authority remains separate from publication/share authority.
- Phase 11.7 historical Cortex decision and 11.7b analyzer connector remain accepted; responders remain outside the accepted analyzer boundary.

## Accepted Phase 11.8 / 11.9 industrialisation baseline

Phase 11.8 and 11.9 remain `PASS / REPOSITORY_COMPLETE` across runtime, identity/secrets, ingress/network, HA, observability, recovery, supply chain, capacity, upgrade/rollback and forward-first migration compatibility. Application rollback does not authorize automatic database down migration. Repository controls do not by themselves establish production-equivalent behavior or production authorization.

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

Whenever lifecycle state, architecture, security boundary, product scope or governance claims materially change, affected professional documents and documentation-contract tests are reconciled in the same bounded PR. Historical evidence is preserved rather than rewritten to support a new candidate.
