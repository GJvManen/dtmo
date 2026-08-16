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
| Phase 11.3 IntelOwl contract | `PASS / REPOSITORY_COMPLETE` | Enrichment service/API/security/licensing baseline accepted |
| Phase 11.3 IntelOwl adapter | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Current bounded integration gate |
| Phase 11 platform industrialisation | `IN PROGRESS / ACTIVE` | Highest-priority programme |
| Phase 12 production authorization | `NOT STARTED` | New decision only after integrated validation and assurance |

## Decision interpretation

The project has not received a production `GO`. The accountable decision remains to industrialise the platform before a new authorization attempt.

The accepted functional, Phase 8 and Phase 9 evidence remains valid only for the candidate it originally covered. Because Phase 11 materially changes the architecture, that evidence cannot be treated as production acceptance of the future integrated platform.

Taranis repository integration through Phase 11.2 is accepted. The IntelOwl Phase 11.3 contract is also accepted. The active engineering decision is whether the bounded IntelOwl adapter satisfies its exact-head code, security and documentation gates; no live IntelOwl or production claim follows from repository acceptance.

## Phase 11 required progression

1. **Completed:** Taranis AI architecture/API/data-model/identity/licensing assessment.
2. **Completed:** Taranis → DTMO canonical adapter repository implementation.
3. **Active:** validate the bounded IntelOwl enrichment adapter; then complete governed execution/persistence and operational integration.
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

The accepted contract and active adapter preserve:

- separate IntelOwl service/API integration rather than source vendoring;
- a dedicated non-admin service identity and runtime-secret API token;
- production HTTPS validation;
- explicit observable and analyzer/playbook allowlists;
- TLP/privacy-aware external-disclosure controls;
- bounded job/rate-limit/failure behavior;
- immutable job correlation and analyzer/result provenance;
- IntelOwl external Connectors excluded from the enrichment path;
- unknown analyzers, job-ID mismatches and malformed/oversized results rejected fail-closed;
- analyzer verdicts treated as context, not local-compromise proof;
- no enrichment outcome granting DTMO publication/share authority;
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

Decision makers should use `CURRENT_STATE.md`, the Platform Industrialisation Roadmap, the IntelOwl integration contract and implementation guide, the Production Readiness Report, Production Checklist, Production Roadmap, Evidence Index and Security Overview. Immutable run/CI evidence remains separate from these stable decision documents.

## Current decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1 and 11.2 are repository-complete. The Phase 11.3 IntelOwl contract is repository-complete and the adapter is the active exact-head gate. DTMO remains not production authorized; Phase 12 is the next production authorization gate only after Phase 11.10/11.11 evidence is accepted.**
