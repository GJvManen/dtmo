# DTMO Documentation Status and Authority

Last reconciled: **2026-08-15**

## Purpose

This document defines which DTMO documents are authoritative for the current product and release state, which records are historical/immutable, and how conflicts are resolved.

## Authority order

For current project decisions, use this order:

1. `docs/project/CURRENT_STATE.md` — current controlled product and lifecycle state;
2. `docs/roadmap/PRODUCTION_ROADMAP.md` — formal production-readiness sequence and active gate;
3. `docs/project/PRODUCTION_READINESS_REPORT.md` — consolidated readiness assessment;
4. `docs/project/PRODUCTION_CHECKLIST.md` — evidence completion checklist;
5. `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md` — active production decision record;
6. architecture, security and governance documents — domain-specific design and claim boundaries;
7. `docs/evidence/EVIDENCE_INDEX.md` — evidence classes and authoritative evidence locations.

If a historical run record conflicts with a later current-state decision, both remain valid in their own scope: the historical record describes what was true at that point in time; current-state documents describe the present controlled state.

## Current documentation baseline

| Document class | Status | Maintenance expectation |
|---|---|---|
| Root README / docs portal | `CURRENT` | Update on material product or lifecycle change |
| Current state / executive views | `CURRENT` | Reconcile together on lifecycle change |
| Production roadmap/readiness/checklist | `CURRENT` | Reconcile together on readiness-gate change |
| Phase 10 decision record | `CURRENT / ACTIVE` | Maintain through final accountable decision |
| System architecture | `CURRENT — STABLE DESIGN` | Update when components/trust/data flow materially change |
| Security model | `CURRENT — STABLE CONTROL MODEL` | Update when identity/authorization/security boundaries change |
| Governance mapping registry | `CURRENT — CONTROLLED CLAIM MODEL` | Update when mappings/framework semantics change |
| QA/release gates | `CURRENT — CONTROL MODEL` | Update when gate/evidence rules change |
| Phase-specific staging/assurance runbooks | `HISTORICAL OR SUPPORTING FOR ACCEPTED RELEASE` | Preserve evidence boundaries; do not rewrite historical facts |
| Release notes | `VERSIONED` | Do not rewrite unrelated historical release scope |
| `docs/development/runs/` | `HISTORICAL / IMMUTABLE` | Never rewrite to simulate current state |

## Current release truth

The professional documentation must consistently distinguish:

- Phases 1–7: `PASS`;
- RC13: `PASS / OWNER_ACCEPTED`;
- E8.1–E8.10: `PASS / REPOSITORY_COMPLETE`;
- Phase 8: `PASS / OWNER_ACCEPTED`;
- Phase 9: `PASS / EXTERNAL_ASSURANCE_ACCEPTED`;
- Phase 10: `IN PROGRESS / DECISION REQUIRED`;
- DTMO: **not production authorized until an accountable Phase 10 GO**.

## Evidence and claim rules

Professional documentation may record an external or accountable decision only when that evidence class exists. Repository CI cannot manufacture staging acceptance. Owner staging acceptance cannot manufacture independent assurance. Independent assurance cannot manufacture production authorization.

Framework mappings are bounded claims. A mapping to Normenkader IBP, MITRE ATT&CK, NIST CSF, CVSS context or another model means only the explicit relationship documented in the governance registry and evidence mapping. It does not imply complete compliance, certification, control effectiveness or local exposure.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only when the document is clearly an immutable point-in-time record under the operational evidence layer. Historical text must not be used as the primary current-state source.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and the professional documentation contract tests before protected merge. Current lifecycle state must be reconciled across the root README, documentation portal, current state, executive views, readiness report/checklist, evidence index, QA/release gates and production roadmap.