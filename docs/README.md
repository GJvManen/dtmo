# DTMO Documentation

This directory contains the authoritative architecture, security, governance, QA and production-readiness documentation for DTMO.

## Current baseline

- **Release candidate:** `16.0.0rc12`
- **Repository-controlled engineering:** Phases 1–7 accepted
- **Phase 6:** manually/externally accepted by the project owner on 2026-08-11
- **Phase 8:** `READY_FOR_EXTERNAL_VALIDATION`
- **Production readiness:** not yet complete

The next formal gate is external validation of one immutable production-equivalent staging deployment.

## Project overview

- [Project homepage](../README.md)
- [Current project state](project/CURRENT_STATE.md)
- [Executive status](project/EXECUTIVE_STATUS.md)
- [Production roadmap](roadmap/PRODUCTION_ROADMAP.md)
- [16.0.0rc12 release notes](releases/16.0.0rc12.md)

## Architecture and engineering

- [System architecture](architecture/SYSTEM_ARCHITECTURE.md)
- [Frontend UX architecture](ux/FRONTEND_UX.md)
- [Traceability matrix](traceability/TRACEABILITY_MATRIX.md)
- [Evidence index](evidence/EVIDENCE_INDEX.md)

The current architecture combines a Python/FastAPI application layer with PostgreSQL, OpenSearch, Redis, object evidence storage, Prometheus, Grafana and an Nginx gateway. The canonical application shell integrates source operations, administration, intelligence investigation and analytics while retaining explicit authorization and approval boundaries.

## Intelligence sources

- [Source connection matrix](qa/SOURCE_CONNECTION_MATRIX.md)
- [Curated source catalog](intelligence/SOURCE_CATALOG.md)
- [Safe source execution gate](qa/SAFE_SOURCE_EXECUTION_GATE.md)

Operational vendor feeds are connected through governed built-in or unified-framework adapters. Research references can remain visible without being treated as executable feeds. Secret values are never stored in the source catalog or registry.

## Security and governance

- [Security overview](security/SECURITY_OVERVIEW.md)
- [Security policy](../SECURITY.md)
- [Licensing](legal/LICENSING.md)
- [Third-party material](legal/THIRD_PARTY.md)
- [ADR-001 — evidence and claim boundaries](project/ADR/ADR-001-EVIDENCE-CLAIM-BOUNDARIES.md)

Core invariants include RBAC, least privilege, separation of duties, privacy/data minimization, provenance preservation, auditability and separate human review/share approval. Technical execution never grants publication authority.

## Accessibility

- [Frontend UX release gate](qa/FRONTEND_UX_RELEASE_GATE.md)
- [RC9.16 assistive-technology acceptance](qa/RC9_16_ASSISTIVE_TECHNOLOGY_EVIDENCE.md)

Phase 6 is accepted. The final manual/external accessibility blocker was closed by accountable project-owner acceptance on 2026-08-11; the repository does not invent unprovided test-environment metadata.

## Staging and external assurance

- [Phase 8 staging deployment-parity gate](qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md)
- [Phase 9 external assurance gate](qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md)

Phase 8 is ready for external project-owner validation after the final repository cleanup is merged. All staging evidence must be tied to one immutable release/deployment identity.

## Operations

- [Operations manual](operations/OPERATIONS_MANUAL.md)
- [Development run log](development/RUN_LOG.md)

Operational setup, deployment procedures and historical execution detail intentionally live outside the project homepage so that the root README remains a professional project overview rather than an operations log.

## QA evidence model

`docs/qa/` contains gate-specific acceptance criteria and evidence decisions. Missing, queued, skipped, cancelled, failed, stale, inaccessible or inferred evidence is never treated as automated `PASS`.

Manual/external acceptance is recorded explicitly as such and is never presented as machine-generated evidence.
