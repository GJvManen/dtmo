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
- [RC10.2 Unified Operational Dashboards Gate](qa/RC10_2_UNIFIED_DASHBOARDS_GATE.md)
- [RUN-176 RC10.2 dashboard implementation](development/runs/RUN-20260810-176.md)
- [RC10.1 Operations Workspace Gate](qa/OPERATIONS_WORKSPACE_GATE.md)
- [RUN-175 RC10.1 acceptance reconciliation](development/runs/RUN-20260810-175.md)

The unified Operations Workspace is available at `/ui/operations`. The primary Threat Operations Console remains available at `/`. Source administration is available at `/ui/admin-sources`. All presentation layers remain subordinate to server-side RBAC, separation of duties, privacy, provenance, auditability and human share approval.

## Intelligence sources

- [Curated intelligence source catalog](intelligence/SOURCE_CATALOG.md)
- [Safe source execution QA gate](qa/SAFE_SOURCE_EXECUTION_GATE.md)
- [16.0.0rc9 release notes](releases/16.0.0rc9.md)

The source catalog distinguishes catalogued, registered, enabled, executable, ingested, reviewed and share-approved states. Catalog membership or source execution never grants publication authority. The accepted rc9 baseline directly supports CISA KEV, NIST NVD CVE API 2.0, GitHub Global Security Advisories and governed DTMO JSON v1 feeds.

## Frontend and accessibility

- [Frontend UX architecture](ux/FRONTEND_UX.md)
- [Frontend UX release gate](qa/FRONTEND_UX_RELEASE_GATE.md)
- [RC10.1 Operations Workspace Gate](qa/OPERATIONS_WORKSPACE_GATE.md)
- [RC10.2 Unified Operational Dashboards Gate](qa/RC10_2_UNIFIED_DASHBOARDS_GATE.md)

RC10.2 replaces the RC10.1 synthetic dashboard placeholder with live read-only widgets derived from the existing Prometheus registry. Genuine VoiceOver/NVDA execution remains an external evidence requirement and is not inferred from browser automation.

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

The browser Operations Workspace exposes only bounded aggregate telemetry. Raw Prometheus label sets and sensitive request dimensions are not passed to the browser. Local/external-test Compose startup requires all fail-closed secret placeholders in `.env` to be replaced with externally supplied values/references; real secret values must not be committed.

## Evidence and traceability

- [Evidence index](evidence/EVIDENCE_INDEX.md)
- [Traceability matrix](traceability/TRACEABILITY_MATRIX.md)

## Architecture decisions

- [ADR-001 — evidence and claim boundaries](project/ADR/ADR-001-EVIDENCE-CLAIM-BOUNDARIES.md)

## QA and evidence model

`docs/qa/` contains gate-specific acceptance criteria and evidence decisions. A QA document may only state `PASS` when the referenced evidence was actually executed, retained and reviewable. Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is never a pass.

## Current release posture

Phases 1–7 remain internally accepted within their documented claim boundaries. RC10.1 is accepted; RUN-176 / RC10.2 remains `CI_VALIDATION_PENDING` until the complete workflow matrix succeeds on one exact head. Phase 6 remains externally blocked for genuine VoiceOver/NVDA execution. Phase 8 remains externally blocked for one approved real staging deployment and the complete ten-class deployment-parity package. Phase 9 remains incomplete pending independent evidence. Phase 10 remains blocked until all prior gates and external acceptance requirements are complete.
