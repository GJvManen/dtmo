# DTMO Documentation Status and Authority

Last reconciled: **2026-08-17**

## Purpose

This document defines which DTMO documents are authoritative for the current product/lifecycle state, which records are historical/immutable, and how conflicts are resolved.

## Authority order

For current project decisions, use this order:

1. `docs/project/CURRENT_STATE.md` — current controlled product and lifecycle state;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md` — active Phase 11 programme and fixed priority order;
3. `docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md` — accepted Phase 11.6 service/API/identity/licensing/authority contract;
4. `docs/integrations/THEHIVE_HANDOFF.md`, `docs/operations/THEHIVE_HANDOFF_RUNBOOK.md`, `docs/user/THEHIVE_CASE_HANDOFF.md` and `docs/administration/THEHIVE_HANDOFF_CONFIGURATION.md` — active bounded implementation and operational/user/admin boundary;
5. `docs/qa/PHASE11_6_THEHIVE_HANDOFF_IMPLEMENTATION_GATE.md` — active exact-head implementation gate;
6. `docs/qa/PHASE11_6_THEHIVE_HANDOFF_CONTRACT_GATE.md` — accepted contract evidence boundary;
7. MISP contract/read/export/state documentation — accepted Phase 11.5 boundary;
8. OpenCTI contract/integration/runbook documentation — accepted Phase 11.4 boundary;
9. IntelOwl integration documentation — accepted Phase 11.3 boundary;
10. Taranis assessment/contract/adapter documentation — accepted Phase 11.1–11.2 boundary;
11. `docs/roadmap/PRODUCTION_ROADMAP.md` — production-readiness sequence from Phase 10 NO-GO to Phase 12;
12. readiness, security, QA and `docs/evidence/EVIDENCE_INDEX.md` — domain-specific current-state/evidence boundaries;
13. `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md` — completed accountable no-go decision.

Historical point-in-time records remain valid for what they originally described and are never rewritten to manufacture later acceptance.

## Current documentation baseline

| Document class | Status | Maintenance expectation |
|---|---|---|
| Root README / docs portal | `CURRENT` | Update on material product/lifecycle change |
| Current state / executive views | `CURRENT` | Reconcile together on lifecycle change |
| Platform Industrialisation Roadmap | `CURRENT / ACTIVE` | Maintain through Phase 11 |
| Taranis / IntelOwl / OpenCTI / MISP accepted docs | `CURRENT / ACCEPTED` | Preserve accepted Phase 11.1–11.5 boundaries |
| TheHive contract docs | `CURRENT / ACCEPTED` | Preserve the accepted Phase 11.6 contract boundary |
| TheHive implementation/runbook/user/admin docs | `CURRENT / IN EXACT-HEAD VALIDATION` | Active Phase 11.6 bounded implementation |
| Phase 11.6 TheHive implementation gate | `CURRENT / IN EXACT-HEAD VALIDATION` | Active implementation acceptance boundary |
| Production roadmap/readiness/checklist | `CURRENT` | Reconcile together on readiness-gate change |
| Phase 10 decision record | `CURRENT / DECIDED` | Preserve NO-GO decision and successor rationale |
| System architecture | `CURRENT — PHASE 11 COMPOSED DESIGN` | Update for accepted component/trust/data-flow changes |
| Security model | `CURRENT — ACTIVE PHASE 11.6 CONTROL BOUNDARY` | Update when identity/authorization/security boundaries change |
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
- Phase 11.1–11.5: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.6 TheHive contract: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.6 TheHive handoff implementation: `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- Phase 12: `NOT STARTED`;
- DTMO: **not production authorized**.

## Active Phase 11.6 documentation rule

Documentation may describe the bounded runtime handoff implementation because the repository now contains it, but must not imply live TheHive connectivity, activated deployment entitlement, effective deployed service-account permissions, target-organization membership, real-data privacy approval, production readiness or a new accepted operator GUI.

The active documentation preserves these boundaries:

- reviewed upstream baseline is TheHive 5.5.16 using public API v1;
- TheHive remains a separate StrangeBee service and source is not vendored;
- TheHive 5.3+ license activation remains a deployment prerequisite for continued write operation;
- a DTMO intelligence item never creates a case automatically;
- `POST /api/v1/case` is invoked only after explicit human `handoff:case` authorization;
- case-handoff authority remains distinct from publication/share authority and service accounts cannot authorize it;
- canonical item identity and repository provenance are required;
- a durable reservation is committed before external mutation;
- stable request/item/TheHive case/organization identity is required for reconciliation;
- known authoritative TLP restrictions cannot be broadened;
- authoritative MISP distribution/sharing-group restrictions block this bounded handoff until a deployment-approved TheHive access mapping exists;
- ambiguous mutation delivery blocks blind replay;
- persisted upstream outcome is minimized rather than treated as unrestricted evidence;
- TheHive handoff state cannot grant external-share authority or prove local compromise;
- responders, task/observable mutations, Cortex, automatic MISP→TheHive automation, case deletion, external sharing and administration remain excluded;
- repository CI is engineering evidence, not live integration or production evidence.

No synthetic screenshot is promoted because this bounded implementation introduces an API-governed handoff rather than a new accepted operator GUI. Fabricating a live-TheHive screenshot would overstate evidence.

## Evidence and claim rules

Repository CI cannot manufacture staging acceptance; owner acceptance cannot manufacture independent assurance; independent assurance cannot manufacture production authorization. Prior Phase 8/9 evidence remains valid only for the prior candidate. Fresh Phase 11.10 validation and Phase 11.11 independent assurance are required before Phase 12.

Framework mappings and integrated service state remain bounded claims and do not imply blanket compliance, local exposure, compromise, case necessity or dissemination authority without separate attributable evidence.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only where the document is clearly an immutable point-in-time record. Historical text must not be used as the primary current-state source or rewritten to manufacture later acceptance.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and professional documentation contract tests before protected merge. Current lifecycle state is reconciled across the root README, documentation portal, current state, executive views, readiness report/checklist, documentation status, evidence index, QA/release gates, production roadmap and active Phase 11 roadmap/integration documents. Historical Phase 8/9 and Phase 10 evidence claims remain preserved in their original scope.
