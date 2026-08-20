# DTMO Platform Industrialisation Roadmap

Last updated: **2026-08-20**  
Programme state: **`ACTIVE / HIGHEST PRIORITY`**

## Purpose

Phase 10 concluded with **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. Phase 11 is the successor industrialisation programme and is delivered one bounded PR at a time with exact-head CI, professional documentation and expected-head merge protection.

Historical Phase 8 remains `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` and historical Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`. These evidence packages are immutable history and cannot be reused for the materially changed integrated candidate. DTMO remains **not production authorized**.

## Fixed priority order

1. 11.1–11.2 Taranis AI architecture and canonical adapter.
2. 11.3 IntelOwl enrichment integration.
3. 11.4 OpenCTI knowledge-graph integration.
4. 11.5 MISP consolidation.
5. 11.6 TheHive incident/case handoff.
6. 11.7 Cortex decision gate.
7. 11.7b Cortex analyzer connector.
8. 11.8 Integrated runtime industrialisation.
9. 11.9 Migration and compatibility.
10. 11.10 Candidate completion and fresh production-equivalent validation.
11. 11.11 Independent external assurance.
12. Phase 12 — Production GO/NO-GO.

## Phase 11 — Platform industrialisation

### 11.1–11.2 Taranis AI
**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.3 IntelOwl enrichment integration
**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.4 OpenCTI knowledge-graph integration
**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.5 MISP consolidation
**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.6 TheHive incident/case handoff
**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.7 Cortex decision gate
**Status:** `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE`

### 11.7b Cortex analyzer connector
**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.8 Integrated runtime industrialisation
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8a Runtime foundation
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8b Workload identity and external secret delivery
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8c Ingress/TLS and network segmentation
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8d HA and disruption hardening
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8e Observability hardening
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8f Backup, restore and recovery hardening
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8g Software supply-chain hardening
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8h Capacity and resource planning
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8i Exercised upgrade and rollback
**Status:** `PASS / REPOSITORY_COMPLETE`

Accepted runtime evidence requires immutable image identities, safe rollout controls, post-upgrade/post-rollback health, recovery boundaries and restoration of the exact prior digest. Application rollback never authorizes automatic database down migration. Repository evidence does not itself prove production-equivalent behavior.

### 11.9 Migration and compatibility
**Status:** `PASS / REPOSITORY_COMPLETE`

The accepted contract requires one connected single-root/single-head Alembic chain, forward-first migration, backward-compatible rolling overlap and expand/migrate/contract for destructive changes. Ambiguity fails closed.

### 11.10 Integrated production-equivalent validation
**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`

The Unified Operations Workbench materially changes the candidate. Therefore 11.10 first completes the interface and integrated user journeys in bounded candidate-completion slices. Only after 11.10o is accepted is one immutable candidate frozen for the fresh 11.10p real-environment exercise.

#### Candidate-completion sequence

- **11.10a Frontend architecture and design contract** — `PASS / REPOSITORY_COMPLETE`;
- **11.10b Canonical application shell** — `PASS / REPOSITORY_COMPLETE`;
- **11.10c Command Center** — `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- **11.10d Unified Intelligence Workspace** — `NOT STARTED`;
- **11.10e IntelOwl/Cortex integrated analysis** — `NOT STARTED`;
- **11.10f OpenCTI graph/entity workspace** — `NOT STARTED`;
- **11.10g MISP Sharing & Exchange** — `NOT STARTED`;
- **11.10h TheHive Investigations & Cases** — `NOT STARTED`;
- **11.10i Vulnerability & Exposure Center** — `NOT STARTED`;
- **11.10j Sources & Collection Control Center** — `NOT STARTED`;
- **11.10k Automation & Playbooks** — `NOT STARTED`;
- **11.10l Governance & Evidence Center** — `NOT STARTED`;
- **11.10m Operations & Administration** — `NOT STARTED`;
- **11.10n Role-aware UX/accessibility** — `NOT STARTED`;
- **11.10o Consolidation and full functional acceptance** — `NOT STARTED`;
- **11.10p Fresh production-equivalent validation** — `NOT STARTED / CANDIDATE FREEZE REQUIRED`.

#### 11.10a–11.10b accepted workbench foundation

The accepted canonical path is **browser → DTMO API → governed integration adapter → upstream service**. The browser never becomes a privileged upstream integration client. **Server-side RBAC**, provenance, human publication/share authority, separate TheHive case authority and fail-closed behavior remain authoritative.

11.10b delivered the React/TypeScript/Vite canonical `/workbench/` shell, committed npm lockfile consumed with `npm ci`, responsive navigation, context rail, command palette, same-origin CSP/asset serving and `/ui/console` as a temporary **compatibility path**.

Accepted evidence remains:

- `docs/architecture/FRONTEND_ARCHITECTURE.md`;
- `docs/architecture/UI_API_CONTRACT.md`;
- `docs/architecture/PHASE11_10B_APPLICATION_SHELL.md`;
- `docs/qa/PHASE11_10A_FRONTEND_ARCHITECTURE_GATE.md`;
- `docs/qa/PHASE11_10B_APPLICATION_SHELL_GATE.md`;
- `.github/workflows/phase11-frontend-architecture.yml`;
- `.github/workflows/phase11-application-shell.yml`.

#### 11.10c active Command Center

11.10c delivers the first functional canonical workspace. It provides accountable read-only visibility into canonical intelligence counts, high/critical activity, 24-hour intake, review/share-decision workload, high education relevance, recent intelligence and the configured capability state of Taranis, IntelOwl, OpenCTI, MISP, TheHive and Cortex.

It must never turn a feature flag or API configuration into a `healthy` claim. Persisted execution may be shown only as attributable observation. When the canonical datastore is unavailable, metric values remain unavailable rather than synthetic zero values. Role-aware quick-action visibility is usability only and never substitutes for server authorization.

Authoritative 11.10c package:

- `backend/dtmo/command_center.py`;
- `backend/dtmo/api_command_center.py`;
- `frontend/src/App.tsx`;
- `frontend/src/command-center.css`;
- `docs/architecture/PHASE11_10C_COMMAND_CENTER.md`;
- `docs/qa/PHASE11_10C_COMMAND_CENTER_GATE.md`;
- `backend/tests/test_phase11_10c_command_center_contract.py`;
- `backend/tests/test_phase11_10c_command_center_browser.py`;
- `.github/workflows/phase11-command-center.yml`.

Only after 11.10c is accepted and merged may **11.10d Unified Intelligence Workspace** begin.

#### 11.10p Fresh production-equivalent validation

After 11.10o acceptance, one immutable integrated candidate is frozen. 11.10p requires fresh evidence for candidate identity, migration/compatibility, upgrade, exact prior-digest rollback with post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity, all bound to the **same immutable** candidate and one approved environment.

The execution package remains:

- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `tools/phase11_production_equivalent_validation.py`;
- `backend/tests/test_phase11_10_production_equivalent_validation.py`;
- `.github/workflows/phase11-production-equivalent-validation.yml`.

Historical Phase 8/9 evidence cannot satisfy 11.10p. Missing, ambiguous, inaccessible, historical-only or mixed-candidate evidence must **fail closed**. Repository CI validates repository contracts only and does not prove production-equivalent execution or production authorization.

### 11.11 Independent external assurance
**Status:** `NOT STARTED`

Fresh independent assurance may start only after Phase 11.10 is explicitly `PASS / OWNER_ACCEPTED` and must target the same immutable integrated candidate.

## Phase 12 — Production GO/NO-GO
**Status:** `NOT STARTED`

A production `GO` requires accepted 11.10 and 11.11 evidence for the same release identity plus accountable ownership, residual-risk, support/change and rollback authority. Missing evidence remains fail-closed.

## Immediate sequence

1. Complete **11.10c Command Center** on one exact green head and merge with expected-head protection.
2. Start **11.10d Unified Intelligence Workspace** only after 11.10c is merged.
3. Continue 11.10e–11.10o one bounded green PR at a time.
4. Freeze one immutable candidate and execute **11.10p**.
5. Complete fresh **11.11** independent assurance for that same candidate.
6. Enter **Phase 12** only after 11.10 and 11.11 are accepted.
