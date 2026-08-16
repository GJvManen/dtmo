# DTMO Documentation Status and Authority

Last reconciled: **2026-08-16**

## Purpose

This document defines which DTMO documents are authoritative for the current product and lifecycle state, which records are historical/immutable, and how conflicts are resolved.

## Authority order

For current project decisions, use this order:

1. `docs/project/CURRENT_STATE.md` — current controlled product and lifecycle state;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md` — active Phase 11 programme and fixed priority order;
3. `docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md` — active Phase 11.3 service/API/security/licensing contract;
4. `docs/integrations/INTELOWL_INTEGRATION.md` — contract-only implementation/operations boundary for the active IntelOwl step;
5. `docs/architecture/TARANIS_PLATFORM_INTEGRATION_ASSESSMENT.md` and `docs/architecture/TARANIS_DTMO_INTEGRATION_CONTRACT.md` — accepted Taranis architecture/service boundary;
6. `docs/integrations/TARANIS_ADAPTER.md` — accepted Phase 11.2 Taranis repository integration guide;
7. `docs/roadmap/PRODUCTION_ROADMAP.md` — production-readiness sequence from Phase 10 NO-GO to Phase 12;
8. `docs/project/PRODUCTION_READINESS_REPORT.md` — consolidated readiness assessment;
9. `docs/project/PRODUCTION_CHECKLIST.md` — evidence completion checklist;
10. `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md` — completed accountable no-go decision;
11. architecture, security and governance documents — domain-specific design and claim boundaries;
12. `docs/evidence/EVIDENCE_INDEX.md` — evidence classes and authoritative evidence locations.

If a historical run record conflicts with a later current-state decision, both remain valid in their own scope: the historical record describes what was true at that point in time; current-state documents describe the present controlled state.

## Current documentation baseline

| Document class | Status | Maintenance expectation |
|---|---|---|
| Root README / docs portal | `CURRENT` | Update on material product or lifecycle change |
| Current state / executive views | `CURRENT` | Reconcile together on lifecycle change |
| Platform Industrialisation Roadmap | `CURRENT / ACTIVE` | Maintain through Phase 11 |
| Taranis assessment/contract/adapter docs | `CURRENT / ACCEPTED` | Preserve accepted service boundary; update only for later material architecture changes |
| IntelOwl integration contract | `CURRENT / ACTIVE` | Maintain through Phase 11.3 contract and implementation work |
| IntelOwl integration guide | `CURRENT / CONTRACT-ONLY` | Do not claim runtime/operator availability until implementation is accepted |
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
- Phase 11.1: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.2: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.3: `IN PROGRESS / CONTRACT BASELINE IN EXACT-HEAD VALIDATION`;
- Phase 12: `NOT STARTED`;
- DTMO: **not production authorized**.

## Active Phase 11.3 documentation rule

The IntelOwl contract step is architecture/documentation work only. It may describe proposed service/API behavior, acceptance criteria and operational/security boundaries, but it must not imply that a live IntelOwl adapter, service identity, provider credentials, analyzer runtime or operator UI already exists.

The active documentation must preserve these boundaries:

- IntelOwl remains a separate service/API component;
- dedicated non-admin service identity and runtime-secret token;
- explicit observable and analyzer/playbook allowlisting;
- TLP/privacy-aware external-disclosure controls;
- analyzer/job/result provenance;
- external IntelOwl Connectors excluded from the initial enrichment path;
- analyzer verdicts do not establish local compromise;
- AGPL-3.0 review before vendoring, embedding, modification or redistribution;
- repository CI is not live integration or production evidence.

## Evidence and claim rules

Professional documentation may record an external or accountable decision only when that evidence class exists. Repository CI cannot manufacture staging acceptance. Owner staging acceptance cannot manufacture independent assurance. Independent assurance cannot manufacture production authorization.

Prior Phase 8/9 evidence remains valid for the prior candidate but cannot be silently transferred to a materially changed Phase 11 integrated platform. Fresh production-equivalent validation and independent assurance are required before Phase 12.

Framework mappings are bounded claims. A mapping to Normenkader IBP, MITRE ATT&CK, NIST CSF, CVSS context or another model means only the explicit relationship documented in the governance registry and evidence mapping. It does not imply complete compliance, certification, control effectiveness or local exposure.

IntelOwl enrichment is likewise a bounded claim: an analyzer/provider verdict is attributed context and must not be represented as proof of local exposure or compromise without separate attributable local evidence.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only when the document is clearly an immutable point-in-time record under the operational evidence layer. Historical text must not be used as the primary current-state source.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and the professional documentation contract tests before protected merge. Current lifecycle state must be reconciled across the root README, documentation portal, current state, executive views, readiness report/checklist, documentation status, evidence index, QA/release gates, production roadmap and the active Phase 11 roadmap/contract/integration documents. Historical Phase 8/9 and Phase 10 evidence claims remain preserved in their original scope.