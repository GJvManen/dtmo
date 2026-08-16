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
| Phase 11.1 Taranis architecture/contract | `PASS / REPOSITORY_COMPLETE` | Service/API/licensing boundary accepted |
| Phase 11.2 Taranis canonical adapter | `PASS / REPOSITORY_COMPLETE` | Repository implementation accepted |
| Phase 11.3 IntelOwl | `IN PROGRESS / CONTRACT BASELINE IN EXACT-HEAD VALIDATION` | Current bounded integration gate |
| Phase 11 platform industrialisation | `IN PROGRESS / ACTIVE` | Highest-priority programme |
| Phase 12 production authorization | `NOT STARTED` | New decision only after integrated validation and assurance |

## Decision interpretation

The project has not received a production `GO`. The accountable decision is to industrialise the platform before a new authorization attempt.

The accepted functional, Phase 8 and Phase 9 evidence remains valid for the candidate it covered. Because Phase 11 materially changes the architecture, that evidence cannot be treated as production acceptance of the future integrated platform.

Taranis repository integration through Phase 11.2 is accepted, but that does not prove live composed-platform production behavior. The current engineering decision is to establish and validate the IntelOwl service/API/security/licensing boundary before any enrichment adapter is merged.

## Phase 11 required progression

1. **Completed:** Taranis AI architecture/API/data-model/identity/licensing assessment.
2. **Completed:** Taranis → DTMO canonical adapter repository implementation.
3. **Active:** accept the IntelOwl integration contract, then implement bounded enrichment.
4. Integrate OpenCTI for STIX entities and relationships.
5. Consolidate MISP inbound/outbound authority and synchronization.
6. Add TheHive incident/case handoff.
7. Adopt Cortex only if a documented analyzer/orchestration gap remains after IntelOwl.
8. Industrialise the composed runtime with Kubernetes/Helm/GitOps, HA, secrets, network policy, observability, backup/recovery and supply-chain controls.
9. Complete migration/compatibility.
10. Execute new production-equivalent validation.
11. Execute new independent external assurance.
12. Enter Phase 12 for the next formal production GO/NO-GO.

## IntelOwl decision boundary

The proposed Phase 11.3 contract requires:

- separate IntelOwl service/API integration rather than source vendoring;
- a dedicated non-admin service identity and runtime-secret API token;
- TLS verification outside local development;
- explicit observable and analyzer/playbook allowlists;
- TLP/privacy-aware external-disclosure controls;
- bounded job/rate-limit/failure behavior;
- analyzer/job/result provenance;
- external IntelOwl Connectors excluded from the initial enrichment path;
- analyzer verdicts treated as context, not local-compromise proof;
- AGPL-3.0 licensing review before embedding, modification, redistribution or modified network-service operation.

## Decision rules

- Green CI is repository engineering evidence, not production authorization.
- Functional owner acceptance is not independent assurance.
- Historical Phase 8/9 evidence remains deployment/candidate-bound.
- A material integrated-platform change requires fresh validation and assurance.
- A framework mapping is not a blanket compliance or maturity claim.
- Technical administration, collectors, publishers, enrichment engines or platform integrations do not grant publication/share authority.
- Missing or inaccessible mandatory evidence is not implicit acceptance.
- Service-to-service integrations must preserve provenance, classification and least privilege.
- Taranis source code remains outside the DTMO repository under the accepted service boundary.
- IntelOwl/pyIntelOwl source must not be vendored or redistributed by this programme without explicit AGPL licensing review.

## Principal decision inputs

Decision makers should use, in order:

1. `CURRENT_STATE.md`;
2. `../roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`;
3. `../architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md`;
4. `../integrations/INTELOWL_INTEGRATION.md`;
5. `../architecture/TARANIS_PLATFORM_INTEGRATION_ASSESSMENT.md`;
6. `../architecture/TARANIS_DTMO_INTEGRATION_CONTRACT.md`;
7. `PRODUCTION_READINESS_REPORT.md`;
8. `PRODUCTION_CHECKLIST.md`;
9. `../roadmap/PRODUCTION_ROADMAP.md`;
10. `../production/PHASE10_PRODUCTION_GO_NO_GO.md`;
11. `../evidence/EVIDENCE_INDEX.md`;
12. `../security/SECURITY_OVERVIEW.md`.

## Current decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1 and 11.2 are repository-complete. Phase 11.3 IntelOwl is active. DTMO remains not production authorized; Phase 12 is the next production authorization gate after Phase 11.10/11.11 evidence is accepted.**