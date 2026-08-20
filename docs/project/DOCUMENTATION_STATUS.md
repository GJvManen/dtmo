# DTMO Documentation Status and Authority

Last reconciled: **2026-08-20**

## Purpose

This document defines the authority order for current DTMO project decisions, accepted Phase 11 evidence, the active Phase 11.10 candidate-completion slice and historical records.

## Authority order

For current project decisions use:

1. `docs/project/CURRENT_STATE.md`;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`;
3. active Phase 11.10g material: `docs/architecture/PHASE11_10G_MISP_SHARING_EXCHANGE.md`, `docs/user/MISP_SHARING_EXCHANGE_WORKSPACE.md`, `docs/qa/PHASE11_10G_MISP_SHARING_EXCHANGE_GATE.md`, backend/frontend implementation and `.github/workflows/phase11-misp-sharing-exchange.yml`;
4. accepted Phase 11.10a–11.10f workbench architecture, shell, Command Center, Unified Intelligence, Integrated Analysis and OpenCTI Graph material;
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
| Phase 11.10e IntelOwl/Cortex integrated analysis | `CURRENT / ACCEPTED` | Preserve human-triggered analyzer execution/history and no-verdict boundary |
| Phase 11.10f OpenCTI graph/entity workspace | `CURRENT / ACCEPTED` | Preserve persisted graph/entity evidence and explicit topology limits |
| Phase 11.10g MISP Sharing & Exchange | `CURRENT / ACTIVE` | Govern separate human review/share approval, source handling and unpublished replay-protected export |
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
- Phase 11.10e `PASS / REPOSITORY_COMPLETE`;
- Phase 11.10f `PASS / REPOSITORY_COMPLETE`;
- Phase 11.10g `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- Phase 11.10h `NOT STARTED`;
- Phase 11.10p `NOT STARTED / CANDIDATE FREEZE REQUIRED`;
- Phase 11.11 `NOT STARTED`;
- Phase 12 `NOT STARTED`;
- DTMO **not production authorized**.

## Active Phase 11.10g documentation rule

Documentation may describe MISP Sharing & Exchange behavior only where attributable to repository implementation, accepted Phase 11.5/E8 governance controls and exact-head browser/contract evidence.

The active package preserves:

- canonical `/workbench/sharing` inside the accepted React/TypeScript/Vite shell;
- `GET /api/v1/sharing/items/{item_id}` as a sanitized DTMO-owned canonical state projection;
- **browser → DTMO API → governed integration adapter → upstream service**;
- **server-side RBAC** with `read:intelligence`, `review:intelligence` and `approve:share` remaining distinct authorities;
- a different human share approver from the recorded reviewer;
- service-account exclusion from human review/share authority and MISP export;
- no ordinary browser-held MISP credentials or direct MISP request;
- authoritative MISP source distribution, sharing-group and TLP constraints on re-export;
- deterministic replay protection for the current canonical revision;
- uncertain delivery classified as requiring operator inspection rather than automatic replay;
- MISP events created with `published=false`;
- no Phase 11.10g Publish or Synchronize action;
- configuration distinguished from live MISP health;
- dependency failure rendered unavailable rather than synthetic approval or export eligibility;
- repository/browser mocks and fixtures classified as engineering evidence only.

Missing or ambiguous authority/handling evidence must **fail closed**. A successful Phase 11 MISP Sharing Exchange Gate **does not prove** live MISP connectivity/health, publication/synchronization, downstream consumption, local compromise, production-equivalent operation, independent assurance or production authorization.

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
