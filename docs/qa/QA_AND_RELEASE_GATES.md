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
| Phase 11.10e IntelOwl/Cortex integrated analysis | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.10f OpenCTI graph/entity workspace | `NOT STARTED` |
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
| Command Center | Canonical read model, fail-closed metrics, role-aware visibility and browser experience | Accepted Phase 11.10c repository/browser evidence |
| Unified Intelligence Workspace | Governed search, IOC-oriented discovery, canonical detail/provenance and fail-closed browser behavior | Accepted Phase 11.10d repository/browser evidence |
| Integrated Analysis Workspace | Human-triggered IntelOwl/Cortex execution, immutable evidence history, server RBAC and no-verdict boundary | Active Phase 11.10e repository/browser evidence |
| Candidate workspaces | Bounded workbench capabilities, browser E2E, RBAC, accessibility | Phase 11.10f–11.10o repository/owner evidence |
| Production-equivalent validation | Same-candidate migration/upgrade/rollback/health/saturation/recovery | Phase 11.10p real-environment evidence |
| Independent assurance | Independent assessment of integrated candidate | Phase 11.11 |
| Production decision | Formal accountable GO/NO-GO | Phase 12 |

## Accepted Phase 11.1–11.9 baseline

Taranis AI, IntelOwl, OpenCTI, MISP, TheHive and Cortex repository integration boundaries remain `PASS / REPOSITORY_COMPLETE`; the original 11.7 Cortex decision remains a historical accepted decision baseline. Phase 11.8 is repository-complete across runtime foundation, workload identity/external secrets, ingress/TLS/network segmentation, HA/disruption, observability, backup/recovery, supply-chain, capacity and exercised upgrade/rollback. Phase 11.9 is repository-complete for the migration graph and forward-first compatibility contract.

These gates remain regression-protected and do not become live deployment or production evidence by themselves.

## Accepted Phase 11.10a frontend architecture gate

Authoritative accepted package:

- `docs/architecture/FRONTEND_ARCHITECTURE.md`;
- `docs/architecture/UI_API_CONTRACT.md`;
- `docs/ux/UNIFIED_OPERATIONS_WORKBENCH.md`;
- `docs/ux/INFORMATION_ARCHITECTURE.md`;
- `docs/ux/DESIGN_SYSTEM.md`;
- `docs/qa/PHASE11_10A_FRONTEND_ARCHITECTURE_GATE.md`;
- `backend/tests/test_phase11_10a_frontend_architecture_contract.py`;
- `.github/workflows/phase11-frontend-architecture.yml`.

Accepted invariant: **browser → DTMO API → governed integration adapter → upstream service**, with server-side RBAC and human authority boundaries preserved.

## Accepted Phase 11.10b application shell gate

Authoritative accepted package:

- `frontend/package.json` and committed `frontend/package-lock.json`;
- `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/styles.css`;
- `backend/dtmo/workbench_frontend.py`;
- `docs/architecture/PHASE11_10B_APPLICATION_SHELL.md`;
- `docs/qa/PHASE11_10B_APPLICATION_SHELL_GATE.md`;
- `backend/tests/test_phase11_10b_application_shell_contract.py`;
- `backend/tests/test_phase11_10b_application_shell_browser.py`;
- `.github/workflows/phase11-application-shell.yml`.

11.10b accepted the React/TypeScript/Vite `/workbench/` shell, `npm ci` dependency immutability, same-origin serving/CSP, keyboard/mobile navigation and `/ui/console` as a temporary **compatibility path**. It did **not prove** live upstream connectivity or production-equivalent execution.

## Accepted Phase 11.10c Command Center gate

Dedicated gate: `docs/qa/PHASE11_10C_COMMAND_CENTER_GATE.md`  
Workflow: `.github/workflows/phase11-command-center.yml`

The accepted exact-head contract proves repository-controlled behavior for `/api/v1/command-center`, canonical-store fail-closed metrics, separation between integration configuration and runtime observation, role-aware visibility without authority, read-only Command Center behavior, frontend build/browser rendering and synchronized documentation.

Repository acceptance **does not prove** upstream service health, production-equivalent operation, independent assurance or production authorization.

## Accepted Phase 11.10d Unified Intelligence Workspace gate

Dedicated gate: `docs/qa/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE_GATE.md`  
Workflow: `.github/workflows/phase11-unified-intelligence-workspace.yml`

The accepted contract covers functional read-only `/workbench/intelligence` and `/workbench/intelligence/iocs`, governed `/api/v1/intelligence/search` discovery, canonical `/api/v1/intelligence/{item_id}/workspace` detail/provenance, explicit search/filter controls, fail-closed dependency behavior and deterministic browser acceptance. Server-side `read:intelligence` remains authoritative and search/object investigation grants no review/share/case/connector/analyzer/admin mutation authority.

Repository/browser acceptance **does not prove** upstream completeness or health, production-equivalent operation, independent assurance or production authorization.

## Active Phase 11.10e Integrated Analysis Workspace gate

Dedicated gate: `docs/qa/PHASE11_10E_INTEGRATED_ANALYSIS_GATE.md`  
Workflow: `.github/workflows/phase11-integrated-analysis-workspace.yml`

The final exact head must prove:

- `/workbench/analysis` renders one canonical Analysis & Enrichment workspace;
- `GET /api/v1/analysis/capabilities` exposes configured allowlists/capability state but never promotes configuration to runtime health;
- `GET /api/v1/analysis/items/{item_id}/history` combines persisted IntelOwl and Cortex evidence for one canonical item;
- the existing IntelOwl enrichment route remains server-authorized by `review:intelligence` and retains its policy/persistence controls;
- `POST /api/v1/analysis/items/{item_id}/cortex` is analyzer-only, feature-gated, allowlist/TLP validated and server-authorized by `review:intelligence`;
- migration `0015_cortex_analysis_history` is connected to `0014_thehive_handoff_state` and durable Cortex records are idempotent by item/job identity;
- persisted Cortex results enforce `external_share_authorized=false` and `local_compromise_proven=false`;
- Cortex responders, automatic analyzer discovery and automatic IntelOwl fallback remain outside scope;
- read-only principals can inspect history but are not presented with authorized execution controls;
- dependency/policy/persistence failures **fail closed** and no synthetic successful analysis is fabricated;
- frontend typecheck/build and deterministic browser acceptance succeed;
- professional current-state, evidence and roadmap documentation is synchronized.

IntelOwl/Cortex analyzer output **does not prove** local compromise and grants no external-share, publication, case or production authority. Repository/browser acceptance does not prove live upstream availability/provider authorization, production-equivalent operation, independent assurance or production authorization.

After 11.10e exact-head acceptance and merge, the only next bounded priority is **Phase 11.10f OpenCTI graph/entity workspace**.

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
