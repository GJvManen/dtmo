# DTMO Documentation Status and Authority

Last reconciled: **2026-08-16**

## Purpose

This document defines which DTMO documents are authoritative for the current product/lifecycle state, which records are historical/immutable, and how conflicts are resolved.

## Authority order

For current project decisions, use this order:

1. `docs/project/CURRENT_STATE.md` — current controlled product and lifecycle state;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md` — active Phase 11 programme and fixed priority order;
3. `docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md` — active Phase 11.4 service/API/STIX/identity/security/licensing contract;
4. `docs/integrations/OPENCTI_INTEGRATION.md` — planned bounded OpenCTI adapter/synchronization boundary;
5. `docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md` and IntelOwl integration/runbook/user documentation — accepted Phase 11.3 boundary;
6. Taranis assessment/contract/adapter documentation — accepted Phase 11.1–11.2 boundary;
7. `docs/roadmap/PRODUCTION_ROADMAP.md` — production-readiness sequence from Phase 10 NO-GO to Phase 12;
8. `docs/project/PRODUCTION_READINESS_REPORT.md` and `PRODUCTION_CHECKLIST.md` — consolidated readiness/evidence completion state;
9. `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md` — completed accountable no-go decision;
10. architecture, security, governance and QA documents — domain-specific design and claim boundaries;
11. `docs/evidence/EVIDENCE_INDEX.md` — evidence classes and authoritative evidence locations.

If a historical run record conflicts with a later current-state decision, both remain valid in their own scope: the historical record describes what was true at that point; current-state documents describe the present controlled state.

## Current documentation baseline

| Document class | Status | Maintenance expectation |
|---|---|---|
| Root README / docs portal | `CURRENT` | Update on material product/lifecycle change |
| Current state / executive views | `CURRENT` | Reconcile together on lifecycle change |
| Platform Industrialisation Roadmap | `CURRENT / ACTIVE` | Maintain through Phase 11 |
| Taranis assessment/contract/adapter docs | `CURRENT / ACCEPTED` | Preserve accepted boundary |
| IntelOwl contract/integration/runbook/user docs | `CURRENT / ACCEPTED` | Preserve repository-complete Phase 11.3 boundary |
| OpenCTI contract | `CURRENT / IN EXACT-HEAD VALIDATION` | Active Phase 11.4 authority boundary |
| OpenCTI integration/runbook | `CURRENT / CONTRACT-PLANNED` | Document planned behavior without live-runtime claims |
| Production roadmap/readiness/checklist | `CURRENT` | Reconcile together on readiness-gate change |
| Phase 10 decision record | `CURRENT / DECIDED` | Preserve NO-GO decision and successor rationale |
| System architecture | `CURRENT — STABLE DESIGN` | Update for accepted component/trust/data-flow changes |
| Security model | `CURRENT — STABLE CONTROL MODEL` | Update when identity/authorization/security boundaries change |
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
- Phase 11.1: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.2: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.3 IntelOwl: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.4 OpenCTI contract: `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- Phase 12: `NOT STARTED`;
- DTMO: **not production authorized**.

## Active Phase 11.4 documentation rule

Documentation may describe the OpenCTI contract and planned adapter behavior, but it must not imply live OpenCTI connectivity, deployed credentials/RBAC/markings, completed STIX synchronization, production graph correctness, production-equivalent behavior or an accepted OpenCTI operator UI.

The active documentation preserves these boundaries:

- OpenCTI remains a separate service/API component; no OpenCTI source is vendored;
- Community Edition Apache-2.0 and separate Enterprise Edition licensing are distinguished;
- Enterprise-only dependencies require explicit entitlement/legal approval;
- dedicated non-human least-privilege identity and runtime secrets are required;
- administrator/`Bypass all capabilities` and connector privileges are not routine requirements;
- GraphQL, STIX 2.1, TAXII 2.1 and access-controlled stream surfaces are bounded;
- OpenCTI/STIX and DTMO canonical identity domains stay separate and explicitly mapped;
- markings/TLP/PAP, confidence and provenance are preserved;
- unknown markings, malformed/unsupported STIX and authorization failures fail closed;
- future replay/checkpoint handling must be durable, restart-safe and idempotent;
- connector registration, MISP synchronization, enrichment, case creation and publication are excluded from the first adapter path;
- graph context does not establish local compromise/exposure or DTMO share/publication authority;
- repository CI is not live integration or production evidence.

No synthetic screenshot is promoted for this contract slice because no accepted OpenCTI operator GUI surface exists.

## Evidence and claim rules

Professional documentation may record an external/accountable decision only when that evidence class exists. Repository CI cannot manufacture staging acceptance; owner acceptance cannot manufacture independent assurance; independent assurance cannot manufacture production authorization.

Prior Phase 8/9 evidence remains valid for the prior candidate but cannot be silently transferred to the materially changed Phase 11 integrated platform. Fresh Phase 11.10 validation and Phase 11.11 independent assurance are required before Phase 12.

Framework mappings, IntelOwl enrichment and OpenCTI graph relationships remain bounded claims. They do not imply blanket compliance, local exposure or compromise without separate attributable evidence.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only where the document is clearly an immutable point-in-time record. Historical text must not be used as the primary current-state source or rewritten to manufacture later acceptance.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and professional documentation contract tests before protected merge. Current lifecycle state is reconciled across the root README, documentation portal, current state, executive views, readiness report/checklist, documentation status, evidence index, QA/release gates, production roadmap and active Phase 11 roadmap/contract/integration documents. Historical Phase 8/9 and Phase 10 evidence claims remain preserved in their original scope.
