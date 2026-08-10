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

- [16.0.0rc10 release notes](releases/16.0.0rc10.md)
- [RC10.3 Threat Intelligence Workspace Gate](qa/RC10_3_THREAT_INTELLIGENCE_WORKSPACE_GATE.md)
- [RUN-178 RC10.3 implementation](development/runs/RUN-20260810-178.md)
- [RC10.2 Unified Operational Dashboards Gate](qa/RC10_2_UNIFIED_DASHBOARDS_GATE.md)
- [RUN-177 RC10.2 acceptance reconciliation](development/runs/RUN-20260810-177.md)
- [RC10.1 Operations Workspace Gate](qa/OPERATIONS_WORKSPACE_GATE.md)

The unified Operations Workspace is available at `/ui/operations`. RC10.3 adds the Threat Intelligence investigation workspace at `/ui/intelligence-workspace`. The primary Threat Operations Console remains at `/`, and source administration at `/ui/admin-sources`. All presentation layers remain subordinate to server-side RBAC, separation of duties, privacy, provenance, auditability and human share approval.

## Intelligence sources and investigation

- [Curated intelligence source catalog](intelligence/SOURCE_CATALOG.md)
- [Safe source execution QA gate](qa/SAFE_SOURCE_EXECUTION_GATE.md)
- [RC10.3 Threat Intelligence Workspace Gate](qa/RC10_3_THREAT_INTELLIGENCE_WORKSPACE_GATE.md)

The accepted source pipeline distinguishes catalogued, registered, enabled, executable, ingested, reviewed and share-approved states. RC10.3 does not change those states; it adds a read-only investigation flow over stored canonical intelligence. Explicit CVE identifiers may be extracted from stored canonical text/tags. CISA KEV context is asserted only from stored source identity; vendor/product context is shown only when explicitly stored. Missing enrichment is never invented.

## Frontend and accessibility

- [Frontend UX architecture](ux/FRONTEND_UX.md)
- [Frontend UX release gate](qa/FRONTEND_UX_RELEASE_GATE.md)
- [RC10.1 Operations Workspace Gate](qa/OPERATIONS_WORKSPACE_GATE.md)
- [RC10.2 Unified Operational Dashboards Gate](qa/RC10_2_UNIFIED_DASHBOARDS_GATE.md)
- [RC10.3 Threat Intelligence Workspace Gate](qa/RC10_3_THREAT_INTELLIGENCE_WORKSPACE_GATE.md)

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
- [Existing Grafana operational dashboard gate](qa/RC10_8_OPERATIONAL_DASHBOARD_GATE.md)

The browser Operations Workspace exposes only bounded aggregate telemetry. The RC10.3 investigation detail similarly uses an explicit safe-field projection and does not expose raw storage/request/credential metadata.

## Evidence and traceability

- [Evidence index](evidence/EVIDENCE_INDEX.md)
- [Traceability matrix](traceability/TRACEABILITY_MATRIX.md)

## Architecture decisions

- [ADR-001 — evidence and claim boundaries](project/ADR/ADR-001-EVIDENCE-CLAIM-BOUNDARIES.md)

## QA and evidence model

`docs/qa/` contains gate-specific acceptance criteria and evidence decisions. A QA document may only state `PASS` when the referenced evidence was actually executed, retained and reviewable. Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is never a pass.

## Current release posture

Phases 1–7 remain internally accepted within their documented claim boundaries. RC10.1 and RC10.2 are accepted. RUN-178 / RC10.3 remains `CI_VALIDATION_PENDING` until the complete workflow matrix succeeds on one exact head. Phase 6 remains externally blocked for genuine VoiceOver/NVDA execution. Phase 8 remains externally blocked for one approved real staging deployment and the complete ten-class deployment-parity package. Phase 9 remains incomplete pending independent evidence. Phase 10 remains blocked until all prior gates and external acceptance requirements are complete.
