# DTMO Documentation Portal

This portal is the primary entry point for DTMO product, administration, operations, architecture, security, governance, quality and release documentation. It is organized around what readers need to do rather than around internal delivery chronology.

> **Release position:** DTMO remains **not production authorized**. Repository CI is engineering evidence for an exact source revision; it does not by itself prove production-equivalent operation, independent assurance or production approval. Use [Current State](project/CURRENT_STATE.md) and [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md) for authoritative lifecycle decisions.

## Start here

| Audience | Recommended entry points |
|---|---|
| Executive / sponsor | [Executive Status](project/EXECUTIVE_STATUS.md) · [Current State](project/CURRENT_STATE.md) · [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md) |
| Security analyst / reviewer | [User Guide](user/USER_GUIDE.md) · [Unified Intelligence](user/UNIFIED_INTELLIGENCE_WORKSPACE.md) · [Integrated Analysis](user/INTEGRATED_ANALYSIS_WORKSPACE.md) · [Vulnerability & Exposure](user/VULNERABILITY_EXPOSURE_WORKSPACE.md) |
| Administrator | [Administrator Guide](administration/ADMINISTRATOR_GUIDE.md) · [Kubernetes Runtime Configuration](administration/KUBERNETES_RUNTIME_CONFIGURATION.md) · [Security Overview](security/SECURITY_OVERVIEW.md) |
| Operations / platform | [Operations Manual](operations/OPERATIONS_MANUAL.md) · [Production-Equivalent Validation Runbook](operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md) |
| Architecture / engineering | [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) · [Frontend Architecture](architecture/FRONTEND_ARCHITECTURE.md) · [UI/API Contract](architecture/UI_API_CONTRACT.md) |
| Governance / compliance | [Governance Mapping Registry](governance/GOVERNANCE_MAPPING_REGISTRY.md) · [Framework Governance](governance/FRAMEWORK_GOVERNANCE.md) · [Data Classification & Retention](governance/DATA_CLASSIFICATION_RETENTION.md) |
| QA / release | [QA and Release Gates](qa/QA_AND_RELEASE_GATES.md) · [Evidence Index](evidence/EVIDENCE_INDEX.md) |
| Product / delivery | [Product Guide](product/PRODUCT_GUIDE.md) · [Unified Operations Workbench](ux/UNIFIED_OPERATIONS_WORKBENCH.md) · [Roadmaps](roadmap/) |

## Product and user documentation

DTMO's canonical Unified Operations Workbench covers governed threat collection, intelligence discovery, IOC exploration, analysis and enrichment, knowledge graphs, vulnerability intelligence, investigations, sharing, automation, operational analytics, administration and governance evidence.

Key workspace documentation:

- [Unified Intelligence](user/UNIFIED_INTELLIGENCE_WORKSPACE.md)
- [IntelOwl Enrichment Workflow](user/INTELOWL_ENRICHMENT_WORKFLOW.md)
- [Integrated Analysis Workspace](user/INTEGRATED_ANALYSIS_WORKSPACE.md)
- [OpenCTI Graph / Entity Workspace](user/OPENCTI_GRAPH_ENTITY_WORKSPACE.md)
- [MISP Sharing & Exchange](user/MISP_SHARING_EXCHANGE_WORKSPACE.md)
- [TheHive Investigations](user/THEHIVE_INVESTIGATIONS_WORKSPACE.md)
- [Vulnerability & Exposure](user/VULNERABILITY_EXPOSURE_WORKSPACE.md)
- [Sources & Collection](user/SOURCES_COLLECTION_WORKSPACE.md)
- [Automation & Playbooks](user/AUTOMATION_PLAYBOOKS_WORKSPACE.md)
- [Governance & Evidence](user/GOVERNANCE_EVIDENCE_WORKSPACE.md)

These guides describe canonical workflows and authority boundaries. Browser visibility does not grant review, case creation, connector execution, external sharing, publication, administrative or production authority.

## Administration and operations

Administration and operations material is separated from analyst guidance so operational control, credentials and platform lifecycle decisions stay explicit.

Primary references include:

- [Administrator Guide](administration/ADMINISTRATOR_GUIDE.md)
- [Kubernetes Runtime Configuration](administration/KUBERNETES_RUNTIME_CONFIGURATION.md)
- [Operations Manual](operations/OPERATIONS_MANUAL.md)
- [IntelOwl Enrichment Runbook](operations/INTELOWL_ENRICHMENT_RUNBOOK.md)
- [OpenCTI Integration Runbook](operations/OPENCTI_INTEGRATION_RUNBOOK.md)
- [TheHive Handoff Runbook](operations/THEHIVE_HANDOFF_RUNBOOK.md)
- [Cortex Analyzer Runbook](operations/CORTEX_ANALYZER_RUNBOOK.md)
- [Production-Equivalent Validation Runbook](operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md)

Runtime credentials remain server-side. Operational success does not automatically establish source truth, local compromise, publication authority, remediation or production readiness.

## Architecture and integration contracts

Architecture documentation defines canonical state, trust boundaries, APIs, upstream integration behavior and persistence contracts. Start with [System Architecture](architecture/SYSTEM_ARCHITECTURE.md), then use the integration-specific contracts where needed.

Important integration references include:

- `architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md`
- `integrations/OPENCTI_INTEGRATION.md`
- `operations/OPENCTI_INTEGRATION_RUNBOOK.md`
- `qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md`
- `qa/PHASE11_4_OPENCTI_PERSISTENCE_GATE.md`
- `architecture/MISP_DTMO_CONSOLIDATION_CONTRACT.md`
- `integrations/MISP_READ_INTEGRATION.md`
- `intelligence/MISP_GOVERNED_EXPORT.md`
- `architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md`
- `integrations/THEHIVE_HANDOFF.md`
- `operations/THEHIVE_HANDOFF_RUNBOOK.md`
- `user/THEHIVE_CASE_HANDOFF.md`
- `administration/THEHIVE_HANDOFF_CONFIGURATION.md`
- `qa/PHASE11_6_THEHIVE_HANDOFF_IMPLEMENTATION_GATE.md`
- `integrations/CORTEX_ANALYZER_CONNECTOR.md`
- `operations/CORTEX_ANALYZER_RUNBOOK.md`
- `qa/PHASE11_7_CORTEX_DECISION_GATE.md`
- `qa/PHASE11_7B_CORTEX_CONNECTOR_GATE.md`

Stable repository contract markers remain explicit for compatibility with the integration documentation gates: **Phase 11.3 IntelOwl**, **Phase 11.4 OpenCTI**, **Phase 11.5 MISP**, **Phase 11.6 TheHive Handoff Implementation Gate**, **Phase 11.7 Cortex Decision Gate** and the later Cortex analyzer connector boundary. These accepted service boundaries remain `PASS / REPOSITORY_COMPLETE`; they are repository lifecycle markers, not claims of external environment readiness.

## Security and governance

Security, governance and compliance interpretation are maintained as separate professional domains:

- [Security Overview](security/SECURITY_OVERVIEW.md)
- [Threat Model](security/THREAT_MODEL.md)
- [Risk Register](security/RISK_REGISTER.md)
- [Governance Mapping Registry](governance/GOVERNANCE_MAPPING_REGISTRY.md)
- [Framework Governance](governance/FRAMEWORK_GOVERNANCE.md)
- [Data Classification & Retention](governance/DATA_CLASSIFICATION_RETENTION.md)

The governance registry contains explicit typed, partial repository-backed relationships for Normenkader IBP, MITRE ATT&CK, NIST CSF and CVSS context. Those mappings are evidence relationships, not certification, blanket compliance, semantic equivalence or proof of environment effectiveness. Missing mappings remain unmapped rather than inferred.

## Platform engineering and recovery

The accepted Phase 11.8 / 11.9 industrialisation baseline remains `PASS / REPOSITORY_COMPLETE` across runtime, identity/secrets, ingress/network, HA, observability, recovery, supply chain, capacity, upgrade/rollback and forward-first migration compatibility. Application rollback does not authorize automatic database down migration.

Core references remain explicitly discoverable:

- `architecture/PHASE11_8_RUNTIME_FOUNDATION.md` and `administration/KUBERNETES_RUNTIME_CONFIGURATION.md`
- `architecture/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS.md`, `administration/WORKLOAD_IDENTITY_EXTERNAL_SECRETS.md`, `operations/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_RUNBOOK.md` and `qa/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_GATE.md`
- `architecture/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION.md`, `administration/INGRESS_TLS_NETWORK_SEGMENTATION.md`, `operations/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION_RUNBOOK.md` and `qa/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION_GATE.md`
- `architecture/PHASE11_8D_HA_DISRUPTION.md`, `operations/PHASE11_8D_HA_DISRUPTION_RUNBOOK.md` and `qa/PHASE11_8D_HA_DISRUPTION_GATE.md`
- `architecture/PHASE11_8E_OBSERVABILITY_HARDENING.md`, `operations/PHASE11_8E_OBSERVABILITY_RUNBOOK.md` and `qa/PHASE11_8E_OBSERVABILITY_GATE.md`
- `architecture/PHASE11_8F_RECOVERY_HARDENING.md`, `operations/PHASE11_8F_RECOVERY_RUNBOOK.md` and `qa/PHASE11_8F_RECOVERY_GATE.md`
- `security/PHASE11_8G_SUPPLY_CHAIN_HARDENING.md`, `operations/PHASE11_8G_SUPPLY_CHAIN_RUNBOOK.md` and `qa/PHASE11_8G_SUPPLY_CHAIN_GATE.md`
- `architecture/PHASE11_9_MIGRATION_COMPATIBILITY.md`, `operations/PHASE11_9_MIGRATION_COMPATIBILITY_RUNBOOK.md` and `qa/PHASE11_9_MIGRATION_COMPATIBILITY_GATE.md`

## Quality, evidence and release validation

Repository tests and CI validate repository-controlled contracts. They do not prove that a specific live or production-equivalent environment behaved correctly.

The Phase 11.10 production-equivalent validation package remains:

- `qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`
- `operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`
- `evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`
- `../tools/phase11_production_equivalent_validation.py`
- `../backend/tests/test_phase11_10_production_equivalent_validation.py`
- `../.github/workflows/phase11-production-equivalent-validation.yml`

Production-equivalent validation requires fresh candidate identity, migration/compatibility, upgrade, rollback, health, saturation and recovery evidence for the **same immutable candidate** and one production-equivalent environment. Historical evidence cannot be reused to satisfy that gate. Missing, ambiguous, inaccessible, historical-only or mixed-candidate evidence fails closed.

The governed screenshot catalogue UI-01 through UI-10 remains documentation illustration only; synthetic screenshots are not operational evidence, live-connectivity proof, staging acceptance, production-equivalent evidence, external assurance or production authorization.

## Current lifecycle reference

Detailed project chronology belongs in [Current State](project/CURRENT_STATE.md), [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md) and the [roadmap directory](roadmap/), not at the top of this documentation portal.

For compatibility with the authoritative lifecycle ledger, the current concise position is: Phases 1–7 `PASS`; RC13 `PASS / OWNER_ACCEPTED`; E8.1–E8.10 `PASS / REPOSITORY_COMPLETE`; Phase 8 `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE`; Phase 9 `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`; Phase 10 `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1–11.9 `PASS / REPOSITORY_COMPLETE`; Phase 11.10 `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`; Phase 11.11 `NOT STARTED`; Phase 12 `NOT STARTED`. Production remains **not production authorized**.

Historical Phase 8/9 evidence remains candidate-bound audit history and cannot be reused for the materially changed Phase 11 candidate. Repository CI remains engineering evidence only.

## Documentation maintenance

Professional documentation should describe stable product behavior, operational procedures, trust boundaries and current lifecycle truth without turning the portal into an execution log. Detailed phase sequencing belongs in `roadmap/`; exact run history belongs in evidence records rather than product-facing navigation.

Whenever lifecycle state, architecture, security boundaries, product scope or governance claims materially change, affected documents and documentation-contract tests must be reconciled in the same bounded PR. Historical evidence is preserved rather than rewritten to support a new candidate.
