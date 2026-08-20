# DTMO Documentation Status and Authority

Last reconciled: **2026-08-20**

## Purpose

This document defines the authority order for current DTMO project decisions, accepted Phase 11 evidence, the active Phase 11.10 candidate-completion slice and historical records.

## Authority order

For current project decisions use:

1. `docs/project/CURRENT_STATE.md`;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`;
3. active Phase 11.10e material: `docs/architecture/PHASE11_10E_INTEGRATED_ANALYSIS_WORKSPACE.md`, `docs/user/INTEGRATED_ANALYSIS_WORKSPACE.md`, `docs/qa/PHASE11_10E_INTEGRATED_ANALYSIS_GATE.md`, backend/frontend implementation and `.github/workflows/phase11-integrated-analysis-workspace.yml`;
4. accepted Phase 11.10a–11.10d workbench architecture, shell, Command Center and Unified Intelligence material;
5. `docs/project/PRODUCTION_READINESS_REPORT.md` and `docs/project/PRODUCTION_CHECKLIST.md`;
6. `docs/evidence/EVIDENCE_INDEX.md`;
7. accepted Phase 11.8/11.9 architecture, operations, security and QA documentation;
8. accepted Taranis, IntelOwl, OpenCTI, MISP, TheHive and Cortex documentation;
9. `docs/roadmap/PRODUCTION_ROADMAP.md`;
10. security, governance and general QA documentation;
11. `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md` as the current immutable production-authorization decision until superseded by a future Phase 12 decision.

Historical point-in-time records remain valid for what they originally described and are never rewritten to manufacture later acceptance.

## Current documentation baseline

| Document class | Status | Maintenance expectation |
|---|---|---|
| Root README / documentation portal | `CURRENT` | Update on material product/lifecycle change |
| Current state / executive views | `CURRENT` | Reconcile together on lifecycle change |
| Platform Industrialisation Roadmap | `CURRENT / ACTIVE` | Maintain through Phase 11 |
| Phase 11.1–11.7b service docs | `CURRENT / ACCEPTED` | Preserve accepted boundaries |
| Phase 11.8 runtime docs | `CURRENT / ACCEPTED` | Preserve accepted controls |
| Phase 11.9 migration/compatibility docs | `CURRENT / ACCEPTED` | Preserve forward-first compatibility boundary |
| Phase 11.10a frontend architecture/design | `CURRENT / ACCEPTED` | Preserve accepted workbench architecture |
| Phase 11.10b canonical shell | `CURRENT / ACCEPTED` | Preserve accepted build/routing/accessibility baseline |
| Phase 11.10c Command Center | `CURRENT / ACCEPTED` | Preserve canonical read model and fail-closed operational overview |
| Phase 11.10d Unified Intelligence Workspace | `CURRENT / ACCEPTED` | Preserve governed discovery, canonical detail/provenance and browser acceptance |
| Phase 11.10e IntelOwl/Cortex integrated analysis | `CURRENT / ACTIVE` | Govern human-triggered analyzer execution/history, immutable evidence and exact-head browser acceptance |
| Phase 11.10 external gate/runbook | `CURRENT / DEFERRED UNTIL 11.10p` | Govern fresh production-equivalent exercise after candidate freeze |
| Production roadmap/readiness/checklist | `CURRENT` | Reconcile on readiness change |
| Security/governance model | `CURRENT` | Reconcile on material control change |
| Historical evidence/run records | `HISTORICAL / IMMUTABLE` | Never rewrite original evidence claims |

## Current release truth

- Phases 1–7 `PASS`;
- RC13 `PASS / OWNER_ACCEPTED`;
- E8.1–E8.10 `PASS / REPOSITORY_COMPLETE`;
- Phase 8 `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE`;
- Phase 9 `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`;
- Phase 10 `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`;
- Phase 11 `IN PROGRESS / ACTIVE`;
- Phase 11.1–11.9 `PASS / REPOSITORY_COMPLETE`;
- Phase 11.10 `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`;
- Phase 11.10a `PASS / REPOSITORY_COMPLETE`;
- Phase 11.10b `PASS / REPOSITORY_COMPLETE`;
- Phase 11.10c `PASS / REPOSITORY_COMPLETE`;
- Phase 11.10d `PASS / REPOSITORY_COMPLETE`;
- Phase 11.10e `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- Phase 11.10f `NOT STARTED`;
- Phase 11.10p `NOT STARTED / CANDIDATE FREEZE REQUIRED`;
- Phase 11.11 `NOT STARTED`;
- Phase 12 `NOT STARTED`;
- DTMO **not production authorized**.

## Active Phase 11.10e documentation rule

Documentation may describe IntelOwl/Cortex integrated-analysis behavior only where attributable to repository implementation, existing governed DTMO APIs/adapters, durable persistence and exact-head browser/contract evidence.

The active package preserves:

- canonical `/workbench/analysis` within the accepted React/TypeScript/Vite shell;
- the existing human-triggered IntelOwl execution/history boundary;
- `GET /api/v1/analysis/capabilities` as configured capability/allowlist visibility, not a runtime-health claim;
- `GET /api/v1/analysis/items/{item_id}/history` as combined persisted IntelOwl/Cortex evidence;
- `POST /api/v1/analysis/items/{item_id}/cortex` as explicit analyzer-only execution;
- **browser → DTMO API → governed integration adapter → upstream service**;
- **server-side RBAC**, with `read:intelligence` for reads and `review:intelligence` for execution;
- explicit Cortex observable/analyzer allowlists and TLP controls;
- no Cortex responders, automatic analyzer discovery or automatic IntelOwl fallback;
- durable Cortex history bound to canonical item and stable job identity;
- `external_share_authorized=false` and `local_compromise_proven=false` as persisted analyzer-evidence invariants;
- dependency/policy/persistence failure rendered as failure/unavailable rather than synthetic success;
- repository/browser mocks and fixtures classified as engineering evidence only.

A successful Phase 11 Integrated Analysis Workspace Gate **does not prove** live IntelOwl/Cortex availability, analyzer/provider authorization, local compromise, production-equivalent operation, independent assurance or production authorization.

## Phase 11.10p external documentation rule

The existing production-equivalent validation gate, runbook, candidate fingerprinting and evidence manifest remain authoritative for 11.10p after candidate completion and freeze.

The external package requires one **same immutable** candidate/environment identity, candidate and prior image digests, forward-first migration, exact prior-digest rollback, post-rollback health, no automatic database down migration, health/readiness, saturation/capacity and recovery/continuity evidence. Historical Phase 8/9 evidence cannot satisfy the new candidate. Missing, inaccessible, placeholder or mixed-candidate evidence must **fail closed**.

A successful repository validator establishes metadata consistency only; it does not prove the truth of external observations.

## Evidence and claim rules

Repository CI cannot manufacture production-equivalent acceptance; owner acceptance cannot manufacture independent assurance; independent assurance cannot manufacture production authorization. Historical Phase 8/9 evidence remains candidate-bound. Fresh Phase 11.10 and Phase 11.11 evidence is required before Phase 12.

Framework mappings, frontend state and integrated service state remain bounded claims and do not imply blanket compliance, local exposure, compromise, case necessity or dissemination authority without separate attributable evidence.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only where the document is clearly a point-in-time record. Historical text must not be used as primary current-state evidence or rewritten to manufacture later acceptance.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and professional documentation contract tests before protected merge. Current lifecycle state is reconciled across README, docs portal, current state, executive views, readiness report/checklist, documentation status, evidence index, QA/release gates, production roadmap and active Phase 11 documents.

## Maintenance rule

Whenever lifecycle state, architecture, security boundary, product scope or governance claims materially change, affected current documents and documentation-contract tests are updated in the same bounded PR. Historical evidence remains unchanged.
