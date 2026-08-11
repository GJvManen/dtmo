# DTMO Documentation

This directory contains the authoritative architecture, security, governance, QA and production-readiness documentation for DTMO.

## Current baseline

- **Release candidate:** `16.0.0rc12`
- **Repository-controlled engineering:** Phases 1–7 accepted
- **Phase 6:** manually/externally accepted by the project owner on 2026-08-11
- **RC13.1–RC13.5 repository-controlled evidence:** `PASS`
- **RC13 accountable owner functional retest:** `PASS` on 2026-08-12
- **RC13 overall:** `PASS`
- **Phase 8:** `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`
- **Production readiness:** not yet complete

The project owner explicitly accepted the repaired canonical product with `RC13 owner retest akkoord` on 2026-08-12. Issue #150 is closed. The current priority is **Phase 8.1 — establish one approved production-equivalent staging environment and immutable deployment identity**.

## Project overview

- [Project homepage](../README.md)
- [Current project state](project/CURRENT_STATE.md)
- [Executive status](project/EXECUTIVE_STATUS.md)
- [Production roadmap](roadmap/PRODUCTION_ROADMAP.md)
- [RC13 functional console acceptance gate](qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md)
- [Phase 8 staging deployment-parity gate](qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md)
- [Phase 8 external deployment identity record](staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md)
- [Staging acceptance plan](staging/STAGING_ACCEPTANCE_PLAN.md)
- [16.0.0rc12 release notes](releases/16.0.0rc12.md)

## Architecture and engineering

- [System architecture](architecture/SYSTEM_ARCHITECTURE.md)
- [Frontend UX architecture](ux/FRONTEND_UX.md)
- [Traceability matrix](traceability/TRACEABILITY_MATRIX.md)
- [Evidence index](evidence/EVIDENCE_INDEX.md)

The canonical application shell integrates source operations, intelligence investigation, native analytics, governed principal/role administration and Governance while retaining explicit authorization and approval boundaries.

## RC13 accepted product evidence

The accepted one-session journey is:

**Overview → Intelligence → Sources & Catalog → register/enable/run → Intelligence update → Visual analytics → Administration → Governance → Overview state confirmation.**

Repository-controlled browser evidence remains synthetic. The separate owner acceptance on 2026-08-12 closes RC13 without rewriting historical CI evidence.

## Intelligence sources

- [Source connection matrix](qa/SOURCE_CONNECTION_MATRIX.md)
- [Curated source catalog](intelligence/SOURCE_CATALOG.md)
- [Safe source execution gate](qa/SAFE_SOURCE_EXECUTION_GATE.md)

Operational vendor feeds remain governed by their accepted source framework. Secret values are never stored in source catalog or repository evidence.

## Security and governance

- [Governance mapping registry](governance/GOVERNANCE_MAPPING_REGISTRY.md)
- [Security overview](security/SECURITY_OVERVIEW.md)
- [Security policy](../SECURITY.md)
- [Licensing](legal/LICENSING.md)
- [Third-party material](legal/THIRD_PARTY.md)
- [ADR-001 — evidence and claim boundaries](project/ADR/ADR-001-EVIDENCE-CLAIM-BOUNDARIES.md)

Normenkader IBP and MITRE ATT&CK remain explicitly `UNMAPPED`, CVSS remains `CONTEXT_ONLY`, and internal DTMO governance mappings remain repository-backed. Missing framework crosswalks are never inferred.

Core invariants include RBAC, least privilege, service-account isolation, administrator safety controls, separation of duties, privacy/data minimization, provenance preservation, auditability and separate human review/share approval. Technical execution, Administration access, Governance visibility or staging access never grants publication authority.

## Staging and external assurance

- [Phase 8 staging deployment-parity gate](qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md)
- [Phase 8 external deployment identity record](staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md)
- [Phase 9 external assurance gate](qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md)

Phase 8 is open for external validation but is **not accepted**. Phase 8.1 remains `PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`: the current repository does not prove a real production-equivalent staging deployment. All later evidence must bind to one immutable external deployment identity.

## Operations

- [Operations manual](operations/OPERATIONS_MANUAL.md)
- [Development run log](development/RUN_LOG.md)

## QA evidence model

Missing, queued, skipped, cancelled, failed, stale, inaccessible or inferred evidence is never treated as automated `PASS`. Manual/external acceptance is recorded explicitly as such and is never presented as machine-generated evidence. Historical run records remain immutable point-in-time evidence.