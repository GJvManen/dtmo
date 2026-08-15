# DTMO Executive Decision View

## Purpose

This document gives accountable decision makers the concise current decision position for DTMO production readiness and the active successor programme.

## Current position

| Decision area | Current state | Decision consequence |
|---|---|---|
| Repository-controlled engineering | `PASS` for Phases 1–7 | Engineering foundation accepted |
| Functional product | `RC13 PASS / OWNER_ACCEPTED` | Canonical product journey accepted |
| E8 vulnerability/CTI product line | `PASS / REPOSITORY_COMPLETE` | Product capabilities repository-complete |
| Phase 8 production-equivalent staging | `PASS / OWNER_ACCEPTED` | Historical staging evidence accepted for prior candidate |
| Phase 9 independent assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` | Historical assurance accepted for prior candidate |
| Phase 10 production authorization | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` | Production authorization not granted |
| Phase 11 platform industrialisation | `IN PROGRESS / ACTIVE` | Highest-priority programme |
| Phase 12 production authorization | `NOT STARTED` | New decision only after integrated validation and assurance |

## Decision interpretation

The project has not received a production `GO`. The accountable decision is to industrialise the platform before a new authorization attempt.

The accepted functional, Phase 8 and Phase 9 evidence remains valid for the candidate it covered. Because Phase 11 materially changes the architecture, that evidence cannot be treated as production acceptance of the future integrated platform.

## Phase 11 required progression

1. Complete Taranis AI architecture/API/data-model/identity/licensing assessment.
2. Implement the Taranis → DTMO canonical adapter.
3. Integrate IntelOwl enrichment.
4. Integrate OpenCTI for STIX entities and relationships.
5. Consolidate MISP inbound/outbound authority and synchronization.
6. Add TheHive incident/case handoff.
7. Adopt Cortex only if a documented analyzer/orchestration gap remains.
8. Industrialise the composed runtime with Kubernetes/Helm/GitOps, HA, secrets, network policy, observability, backup/recovery and supply-chain controls.
9. Complete migration/compatibility.
10. Execute new production-equivalent validation.
11. Execute new independent external assurance.
12. Enter Phase 12 for the next formal production GO/NO-GO.

## Decision rules

- Green CI is repository engineering evidence, not production authorization.
- Functional owner acceptance is not independent assurance.
- Historical Phase 8/9 evidence remains deployment/candidate-bound.
- A material integrated-platform change requires fresh validation and assurance.
- A framework mapping is not a blanket compliance or maturity claim.
- Technical administration, collectors, publishers or platform integrations do not grant publication/share authority.
- Missing or inaccessible mandatory evidence is not implicit acceptance.
- Service-to-service integrations must preserve provenance, classification and least privilege.
- Taranis source code must not be copied into DTMO before licensing review.

## Principal decision inputs

Decision makers should use, in order:

1. `CURRENT_STATE.md`;
2. `../roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`;
3. `../architecture/TARANIS_PLATFORM_INTEGRATION_ASSESSMENT.md`;
4. `PRODUCTION_READINESS_REPORT.md`;
5. `PRODUCTION_CHECKLIST.md`;
6. `../roadmap/PRODUCTION_ROADMAP.md`;
7. `../production/PHASE10_PRODUCTION_GO_NO_GO.md`;
8. `../evidence/EVIDENCE_INDEX.md`;
9. `../security/SECURITY_OVERVIEW.md`.

## Current decision

**Phase 10 is `NO-GO / BLOCKED`. Phase 11 is active. DTMO remains not production authorized; Phase 12 is the next production authorization gate.**