# DTMO QA and Release Gates

## Purpose

DTMO separates repository engineering evidence, accountable functional acceptance, production-equivalent validation, independent assurance and formal production authorization. The release model is fail-closed: configured checks, mock data, design artifacts or documented intent are never promoted to evidence they do not establish.

## Core release principles

1. **Exact-head evidence** — PR evidence belongs only to the exact final PR head.
2. **New commit, new evidence** — any new commit invalidates earlier exact-head acceptance evidence for that PR.
3. **No inferred PASS** — queued, in-progress, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
4. **Expected-head merge protection** — merge must reject a moved head.
5. **Evidence classes remain separate** — CI, owner acceptance, real-environment validation, external assurance and production authorization are not interchangeable.
6. **Historical evidence is immutable** — later lifecycle changes do not rewrite prior candidate evidence.
7. **One bounded objective per PR** — the next slice does not start before the current slice is green and merged.
8. **Professional documentation is a merge criterion** — affected authoritative documentation and its CI contracts must be current on the exact head.
9. **External evidence remains external** — fixtures, emulators, screenshots, mock responses and CI artifacts do not prove production-equivalent operation.
10. **UI convenience is not authority** — role-aware visibility never replaces **server-side RBAC** or required human approval.

## Current acceptance status

| Stage | Status |
|---|---|
| Phases 1–7 | `PASS` |
| RC13 functional console | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 10 | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11 | `IN PROGRESS / ACTIVE` |
| Phase 11.1–11.9 | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10 production-equivalent validation | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` |
| Phase 11.10a–11.10h | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10i Vulnerability & Exposure Center | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.10j Sources & Collection Control Center | `NOT STARTED` |
| Phase 11.10p production-equivalent validation | `NOT STARTED / CANDIDATE FREEZE REQUIRED` |
| Phase 11.11 independent external assurance | `NOT STARTED` |
| Phase 12 | `NOT STARTED` |

DTMO is **not production authorized**.

## Gate families

| Gate family | Objective | Evidence boundary |
|---|---|---|
| Build & quality | Packaging, lint, typing, tests | Repository CI |
| Security & identity | Authentication, authorization, secrets, privileged actions | Repository CI + deployed assurance |
| Data integrity & recovery | Migration, persistence, integrity, recovery | Repository CI + deployed validation |
| Connector reliability | Contract/state/retry/timeout/replay/provenance/isolation | Repository CI + deployed validation |
| Governance | Mapping truth and authority separation | Repository CI + governance review |
| Platform integration | Upstream API/model interoperability | Phase 11 repository evidence |
| Integrated runtime | Kubernetes/Helm/GitOps, identity, network, HA, recovery, observability, supply chain | Phase 11 repository + deployed evidence |
| Workbench slices 11.10a–h | Accepted bounded functionality | Repository/browser evidence |
| Vulnerability & Exposure | Canonical vulnerability evidence, prioritization semantics and fail-closed degraded state | Active Phase 11.10i repository/browser evidence |
| Candidate workspaces | Remaining bounded workbench capabilities, browser E2E, RBAC, accessibility | Phase 11.10j–11.10o repository/owner evidence |
| Production-equivalent validation | Same-candidate migration/upgrade/rollback/health/saturation/recovery | Phase 11.10p real-environment evidence |
| Independent assurance | Independent assessment of integrated candidate | Phase 11.11 |
| Production decision | Formal accountable GO/NO-GO | Phase 12 |

## Accepted Phase 11.10a–11.10h baseline

The accepted workbench sequence preserves the invariant **browser → DTMO API → governed integration adapter → upstream service**, with server-side RBAC and human authority boundaries intact. Command Center, Unified Intelligence, Integrated Analysis, OpenCTI, MISP and TheHive repository/browser acceptance remain regression protected. None of these accepted slices proves live upstream health, local compromise or production authorization.

## Active Phase 11.10i Vulnerability & Exposure gate

Dedicated gate: `docs/qa/PHASE11_10I_VULNERABILITY_EXPOSURE_GATE.md`  
Workflow: `.github/workflows/phase11-vulnerability-exposure.yml`

The final exact head must prove:

- `/workbench/exposure` is wired to `ExposureWorkspace` inside the canonical application shell;
- browser code calls the same-origin DTMO API only;
- the workspace uses the accepted canonical vulnerability analytics projection rather than a parallel datastore;
- server-side `read:intelligence` remains the authoritative access boundary;
- CVSS, EPSS, KEV, CWE and vendor/product mappings are represented as prioritization evidence rather than local-exposure or compromise assertions;
- missing, malformed, inaccessible or degraded evidence fails closed and is not rendered as a healthy or zero-risk state;
- no browser-held scanner/upstream credentials are introduced;
- no remediation, publication/share or case authority is introduced;
- deterministic contract coverage and frontend production build succeed;
- application-shell and relevant accessibility/frontend regression gates succeed;
- professional current-state, architecture, user/operator, QA and evidence-boundary documentation is synchronized.

Repository/browser acceptance **does not prove** live vulnerability-source health, asset exposure, exploitability, compromise, remediation, production-equivalent operation, independent assurance or production authorization.

Any commit after an all-green run invalidates that run for merge acceptance. Merge requires every workflow registered for the final exact head to be `completed/success`, the PR to be ready for review and expected-head protection to match that same SHA.

After 11.10i exact-head acceptance and protected merge, the only next bounded priority is **Phase 11.10j — Sources & Collection Control Center**.

## Phase 11.10p production-equivalent gate

After 11.10o, one immutable integrated candidate is frozen. Fresh real-environment evidence must cover candidate identity, migration/compatibility, upgrade, exact prior-digest rollback with post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity.

Authoritative package:

- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `tools/phase11_production_equivalent_validation.py`;
- `backend/tests/test_phase11_10_production_equivalent_validation.py`;
- `.github/workflows/phase11-production-equivalent-validation.yml`.

All external evidence must identify the **same immutable** candidate and environment. Historical Phase 8/9 evidence cannot satisfy 11.10p. Missing, placeholder, inaccessible or mixed-candidate evidence must **fail closed**. Repository CI alone cannot complete 11.10.

## Phase 11.11 and Phase 12

Phase 11.11 remains `NOT STARTED` until 11.10 is explicitly `PASS / OWNER_ACCEPTED` and must assess the same immutable candidate. Phase 12 remains `NOT STARTED`; only an accountable Phase 12 GO can authorize production.
