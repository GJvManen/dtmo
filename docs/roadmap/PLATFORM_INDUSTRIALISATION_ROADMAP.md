# DTMO Platform Industrialisation Roadmap

Last updated: **2026-08-20**  
Programme state: **`ACTIVE / HIGHEST PRIORITY`**

## Purpose

Phase 10 concluded with `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` for production authorization. Phase 11 is the successor industrialisation programme and is executed one bounded pull request at a time.

Historical Phase 8 remains `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` and historical Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`. Those evidence packages remain candidate-bound and are not reused for the materially changed integrated platform. E8.1–E8.10 and accepted Phase 11 repository work remain `PASS / REPOSITORY_COMPLETE` within their bounded claims.

DTMO prefers mature service integrations over rebuilding generic collection, enrichment, graph, exchange and case-management platforms inside DTMO. The next-generation interface is therefore a DTMO control plane over governed capabilities, not a browser-side replacement for those services.

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
12. 11.11 new independent external assurance.
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

Phase 11.8 was delivered as bounded sub-slices with exact-head repository evidence and professional documentation.

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

Accepted repository evidence requires immutable baseline/candidate/rollback digests, safe RollingUpdate controls, revision history, finite progress/min-ready bounds, mandatory post-upgrade/post-rollback health evidence and restoration of the exact prior digest. Automatic database down migration remains forbidden. Repository acceptance does not prove a live-cluster rollback, stateful recovery, production-equivalent continuity or production authorization.

### 11.9 Migration and compatibility
**Status:** `PASS / REPOSITORY_COMPLETE`

The accepted repository slice validates one connected single-root/single-head Alembic revision graph, explicit upgrade/downgrade contracts and forward-first deployment sequencing. Rolling overlap is allowed only for backward-compatible schema changes. Destructive changes require an explicit expand/migrate/contract sequence. Application rollback never implies automatic database down migration; ambiguity fails closed.

Repository acceptance establishes engineering graph/contract integrity only. It does not prove migration of production data, live application/schema compatibility, production-equivalent continuity, independent assurance or production authorization.

### 11.10 Integrated production-equivalent validation
**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`

Phase 11.10 remains the active production-readiness stage. Before external execution, the candidate must first incorporate the owner-required next-generation Unified Operations Workbench because that work materially changes the integrated candidate and user workflows. Running external validation before this candidate-completion track would create immediately stale candidate-bound evidence.

#### Candidate-completion sequence

The following order is fixed and remains one bounded PR at a time:

- **11.10a Frontend architecture and design contract** — `IN PROGRESS / REPOSITORY ARCHITECTURE CONTRACT`;
- **11.10b Canonical application shell** — `NOT STARTED`;
- **11.10c Command Center** — `NOT STARTED`;
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

11.10a defines the target architecture only. It explicitly does not implement or accept the new frontend. Its repository-controlled contract is documented by:

- `docs/architecture/FRONTEND_ARCHITECTURE.md`;
- `docs/architecture/UI_API_CONTRACT.md`;
- `docs/ux/UNIFIED_OPERATIONS_WORKBENCH.md`;
- `docs/ux/INFORMATION_ARCHITECTURE.md`;
- `docs/ux/DESIGN_SYSTEM.md`;
- `docs/qa/PHASE11_10A_FRONTEND_ARCHITECTURE_GATE.md`;
- `backend/tests/test_phase11_10a_frontend_architecture_contract.py`;
- `.github/workflows/phase11-frontend-architecture.yml`.

The canonical security path is **browser → DTMO API → governed integration adapter → upstream service**. Role-aware rendering is a usability feature only; server-side RBAC, human publication/share authority, case authority, provenance and fail-closed behavior remain authoritative.

#### 11.10p external execution boundary

After 11.10o functional acceptance, one immutable integrated candidate is frozen and the fresh production-equivalent exercise is executed. Operational acceptance still requires fresh candidate identity, migration/compatibility, upgrade, rollback, health/readiness, saturation/capacity and recovery/continuity evidence, all attributable to the same candidate fingerprint and environment.

The controlled external execution package remains:

- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `tools/phase11_production_equivalent_validation.py`;
- `backend/tests/test_phase11_10_production_equivalent_validation.py`;
- `.github/workflows/phase11-production-equivalent-validation.yml`;
- `docs/evidence/EVIDENCE_INDEX.md`.

The evidence template is intentionally incomplete until the real production-equivalent exercise supplies observations and references. The validator calculates one deterministic candidate fingerprint and fails closed on missing placeholders, malformed immutable identities, mixed-candidate evidence, historical-only references, wrong rollback target, missing post-rollback health, open release-blocking findings or incomplete accountable review.

```mermaid
flowchart LR
    C[11.10a-o candidate completion] --> F[Immutable candidate freeze]
    F --> I[Candidate + environment identity]
    I --> M[Migration + compatibility]
    M --> U[Upgrade]
    U --> H[Health]
    H --> S[Saturation]
    S --> R[Recovery]
    R --> B[Exact prior-digest rollback]
    B --> V[Post-rollback health]
    V --> O[Accountable owner review]
```

Historical Phase 8/9 evidence is audit history only and cannot satisfy this gate. Missing, ambiguous, inaccessible or mixed-candidate evidence fails closed.

Repository CI can validate Phase 11.10 contracts and exact-head binding, but repository-green status does not prove that a production-equivalent environment was deployed or exercised. A valid manifest proves metadata consistency only; referenced external evidence still requires human review. Operational Phase 11.10 acceptance remains separate from repository merge and is required before Phase 11.11.

### 11.11 Independent external assurance
**Status:** `NOT STARTED`

Run fresh independent assurance against the same immutable integrated candidate only after Phase 11.10p production-equivalent evidence is complete and explicitly `PASS / OWNER_ACCEPTED`. A material candidate change requires a new Phase 11.10 evidence binding first.

## Phase 12 — Production GO/NO-GO
**Status:** `NOT STARTED`

A `GO` requires accepted 11.10 and 11.11 evidence for the same immutable integrated release identity plus accountable production ownership, residual-risk, change/support and rollback authority. Missing evidence remains fail-closed.

DTMO remains **not production authorized** until a future Phase 12 accountable decision grants a GO.

## Delivery discipline

Every bounded PR requires one primary objective, exact-head CI, expected-head merge protection, professional documentation synchronization, explicit security/licensing/evidence boundaries and one declared next priority. A code/integration PR does not merge when required documentation is missing or stale.

## Immediate sequence

1. Complete **Phase 11.10a Frontend architecture and design contract** with exact-head repository evidence.
2. If 11.10a is accepted, start **11.10b Canonical application shell** as the next and only bounded PR.
3. Continue the fixed 11.10c–11.10o candidate-completion sequence one green merged PR at a time.
4. Freeze one immutable integrated candidate and execute **11.10p fresh production-equivalent validation** using the full external evidence set.
5. Run **Phase 11.11 independent external assurance** against that same immutable candidate only after explicit 11.10 acceptance.
6. Enter Phase 12 only after both 11.10 and 11.11 are accepted for the same candidate.
