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

## Current frontend release candidate

- [16.0.0rc6 release notes](releases/16.0.0rc6.md)
- [Frontend UX architecture](ux/FRONTEND_UX.md)
- [Frontend UX release gate](qa/FRONTEND_UX_RELEASE_GATE.md)
- [RUN-162 professional frontend UX overhaul](development/runs/RUN-20260810-162.md)
- [16.0.0rc5 release notes](releases/16.0.0rc5.md) — accepted predecessor baseline

The primary DTMO Threat Operations Console is available at `http://localhost:8000/` after a successful local build. rc6 organizes the experience around Overview, Intelligence, Governance, Audit and Security and aligns the Analyst, Share Approval, Auditor and CISO role views to the same design system. The frontend remains a presentation layer over server-side RBAC and does not weaken human share-approval or separation-of-duties requirements.

## Architecture

- [System architecture](architecture/SYSTEM_ARCHITECTURE.md)
- [Frontend UX architecture](ux/FRONTEND_UX.md)

## Security and governance

- [Security overview](security/SECURITY_OVERVIEW.md)
- [External assurance gate](qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md)
- [Staging deployment-parity gate](qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md)
- [Frontend UX release gate](qa/FRONTEND_UX_RELEASE_GATE.md)
- [Security policy](../SECURITY.md)

## Operations

- [Operations manual](operations/OPERATIONS_MANUAL.md)

Local/external-test Compose startup requires all fail-closed secret placeholders in `.env` to be replaced with externally supplied values/references, including `OPENSEARCH_INITIAL_ADMIN_PASSWORD`, AIStor image identity, license-file path and administrative credentials. Real secret values must not be committed.

## Evidence and traceability

- [Evidence index](evidence/EVIDENCE_INDEX.md)
- [Traceability matrix](traceability/TRACEABILITY_MATRIX.md)

## Architecture decisions

- [ADR-001 — evidence and claim boundaries](project/ADR/ADR-001-EVIDENCE-CLAIM-BOUNDARIES.md)

## QA and evidence model

`docs/qa/` contains gate-specific acceptance criteria and evidence decisions. A QA document may only state `PASS` when the referenced evidence was actually executed, retained and reviewable. Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is never a pass.

## Governance invariants

DTMO preserves RBAC, separation of duties, privacy, provenance, auditability and human share approval. Review and share approval remain distinct human decisions. Technical access, connector execution, emulator/staging access, CI success or operational recovery do not grant publication authority.

## Current release posture

Phases 1–5 are internally accepted. Phase 6 remains externally blocked for genuine VoiceOver/NVDA execution; the repository-controlled rc5 frontend baseline is accepted and rc6 professional UX remains `CI_VALIDATION_PENDING`. Phase 7 is accepted. Phase 8 remains externally blocked for one approved real staging deployment and the complete ten-class deployment-parity package. Phase 9 has an external-assurance intake contract but remains incomplete until the required independent evidence is produced. Phase 10 remains blocked until all prior gates and external acceptance requirements are complete.
