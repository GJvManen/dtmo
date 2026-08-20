# DTMO Documentation Status and Authority

Last reconciled: **2026-08-20**

## Purpose

This document defines the authority order for current DTMO project decisions, accepted Phase 11 evidence, the active Phase 11.10 candidate-completion slice and historical records.

## Authority order

For current project decisions use:

1. `docs/project/CURRENT_STATE.md`;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`;
3. active Phase 11.10c material: `docs/architecture/PHASE11_10C_COMMAND_CENTER.md`, `docs/qa/PHASE11_10C_COMMAND_CENTER_GATE.md`, `backend/dtmo/command_center.py`, `backend/dtmo/api_command_center.py`, frontend implementation and `.github/workflows/phase11-command-center.yml`;
4. accepted 11.10a/11.10b workbench architecture and shell material;
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
| Phase 11.10c Command Center | `CURRENT / ACTIVE` | Govern canonical read model, fail-closed UI and exact-head browser acceptance |
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
- Phase 11.10c `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- Phase 11.10d `NOT STARTED`;
- Phase 11.10p `NOT STARTED / CANDIDATE FREEZE REQUIRED`;
- Phase 11.11 `NOT STARTED`;
- Phase 12 `NOT STARTED`;
- DTMO **not production authorized**.

## Active Phase 11.10c documentation rule

Documentation may describe Command Center behavior only where attributable to repository implementation and exact-head browser/contract evidence.

The active package preserves:

- one canonical `/workbench/command-center` workspace;
- canonical DTMO read models rather than browser-to-upstream privileged calls;
- **browser → DTMO API → governed integration adapter → upstream service**;
- **server-side RBAC** as the authority boundary;
- role-aware visibility as usability only;
- separate human publication/share and TheHive case authority;
- explicit distinction between integration configuration and runtime observation;
- no `healthy` claim solely from a feature flag/API base;
- `null`/unavailable metrics when canonical evidence is unavailable rather than synthetic zeros;
- accessible/responsive behavior inherited from the accepted shell;
- `/ui/console` as a migration **compatibility path** only;
- repository/browser mocks and fixtures classified as engineering evidence only.

A successful Phase 11 Command Center Gate **does not prove** live upstream behavior, production-equivalent operation, independent assurance or production authorization.

## Phase 11.10p external documentation rule

The existing production-equivalent validation gate, runbook, candidate fingerprinting and evidence manifest remain authoritative for 11.10p after candidate completion and freeze.

The external package requires one **same immutable** candidate/environment identity, candidate and prior image digests, forward-first migration, exact prior-digest rollback, post-rollback health, no automatic database down migration, health/readiness, saturation/capacity and recovery/continuity evidence. Historical Phase 8/9 evidence cannot satisfy the new candidate. Missing, inaccessible, placeholder or mixed-candidate evidence must **fail closed**.

A successful repository validator establishes metadata consistency only; it does not prove the truth of external observations.

## Maintenance rule

Whenever lifecycle state, architecture, security boundary, product scope or governance claims materially change, affected current documents and documentation-contract tests are updated in the same bounded PR. Historical evidence remains unchanged.
