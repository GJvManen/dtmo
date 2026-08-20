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
| Phase 11.10a frontend architecture/design contract | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10b canonical application shell | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10c Command Center | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10d Unified Intelligence Workspace | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10e IntelOwl/Cortex integrated analysis | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10f OpenCTI graph/entity workspace | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10g MISP Sharing & Exchange | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.10h TheHive Investigations & Cases | `NOT STARTED` |
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
| Frontend architecture/design | Canonical workbench and UI/API trust path | Phase 11.10a repository evidence |
| Canonical application shell | Build, route, CSP, responsive shell and browser mechanics | Phase 11.10b repository/browser evidence |
| Command Center | Canonical read model and truthful degraded state | Accepted Phase 11.10c repository/browser evidence |
| Unified Intelligence Workspace | Governed search and canonical detail/provenance | Accepted Phase 11.10d repository/browser evidence |
| Integrated Analysis Workspace | Human-triggered IntelOwl/Cortex analysis and immutable evidence history | Accepted Phase 11.10e repository/browser evidence |
| OpenCTI Graph / Entity Workspace | Persisted graph/entity evidence with no inferred topology | Accepted Phase 11.10f repository/browser evidence |
| MISP Sharing & Exchange | Separate human review/share approval, authoritative handling and unpublished replay-protected export | Active Phase 11.10g repository/browser evidence |
| Candidate workspaces | Bounded workbench capabilities, browser E2E, RBAC, accessibility | Phase 11.10h–11.10o repository/owner evidence |
| Production-equivalent validation | Same-candidate migration/upgrade/rollback/health/saturation/recovery | Phase 11.10p real-environment evidence |
| Independent assurance | Independent assessment of integrated candidate | Phase 11.11 |
| Production decision | Formal accountable GO/NO-GO | Phase 12 |

## Accepted Phase 11.1–11.9 baseline

Taranis AI, IntelOwl, OpenCTI, MISP, TheHive and Cortex repository integration boundaries remain `PASS / REPOSITORY_COMPLETE`; the original 11.7 Cortex decision remains historical accepted decision evidence. Phase 11.8 runtime industrialisation and Phase 11.9 forward-first migration/compatibility are regression protected. Repository acceptance does not become live deployment or production evidence by itself.

## Accepted Phase 11.10a–11.10f gates

The accepted workbench sequence preserves the invariant **browser → DTMO API → governed integration adapter → upstream service**, with server-side RBAC and human authority boundaries intact.

Accepted packages include:

- Phase 11.10a: `docs/qa/PHASE11_10A_FRONTEND_ARCHITECTURE_GATE.md`, `.github/workflows/phase11-frontend-architecture.yml`;
- Phase 11.10b: `docs/qa/PHASE11_10B_APPLICATION_SHELL_GATE.md`, `.github/workflows/phase11-application-shell.yml`;
- Phase 11.10c: `docs/qa/PHASE11_10C_COMMAND_CENTER_GATE.md`, `.github/workflows/phase11-command-center.yml`;
- Phase 11.10d: `docs/qa/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE_GATE.md`, `.github/workflows/phase11-unified-intelligence-workspace.yml`;
- Phase 11.10e: `docs/qa/PHASE11_10E_INTEGRATED_ANALYSIS_GATE.md`, `.github/workflows/phase11-integrated-analysis-workspace.yml`;
- Phase 11.10f: `docs/qa/PHASE11_10F_OPENCTI_GRAPH_ENTITY_GATE.md`, `.github/workflows/phase11-opencti-graph-workspace.yml`.

11.10e accepted human-triggered IntelOwl enrichment and analyzer-only Cortex execution/history. 11.10f accepted a read-only graph over persisted OpenCTI/STIX mappings without inferred generic upstream topology. Neither output class proves local compromise or grants external-share/publication/case authority.

## Active Phase 11.10g MISP Sharing & Exchange gate

Dedicated gate: `docs/qa/PHASE11_10G_MISP_SHARING_EXCHANGE_GATE.md`  
Workflow: `.github/workflows/phase11-misp-sharing-exchange.yml`

The final exact head must prove:

- `/workbench/sharing` is functional inside the canonical workbench;
- browser code calls DTMO APIs only and contains no privileged MISP credential or direct MISP request;
- `GET /api/v1/sharing/items/{item_id}` requires server-side `read:intelligence`;
- review remains separately protected by `review:intelligence`;
- share approval remains separately protected by `approve:share`;
- the share approver is a different human principal from the reviewer and service accounts cannot substitute for either human decision;
- MISP export cannot grant approval itself and accepts only already reviewed/share-approved canonical state;
- authoritative MISP distribution, sharing-group and TLP restrictions cannot be weakened on re-export;
- MISP-origin intelligence without authoritative restriction evidence fails closed;
- deterministic current-revision replay remains blocked after `pending`, `success` or `uncertain` export evidence;
- uncertain delivery is not automatically replayed;
- exported events are created with `published=false`;
- no Publish or Synchronize action exists in Phase 11.10g;
- feature/configuration state is not presented as runtime health;
- dependency failure renders unavailable rather than synthetic approval/export eligibility;
- frontend typecheck/build, deterministic browser acceptance and accepted Phase 11.5/E8 MISP regressions succeed;
- professional current-state, evidence and roadmap documentation is synchronized.

Missing or ambiguous authority/handling evidence must **fail closed**. Successful technical event creation does **not prove** MISP publication, synchronization, downstream consumption, local compromise or remediation status.

Repository/browser acceptance **does not prove** live MISP connectivity or health, production-equivalent operation, independent assurance or production authorization.

After 11.10g exact-head acceptance and merge, the only next bounded priority is **Phase 11.10h TheHive Investigations & Cases**.

## Phase 11.10p production-equivalent gate

After 11.10o, one immutable integrated candidate is frozen. Fresh real-environment evidence must cover candidate identity, migration/compatibility, upgrade, exact prior-digest rollback with post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity.

Authoritative package:

- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `tools/phase11_production_equivalent_validation.py`;
- `backend/tests/test_phase11_10_production_equivalent_validation.py`;
- `.github/workflows/phase11-production-equivalent-validation.yml`.

All external evidence must identify the **same immutable** candidate and environment. Historical Phase 8/9 evidence cannot satisfy 11.10p. Missing, placeholder, inaccessible or mixed-candidate evidence must **fail closed**. Repository-green status alone cannot complete 11.10.

## Phase 11.11 and Phase 12

Phase 11.11 remains `NOT STARTED` until 11.10 is explicitly `PASS / OWNER_ACCEPTED` and must assess the same immutable candidate. Phase 12 remains `NOT STARTED`; only an accountable Phase 12 GO can authorize production.
