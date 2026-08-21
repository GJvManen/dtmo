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
| Analyst / reviewer | [Governance & Evidence](user/GOVERNANCE_EVIDENCE_WORKSPACE.md), [Automation & Playbooks](user/AUTOMATION_PLAYBOOKS_WORKSPACE.md), [Sources & Collection](user/SOURCES_COLLECTION_WORKSPACE.md), [Vulnerability & Exposure](user/VULNERABILITY_EXPOSURE_WORKSPACE.md), [TheHive Investigations](user/THEHIVE_INVESTIGATIONS_WORKSPACE.md), [MISP Sharing & Exchange](user/MISP_SHARING_EXCHANGE_WORKSPACE.md), [Unified Intelligence](user/UNIFIED_INTELLIGENCE_WORKSPACE.md) |
| Administrator | [Administrator Guide](administration/ADMINISTRATOR_GUIDE.md), [Kubernetes Runtime Configuration](administration/KUBERNETES_RUNTIME_CONFIGURATION.md), [Security Overview](security/SECURITY_OVERVIEW.md) |
| Architecture / engineering | [Phase 11.10l Governance & Evidence](architecture/PHASE11_10L_GOVERNANCE_EVIDENCE.md), [Frontend Architecture](architecture/FRONTEND_ARCHITECTURE.md), [UI/API Contract](architecture/UI_API_CONTRACT.md), [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) |
| Governance / compliance | [Governance Mapping Registry](governance/GOVERNANCE_MAPPING_REGISTRY.md), [Framework Governance](governance/FRAMEWORK_GOVERNANCE.md), [Data Classification & Retention](governance/DATA_CLASSIFICATION_RETENTION.md) |
| Security / CISO | [Security Overview](security/SECURITY_OVERVIEW.md), [Threat Model](security/THREAT_MODEL.md), [Risk Register](security/RISK_REGISTER.md) |
| QA / release | [Phase 11.10l Governance & Evidence Gate](qa/PHASE11_10L_GOVERNANCE_EVIDENCE_GATE.md), [QA and Release Gates](qa/QA_AND_RELEASE_GATES.md), [Evidence Index](evidence/EVIDENCE_INDEX.md) |
| Operations | [Operations Manual](operations/OPERATIONS_MANUAL.md), [Phase 11.10 Production-Equivalent Validation Runbook](operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md) |

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

## Evidence and release rule

Every commit invalidates prior exact-head CI evidence. A bounded PR is accepted only when its final unchanged head is mergeable, ready for review, professionally documented and every workflow registered for that exact head is `completed/success`.

Fresh production-equivalent validation remains **Phase 11.10p**, only after 11.10a–11.10o are complete and one immutable integrated candidate is frozen. Phase 11.11 independent external assurance follows against that same candidate; Phase 12 is the later formal production GO/NO-GO.

## Documentation maintenance rule

Whenever lifecycle state, architecture, security boundaries, product scope or governance claims materially change, affected professional documents and documentation-contract tests must be reconciled in the same bounded PR. Historical evidence is preserved rather than rewritten to support a new candidate.
