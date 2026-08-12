# DTMO Stakeholder Guide

## Purpose

DTMO documentation serves different decision makers. This guide identifies the shortest authoritative reading path for each audience and prevents technical implementation evidence from being mistaken for business, security or production approval.

## Executive and sponsor

Start with:

1. `docs/project/EXECUTIVE_STATUS.md`
2. `docs/project/PRODUCTION_READINESS_REPORT.md`
3. `docs/roadmap/PRODUCTION_ROADMAP.md`

Focus on current readiness, material risks, outstanding gates and decisions. Detailed CI history is supporting evidence rather than the executive status itself.

## Product owner and delivery

Start with:

1. `docs/project/CURRENT_STATE.md`
2. `docs/project/PROJECT_GOVERNANCE.md`
3. `docs/roadmap/PRODUCTION_ROADMAP.md`
4. `docs/ux/FRONTEND_UX.md`

Use these documents to distinguish accepted product behavior from planned enhancement work and from production-readiness requirements.

## CISO, security reviewer and risk owner

Start with:

1. `docs/security/SECURITY_OVERVIEW.md`
2. `docs/project/PRODUCTION_READINESS_REPORT.md`
3. `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`
4. `docs/traceability/TRACEABILITY_MATRIX.md`
5. `docs/qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md`

Security claims must remain attributable to explicit controls and evidence. Framework mappings are not inferred from descriptive similarity.

## Architect and engineer

Start with:

1. `docs/architecture/SYSTEM_ARCHITECTURE.md`
2. `docs/api/`
3. `docs/intelligence/SOURCE_CATALOG.md`
4. `docs/security/SECURITY_OVERVIEW.md`
5. `docs/project/GLOSSARY.md`

Engineering decisions that materially change components, trust boundaries, persistence, authorization or deployment assumptions require corresponding professional-documentation updates.

## QA and release management

Start with:

1. `docs/qa/QA_AND_RELEASE_GATES.md`
2. `docs/project/PRODUCTION_CHECKLIST.md`
3. `docs/evidence/EVIDENCE_INDEX.md`
4. `docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md`

Apply exact-head discipline. Evidence from a different commit or deployment must not be silently reused for a new acceptance identity.

## Operations

Start with:

1. `docs/operations/OPERATIONS_MANUAL.md`
2. `docs/architecture/SYSTEM_ARCHITECTURE.md`
3. `docs/project/PRODUCTION_CHECKLIST.md`
4. `docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md`

Operational readiness includes observability, recovery, deployment controls and accountable environment evidence; local development convenience is not a production control.

## Governance and compliance

Start with:

1. `docs/project/PROJECT_GOVERNANCE.md`
2. `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`
3. `docs/traceability/TRACEABILITY_MATRIX.md`
4. `docs/project/DOCUMENT_CONTROL.md`

Treat `UNMAPPED` and `CONTEXT_ONLY` as intentional truth states, not documentation gaps that may be filled by inference.

## External assessor

Start with:

1. `docs/project/PRODUCTION_READINESS_REPORT.md`
2. `docs/architecture/SYSTEM_ARCHITECTURE.md`
3. `docs/security/SECURITY_OVERVIEW.md`
4. `docs/qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md`
5. `docs/evidence/EVIDENCE_INDEX.md`

External assessors should receive evidence scoped to the approved target environment and deployment identity. Repository-controlled evidence can establish engineering facts but does not replace observations required from the assessed environment.

## Universal interpretation rule

When documents appear to conflict, prefer the most specific authoritative document for the claim and verify that its evidence applies to the same commit, release or deployment. Do not upgrade a status because a less-specific document uses broader language. Material inconsistencies should be corrected as documentation defects.
