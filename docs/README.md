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

## Current application and source releases

- [16.0.0rc9 release notes](releases/16.0.0rc9.md) — safe registered-source execution candidate
- [Curated intelligence source catalog](intelligence/SOURCE_CATALOG.md)
- [Safe source execution QA gate](qa/SAFE_SOURCE_EXECUTION_GATE.md)
- [RUN-172 safe source execution](development/runs/RUN-20260810-172.md)
- [16.0.0rc8 release notes](releases/16.0.0rc8.md) — accepted Admin Configuration & Source Registry baseline
- [16.0.0rc6 release notes](releases/16.0.0rc6.md) — accepted professional frontend baseline
- [Frontend UX architecture](ux/FRONTEND_UX.md)
- [Frontend UX release gate](qa/FRONTEND_UX_RELEASE_GATE.md)

The primary DTMO Threat Operations Console is available at `http://localhost:8000/`. Source administration is available at `/ui/admin-sources`. The presentation layer remains subordinate to server-side RBAC, separation of duties and human share approval.

## Intelligence sources

The source catalog distinguishes catalogued, registered, enabled, executable, ingested, reviewed and share-approved states. Catalog membership or source execution never grants publication authority. rc9 directly supports CISA KEV, NIST NVD CVE API 2.0, GitHub Global Security Advisories and governed custom feeds implementing the DTMO JSON v1 contract. Additional NCSC-NL, CERT-EU, vendor and education-sector sources remain explicit onboarding targets until their parser/access contracts are evidenced.

## Architecture

- [System architecture](architecture/SYSTEM_ARCHITECTURE.md)
- [Frontend UX architecture](ux/FRONTEND_UX.md)

## Security and governance

- [Security overview](security/SECURITY_OVERVIEW.md)
- [External assurance gate](qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md)
- [Staging deployment-parity gate](qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md)
- [Frontend UX release gate](qa/FRONTEND_UX_RELEASE_GATE.md)
- [Safe source execution gate](qa/SAFE_SOURCE_EXECUTION_GATE.md)
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

Phases 1–7 remain internally accepted within their documented claim boundaries. rc8 is the accepted Admin Configuration & Source Registry baseline; rc9 safe registered-source execution is `CI_VALIDATION_PENDING`. Phase 6 remains externally blocked for genuine VoiceOver/NVDA execution. Phase 8 remains externally blocked for one approved real staging deployment and the complete ten-class deployment-parity package. Phase 9 remains incomplete pending independent evidence. Phase 10 remains blocked until all prior gates and external acceptance requirements are complete.
