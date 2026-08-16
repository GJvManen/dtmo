# DTMO Documentation Status and Authority

Last reconciled: **2026-08-16**

## Purpose

This document defines which DTMO documents are authoritative for the current product and lifecycle state, which records are historical/immutable, and how conflicts are resolved.

## Authority order

For current project decisions, use this order:

1. `docs/project/CURRENT_STATE.md` — current controlled product and lifecycle state;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md` — active Phase 11 programme and fixed priority order;
3. `docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md` — accepted Phase 11.3 service/API/security/licensing contract;
4. `docs/integrations/INTELOWL_INTEGRATION.md` — active bounded IntelOwl adapter implementation/operations boundary;
5. Taranis assessment/contract/adapter documentation — accepted Phase 11.1–11.2 service boundary;
6. `docs/roadmap/PRODUCTION_ROADMAP.md` — production-readiness sequence from Phase 10 NO-GO to Phase 12;
7. `docs/project/PRODUCTION_READINESS_REPORT.md` and `PRODUCTION_CHECKLIST.md` — consolidated readiness and evidence completion state;
8. `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md` — completed accountable no-go decision;
9. architecture, security, governance and QA documents — domain-specific design and claim boundaries;
10. `docs/evidence/EVIDENCE_INDEX.md` — evidence classes and authoritative evidence locations.

If a historical run record conflicts with a later current-state decision, both remain valid in their own scope: the historical record describes what was true at that point in time; current-state documents describe the present controlled state.

## Current documentation baseline

| Document class | Status | Maintenance expectation |
|---|---|---|
| Root README / docs portal | `CURRENT` | Update on material product or lifecycle change |
| Current state / executive views | `CURRENT` | Reconcile together on lifecycle change |
| Platform Industrialisation Roadmap | `CURRENT / ACTIVE` | Maintain through Phase 11 |
| Taranis assessment/contract/adapter docs | `CURRENT / ACCEPTED` | Preserve accepted boundary |
| IntelOwl integration contract | `CURRENT / ACCEPTED` | Preserve accepted service/API/security/licensing baseline |
| IntelOwl integration guide | `CURRENT / ADAPTER IN VALIDATION` | Document implemented bounded behavior without claiming live runtime evidence |
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
- Phase 8: `PASS / OWNER_ACCEPTED`;
- Phase 9: `PASS / EXTERNAL_ASSURANCE_ACCEPTED`;
- Phase 10: `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`;
- Phase 11: `IN PROGRESS / ACTIVE`;
- Phase 11.1: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.2: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.3 IntelOwl contract: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.3 IntelOwl adapter: `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- Phase 12: `NOT STARTED`;
- DTMO: **not production authorized**.

## Active Phase 11.3 documentation rule

The contract baseline is accepted and the bounded adapter is implemented in the active PR. Documentation may therefore describe the adapter's repository behavior, configuration and synthetic test contract, but it must not imply live IntelOwl connectivity, deployed service identity, provider credentials, durable enrichment-history persistence, production-equivalent behavior or an accepted operator UI.

The active documentation preserves these boundaries:

- IntelOwl remains a separate service/API component; no IntelOwl/pyIntelOwl source is vendored;
- runtime-secret authentication and production HTTPS are required;
- explicit observable and analyzer/playbook allowlisting precede disclosure;
- TLP/privacy controls fail closed;
- `connectors_requested=[]` excludes IntelOwl external Connector side effects from the bounded path;
- analyzer/job/result provenance and immutable job identity are retained;
- malformed/oversized results, unknown analyzers and job-ID mismatches fail closed;
- analyzer verdicts do not establish local compromise;
- enrichment never grants DTMO external-share/publication authority;
- AGPL-3.0 review remains required before embedding, modification or redistribution;
- repository CI is not live integration or production evidence.

## Evidence and claim rules

Professional documentation may record an external or accountable decision only when that evidence class exists. Repository CI cannot manufacture staging acceptance. Owner staging acceptance cannot manufacture independent assurance. Independent assurance cannot manufacture production authorization.

Prior Phase 8/9 evidence remains valid for the prior candidate but cannot be silently transferred to a materially changed Phase 11 integrated platform. Fresh production-equivalent validation and independent assurance are required before Phase 12.

Framework mappings and enrichment results are bounded claims. A framework mapping does not imply blanket compliance, and an IntelOwl analyzer/provider verdict is attributed context rather than proof of local exposure or compromise.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only when the document is clearly an immutable point-in-time record under the operational evidence layer. Historical text must not be used as the primary current-state source.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and the professional documentation contract tests before protected merge. Current lifecycle state must be reconciled across the root README, documentation portal, current state, executive views, readiness report/checklist, documentation status, evidence index, QA/release gates, production roadmap and active Phase 11 roadmap/contract/integration documents. Historical Phase 8/9 and Phase 10 evidence claims remain preserved in their original scope.
