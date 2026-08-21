# DTMO Platform Industrialisation Roadmap

Last updated: **2026-08-21**  
Programme state: **`ACTIVE / HIGHEST PRIORITY`**

## Purpose and release truth

Phase 10 concluded with **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. Phase 11 is the successor industrialisation programme and is delivered one bounded PR at a time with exact-head CI, professional documentation and expected-head merge protection. DTMO remains **not production authorized**.

Historical Phase 8 remains `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` and historical Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`. Those packages are immutable history and cannot be reused for the materially changed integrated candidate.

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

The accepted Taranis programme preserves Taranis as a separate service/licensing boundary. Phase 11.1 assessed architecture/API/data-model/identity/licensing constraints; Phase 11.2 Taranis → DTMO canonical adapter established the governed canonical integration without vendoring Taranis source or moving privileged upstream credentials into the browser.

### 11.3 IntelOwl enrichment integration
**Status:** `PASS / REPOSITORY_COMPLETE`

IntelOwl enrichment remains server-side and governed. Analyzer output is evidence and does not itself establish compromise, remediation, publication authority or production readiness.

### 11.4 OpenCTI knowledge-graph integration
**Status:** `PASS / REPOSITORY_COMPLETE`

The OpenCTI STIX knowledge-graph integration preserves canonical DTMO provenance and does not infer relationship topology beyond persisted mapping evidence.

### 11.5 MISP consolidation
**Status:** `PASS / REPOSITORY_COMPLETE`

MISP consolidation preserves the authoritative governed sharing model: technical transfer is separate from human review, external-share approval and publication authority.

### 11.6 TheHive incident/case handoff
**Status:** `PASS / REPOSITORY_COMPLETE`

TheHive handoff preserves explicit human case-creation/handoff authority. Connectivity, intelligence presence or an upstream case identifier does not prove compromise, containment or remediation.

### 11.7 Cortex decision gate
**Status:** `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE`

The Cortex decision gate remains preserved as historical decision evidence and must not be rewritten as a current production claim.

### 11.7b Cortex analyzer connector
**Status:** `PASS / REPOSITORY_COMPLETE`

The owner-required Cortex analyzer connector remains bounded by the same server-side credentials, RBAC, provenance and non-inference rules as other enrichment services.

### 11.8 Integrated runtime industrialisation
**Status:** `PASS / REPOSITORY_COMPLETE`

The accepted platform baseline covers Kubernetes/Helm/GitOps, workload identity, external secret delivery, ingress/TLS, network segmentation, HA/disruption controls, observability, backup/recovery, software supply-chain hardening, capacity planning and upgrade/rollback. Repository evidence does not itself prove production-equivalent behavior.

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

### 11.10 Integrated production-equivalent validation
**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`

The Unified Operations Workbench materially changes the candidate. Candidate-completion slices 11.10a–11.10o must be accepted before one immutable integrated candidate is frozen for the fresh 11.10p production-equivalent exercise.

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
- **11.10l Governance & Evidence Center** — `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- **11.10m Operations & Administration** — `NOT STARTED`;
- **11.10n Role-aware UX/accessibility** — `NOT STARTED`;
- **11.10o Consolidation and full functional acceptance** — `NOT STARTED`;
- **11.10p Fresh production-equivalent validation** — `NOT STARTED / CANDIDATE FREEZE REQUIRED`.

#### Accepted workbench foundation through 11.10k

The canonical path is **browser → DTMO API → governed integration adapter/data contract → governed service/evidence source**. The browser never becomes a privileged upstream integration client. **Server-side RBAC**, provenance, human review/share/publication authority, separate case authority, replay protection and fail-closed behavior remain authoritative.

11.10a–11.10k delivered the frontend architecture, application shell, Command Center, Unified Intelligence, IntelOwl/Cortex Analysis, OpenCTI Graph/Entity, MISP Sharing & Exchange, TheHive Investigations & Cases, Vulnerability & Exposure, Sources & Collection and Automation & Playbooks. Enrichment is evidence rather than a compromise verdict; graph topology is not inferred; MISP transfer is not publication; TheHive handoff remains explicit human authority; vulnerability context is not local exposure; connector/automation success is not source truth or production evidence.

#### 11.10l active Governance & Evidence Center

11.10l makes `/workbench/governance` functional through DTMO-owned same-origin APIs. It reuses the existing repository-backed governance/control crosswalk rather than creating a second compliance store.

Authoritative active package:

- `backend/dtmo/governance_knowledge.py`;
- `backend/dtmo/governance_crosswalk.py`;
- `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`;
- `frontend/src/GovernanceWorkspace.tsx`;
- `frontend/src/App.tsx` canonical `/governance` routing;
- `docs/architecture/PHASE11_10L_GOVERNANCE_EVIDENCE.md`;
- `docs/user/GOVERNANCE_EVIDENCE_WORKSPACE.md`;
- `docs/qa/PHASE11_10L_GOVERNANCE_EVIDENCE_GATE.md`;
- `backend/tests/test_phase11_10l_governance_evidence_contract.py`;
- `tests/browser/phase11_10l_governance.py`;
- `.github/workflows/phase11-governance-evidence.yml`.

The governance crosswalk contains explicit typed **partial** relationships for Normenkader IBP, MITRE ATT&CK and NIST CSF plus CVSS context. Unrecorded controls/techniques remain unmapped. A mapping does not establish complete compliance, certification, environment effectiveness, local compromise, audit acceptance, independent assurance or production authorization.

Governance visibility is read-oriented and does not grant review, case creation, remediation, connector execution, external sharing, publication, administration or production authority. Exact-head repository CI remains non-production evidence.

Acceptance requires one final unchanged exact head on which every registered workflow is `completed/success`, documentation is synchronized, the PR is mergeable and ready for review, followed by squash merge with expected-head protection.

Only after 11.10l is accepted and merged may **11.10m Operations & Administration** begin.

#### 11.10p Fresh production-equivalent validation

After 11.10o acceptance, freeze one immutable integrated candidate. 11.10p requires fresh candidate identity, migration/compatibility, upgrade, rollback to the exact prior immutable digest with post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity evidence for the **same immutable** candidate and approved production-equivalent environment.

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

1. Complete **11.10l Governance & Evidence Center** on one final exact green head and merge with expected-head protection.
2. Start **11.10m Operations & Administration** only after 11.10l is merged.
3. Continue 11.10n and 11.10o one bounded green PR at a time.
4. Freeze one immutable candidate and execute **11.10p**.
5. Complete fresh **Phase 11.11** independent assurance for that same candidate.
6. Enter **Phase 12** only after 11.10 and 11.11 are accepted.
