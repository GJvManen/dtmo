# DTMO Documentation Status and Authority

Last reconciled: **2026-08-17**

## Purpose

This document defines which DTMO documents are authoritative for the current product/lifecycle state, which records are historical/immutable, and how conflicts are resolved.

## Authority order

For current project decisions, use this order:

1. `docs/project/CURRENT_STATE.md` — current controlled product and lifecycle state;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md` — active Phase 11 programme and fixed priority order;
3. `docs/architecture/MISP_DTMO_CONSOLIDATION_CONTRACT.md` — accepted Phase 11.5 service/API/licensing/authority contract;
4. `docs/integrations/MISP_READ_INTEGRATION.md` and `docs/intelligence/MISP_GOVERNED_EXPORT.md` — existing inbound/outbound paths being reconciled;
5. `docs/qa/PHASE11_5_MISP_CONSOLIDATION_STATE_GATE.md` — active exact-head synchronization-state/persistence gate;
6. OpenCTI contract/integration/runbook documentation — accepted Phase 11.4 boundary;
7. IntelOwl integration documentation — accepted Phase 11.3 boundary;
8. Taranis assessment/contract/adapter documentation — accepted Phase 11.1–11.2 boundary;
9. `docs/roadmap/PRODUCTION_ROADMAP.md` — production-readiness sequence from Phase 10 NO-GO to Phase 12;
10. `docs/project/PRODUCTION_READINESS_REPORT.md` and `PRODUCTION_CHECKLIST.md` — consolidated readiness/evidence completion state;
11. `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md` — completed accountable no-go decision;
12. architecture, security, governance, QA and `docs/evidence/EVIDENCE_INDEX.md` — domain-specific boundaries and evidence classes.

Historical point-in-time records remain valid for what they originally described and are never rewritten to manufacture later acceptance.

## Current documentation baseline

| Document class | Status | Maintenance expectation |
|---|---|---|
| Root README / docs portal | `CURRENT` | Update on material product/lifecycle change |
| Current state / executive views | `CURRENT` | Reconcile together on lifecycle change |
| Platform Industrialisation Roadmap | `CURRENT / ACTIVE` | Maintain through Phase 11 |
| Taranis assessment/contract/adapter docs | `CURRENT / ACCEPTED` | Preserve accepted boundary |
| IntelOwl contract/integration/runbook/user docs | `CURRENT / ACCEPTED` | Preserve repository-complete Phase 11.3 boundary |
| OpenCTI contract/integration/persistence docs | `CURRENT / ACCEPTED` | Preserve repository-complete Phase 11.4 boundary |
| MISP consolidation contract | `CURRENT / ACCEPTED` | Preserve accepted Phase 11.5 contract boundary |
| MISP read/export documentation | `CURRENT / ACTIVE IMPLEMENTATION CONTEXT` | Keep synchronized with shared authority state |
| Phase 11.5 MISP state gate | `CURRENT / IN EXACT-HEAD VALIDATION` | Active persistence/authority implementation boundary |
| Production roadmap/readiness/checklist | `CURRENT` | Reconcile together on readiness-gate change |
| Phase 10 decision record | `CURRENT / DECIDED` | Preserve NO-GO decision and successor rationale |
| System architecture | `CURRENT — STABLE DESIGN` | Update for accepted component/trust/data-flow changes |
| Security model | `CURRENT — ACTIVE PHASE 11.5 CONTROL BOUNDARY` | Update when identity/authorization/security boundaries change |
| Governance mapping registry | `CURRENT — CONTROLLED CLAIM MODEL` | Update when mappings/framework semantics change |
| QA/release gates | `CURRENT — CONTROL MODEL` | Update when gate/evidence rules change |
| Historical phase runbooks/evidence | `HISTORICAL / SUPPORTING` | Never rewrite original evidence claims |
| `docs/development/runs/` | `HISTORICAL / IMMUTABLE` | Never rewrite to simulate current state |

## Current release truth

The professional documentation must consistently distinguish:

- Phases 1–7: `PASS`;
- RC13: `PASS / OWNER_ACCEPTED`;
- E8.1–E8.10: `PASS / REPOSITORY_COMPLETE`;
- Phase 8: `PASS / OWNER_ACCEPTED` for the earlier candidate;
- Phase 9: `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate;
- Phase 10: `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`;
- Phase 11: `IN PROGRESS / ACTIVE`;
- Phase 11.1–11.2 Taranis: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.3 IntelOwl: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.4 OpenCTI: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.5 MISP consolidation contract: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.5 MISP synchronization state/persistence: `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- Phase 12: `NOT STARTED`;
- DTMO: **not production authorized**.

## Active Phase 11.5 documentation rule

Documentation may describe repository-implemented MISP authority-state behavior but must not imply live MISP connectivity, deployed credentials/RBAC, lawful live-data sharing, successful remote delivery, federation behavior, production-equivalent behavior or an accepted new operator UI.

The active documentation preserves these boundaries:

- MISP v2.5.44 remains a separate AGPL-3.0 service/API component and source is not vendored;
- the existing `events/restSearch` read path and human-approved unpublished `events/add` path are reused rather than duplicated;
- one stable MISP event UUID maps to one canonical DTMO item;
- normalized distribution, sharing-group and TLP restrictions are persisted in `misp_synchronization_state`;
- accepted restrictions are projected to canonical `metadata_json.misp_restrictions` for governed export enforcement;
- canonical item creation and authority-state reconciliation occur before the database transaction commits;
- identity collision/drift, malformed/unknown restrictions and inbound share authority fail closed;
- database constraints preserve known distribution/sharing semantics and `external_share_authorized=false`;
- human review/share approval remains the only outbound authority;
- automatic publication, MISP push/pull federation, OpenCTI↔MISP synchronization, TheHive case creation and Cortex adoption remain excluded;
- repository CI is engineering evidence, not live integration or production evidence.

No synthetic screenshot is promoted because this persistence/authority slice introduces no accepted operator GUI surface.

## Evidence and claim rules

Repository CI cannot manufacture staging acceptance; owner acceptance cannot manufacture independent assurance; independent assurance cannot manufacture production authorization. Prior Phase 8/9 evidence remains valid only for the prior candidate. Fresh Phase 11.10 validation and Phase 11.11 independent assurance are required before Phase 12.

Framework mappings, IntelOwl enrichment, OpenCTI graph context and MISP event membership remain bounded claims and do not imply blanket compliance, local exposure, compromise or dissemination authority without separate attributable evidence.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only where the document is clearly an immutable point-in-time record. Historical text must not be used as the primary current-state source or rewritten to manufacture later acceptance.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and professional documentation contract tests before protected merge. Current lifecycle state is reconciled across the root README, documentation portal, current state, executive views, readiness report/checklist, documentation status, evidence index, QA/release gates, production roadmap and active Phase 11 roadmap/integration documents. Historical Phase 8/9 and Phase 10 evidence claims remain preserved in their original scope.
