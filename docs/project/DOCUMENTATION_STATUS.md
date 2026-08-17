# DTMO Documentation Status and Authority

Last reconciled: **2026-08-17**

## Purpose

This document defines which DTMO documents are authoritative for the current product/lifecycle state, which records are historical/immutable, and how conflicts are resolved.

## Authority order

For current project decisions, use this order:

1. `docs/project/CURRENT_STATE.md` — current controlled product and lifecycle state;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md` — active Phase 11 programme and fixed priority order;
3. `docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md` — active Phase 11.6 service/API/identity/licensing/authority contract;
4. `docs/integrations/THEHIVE_HANDOFF.md` and `docs/operations/THEHIVE_HANDOFF_RUNBOOK.md` — active integration and operational boundary;
5. `docs/qa/PHASE11_6_THEHIVE_HANDOFF_CONTRACT_GATE.md` — active exact-head contract gate;
6. MISP contract/read/export/state documentation — accepted Phase 11.5 boundary;
7. OpenCTI contract/integration/runbook documentation — accepted Phase 11.4 boundary;
8. IntelOwl integration documentation — accepted Phase 11.3 boundary;
9. Taranis assessment/contract/adapter documentation — accepted Phase 11.1–11.2 boundary;
10. `docs/roadmap/PRODUCTION_ROADMAP.md` — production-readiness sequence from Phase 10 NO-GO to Phase 12;
11. readiness, security, QA and `docs/evidence/EVIDENCE_INDEX.md` — domain-specific current-state/evidence boundaries;
12. `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md` — completed accountable no-go decision.

Historical point-in-time records remain valid for what they originally described and are never rewritten to manufacture later acceptance.

## Current documentation baseline

| Document class | Status | Maintenance expectation |
|---|---|---|
| Root README / docs portal | `CURRENT` | Update on material product/lifecycle change |
| Current state / executive views | `CURRENT` | Reconcile together on lifecycle change |
| Platform Industrialisation Roadmap | `CURRENT / ACTIVE` | Maintain through Phase 11 |
| Taranis / IntelOwl / OpenCTI / MISP accepted docs | `CURRENT / ACCEPTED` | Preserve accepted Phase 11.1–11.5 boundaries |
| TheHive contract/integration/runbook docs | `CURRENT / IN EXACT-HEAD VALIDATION` | Active Phase 11.6 contract boundary |
| Phase 11.6 TheHive contract gate | `CURRENT / IN EXACT-HEAD VALIDATION` | Active contract acceptance boundary |
| Production roadmap/readiness/checklist | `CURRENT` | Reconcile together on readiness-gate change |
| Phase 10 decision record | `CURRENT / DECIDED` | Preserve NO-GO decision and successor rationale |
| System architecture | `CURRENT — STABLE DESIGN` | Update for accepted component/trust/data-flow changes |
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
- Phase 11.6 TheHive handoff contract: `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- Phase 12: `NOT STARTED`;
- DTMO: **not production authorized**.

## Active Phase 11.6 documentation rule

Documentation may describe the TheHive service/API/licensing/authority contract but must not imply a live mutation adapter, case-creation success, activated deployment entitlement, effective service-account permissions, production access configuration or an accepted new operator UI.

The active documentation preserves these boundaries:

- reviewed upstream baseline is TheHive 5.5.16 using public API v1;
- TheHive remains a separate StrangeBee service and source is not vendored;
- TheHive 5.3+ license activation is an explicit deployment prerequisite for continued write operation;
- a DTMO intelligence item never creates a case automatically;
- `POST /api/v1/case` is a future mutation candidate only after explicit human case-handoff approval;
- case-handoff authority remains distinct from publication/share authority;
- stable DTMO canonical identity, handoff/idempotency identity, TheHive case identity and organization context are required for durable reconciliation;
- TLP/PAP/access restrictions cannot be broadened;
- ambiguous mutation delivery blocks blind replay;
- TheHive case state does not become canonical CTI truth, local-compromise proof or DTMO external-share authority;
- responders, Cortex, automatic MISP→TheHive automation, external sharing and administration remain excluded;
- repository CI is engineering evidence, not live integration or production evidence.

No synthetic screenshot is promoted because this contract slice introduces no accepted operator GUI surface.

## Evidence and claim rules

Repository CI cannot manufacture staging acceptance; owner acceptance cannot manufacture independent assurance; independent assurance cannot manufacture production authorization. Prior Phase 8/9 evidence remains valid only for the prior candidate. Fresh Phase 11.10 validation and Phase 11.11 independent assurance are required before Phase 12.

Framework mappings and integrated service state remain bounded claims and do not imply blanket compliance, local exposure, compromise, case necessity or dissemination authority without separate attributable evidence.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only where the document is clearly an immutable point-in-time record. Historical text must not be used as the primary current-state source or rewritten to manufacture later acceptance.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and professional documentation contract tests before protected merge. Current lifecycle state is reconciled across the root README, documentation portal, current state, executive views, readiness report/checklist, documentation status, evidence index, QA/release gates, production roadmap and active Phase 11 roadmap/integration documents. Historical Phase 8/9 and Phase 10 evidence claims remain preserved in their original scope.
