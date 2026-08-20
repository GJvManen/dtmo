# DTMO Platform Industrialisation Roadmap

Last updated: **2026-08-20**  
Programme state: **`ACTIVE / HIGHEST PRIORITY`**

## Purpose

Phase 10 concluded with **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. Phase 11 is the successor industrialisation programme and is delivered one bounded PR at a time with exact-head CI, professional documentation and expected-head merge protection.

Historical Phase 8 remains `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` and historical Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`. These evidence packages are immutable history and cannot be reused for the materially changed integrated candidate. DTMO remains **not production authorized**.

## Fixed priority order

1. 11.1 Taranis AI architecture/API/data-model/identity/licensing assessment.
2. 11.2 Taranis → DTMO canonical adapter.
3. 11.3 IntelOwl enrichment integration.
4. 11.4 OpenCTI STIX knowledge-graph integration.
5. 11.5 MISP consolidation and authoritative governed sharing model.
6. 11.6 TheHive incident/case handoff.
7. 11.7 Cortex conditional decision gate.
8. 11.7b owner-required Cortex analyzer connector.
9. 11.8 Kubernetes/Helm/GitOps plus HA/secrets/network/observability/recovery/supply-chain/capacity/upgrade hardening.
10. 11.9 migration/compatibility.
11. 11.10 integrated candidate completion and new production-equivalent validation.
12. Phase 11.11 new independent external assurance.
13. Phase 12 formal production GO/NO-GO.

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

The accepted contract requires one connected single-root/single-head Alembic chain, forward-first migration, backward-compatible rolling overlap and expand/migrate/contract for destructive changes. Ambiguity must **fail closed**.

### 11.10 Integrated production-equivalent validation
**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`

The Unified Operations Workbench materially changes the candidate. Candidate-completion slices are therefore accepted before one immutable integrated candidate is frozen for the fresh 11.10p real-environment exercise.

#### Candidate-completion sequence

- **11.10a Frontend architecture and design contract** — `PASS / REPOSITORY_COMPLETE`;
- **11.10b Canonical application shell** — `PASS / REPOSITORY_COMPLETE`;
- **11.10c Command Center** — `PASS / REPOSITORY_COMPLETE`;
- **11.10d Unified Intelligence Workspace** — `PASS / REPOSITORY_COMPLETE`;
- **11.10e IntelOwl/Cortex integrated analysis** — `PASS / REPOSITORY_COMPLETE`;
- **11.10f OpenCTI graph/entity workspace** — `PASS / REPOSITORY_COMPLETE`;
- **11.10g MISP Sharing & Exchange** — `PASS / REPOSITORY_COMPLETE`;
- **11.10h TheHive Investigations & Cases** — `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- **11.10i Vulnerability & Exposure Center** — `NOT STARTED`;
- **11.10j Sources & Collection Control Center** — `NOT STARTED`;
- **11.10k Automation & Playbooks** — `NOT STARTED`;
- **11.10l Governance & Evidence Center** — `NOT STARTED`;
- **11.10m Operations & Administration** — `NOT STARTED`;
- **11.10n Role-aware UX/accessibility** — `NOT STARTED`;
- **11.10o Consolidation and full functional acceptance** — `NOT STARTED`;
- **11.10p Fresh production-equivalent validation** — `NOT STARTED / CANDIDATE FREEZE REQUIRED`.

#### Accepted workbench foundation through 11.10g

The accepted canonical path is **browser → DTMO API → governed integration adapter → upstream service**. The browser never becomes a privileged upstream integration client. **Server-side RBAC**, provenance, human publication/share authority, separate TheHive case authority and fail-closed behavior remain authoritative.

11.10a–11.10g delivered the frontend architecture, React/TypeScript/Vite canonical shell, Command Center, Unified Intelligence Workspace, Integrated Analysis workspace, OpenCTI Graph/Entity workspace and MISP Sharing/Exchange workspace. IntelOwl/Cortex output remains evidence rather than a compromise verdict. OpenCTI generic relationship topology is not inferred beyond persisted mapping evidence. MISP technical transfer remains separate from publication/synchronization authority.

#### 11.10h active TheHive Investigations & Cases

11.10h makes `/workbench/investigations` functional using the accepted Phase 11.6 human-authorized TheHive handoff/persistence boundary rather than a parallel case backend.

Frontend-facing state contract:

- `GET /api/v1/thehive/items/{item_id}/investigation` — canonical intelligence, provenance and durable handoff state protected by `read:intelligence`.

Existing governed action remains authoritative:

- `POST /api/v1/thehive/items/{item_id}/cases` — explicit human `handoff:case` case creation.

Service accounts cannot substitute for human case authority. Canonical provenance remains mandatory. The browser never receives TheHive credentials or organization authorization and does not call TheHive directly. TLP/PAP and authoritative source restrictions fail closed.

Durable `reserved`, `delivered`, `ambiguous` and `failed` handoff evidence is exposed. `reserved` or `ambiguous` state requires manual reconciliation and the canonical UI blocks a blind new case request. A delivered result proves only stable case identity at creation time.

The accepted persistence does not mirror generic TheHive alerts, tasks, case timeline, later case state or responder results. 11.10h therefore does not infer them. Configuration is not live TheHive health. Case/handoff evidence does not prove external-share authority, responder/remediation execution, local compromise or production readiness.

Authoritative 11.10h package:

- `backend/dtmo/thehive_handoff.py`;
- `backend/dtmo/integrations/thehive.py`;
- `backend/dtmo/persistence/thehive.py`;
- `frontend/src/InvestigationsWorkspace.tsx`;
- `frontend/src/investigations.css`;
- `docs/architecture/PHASE11_10H_THEHIVE_INVESTIGATIONS_CASES.md`;
- `docs/user/THEHIVE_INVESTIGATIONS_WORKSPACE.md`;
- `docs/qa/PHASE11_10H_THEHIVE_INVESTIGATIONS_GATE.md`;
- `backend/tests/test_phase11_10h_thehive_investigations_contract.py`;
- `backend/tests/test_phase11_10h_thehive_investigations_api.py`;
- `backend/tests/test_phase11_10h_thehive_investigations_browser.py`;
- `.github/workflows/phase11-thehive-investigations.yml`.

Only after 11.10h is accepted and merged may **11.10i Vulnerability & Exposure Center** begin.

#### 11.10p Fresh production-equivalent validation

After 11.10o acceptance, one immutable integrated candidate is frozen. 11.10p requires fresh evidence for candidate identity, migration/compatibility, upgrade, exact prior-digest rollback with post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity, all bound to the **same immutable** candidate and one approved environment.

The execution package remains:

- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `tools/phase11_production_equivalent_validation.py`;
- `backend/tests/test_phase11_10_proDUCTION_EQUIVALENT_VALIDATION.py`;
- `.github/workflows/phase11-production-equivalent-validation.yml`.

Historical Phase 8/9 evidence cannot satisfy 11.10p. Missing, ambiguous, inaccessible, historical-only or mixed-candidate evidence must **fail closed**. Repository CI validates repository contracts only and does not prove production-equivalent execution or production authorization.

### Phase 11.11 Independent external assurance
**Status:** `NOT STARTED`

Fresh independent assurance may start only after Phase 11.10 is explicitly `PASS / OWNER_ACCEPTED` and must target the same immutable integrated candidate.

## Phase 12 — Production GO/NO-GO
**Status:** `NOT STARTED`

A production `GO` requires accepted 11.10 and 11.11 evidence for the same release identity plus accountable ownership, residual-risk, support/change and rollback authority. Missing evidence remains fail-closed.

## Immediate sequence

1. Complete **11.10h TheHive Investigations & Cases** on one exact green head and merge with expected-head protection.
2. Start **11.10i Vulnerability & Exposure Center** only after 11.10h is merged.
3. Continue 11.10j–11.10o one bounded green PR at a time.
4. Freeze one immutable candidate and execute **11.10p**.
5. Complete fresh **Phase 11.11** independent assurance for that same candidate.
6. Enter **Phase 12** only after 11.10 and 11.11 are accepted.
