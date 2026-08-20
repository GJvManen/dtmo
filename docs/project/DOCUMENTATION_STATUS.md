# DTMO Documentation Status and Authority

Last reconciled: **2026-08-20**

## Purpose

This document defines authoritative current-state documentation, active Phase 11.10 execution material, historical/immutable records and conflict-resolution order.

## Authority order

For current project decisions use:

1. `docs/project/CURRENT_STATE.md`;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`;
3. `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
4. `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
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
| Phase 11.10 gate/runbook/evidence contract | `CURRENT / ACTIVE` | Govern fresh production-equivalent validation |
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
- Phase 11.11 `NOT STARTED`;
- Phase 12 `NOT STARTED`;
- DTMO **not production authorized**.

## Active Phase 11.10 documentation rule

Documentation may define the production-equivalent execution procedure, candidate fingerprint, manifest schema and fail-closed evidence checks. It must not imply that the required external evidence exists until the production-equivalent exercise actually occurs and the referenced evidence has been reviewed.

A successful repository validator result establishes only that supplied metadata satisfies the contract. It does not prove the truth of external observations, live Kubernetes behavior, real migration/rollback/recovery, independent assurance or production authorization.

The active package preserves:

- one immutable candidate and environment identity;
- exact candidate and prior application image digests;
- forward-first migration compatibility and no automatic database down migration;
- post-upgrade and post-rollback health evidence;
- representative saturation/capacity observations;
- recovery integrity and RPO/RTO observations where applicable;
- no historical Phase 8/9 evidence reuse;
- no secrets or raw credential material in repository evidence;
- RBAC, provenance, least privilege, human publication/share authority and separate service/licensing boundaries.

No synthetic screenshot, local Compose run, emulator result or repository CI artifact is promoted as live production-equivalent evidence. Mermaid diagrams are documentation models only.

## Evidence and claim rules

Repository CI cannot manufacture production-equivalent acceptance; owner acceptance cannot manufacture independent assurance; independent assurance cannot manufacture production authorization. Historical Phase 8/9 evidence remains candidate-bound. Fresh Phase 11.10 and Phase 11.11 evidence is required before Phase 12.

Framework mappings and integrated service state remain bounded claims and do not imply blanket compliance, local exposure, compromise, case necessity or dissemination authority without separate attributable evidence.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only where the document is clearly a point-in-time record. Historical text must not be used as primary current-state evidence or rewritten to manufacture later acceptance.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and professional documentation contract tests before protected merge. Current lifecycle state is reconciled across README, docs portal, current state, executive views, readiness report/checklist, documentation status, evidence index, QA/release gates, production roadmap and active Phase 11 documents.
