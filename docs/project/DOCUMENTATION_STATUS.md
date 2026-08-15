# DTMO Documentation Status and Authority

Last reconciled: **2026-08-15**

## Purpose

This document defines which DTMO documents are authoritative for the current product and lifecycle state, which records are historical/immutable, and how conflicts are resolved.

## Authority order

For current project decisions, use this order:

1. `docs/project/CURRENT_STATE.md` — current controlled product and lifecycle state;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md` — active Phase 11 programme and fixed priority order;
3. `docs/architecture/TARANIS_PLATFORM_INTEGRATION_ASSESSMENT.md` — active Phase 11.1 architecture assessment;
4. `docs/roadmap/PRODUCTION_ROADMAP.md` — production-readiness sequence from Phase 10 NO-GO to Phase 12;
5. `docs/project/PRODUCTION_READINESS_REPORT.md` — consolidated readiness assessment;
6. `docs/project/PRODUCTION_CHECKLIST.md` — evidence completion checklist;
7. `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md` — completed accountable no-go decision;
8. architecture, security and governance documents — domain-specific design and claim boundaries;
9. `docs/evidence/EVIDENCE_INDEX.md` — evidence classes and authoritative evidence locations.

If a historical run record conflicts with a later current-state decision, both remain valid in their own scope: the historical record describes what was true at that point in time; current-state documents describe the present controlled state.

## Current documentation baseline

| Document class | Status | Maintenance expectation |
|---|---|---|
| Root README / docs portal | `CURRENT` | Update on material product or lifecycle change |
| Current state / executive views | `CURRENT` | Reconcile together on lifecycle change |
| Platform Industrialisation Roadmap | `CURRENT / ACTIVE` | Maintain through Phase 11 |
| Taranis integration assessment | `CURRENT / ACTIVE` | Maintain through Phase 11.1 and update when architecture decisions change |
| Production roadmap/readiness/checklist | `CURRENT` | Reconcile together on readiness-gate change |
| Phase 10 decision record | `CURRENT / DECIDED` | Preserve NO-GO decision and successor-programme rationale |
| System architecture | `CURRENT — STABLE DESIGN` | Update when Phase 11 introduces accepted component/trust/data-flow changes |
| Security model | `CURRENT — STABLE CONTROL MODEL` | Update when identity/authorization/security boundaries change |
| Governance mapping registry | `CURRENT — CONTROLLED CLAIM MODEL` | Update when mappings/framework semantics change |
| QA/release gates | `CURRENT — CONTROL MODEL` | Update when gate/evidence rules change |
| Phase-specific staging/assurance runbooks | `HISTORICAL OR SUPPORTING FOR PRIOR ACCEPTED RELEASE` | Preserve evidence boundaries; do not rewrite historical facts |
| Release notes | `VERSIONED` | Do not rewrite unrelated historical release scope |
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
- Phase 12: `NOT STARTED`;
- DTMO: **not production authorized**.

## Evidence and claim rules

Professional documentation may record an external or accountable decision only when that evidence class exists. Repository CI cannot manufacture staging acceptance. Owner staging acceptance cannot manufacture independent assurance. Independent assurance cannot manufacture production authorization.

Prior Phase 8/9 evidence remains valid for the prior candidate but cannot be silently transferred to a materially changed Phase 11 integrated platform. Fresh production-equivalent validation and independent assurance are required before Phase 12.

Framework mappings are bounded claims. A mapping to Normenkader IBP, MITRE ATT&CK, NIST CSF, CVSS context or another model means only the explicit relationship documented in the governance registry and evidence mapping. It does not imply complete compliance, certification, control effectiveness or local exposure.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only when the document is clearly an immutable point-in-time record under the operational evidence layer. Historical text must not be used as the primary current-state source.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and the professional documentation contract tests before protected merge. Current lifecycle state must be reconciled across the root README, documentation portal, current state, executive views, readiness report/checklist, evidence index, QA/release gates, production roadmap, Phase 10 decision record and the active Phase 11 roadmap/assessment.