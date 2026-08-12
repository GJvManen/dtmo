# DTMO Documentation

This directory contains the authoritative architecture, security, governance, QA and production-readiness documentation for DTMO.

## Current baseline

- **Release candidate:** `16.0.0rc12`
- **Repository-controlled engineering:** Phases 1–7 accepted
- **RC13.1–RC13.5 historical repository evidence:** `PASS`
- **Earlier RC13 owner acceptance:** recorded on 2026-08-12
- **RC13 current decision:** `REOPENED / BLOCKED_INTERNAL`
- **Phase 8:** `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`
- **Phase 9:** `NOT COMPLETE`
- **Phase 10:** `NOT STARTED`
- **Production readiness:** not complete

A subsequent project-owner functional retest on 2026-08-12 found blocking canonical-console defects after the earlier RC13 acceptance. Issue #150 is reopened. Phase 8 issue #158 is paused until the repair is exact-head green, merged and explicitly accepted by the project owner again.

## Current owner-observed blockers

- Overview `Alles vernieuwen` was not a reliable operator action.
- Empty intelligence could still produce `Data bijgewerkt`.
- Buttons were not reliably functional under Chrome.
- The navigation version badge was unnecessary.
- Administration was insufficiently clear.
- Empty graph datasets were visually ambiguous.

The current repair adds truthful refresh/empty-state behavior, explicit Chrome-channel interaction evidence, zero page/console-error requirements and a clearer governed Administration surface.

## Project overview

- [Project homepage](../README.md)
- [Current project state](project/CURRENT_STATE.md)
- [Executive status](project/EXECUTIVE_STATUS.md)
- [Production roadmap](roadmap/PRODUCTION_ROADMAP.md)
- [RC13 functional console acceptance gate](qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md)
- [Phase 8 staging deployment-parity gate](qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md)
- [Phase 8 external deployment identity record](staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md)

## Architecture and engineering

- [System architecture](architecture/SYSTEM_ARCHITECTURE.md)
- [Frontend UX architecture](ux/FRONTEND_UX.md)
- [Traceability matrix](traceability/TRACEABILITY_MATRIX.md)
- [Evidence index](evidence/EVIDENCE_INDEX.md)

The canonical application shell integrates source operations, intelligence investigation, native analytics, governed principal/role administration and Governance while retaining explicit authorization and approval boundaries.

## Evidence boundary

The earlier one-session RC13.5 journey and owner acceptance remain historical evidence. They are not erased. Newer owner-observed product defects control the **current** release decision, so RC13 is reopened until the current repair is accepted.

Synthetic Chrome/browser fixtures cannot manufacture project-owner acceptance. After merge, the owner must retest the repaired local product.

## Intelligence sources

- [Source connection matrix](qa/SOURCE_CONNECTION_MATRIX.md)
- [Curated source catalog](intelligence/SOURCE_CATALOG.md)
- [Safe source execution gate](qa/SAFE_SOURCE_EXECUTION_GATE.md)

Secret values are never stored in source catalog or repository evidence.

## Security and governance

- [Governance mapping registry](governance/GOVERNANCE_MAPPING_REGISTRY.md)
- [Security overview](security/SECURITY_OVERVIEW.md)
- [Security policy](../SECURITY.md)
- [Licensing](legal/LICENSING.md)
- [Third-party material](legal/THIRD_PARTY.md)

Normenkader IBP and MITRE ATT&CK remain `UNMAPPED`, CVSS remains `CONTEXT_ONLY`, and internal DTMO governance mappings remain repository-backed. Missing framework crosswalks are never inferred.

RBAC, least privilege, service-account isolation, administrator safety controls, separation of duties, privacy/data minimization, provenance, auditability and separate human review/share approval remain authoritative. Technical execution, Administration access, Governance visibility or staging access never grants publication authority.

## Staging and external assurance

Phase 8 is paused. The fail-closed deployment identity record remains preparatory evidence with `evidence_complete: false`; no external deployment is accepted while RC13 is reopened.

## Operations

- [Operations manual](operations/OPERATIONS_MANUAL.md)
- [Development run log](development/RUN_LOG.md)

## QA evidence model

Missing, queued, skipped, cancelled, failed, stale, inaccessible or inferred evidence is never `PASS`. Manual/external acceptance is recorded explicitly. Historical run records remain immutable point-in-time evidence.
