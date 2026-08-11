# DTMO Documentation

This directory contains the authoritative architecture, security, governance, QA and production-readiness documentation for DTMO.

## Current baseline

- **Release candidate:** `16.0.0rc12`
- **Repository-controlled engineering:** Phases 1–7 accepted
- **Phase 6:** manually/externally accepted by the project owner on 2026-08-11
- **RC13 functional console acceptance:** `BLOCKED_INTERNAL`
- **RC13.1:** accepted via PR #151
- **RC13.2:** accepted via PR #152 (`b8c254c5d099cde5dca624aa85b17c320594847e`)
- **RC13.3:** accepted via PR #153 (`2e1029a43f7b44d8525fb89197d0a10458a3e992`)
- **RC13.4:** current priority — repository-backed Governance knowledge surface, `PENDING_CI`
- **Phase 8:** `PAUSED_PENDING_RC13`
- **Production readiness:** not yet complete

The next formal gate is **RC13.4**, not external staging. Phase 8 may resume only after RC13.5 completes the full functional browser acceptance and accountable owner acceptance.

## Project overview

- [Project homepage](../README.md)
- [Current project state](project/CURRENT_STATE.md)
- [Executive status](project/EXECUTIVE_STATUS.md)
- [Production roadmap](roadmap/PRODUCTION_ROADMAP.md)
- [RC13 functional console acceptance gate](qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md)
- [16.0.0rc12 release notes](releases/16.0.0rc12.md)

## Architecture and engineering

- [System architecture](architecture/SYSTEM_ARCHITECTURE.md)
- [Frontend UX architecture](ux/FRONTEND_UX.md)
- [Traceability matrix](traceability/TRACEABILITY_MATRIX.md)
- [Evidence index](evidence/EVIDENCE_INDEX.md)

The canonical application shell integrates source operations, intelligence investigation, native analytics, governed principal/role administration and governance while retaining explicit authorization and approval boundaries.

Normal product analytics are native DTMO views. Grafana remains an authenticated operational/advanced deployment component and is not a prerequisite for canonical console analytics.

RC13.3 introduced an auditable managed-principal/role registry. Built-in roles remain server-side controlled. Production bearer tokens remain externally issued; managed assignment changes require identity-provider reconciliation or token reissue and never silently rewrite active token claims.

## Intelligence sources

- [Source connection matrix](qa/SOURCE_CONNECTION_MATRIX.md)
- [Curated source catalog](intelligence/SOURCE_CATALOG.md)
- [Safe source execution gate](qa/SAFE_SOURCE_EXECUTION_GATE.md)

Operational vendor feeds are connected through governed built-in or unified-framework adapters. Research references can remain visible without being treated as executable feeds. Secret values are never stored in the source catalog or registry.

## Security and governance

- [Governance mapping registry](governance/GOVERNANCE_MAPPING_REGISTRY.md)
- [Security overview](security/SECURITY_OVERVIEW.md)
- [Security policy](../SECURITY.md)
- [Licensing](legal/LICENSING.md)
- [Third-party material](legal/THIRD_PARTY.md)
- [ADR-001 — evidence and claim boundaries](project/ADR/ADR-001-EVIDENCE-CLAIM-BOUNDARIES.md)

RC13.4 exposes a read-only repository-backed governance snapshot in the canonical Governance tab. Normenkader IBP and MITRE ATT&CK remain explicitly `UNMAPPED` until curated control/technique datasets exist. CVSS is `CONTEXT_ONLY` because canonical ingest currently has severity/free metadata but no first-class vector/base-score field. Internal DTMO governance mappings remain traceable to repository evidence.

Core invariants include RBAC, least privilege, service-account isolation, administrator safety controls, separation of duties, privacy/data minimization, provenance preservation, auditability and separate human review/share approval. Technical execution, Administration access or Governance visibility never grants publication authority.

## Accessibility

- [Frontend UX release gate](qa/FRONTEND_UX_RELEASE_GATE.md)
- [RC9.16 assistive-technology acceptance](qa/RC9_16_ASSISTIVE_TECHNOLOGY_EVIDENCE.md)

Phase 6 is accepted. The final manual/external accessibility blocker was closed by accountable project-owner acceptance on 2026-08-11; the repository does not invent unprovided test-environment metadata.

## Staging and external assurance

- [Phase 8 staging deployment-parity gate](qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md)
- [Phase 9 external assurance gate](qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md)

Phase 8 is currently **paused pending RC13**. Once RC13 is accepted, Phase 8 will still require one immutable production-equivalent staging deployment and the complete deployment-parity evidence package.

## Operations

- [Operations manual](operations/OPERATIONS_MANUAL.md)
- [Development run log](development/RUN_LOG.md)

## QA evidence model

`docs/qa/` contains gate-specific acceptance criteria and evidence decisions. Missing, queued, skipped, cancelled, failed, stale, inaccessible or inferred evidence is never treated as automated `PASS`.

Manual/external acceptance is recorded explicitly as such and is never presented as machine-generated evidence. Historical evidence remains point-in-time evidence and is not rewritten to make current claims appear green.
