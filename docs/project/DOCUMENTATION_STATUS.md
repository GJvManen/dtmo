# DTMO Documentation Status and Authority

Last reconciled: **2026-08-18**

## Purpose

This document defines authoritative current-state documentation, historical/immutable records and conflict-resolution order.

## Authority order

For current project decisions use:

1. `docs/project/CURRENT_STATE.md`;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`;
3. `docs/security/PHASE11_8G_SUPPLY_CHAIN_HARDENING.md`;
4. `docs/administration/SUPPLY_CHAIN_RELEASE_VERIFICATION.md` and `docs/operations/PHASE11_8G_SUPPLY_CHAIN_RUNBOOK.md`;
5. `docs/qa/PHASE11_8G_SUPPLY_CHAIN_GATE.md`;
6. accepted Phase 11.8a–11.8f documentation;
7. accepted Cortex, TheHive, MISP, OpenCTI, IntelOwl and Taranis documentation;
8. `docs/roadmap/PRODUCTION_ROADMAP.md`;
9. readiness, security, governance, QA and `docs/evidence/EVIDENCE_INDEX.md`;
10. `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`.

Historical point-in-time records remain valid for what they originally described and are never rewritten to manufacture later acceptance.

## Current documentation baseline

| Document class | Status | Maintenance expectation |
|---|---|---|
| Root README / docs portal | `CURRENT` | Update on material product/lifecycle change |
| Current state / executive views | `CURRENT` | Reconcile together on lifecycle change |
| Platform Industrialisation Roadmap | `CURRENT / ACTIVE` | Maintain through Phase 11 |
| Phase 11.1–11.7b service docs | `CURRENT / ACCEPTED` | Preserve accepted boundaries |
| Phase 11.8a–11.8f runtime docs | `CURRENT / ACCEPTED` | Preserve accepted runtime boundaries |
| Phase 11.8g supply-chain docs | `CURRENT / IN EXACT-HEAD VALIDATION` | Active bounded control/evidence boundary |
| Production roadmap/readiness/checklist | `CURRENT` | Reconcile on readiness-gate change |
| Security/governance model | `CURRENT` | Reconcile on material control changes |
| Historical phase runbooks/evidence | `HISTORICAL / SUPPORTING` | Never rewrite original evidence claims |
| `docs/development/runs/` | `HISTORICAL / IMMUTABLE` | Never rewrite to simulate current state |

## Current release truth

The professional documentation consistently distinguishes Phases 1–7 `PASS`; RC13 `PASS / OWNER_ACCEPTED`; E8.1–E8.10 `PASS / REPOSITORY_COMPLETE`; historical Phase 8 `PASS / OWNER_ACCEPTED`; historical Phase 9 `PASS / EXTERNAL_ASSURANCE_ACCEPTED`; Phase 10 `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11 `IN PROGRESS / ACTIVE`; Phase 11.1–11.8f `PASS / REPOSITORY_COMPLETE`; Phase 11.8g `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`; Phase 11.9–11.11 `NOT STARTED`; Phase 12 `NOT STARTED`; and DTMO **not production authorized**.

## Active Phase 11.8g documentation rule

Documentation may describe exact-head SBOM generation, vulnerability evidence, artifact hashes and the governed release attestation mechanism because those controls are part of the active slice. It must not imply that a release attestation exists until the release workflow actually executes for the exact subject, nor that signed provenance proves vulnerability absence, deployment admission, production-equivalent behavior or production authorization.

The active documentation preserves short-lived OIDC-backed signing, no repository-stored long-lived signing keys, exact artifact identity, consumer verification, fail-closed missing evidence and all accepted service/licensing/human-authority boundaries.

No synthetic signing or deployment screenshot is promoted as live evidence. Mermaid diagrams are documentation models only.

## Evidence and claim rules

Repository CI cannot manufacture staging acceptance; a signing mechanism cannot manufacture an actual release signature; owner acceptance cannot manufacture independent assurance; independent assurance cannot manufacture production authorization. Historical Phase 8/9 evidence remains candidate-bound. Fresh Phase 11.10 and Phase 11.11 evidence is required before Phase 12.

Framework mappings and integrated service state remain bounded claims and do not imply blanket compliance, local exposure, compromise, case necessity or dissemination authority without separate attributable evidence.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only where the document is clearly a point-in-time record. Historical text must not be used as primary current-state evidence or rewritten to manufacture later acceptance.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and professional documentation contract tests before protected merge. Current lifecycle state is reconciled across README, docs portal, current state, executive views, readiness report/checklist, documentation status, evidence index, QA/release gates, production roadmap and active Phase 11 documents.
