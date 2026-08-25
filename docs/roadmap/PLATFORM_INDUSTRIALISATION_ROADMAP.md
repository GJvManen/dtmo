# DTMO Platform Industrialisation Roadmap

Last updated: **2026-08-25**  
Programme state: **`ACTIVE / IN PROGRESS — FRESH CANDIDATE VALIDATION`**

## Purpose and release truth

Phase 10 concluded with the historical **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`** decision. Phase 11 is the successor industrialisation programme and remains `IN PROGRESS` while the current integrated candidate advances through fresh candidate-bound validation. DTMO remains **not production authorized**.

Historical lifecycle evidence is preserved explicitly: E8 is `PASS / REPOSITORY_COMPLETE`; Phase 8 is `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE`; Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`. Those packages are immutable history and cannot be reused for the materially changed integrated candidate.

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

### 11.1–11.7b governed service integrations
**Status:** `PASS / REPOSITORY_COMPLETE`

Taranis AI, IntelOwl, OpenCTI, MISP, TheHive and Cortex are integrated through DTMO-owned server-side contracts. Browser access does not become privileged upstream access. Credentials remain server-side. Enrichment output is evidence rather than a compromise verdict. MISP transport is separate from human review/share/publication authority. TheHive case handoff remains separately authorized. Graph topology is not inferred beyond persisted evidence.

### 11.8 Integrated runtime industrialisation
**Status:** `PASS / REPOSITORY_COMPLETE`

The repository baseline covers Kubernetes/Helm/GitOps, workload identity/external secret delivery, ingress/TLS/network segmentation, HA/disruption handling, observability, backup/recovery, software supply-chain controls, capacity planning and upgrade/rollback contracts. Repository acceptance does not itself prove production-equivalent behavior.

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

Accepted runtime evidence requires immutable image identities, safe rollout controls, post-upgrade/post-rollback health, recovery boundaries and restoration of the exact prior digest. Application rollback never authorizes automatic database down migration. Missing or ambiguous evidence must **fail closed**.

### 11.9 Migration and compatibility
**Status:** `PASS / REPOSITORY_COMPLETE`

The accepted contract requires one connected single-root/single-head Alembic chain, forward-first migration, backward-compatible rolling overlap and expand/migrate/contract for destructive changes. Ambiguity must **fail closed**.

### 11.10 Integrated candidate completion and validation
**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`

The Unified Operations Workbench materially changes the candidate. Repository candidate completion and functional recovery are merged; Phase 11 remains in progress until a new immutable candidate completes fresh production-equivalent validation and the subsequent lifecycle gates.

#### Candidate-completion sequence

- **11.10a Frontend architecture and design contract** — `PASS / REPOSITORY_COMPLETE`;
- **11.10b Canonical application shell** — `PASS / REPOSITORY_COMPLETE`;
- **11.10c Command Center** — `PASS / REPOSITORY_COMPLETE`;
- **11.10d Unified Intelligence Workspace** — `PASS / REPOSITORY_COMPLETE`;
- **11.10e IntelOwl/Cortex integrated analysis** — `PASS / REPOSITORY_COMPLETE`;
- **11.10f OpenCTI graph/entity workspace** — `PASS / REPOSITORY_COMPLETE`;
- **11.10g MISP Sharing & Exchange** — `PASS / REPOSITORY_COMPLETE`;
- **11.10h TheHive Investigations & Cases** — `PASS / REPOSITORY_COMPLETE`;
- **11.10i Vulnerability & Exposure Center** — `PASS / REPOSITORY_COMPLETE`;
- **11.10j Sources & Collection Control Center** — `PASS / REPOSITORY_COMPLETE`;
- **11.10k Automation & Playbooks** — `PASS / REPOSITORY_COMPLETE`;
- **11.10l Governance & Evidence Center** — `PASS / REPOSITORY_COMPLETE`;
- **11.10m Operations & Administration** — `PASS / REPOSITORY_COMPLETE`;
- **11.10n Role-aware UX/accessibility** — `PASS / REPOSITORY_COMPLETE`;
- **11.10o Consolidation and full functional acceptance contracts** — `PASS / REPOSITORY_COMPLETE`;
- **11.10q Functional completeness remediation** — `MERGED / OWNER-AUTHORIZED`;
- **11.10p Fresh production-equivalent validation** — `IN PROGRESS / CANDIDATE FREEZE REQUIRED`.

The explicit 11.10a–11.10l identifiers above remain part of the authoritative architecture history and must not be collapsed away by lifecycle summaries.

#### Accepted workbench foundation and functional recovery

The canonical path is **browser → DTMO API → governed integration adapter/data contract → governed service/evidence source**. The browser never becomes a privileged upstream integration client. **Server-side RBAC**, provenance, human review/share/publication authority, separate case authority, replay protection and fail-closed behavior remain authoritative.

PR #316 (`Phase 11.10q: Functional Completeness Remediation`) was merged on 2026-08-25 from exact head `a2dff382d7d08d9058db0d0540c9ef1af172090a` as merge commit `e0a6019f561eaedade250093225ca22d9c937e8b` after the owner explicitly directed merge and GitHub reported zero failed pull-request workflow runs for that exact head.

The recovery work includes canonical framework readiness/configuration, source bootstrap/control, Threat Intelligence population/default discovery, IOC inventory/pivots, Knowledge Graph discovery/population, Exposure population/filtering, object-driven Analysis/Investigations/Sharing, executable and observable Automation/Playbooks, Command Center readiness/trends, canonical operational telemetry, and unmocked same-origin repository browser acceptance.

The merge is an owner-authorized repository lifecycle decision. It does not create fresh production-equivalent, staging or independent-assurance evidence.

#### 11.10p Fresh production-equivalent validation

After candidate-readiness contracts are green and documentation remains synchronized, freeze one immutable integrated `main` identity. 11.10p requires fresh candidate identity, migration/compatibility, upgrade, rollback to the exact prior immutable digest with post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity evidence for the **same immutable** candidate and approved production-equivalent environment.

The execution package remains:

- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `tools/phase11_production_equivalent_validation.py`;
- `backend/tests/test_phase11_10_production_equivalent_validation.py`;
- `.github/workflows/phase11-production-equivalent-validation.yml`.

Historical Phase 8/9 evidence cannot satisfy 11.10p. Missing, ambiguous, inaccessible, historical-only or mixed-candidate evidence must **fail closed**. Repository CI validates repository contracts only and does not prove production-equivalent execution or production authorization.

### Phase 11.11 Independent external assurance
**Status:** `NOT STARTED / BLOCKED UNTIL FRESH PRODUCTION-EQUIVALENT PASS`

Fresh independent assurance may start only after the newly frozen integrated candidate passes production-equivalent validation and must target the same immutable candidate identity. Historical Phase 9 evidence cannot satisfy this gate.

## Phase 12 — Production GO/NO-GO
**Status:** `NOT STARTED / BLOCKED`

A production `GO` requires accepted 11.10 and 11.11 evidence for the same release identity plus accountable ownership, residual-risk, support/change and rollback authority. Missing evidence remains fail-closed.

## Immediate sequence

1. Complete candidate-readiness CI normalization and preserve synchronized authoritative documentation.
2. Freeze the resulting synchronized `main` head as one immutable candidate.
3. Execute the fresh 11.10p production-equivalent validation package against that exact candidate.
4. If validation changes code or configuration, invalidate the freeze, remediate the root cause and freeze a new candidate.
5. After explicit production-equivalent acceptance, restart Phase 11.11 external assurance for that same candidate.
6. Enter Phase 12 only after both fresh evidence classes are accepted.
