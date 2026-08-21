# DTMO Documentation Portal

This directory contains the authoritative professional documentation for Dutch Threat Monitoring for Education (DTMO). Current architecture, security, governance, operations, user and release material is separated from immutable historical evidence.

## Current controlled baseline

| Area | Current state |
|---|---|
| Software baseline | `16.0.0rc12` plus accepted post-RC13/E8/Phase-11 repository enhancements |
| Phases 1–7 | `PASS` |
| RC13 | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 10 | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11.1–11.9 | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10 | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` |
| Phase 11.10a–11.10k | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10l Governance & Evidence | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.10m–11.10o | `NOT STARTED` |
| Phase 11.10p production-equivalent validation | `NOT STARTED / CANDIDATE FREEZE REQUIRED` |
| Phase 11.11 independent external assurance | `NOT STARTED` |
| Phase 12 production GO/NO-GO | `NOT STARTED` |
| Production readiness | **not production authorized** |

The sole active bounded objective is **Phase 11.10l — Governance & Evidence**. The canonical `/workbench/governance` route reads governance knowledge through DTMO-owned same-origin APIs and preserves server-side RBAC, provenance, separation of duties and fail-closed evidence semantics. Repository CI is engineering evidence only and does not establish production-equivalent behavior, independent assurance or production authorization.

Historical Phase 8/9 evidence remains candidate-bound audit history and cannot be reused for the materially changed Phase 11.10 candidate. Phase 10 therefore remains **NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED**.

## Start here

| Audience | Primary documents |
|---|---|
| Executive / sponsor | [Current State](project/CURRENT_STATE.md), [Executive Status](project/EXECUTIVE_STATUS.md), [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md) |
| Product / delivery | [Product Guide](product/PRODUCT_GUIDE.md), [Unified Operations Workbench](ux/UNIFIED_OPERATIONS_WORKBENCH.md), [Platform Industrialisation Roadmap](roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md) |
| Analyst / reviewer | [Governance & Evidence](user/GOVERNANCE_EVIDENCE_WORKSPACE.md), [Automation & Playbooks](user/AUTOMATION_PLAYBOOKS_WORKSPACE.md), [Sources & Collection](user/SOURCES_COLLECTION_WORKSPACE.md), [Vulnerability & Exposure](user/VULNERABILITY_EXPOSURE_WORKSPACE.md), [TheHive Investigations](user/THEHIVE_INVESTIGATIONS_WORKSPACE.md), [MISP Sharing & Exchange](user/MISP_SHARING_EXCHANGE_WORKSPACE.md), [OpenCTI Graph / Entity Workspace](user/OPENCTI_GRAPH_ENTITY_WORKSPACE.md), [Integrated Analysis Workspace](user/INTEGRATED_ANALYSIS_WORKSPACE.md), [Unified Intelligence](user/UNIFIED_INTELLIGENCE_WORKSPACE.md), [IntelOwl Enrichment Workflow](user/INTELOWL_ENRICHMENT_WORKFLOW.md), [User Guide](user/USER_GUIDE.md) |
| Administrator | [Administrator Guide](administration/ADMINISTRATOR_GUIDE.md), [Kubernetes Runtime Configuration](administration/KUBERNETES_RUNTIME_CONFIGURATION.md), [Security Overview](security/SECURITY_OVERVIEW.md) |
| Architecture / engineering | [Phase 11.10l Governance & Evidence](architecture/PHASE11_10L_GOVERNANCE_EVIDENCE.md), [Frontend Architecture](architecture/FRONTEND_ARCHITECTURE.md), [UI/API Contract](architecture/UI_API_CONTRACT.md), [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) |
| Governance / compliance | [Governance Mapping Registry](governance/GOVERNANCE_MAPPING_REGISTRY.md), [Framework Governance](governance/FRAMEWORK_GOVERNANCE.md), [Data Classification & Retention](governance/DATA_CLASSIFICATION_RETENTION.md) |
| Security / CISO | [Security Overview](security/SECURITY_OVERVIEW.md), [Threat Model](security/THREAT_MODEL.md), [Risk Register](security/RISK_REGISTER.md) |
| QA / release | [Phase 11.10l Governance & Evidence Gate](qa/PHASE11_10L_GOVERNANCE_EVIDENCE_GATE.md), [QA and Release Gates](qa/QA_AND_RELEASE_GATES.md), [Evidence Index](evidence/EVIDENCE_INDEX.md) |
| Operations | [Operations Manual](operations/OPERATIONS_MANUAL.md), [IntelOwl Enrichment Runbook](operations/INTELOWL_ENRICHMENT_RUNBOOK.md), [Phase 11.10 Production-Equivalent Validation Runbook](operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md) |

## Unified Operations Workbench programme

Accepted repository-complete slices are 11.10a frontend architecture, 11.10b application shell, 11.10c Command Center, 11.10d Unified Intelligence, 11.10e IntelOwl/Cortex analysis, 11.10f OpenCTI graph/entity, 11.10g MISP Sharing & Exchange, 11.10h TheHive Investigations & Cases, 11.10i Vulnerability & Exposure, 11.10j Sources & Collection and 11.10k Automation & Playbooks.

**Phase 11.10l is active.** Its authoritative package is:

- `architecture/PHASE11_10L_GOVERNANCE_EVIDENCE.md`;
- `user/GOVERNANCE_EVIDENCE_WORKSPACE.md`;
- `qa/PHASE11_10L_GOVERNANCE_EVIDENCE_GATE.md`;
- `governance/GOVERNANCE_MAPPING_REGISTRY.md`;
- `../backend/dtmo/governance_knowledge.py`;
- `../backend/dtmo/governance_crosswalk.py`;
- `../frontend/src/GovernanceWorkspace.tsx`;
- `../backend/tests/test_phase11_10l_governance_evidence_contract.py`;
- `../tests/browser/phase11_10l_governance.py`;
- `../.github/workflows/phase11-governance-evidence.yml`.

The accepted governance registry already contains explicit typed, partial repository-backed relationships for Normenkader IBP, MITRE ATT&CK, NIST CSF and CVSS context. Those mappings may be displayed, but they are **not** certification, blanket compliance, semantic equivalence or evidence of environment effectiveness. Missing mappings remain unmapped rather than inferred.

The canonical trust path remains **browser → DTMO API → governed integration adapter/data contract → governed evidence source**. Browser visibility does not grant review, case creation, connector execution, external sharing, publication, administrative or production authority. Human review/share/publication decisions remain separate server-authorized actions.

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

- `qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
- `operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `../tools/phase11_production_equivalent_validation.py`;
- `../backend/tests/test_phase11_10_production_equivalent_validation.py`;
- `../.github/workflows/phase11-production-equivalent-validation.yml`.

11.10p requires fresh candidate identity, migration/compatibility, upgrade, rollback, health, saturation and recovery evidence for the **same immutable** candidate and one production-equivalent environment. Historical Phase 8/9 evidence cannot satisfy this gate. Missing, ambiguous, inaccessible, historical-only or mixed-candidate evidence must **fail closed**.

Repository CI validates repository-controlled contracts only. It does not prove production-equivalent operation and does not authorize production. Phase 11.11 remains `NOT STARTED` until Phase 11.10 is explicitly `PASS / OWNER_ACCEPTED`; Phase 12 remains `NOT STARTED` until fresh independent assurance is accepted.

## Evidence and release rule

Every commit invalidates prior exact-head CI evidence. A bounded PR is accepted only when its final unchanged head is mergeable, ready for review, professionally documented and every workflow registered for that exact head is `completed/success`.

Fresh production-equivalent validation remains **Phase 11.10p**, only after 11.10a–11.10o are complete and one immutable integrated candidate is frozen. Phase 11.11 independent external assurance follows against that same candidate; Phase 12 is the later formal production GO/NO-GO.

## Documentation maintenance rule

Whenever lifecycle state, architecture, security boundaries, product scope or governance claims materially change, affected professional documents and documentation-contract tests must be reconciled in the same bounded PR. Historical evidence is preserved rather than rewritten to support a new candidate.
