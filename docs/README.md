# DTMO Documentation Index

This directory is the authoritative documentation entry point for DTMO. Detailed run records provide the audit trail; the documents below provide the current operational and production-readiness view.

## Project and production readiness

- [Current state](project/CURRENT_STATE.md)
- [Executive status](project/EXECUTIVE_STATUS.md)
- [Production readiness report](project/PRODUCTION_READINESS_REPORT.md)
- [Production checklist](project/PRODUCTION_CHECKLIST.md)
- [Lessons learned](project/LESSONS_LEARNED.md)
- [Production roadmap](roadmap/PRODUCTION_ROADMAP.md)
- [Development run log](development/RUN_LOG.md)

## Current application release

- [16.0.0rc12 release notes](releases/16.0.0rc12.md)
- [RC12.6 unified-console programme completion gate](qa/RC12_6_UNIFIED_CONSOLE_COMPLETION_GATE.md)
- [RC12.5b same-origin Grafana console gate](qa/RC12_5B_SAME_ORIGIN_GRAFANA_CONSOLE_GATE.md)
- [RC12.5a same-origin Grafana gateway gate](qa/RC12_5A_SAME_ORIGIN_GRAFANA_GATE.md)
- [RC12.4 unified Grafana embedding gate](qa/RC12_4_UNIFIED_GRAFANA_EMBEDDING_GATE.md)
- [RC12.3 least-privilege Grafana intelligence gate](qa/RC12_3_GRAFANA_INTELLIGENCE_READER_GATE.md)
- [RC12.2 Grafana dashboard gate](qa/RC12_2_GRAFANA_DASHBOARD_GATE.md)
- [RC12.1 unified source operations gate](qa/RC12_1_UNIFIED_SOURCE_OPERATIONS_GATE.md)
- [Source connection matrix](qa/SOURCE_CONNECTION_MATRIX.md)

The canonical application shell is available at `/` with `/ui/console` as an alias. Source catalog/operations, administration, intelligence investigation and graphical analytics are integrated into that shell. Grafana Operations and Intelligence dashboards are embedded through the managed same-origin `/grafana/` path. Legacy `/ui/*` routes may remain for compatibility but are not separate intended product shells.

All presentation layers remain subordinate to server-side RBAC, separation of duties, privacy, provenance, auditability and human share approval.

## Intelligence sources and investigation

- [Curated intelligence source catalog](intelligence/SOURCE_CATALOG.md)
- [Source connection matrix](qa/SOURCE_CONNECTION_MATRIX.md)
- [Safe source execution QA gate](qa/SAFE_SOURCE_EXECUTION_GATE.md)

The accepted source pipeline distinguishes catalogued, registered, enabled, executable, ingested, reviewed and share-approved states. The current operational vendor catalog is connected through governed built-in or unified-framework adapters. Research-reference sources remain deliberately non-executable where appropriate. Credential values are not stored in the catalog or source registry.

## Frontend and accessibility

- [Frontend UX architecture](ux/FRONTEND_UX.md)
- [Frontend UX release gate](qa/FRONTEND_UX_RELEASE_GATE.md)
- [RC12.6 unified-console programme completion gate](qa/RC12_6_UNIFIED_CONSOLE_COMPLETION_GATE.md)

Genuine VoiceOver/NVDA execution remains an external evidence requirement and is not inferred from browser automation.

## Architecture

- [System architecture](architecture/SYSTEM_ARCHITECTURE.md)
- [Frontend UX architecture](ux/FRONTEND_UX.md)

## Security and governance

- [Security overview](security/SECURITY_OVERVIEW.md)
- [External assurance gate](qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md)
- [Staging deployment-parity gate](qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md)
- [Safe source execution gate](qa/SAFE_SOURCE_EXECUTION_GATE.md)
- [Security policy](../SECURITY.md)

## Operations

- [Operations manual](operations/OPERATIONS_MANUAL.md)
- [RC12.2 Grafana dashboard gate](qa/RC12_2_GRAFANA_DASHBOARD_GATE.md)
- [RC12.3 least-privilege Grafana intelligence gate](qa/RC12_3_GRAFANA_INTELLIGENCE_READER_GATE.md)
- [RC12.5b same-origin Grafana console gate](qa/RC12_5B_SAME_ORIGIN_GRAFANA_CONSOLE_GATE.md)

Grafana does not reuse the DTMO application database identity for intelligence reporting. The accepted reporting datasource is constrained to explicit reporting views through a dedicated least-privilege role. Anonymous Grafana access remains disabled. Native console chart/table fallbacks remain available.

## Evidence and traceability

- [Evidence index](evidence/EVIDENCE_INDEX.md)
- [Traceability matrix](traceability/TRACEABILITY_MATRIX.md)

## Architecture decisions

- [ADR-001 — evidence and claim boundaries](project/ADR/ADR-001-EVIDENCE-CLAIM-BOUNDARIES.md)

## QA and evidence model

`docs/qa/` contains gate-specific acceptance criteria and evidence decisions. A QA document may only state `PASS` when the referenced evidence was actually executed, retained and reviewable. Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is never a pass.

## Current release posture

Phases 1–7 remain internally accepted within their documented claim boundaries. RC11 and RC12 repository-controlled programmes are complete and accepted through PR #148. Issue #125 is closed as completed. Phase 6 remains externally blocked for genuine VoiceOver/NVDA execution. Phase 8 remains externally blocked for one approved real staging deployment and the complete ten-class deployment-parity package. Phase 9 remains incomplete pending independent evidence. Phase 10 remains blocked until all prior gates and external acceptance requirements are complete.

## Exactly one next priority

Obtain the approved real Phase 8 staging deployment-parity evidence package tied to one immutable release/deployment identity.
