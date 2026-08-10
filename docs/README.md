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

## Current release candidate

- [16.0.0rc5 release notes](releases/16.0.0rc5.md)
- [Frontend release gate](qa/FRONTEND_RELEASE_GATE.md)
- [RUN-161 frontend productionization](development/runs/RUN-20260810-161.md)

After a successful 16.0.0rc5 build, the governed DTMO Console is available at `http://localhost:8000/`. The console is a presentation layer over existing server-side RBAC and does not change authorization or human share-approval requirements.

## Architecture

- [System architecture](architecture/SYSTEM_ARCHITECTURE.md)

## Security and governance

- [Security overview](security/SECURITY_OVERVIEW.md)
- [External assurance gate](qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md)
- [Staging deployment-parity gate](qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md)
- [Frontend release gate](qa/FRONTEND_RELEASE_GATE.md)
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

Phases 1–5 are internally accepted. Phase 6 remains externally blocked for genuine VoiceOver/NVDA execution; the 16.0.0rc5 root-console candidate is separately `CI_VALIDATION_PENDING`. Phase 7 is accepted. Phase 8 remains externally blocked for one approved real staging deployment and the complete ten-class deployment-parity package. Phase 9 has an external-assurance intake contract but remains incomplete until the required independent evidence is produced. Phase 10 remains blocked until all prior gates and external acceptance requirements are complete.
