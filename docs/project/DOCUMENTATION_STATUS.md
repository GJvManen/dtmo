# DTMO Documentation Status and Authority

Last reconciled: **2026-08-20**

## Purpose

This document defines authoritative current-state documentation, active Phase 11.10 candidate-completion/execution material, historical/immutable records and conflict-resolution order.

## Authority order

For current project decisions use:

1. `docs/project/CURRENT_STATE.md`;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`;
3. active bounded Phase 11.10 slice documentation — currently `docs/qa/PHASE11_10A_FRONTEND_ARCHITECTURE_GATE.md`, `docs/architecture/FRONTEND_ARCHITECTURE.md`, `docs/architecture/UI_API_CONTRACT.md`, `docs/ux/UNIFIED_OPERATIONS_WORKBENCH.md`, `docs/ux/INFORMATION_ARCHITECTURE.md` and `docs/ux/DESIGN_SYSTEM.md`;
4. `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md` and `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md` for the future 11.10p external exercise;
5. `docs/project/PRODUCTION_READINESS_REPORT.md` and `docs/project/PRODUCTION_CHECKLIST.md`;
6. `docs/evidence/EVIDENCE_INDEX.md` and the controlled Phase 11.10 evidence template;
7. accepted Phase 11.8 and Phase 11.9 architecture, security, operations and QA documentation;
8. accepted Cortex, TheHive, MISP, OpenCTI, IntelOwl and Taranis documentation;
9. `docs/roadmap/PRODUCTION_ROADMAP.md`;
10. security, governance and general QA documentation;
11. `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md` as the immutable current production-authorization decision until superseded by Phase 12.

Historical point-in-time records remain valid for what they originally described and are never rewritten to manufacture later acceptance.

## Current documentation baseline

| Document class | Status | Maintenance expectation |
|---|---|---|
| Root README / docs portal | `CURRENT` | Update on material product/lifecycle change |
| Current state / executive views | `CURRENT` | Reconcile together on lifecycle change |
| Platform Industrialisation Roadmap | `CURRENT / ACTIVE` | Maintain through Phase 11 |
| Phase 11.1–11.7b service docs | `CURRENT / ACCEPTED` | Preserve accepted boundaries |
| Phase 11.8 runtime docs | `CURRENT / ACCEPTED` | Preserve accepted runtime boundaries |
| Phase 11.9 migration/compatibility docs | `CURRENT / ACCEPTED` | Preserve forward-first compatibility boundary |
| Phase 11.10a frontend architecture/design docs | `CURRENT / ACTIVE` | Govern the next-generation workbench architecture contract |
| Phase 11.10 external gate/runbook/evidence contract | `CURRENT / DEFERRED UNTIL 11.10p` | Govern fresh production-equivalent validation after candidate freeze |
| Production roadmap/readiness/checklist | `CURRENT` | Reconcile on readiness-gate change |
| Security/governance model | `CURRENT` | Reconcile on material control changes |
| Historical phase runbooks/evidence | `HISTORICAL / SUPPORTING` | Never rewrite original evidence claims |
| `docs/development/runs/` | `HISTORICAL / IMMUTABLE` | Never rewrite to simulate current state |

## Current release truth

The professional documentation consistently distinguishes:

- Phases 1–7 `PASS`;
- RC13 `PASS / OWNER_ACCEPTED`;
- E8.1–E8.10 `PASS / REPOSITORY_COMPLETE`;
- historical Phase 8 `PASS / OWNER_ACCEPTED`;
- historical Phase 9 `PASS / EXTERNAL_ASSURANCE_ACCEPTED`;
- Phase 10 `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`;
- Phase 11 `IN PROGRESS / ACTIVE`;
- Phase 11.1–11.9 `PASS / REPOSITORY_COMPLETE`;
- Phase 11.10 `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`;
- Phase 11.10a `IN PROGRESS / REPOSITORY ARCHITECTURE CONTRACT`;
- Phase 11.11 `NOT STARTED`;
- Phase 12 `NOT STARTED`;
- DTMO **not production authorized**.

## Active Phase 11.10a documentation rule

Documentation may define the target frontend architecture, information architecture, design system and governed UI/API boundary. It must not imply that the new shell, workspaces or integration capabilities have already been implemented or exercised.

The active 11.10a package preserves:

- one canonical DTMO browser product as the target;
- normal request path **browser → DTMO API → governed integration adapter → upstream service**;
- server-side RBAC and least privilege;
- human/service identity separation;
- human publication/share authority;
- separate TheHive case authority;
- no local-compromise inference from enrichment, graph presence or correlation;
- accessible dark/light semantic design;
- truthful loading/empty/stale/partial-failure/error states;
- mockups/generated visuals as design artifacts only.

A successful 11.10a repository gate establishes only architecture-contract consistency. It does not prove frontend implementation, live upstream behavior, production-equivalent validation, independent assurance or production authorization.

## Phase 11.10p external documentation rule

The existing production-equivalent execution procedure, candidate fingerprint, manifest schema and fail-closed evidence checks remain authoritative for 11.10p after candidate completion and freeze. Documentation must not imply that required external evidence exists until that exercise actually occurs and the referenced evidence has been reviewed.

A successful repository validator result establishes only that supplied metadata satisfies the contract. It does not prove the truth of external observations, live Kubernetes behavior, real migration/rollback/recovery, independent assurance or production authorization.

The external package preserves:

- one immutable candidate and environment identity;
- exact candidate and prior application image digests;
- forward-first migration compatibility and no automatic database down migration;
- post-upgrade and post-rollback health evidence;
- representative saturation/capacity observations;
- recovery integrity and RPO/RTO observations where applicable;
- no historical Phase 8/9 evidence reuse;
- no secrets or raw credential material in repository evidence;
- RBAC, provenance, least privilege, human publication/share authority and separate service/licensing boundaries.

No synthetic screenshot, generated design, local Compose run, emulator result or repository CI artifact is promoted as live production-equivalent evidence. Mermaid diagrams are documentation models only.

## Evidence and claim rules

Repository CI cannot manufacture production-equivalent acceptance; owner acceptance cannot manufacture independent assurance; independent assurance cannot manufacture production authorization. Historical Phase 8/9 evidence remains candidate-bound. Fresh Phase 11.10 and Phase 11.11 evidence is required before Phase 12.

Framework mappings, frontend state and integrated service state remain bounded claims and do not imply blanket compliance, local exposure, compromise, case necessity or dissemination authority without separate attributable evidence.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only where the document is clearly a point-in-time record. Historical text must not be used as primary current-state evidence or rewritten to manufacture later acceptance.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and professional documentation contract tests before protected merge. Current lifecycle state is reconciled across README, docs portal, current state, executive views, readiness report/checklist, documentation status, evidence index, QA/release gates, production roadmap and active Phase 11 documents.
