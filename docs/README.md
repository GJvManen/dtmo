# DTMO Documentation Portal

This directory contains the authoritative professional documentation for Dutch Threat Monitoring for Education (DTMO). Stable product, architecture, security, governance and readiness documentation is separated from immutable operational history and CI evidence.

## Current controlled baseline

| Area | Current state |
|---|---|
| Software baseline | `16.0.0rc12` plus accepted post-RC13/E8/Phase-11 repository enhancements |
| Phases 1–7 | `PASS` |
| RC13 functional product acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 production-equivalent staging | `PASS / OWNER_ACCEPTED` |
| Phase 9 independent assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 production go/no-go | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11.3 IntelOwl integration | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.4 OpenCTI integration | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.5 MISP consolidation | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.6 TheHive | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.7 Cortex decision gate | `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE` |
| Phase 11.7b Cortex analyzer connector | `IN PROGRESS / OWNER-REQUIRED EXACT-HEAD VALIDATION` |
| Phase 11.8 runtime industrialisation | `NOT STARTED / BLOCKED BY 11.7b` |
| Phase 12 production go/no-go | `NOT STARTED` |
| Production readiness | **not production authorized** |

The active bounded programme step is **Phase 11.7b Cortex analyzer connector**. The earlier Phase 11.7 no-adoption decision remains preserved as historical evidence for the requirement set that existed at that time. On 2026-08-17 the accountable owner added Cortex connector integration as a new attributable requirement. Phase 10 did not grant production authorization. Fresh Phase 11.10 production-equivalent validation and Phase 11.11 independent external assurance remain required before Phase 12.

## Start here

| Audience | Primary documents |
|---|---|
| Executive / sponsor | [Executive Status](project/EXECUTIVE_STATUS.md), [Executive Decision View](project/EXECUTIVE_DECISION_VIEW.md), [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md) |
| Product / delivery | [Product Guide](product/PRODUCT_GUIDE.md), [Platform Industrialisation Roadmap](roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md), [Current State](project/CURRENT_STATE.md), [Production Roadmap](roadmap/PRODUCTION_ROADMAP.md) |
| Analyst / reviewer | [User Guide](user/USER_GUIDE.md), [IntelOwl Governed Enrichment Workflow](user/INTELOWL_ENRICHMENT_WORKFLOW.md), [TheHive Case Handoff Workflow](user/THEHIVE_CASE_HANDOFF.md), [System Workflows](architecture/SYSTEM_WORKFLOWS.md), [Screenshot Catalogue](visual/screenshots/README.md) |
| Administrator | [Administrator Guide](administration/ADMINISTRATOR_GUIDE.md), [TheHive Handoff Configuration](administration/THEHIVE_HANDOFF_CONFIGURATION.md), [Cortex Analyzer Runbook](operations/CORTEX_ANALYZER_RUNBOOK.md), [OpenCTI Integration Runbook](operations/OPENCTI_INTEGRATION_RUNBOOK.md), [Security Overview](security/SECURITY_OVERVIEW.md) |
| Architecture / engineering | [Cortex → DTMO Integration Contract](architecture/CORTEX_DTMO_INTEGRATION_CONTRACT.md), [Cortex Analyzer Connector](integrations/CORTEX_ANALYZER_CONNECTOR.md), [Cortex Historical Decision Gate](architecture/CORTEX_DECISION_GATE.md), [TheHive → DTMO Handoff Contract](architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md), [MISP → DTMO Consolidation Contract](architecture/MISP_DTMO_CONSOLIDATION_CONTRACT.md), [OpenCTI → DTMO Integration Contract](architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md), [OpenCTI Integration](integrations/OPENCTI_INTEGRATION.md), [IntelOwl → DTMO Integration Contract](architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md), [Taranis → DTMO Contract](architecture/TARANIS_DTMO_INTEGRATION_CONTRACT.md) |
| Security / CISO | [Security Overview](security/SECURITY_OVERVIEW.md), [Threat Model](security/THREAT_MODEL.md), [Risk Register](security/RISK_REGISTER.md), [Cortex Integration Contract](architecture/CORTEX_DTMO_INTEGRATION_CONTRACT.md) |
| Governance / compliance | [Governance Mapping Registry](governance/GOVERNANCE_MAPPING_REGISTRY.md), [Data Classification & Retention](governance/DATA_CLASSIFICATION_RETENTION.md) |
| QA / release | [QA and Release Gates](qa/QA_AND_RELEASE_GATES.md), [Phase 11.7b Cortex Connector Gate](qa/PHASE11_7B_CORTEX_CONNECTOR_GATE.md), [Phase 11.7 Cortex Decision Gate](qa/PHASE11_7_CORTEX_DECISION_GATE.md), [Phase 11.6 TheHive Handoff Implementation Gate](qa/PHASE11_6_THEHIVE_HANDOFF_IMPLEMENTATION_GATE.md), [Phase 11.5 MISP Consolidation Contract Gate](qa/PHASE11_5_MISP_CONSOLIDATION_CONTRACT_GATE.md), [Phase 11.4 OpenCTI Contract Gate](qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md), [Evidence Index](evidence/EVIDENCE_INDEX.md) |
| Operations | [Operating Model](operations/OPERATING_MODEL.md), [Operations Manual](operations/OPERATIONS_MANUAL.md), [Cortex Analyzer Runbook](operations/CORTEX_ANALYZER_RUNBOOK.md), [TheHive Handoff Operations Runbook](operations/THEHIVE_HANDOFF_RUNBOOK.md), [IntelOwl Enrichment Runbook](operations/INTELOWL_ENRICHMENT_RUNBOOK.md), [OpenCTI Integration Runbook](operations/OPENCTI_INTEGRATION_RUNBOOK.md) |

The governed screenshot catalogue now contains UI-01 through UI-10 and remains the controlled visual reference for accepted operator journeys. These governed screenshots are documentation illustrations rather than proof of live-source connectivity, staging acceptance or production readiness.

No synthetic screenshot is promoted for integrations or architecture decisions without an accepted operator GUI or live evidence surface. Phase 11.7b introduces repository-side Cortex adapter behavior but no accepted live Cortex operator surface, so a synthetic Cortex screenshot would be false evidence.

## Phase 11 programme documentation

- [Platform Industrialisation Roadmap](roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md) defines the controlled sequence and the owner-required Phase 11.7b insertion before runtime industrialisation.
- Phase 11.3 IntelOwl, Phase 11.4 OpenCTI, Phase 11.5 MISP and Phase 11.6 TheHive are `PASS / REPOSITORY_COMPLETE` repository engineering boundaries.
- [Cortex Decision Gate](architecture/CORTEX_DECISION_GATE.md) preserves the accepted historical Phase 11.7 no-adoption decision for the then-current requirement set.
- [Cortex → DTMO Integration Contract](architecture/CORTEX_DTMO_INTEGRATION_CONTRACT.md) records the new attributable owner requirement and analyzer-only authority boundary.
- [Cortex Analyzer Connector](integrations/CORTEX_ANALYZER_CONNECTOR.md) defines the implementation/configuration surface.
- [Phase 11.7b Cortex Connector Gate](qa/PHASE11_7B_CORTEX_CONNECTOR_GATE.md) defines exact-head acceptance for the new bounded integration.
- [Evidence Index](evidence/EVIDENCE_INDEX.md) keeps repository evidence separate from deployment, assurance and production authorization evidence.

## Phase 11.7b trust boundary

```mermaid
flowchart LR
    D[DTMO canonical observable] --> G{Approved type + analyzer + TLP?}
    G -->|no| X[Fail closed]
    G -->|yes| C[Cortex REST API\nseparate service identity]
    C --> J[Analyzer job]
    J --> R[Bounded report]
    R --> E[DTMO enrichment evidence\nshare=false\ncompromise=false]
    C -. excluded .-> Z[Responders / side effects]
```

## Security and authority invariants

- server-side RBAC and least privilege remain authoritative;
- human and service identities remain separate;
- publication/share authority remains human-controlled;
- TheHive case-handoff authority remains distinct from publication/share authority;
- IntelOwl and Cortex enrichment do not grant share authority or prove local compromise;
- Cortex responders and external side-effect actions remain excluded from Phase 11.7b;
- Cortex analyzer IDs and datatypes are explicit allowlists and production requires HTTPS plus a runtime API key;
- Taranis, IntelOwl, OpenCTI, MISP, TheHive and Cortex remain separate services under their applicable licensing/provider boundaries.

## Evidence and history model

Professional current-state documentation describes the present controlled state. Historical records under `docs/development/` and earlier Phase 8/9 evidence remain scoped to the candidate and moment they originally covered; they are not rewritten or reused as evidence for the materially changed Phase 11 candidate. The accepted Phase 11.7 Cortex decision record also remains historical and is not rewritten to pretend the later owner requirement existed earlier.

Repository CI and documentation-contract tests are engineering evidence only. They do not prove live provider coverage, production permissions, staging acceptance, independent assurance or production readiness.

## Maintenance rule

Whenever lifecycle state, architecture, security boundary, product scope or governance claims materially change, affected professional documents and documentation-contract tests must be reconciled in the same bounded PR before merge. See [Documentation Status and Authority](project/DOCUMENTATION_STATUS.md), [Documentation Standard](project/DOCUMENTATION_STANDARD.md) and [Visual Documentation Standard](visual/DOCUMENTATION_VISUAL_STANDARD.md).
