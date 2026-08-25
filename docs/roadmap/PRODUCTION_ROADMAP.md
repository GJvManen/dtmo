# DTMO Roadmap — Production Readiness and Product Evolution

Last updated: **2026-08-25**

## Purpose

This roadmap keeps repository engineering, owner product acceptance, production-equivalent validation, independent external assurance and production authorization as separate evidence classes. Passing one class does not imply another.

## Current position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Repository-controlled engineering baseline | `PASS` |
| RC13 + owner retest | Historical unified-console functional acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | Vulnerability & CTI ecosystem integrations | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Earlier production-equivalent validation | `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE ONLY` |
| Phase 9 | Earlier independent external assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE ONLY` |
| Phase 10 | Earlier formal production go/no-go | `NO-GO / BLOCKED — HISTORICAL PLATFORM INDUSTRIALISATION DECISION` |
| Phase 11.1–11.9 | Service integrations, runtime and migration compatibility | `PASS / REPOSITORY_COMPLETE` |
| Phase 11 | Current platform industrialisation programme | `IN PROGRESS / ACTIVE` |
| Phase 11.10a–11.10q | Unified Operations Workbench candidate completion and functional recovery | `MERGED / OWNER-AUTHORIZED` |
| Phase 11.10p | Fresh candidate freeze + production-equivalent validation | `IN PROGRESS / CANDIDATE-BOUND EVIDENCE REQUIRED` |
| Phase 11.11 | New independent external assurance | `NOT STARTED / BLOCKED UNTIL FRESH PRODUCTION-EQUIVALENT PASS` |
| Phase 12 | New formal production GO/NO-GO | `NOT STARTED / BLOCKED UNTIL 11.10 + 11.11 ACCEPTED` |

DTMO remains **not production authorized**. Phase 11 remains `IN PROGRESS`; the immediate priority is a new immutable candidate freeze followed by fresh production-equivalent validation.

## Historical readiness evidence

The lifecycle markers above are preserved deliberately. E8 is `PASS / REPOSITORY_COMPLETE`; Phase 8 is `PASS / OWNER_ACCEPTED` for its historical candidate; Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for its historical candidate; and Phase 10 remains the historical `NO-GO / BLOCKED` decision that triggered Phase 11. None of those historical evidence classes transfers to the materially changed current candidate.

## Phase 11.10 candidate-completion ledger

The following identifiers remain explicit because they are part of the accepted architecture and release-history contract:

1. 11.10a frontend architecture/design contract — `PASS / REPOSITORY_COMPLETE`;
2. 11.10b canonical application shell — `PASS / REPOSITORY_COMPLETE`;
3. 11.10c Command Center — `PASS / REPOSITORY_COMPLETE`;
4. 11.10d Unified Intelligence Workspace — `PASS / REPOSITORY_COMPLETE`;
5. 11.10e IntelOwl/Cortex integrated analysis — `PASS / REPOSITORY_COMPLETE`;
6. 11.10f OpenCTI graph/entity workspace — `PASS / REPOSITORY_COMPLETE`;
7. 11.10g MISP Sharing & Exchange — `PASS / REPOSITORY_COMPLETE`;
8. 11.10h TheHive Investigations & Cases — `PASS / REPOSITORY_COMPLETE`;
9. 11.10i Vulnerability & Exposure Center — `PASS / REPOSITORY_COMPLETE`;
10. 11.10j Sources & Collection Control Center — `PASS / REPOSITORY_COMPLETE`;
11. 11.10k Automation & Playbooks — `PASS / REPOSITORY_COMPLETE`;
12. 11.10l Governance & Evidence Center — `PASS / REPOSITORY_COMPLETE`;
13. 11.10m Operations & Administration — `PASS / REPOSITORY_COMPLETE`;
14. 11.10n role-aware UX/accessibility — `PASS / REPOSITORY_COMPLETE`;
15. 11.10o consolidation/full functional acceptance contracts — `PASS / REPOSITORY_COMPLETE`;
16. 11.10q functional completeness remediation — `MERGED / OWNER-AUTHORIZED`;
17. 11.10p fresh production-equivalent validation — `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`.

Repository acceptance of these controls does not establish production-equivalent behavior.

## Phase 11.10 functional recovery closure

PR #316 (`Phase 11.10q: Functional Completeness Remediation`) was merged on 2026-08-25. The final PR head was `a2dff382d7d08d9058db0d0540c9ef1af172090a`; the merge commit is `e0a6019f561eaedade250093225ca22d9c937e8b`. The owner explicitly directed the merge after GitHub reported zero failed pull-request workflow runs for that exact head.

The remediation integrated the canonical Administration control plane, Sources & Collection, Threat Intelligence population/default discovery, IOC Explorer inventory and pivots, Knowledge Graph discovery/population, Vulnerability & Exposure population/filtering, object-driven Analysis and Investigations, Sharing & Exchange, executable/observable Automation & Playbooks, Command Center readiness/trends, canonical Operations, and unmocked same-origin repository browser acceptance.

The merge decision is owner product acceptance for this repository lifecycle step. It is **not** new production-equivalent or external-assurance evidence. Historical Phase 8/9 evidence remains historical and cannot be transferred to the current candidate.

## Phase 11.10p — immutable candidate freeze and fresh production-equivalent validation

**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`

The next candidate must be frozen from an identified, synchronized `main` commit. The production-equivalent validation must evaluate that exact frozen identity and produce fresh candidate-bound evidence for at least:

- candidate/image/deployment identity;
- migration and compatibility behavior;
- upgrade behavior;
- rollback to the exact prior immutable digest plus post-rollback health;
- health/readiness and dependency behavior;
- representative saturation/capacity behavior;
- backup/recovery/continuity behavior;
- evidence integrity and traceability to the same candidate.

The existing controlled validation package remains authoritative:

- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `tools/phase11_production_equivalent_validation.py`;
- `backend/tests/test_phase11_10_production_equivalent_validation.py`;
- `.github/workflows/phase11-production-equivalent-validation.yml`.

Repository CI can validate the contracts and evidence package but cannot manufacture real production-equivalent observations. Missing, ambiguous, inaccessible, historical-only or mixed-candidate evidence must fail closed.

## Phase 11.11 — new independent external assurance

**Status:** `NOT STARTED / BLOCKED / WAITING FOR FRESH PRODUCTION-EQUIVALENT PASS`

Independent assurance must restart only after the new frozen candidate has passed production-equivalent validation. It must target the same immutable candidate identity; historical Phase 9 evidence cannot satisfy this gate.

## Phase 12 — formal production GO/NO-GO

**Status:** `NOT STARTED / BLOCKED`

A production `GO` requires accepted fresh production-equivalent evidence and fresh independent external assurance for the same release identity, together with accountable production ownership, residual-risk acceptance, IAM/secrets/network/recovery/monitoring/privacy/legal/change prerequisites and explicit rollback authority.

## Delivery discipline

Every material repository change remains bounded and reviewable with exact-head CI and synchronized documentation. External evidence classes remain external: repository changes must never be described as live, staging, production-equivalent, penetration-test or external-assurance proof unless that evidence actually exists and identifies the exact candidate.

## Immediate sequence

1. Complete candidate-readiness CI normalization and keep authoritative documentation synchronized.
2. Freeze one immutable candidate from the resulting synchronized `main` head.
3. Execute fresh production-equivalent validation against that exact candidate.
4. Record accountable acceptance or concrete failures; repair only root causes and refreeze if the candidate changes.
5. After production-equivalent acceptance, restart Phase 11.11 independent external assurance against the same immutable candidate.
6. Enter Phase 12 only after both fresh evidence classes are accepted.
