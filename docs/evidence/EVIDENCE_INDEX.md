# DTMO Evidence Index

Last updated: **2026-08-20**

## Purpose

This index maps lifecycle stages to evidence classes and authoritative professional documentation. It is not a CI chronology. Exact run/commit/job history remains in immutable operational records, pull requests and CI artifacts.

**Current lifecycle:** Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate only; Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1–11.9 and Phase 11.10a are `PASS / REPOSITORY_COMPLETE`; Phase 11.10 is `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`; its active bounded candidate-completion slice is 11.10b canonical application shell, `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 11.10c, Phase 11.11 and Phase 12 are `NOT STARTED`. DTMO is not production authorized. Historical Phase 8/9 evidence remains candidate-bound and cannot satisfy Phase 11.10/11.11.

## Authoritative current-state sources

- `README.md`
- `docs/README.md`
- `docs/project/CURRENT_STATE.md`
- `docs/project/EXECUTIVE_STATUS.md`
- `docs/project/EXECUTIVE_DECISION_VIEW.md`
- `docs/project/PRODUCTION_READINESS_REPORT.md`
- `docs/project/PRODUCTION_CHECKLIST.md`
- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`
- `docs/roadmap/PRODUCTION_ROADMAP.md`
- `docs/architecture/PHASE11_8I_UPGRADE_ROLLBACK.md`
- `docs/architecture/PHASE11_9_MIGRATION_COMPATIBILITY.md`
- `docs/operations/PHASE11_9_MIGRATION_COMPATIBILITY_RUNBOOK.md`
- `docs/qa/PHASE11_9_MIGRATION_COMPATIBILITY_GATE.md`
- `backend/tests/test_phase11_9_migration_compatibility.py`
- `tools/phase11_migration_compatibility.py`
- `.github/workflows/phase11-migration-compatibility.yml`
- `docs/architecture/FRONTEND_ARCHITECTURE.md`
- `docs/architecture/UI_API_CONTRACT.md`
- `docs/ux/UNIFIED_OPERATIONS_WORKBENCH.md`
- `docs/ux/INFORMATION_ARCHITECTURE.md`
- `docs/ux/DESIGN_SYSTEM.md`
- `docs/qa/PHASE11_10A_FRONTEND_ARCHITECTURE_GATE.md`
- `backend/tests/test_phase11_10a_frontend_architecture_contract.py`
- `.github/workflows/phase11-frontend-architecture.yml`
- `docs/architecture/PHASE11_10B_APPLICATION_SHELL.md`
- `docs/qa/PHASE11_10B_APPLICATION_SHELL_GATE.md`
- `frontend/package.json`
- `frontend/package-lock.json`
- `backend/tests/test_phase11_10b_application_shell_contract.py`
- `backend/tests/test_phase11_10b_application_shell_browser.py`
- `.github/workflows/phase11-application-shell.yml`
- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`
- `backend/tests/test_phase11_10_production_equivalent_validation.py`
- `tools/phase11_production_equivalent_validation.py`
- `.github/workflows/phase11-production-equivalent-validation.yml`
- `docs/security/SECURITY_OVERVIEW.md`
- `docs/qa/QA_AND_RELEASE_GATES.md`
- `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`

## Evidence hierarchy

1. **Repository-controlled engineering evidence** — exact-head CI, contracts, SBOMs, vulnerability scans, migrations, architecture contracts, frontend builds/browser tests and synthetic integration/runtime tests.
2. **Release supply-chain evidence** — artifact hashes plus signed provenance/SBOM attestations for the exact release subject.
3. **Accountable functional evidence** — explicit owner acceptance of product behavior.
4. **Real-environment evidence** — production-equivalent validation bound to an immutable deployment identity.
5. **Independent assurance evidence** — external assessment independent from repository CI.
6. **Formal production authorization** — accountable GO/NO-GO for a specific candidate.

These evidence classes are not interchangeable.

## Lifecycle evidence map

### Phases 1–7

**Status:** `PASS`.

### RC13 and E8

RC13 remains `PASS / OWNER_ACCEPTED`; E8.1–E8.10 remain `PASS / REPOSITORY_COMPLETE`. Accepted historical repository/owner evidence remains unchanged and is not upgraded by Phase 11 work.

### Phase 8–9

Phase 8 remains `PASS / OWNER_ACCEPTED` and Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate only. These records are historical and cannot satisfy Phase 11.10 or 11.11.

### Phase 10

**Status:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.

### Phase 11.1–11.7b

**Status:** `PASS / REPOSITORY_COMPLETE` except the original 11.7 decision, which remains `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE`.

Accepted repository evidence covers Taranis, IntelOwl, OpenCTI, MISP, TheHive and the later bounded Cortex analyzer connector. The accepted TheHive implementation evidence chain includes `.github/workflows/phase11-thehive-handoff-implementation.yml`. Service identity/licensing boundaries, provenance, RBAC, human publication/share authority and fail-closed semantics remain authoritative. This workflow reference identifies repository evidence only and does not prove live TheHive availability, live case creation or production authorization.

### Phase 11.8

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers runtime foundation, workload identity/external-secret delivery, TLS ingress/network segmentation, HA/disruption controls, observability, recovery, supply-chain hardening, capacity/resource planning and exercised upgrade/rollback.

Accepted workflow references remain discoverable as evidence-chain identifiers, including:

- `.github/workflows/phase11-workload-identity-secrets.yml`;
- `.github/workflows/phase11-ingress-tls-network.yml`;
- `.github/workflows/phase11-ha-disruption.yml`;
- `.github/workflows/phase11-supply-chain-hardening.yml`;
- `.github/workflows/release-artifact-attestation.yml`;
- `.github/workflows/phase11-upgrade-rollback.yml`.

These references identify repository evidence paths only; they do not prove live provider enforcement, admission, deployment or production authorization.

Phase 11.8i evidence remains `backend/tests/test_phase11_8i_upgrade_rollback.py`, `tools/phase11_upgrade_rollback_exercise.py`, `.github/workflows/phase11-upgrade-rollback.yml`, `docs/architecture/PHASE11_8I_UPGRADE_ROLLBACK.md`, `docs/operations/PHASE11_8I_UPGRADE_ROLLBACK_RUNBOOK.md` and `docs/qa/PHASE11_8I_UPGRADE_ROLLBACK_GATE.md`. Repository acceptance does not prove live rollback, stateful recovery, production-equivalent continuity or production authorization.

### Phase 11.9 Migration and compatibility

**Status:** `PASS / REPOSITORY_COMPLETE`.

The accepted repository evidence requires a single connected Alembic revision graph with exactly one root and one head, no duplicate/missing/disconnected revision identities, explicit upgrade/downgrade functions, forward-first deployment sequencing and explicit compatibility handling for rolling application overlap. Destructive schema changes require an expand/migrate/contract sequence. Application rollback does not authorize automatic database down migration; ambiguous compatibility must fail closed.

Dedicated repository evidence is `backend/tests/test_phase11_9_migration_compatibility.py`, `tools/phase11_migration_compatibility.py`, `.github/workflows/phase11-migration-compatibility.yml`, `docs/architecture/PHASE11_9_MIGRATION_COMPATIBILITY.md`, `docs/operations/PHASE11_9_MIGRATION_COMPATIBILITY_RUNBOOK.md` and `docs/qa/PHASE11_9_MIGRATION_COMPATIBILITY_GATE.md`.

Repository acceptance establishes graph/contract integrity only. It does **not** prove migration of production data, live application/schema compatibility, production-equivalent continuity, independent assurance or production authorization.

### Phase 11.10 Integrated production-equivalent validation

**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`.

The owner-required next-generation Unified Operations Workbench materially changes the integrated candidate. The Phase 11.10 stage therefore contains a bounded candidate-completion track before the existing external execution package is exercised.

#### Phase 11.10a frontend architecture/design contract

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted 11.10a repository evidence is:

- `docs/architecture/FRONTEND_ARCHITECTURE.md`;
- `docs/architecture/UI_API_CONTRACT.md`;
- `docs/ux/UNIFIED_OPERATIONS_WORKBENCH.md`;
- `docs/ux/INFORMATION_ARCHITECTURE.md`;
- `docs/ux/DESIGN_SYSTEM.md`;
- `docs/qa/PHASE11_10A_FRONTEND_ARCHITECTURE_GATE.md`;
- `backend/tests/test_phase11_10a_frontend_architecture_contract.py`;
- `.github/workflows/phase11-frontend-architecture.yml`.

The accepted architecture preserves **browser → DTMO API → governed integration adapter → upstream service**, **server-side RBAC**, provenance, human/service identity separation, separate case and publication/share authority, and no local-compromise inference from enrichment/graph/correlation state.

11.10a acceptance proves the repository architecture/design contract only. It does not prove frontend feature implementation, live Taranis/IntelOwl/OpenCTI/MISP/TheHive/Cortex behavior, production-equivalent operation, independent assurance or production authorization.

Design mockups and generated visuals are design artifacts only and cannot be promoted to live screenshot, staging, production-equivalent or production evidence.

#### Phase 11.10b canonical application shell

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

The active repository evidence package is:

- `docs/architecture/PHASE11_10B_APPLICATION_SHELL.md`;
- `docs/qa/PHASE11_10B_APPLICATION_SHELL_GATE.md`;
- `frontend/README.md`;
- `frontend/THIRD_PARTY_NOTICES.md`;
- `frontend/package.json`;
- `frontend/package-lock.json`;
- `frontend/src/main.tsx`;
- `frontend/src/App.tsx`;
- `frontend/src/styles.css`;
- `backend/dtmo/workbench_frontend.py`;
- `backend/tests/test_phase11_10b_application_shell_contract.py`;
- `backend/tests/test_phase11_10b_application_shell_browser.py`;
- `.github/workflows/phase11-application-shell.yml`.

The committed npm lockfile is the authoritative frontend dependency graph. The final exact-head gate must consume it unchanged with `npm ci`, audit production frontend dependencies, typecheck/build the workbench, record deterministic built-asset hashes, run the repository contract and exercise canonical shell browser journeys.

The supported built route is `/workbench/`; `/ui/console` is a temporary **compatibility path** and not a parallel feature target. Route foundations for later workspaces explicitly avoid synthetic operational state. The command palette is navigation-only in 11.10b.

A green 11.10b shell workflow can prove repository-controlled dependency/build integrity, same-origin serving, canonical routing, CSP/cache behavior and bounded browser mechanics. It **does not prove** live upstream integration behavior, Command Center feature acceptance, production-equivalent deployment/continuity, independent assurance or production authorization.

#### Candidate-completion order

After 11.10b acceptance, the fixed bounded order is 11.10c Command Center; 11.10d Unified Intelligence Workspace; 11.10e IntelOwl/Cortex analysis; 11.10f OpenCTI graph/entity workspace; 11.10g MISP Sharing & Exchange; 11.10h TheHive Investigations & Cases; 11.10i Vulnerability & Exposure; 11.10j Sources & Collection; 11.10k Automation & Playbooks; 11.10l Governance & Evidence; 11.10m Operations & Administration; 11.10n role-aware UX/accessibility; 11.10o consolidation/full functional acceptance; then 11.10p fresh production-equivalent validation.

Repository evidence from 11.10a–11.10o remains engineering/functional candidate-completion evidence and is not a substitute for 11.10p external evidence.

#### Repository evidence contract for external validation

The existing production-equivalent repository contract remains defined by:

- `backend/tests/test_phase11_10_production_equivalent_validation.py`;
- `tools/phase11_production_equivalent_validation.py`;
- `.github/workflows/phase11-production-equivalent-validation.yml`;
- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`.

Repository CI validates contract behavior, candidate identity requirements, migration/compatibility, upgrade, rollback, health, saturation, recovery, fail closed parsing and exact-head metadata only. It does not contact or prove a production-equivalent environment.

#### 11.10p external execution package

After candidate freeze, the governed production-equivalent exercise is defined by:

- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `tools/phase11_production_equivalent_validation.py` for candidate fingerprint calculation and final manifest validation.

The checked-in evidence template is intentionally incomplete and therefore must fail validation until real observations replace placeholders. A populated manifest should normally live in approved restricted evidence storage if references or metadata are sensitive.

#### Candidate binding

One deterministic candidate fingerprint binds production-equivalent `environment_id`, exact deployed Git commit, immutable application image digest, immutable supporting image digests where applicable, migration head and deployment/GitOps revision.

The exact approved prior immutable application digest is also recorded for rollback. Every required evidence item must carry the candidate fingerprint of the exercised candidate.

#### Required fresh evidence classes

Operational acceptance requires fresh external evidence for:

1. immutable candidate identity;
2. migration/compatibility;
3. upgrade;
4. rollback;
5. health/readiness;
6. saturation/capacity;
7. recovery/continuity.

Rollback evidence must show restoration of the exact prior immutable application digest and successful post-rollback health. Application rollback does not authorize automatic database down migration. Saturation evidence must identify the approved workload profile. Recovery evidence records observed RPO/RTO where applicable.

#### Fail-closed rule

Historical Phase 8/9 artifacts, mixed-candidate artifacts, ambiguous identity, placeholders, mutable image tags without immutable digests, inaccessible evidence, repository-CI-only evidence, emulators, synthetic fixtures or missing evidence cannot satisfy this gate. Release-blocking findings must be closed and deviations must have accountable disposition.

#### Acceptance boundary

A successful manifest validation proves only that supplied metadata satisfies the repository contract. Reviewers must inspect the referenced external evidence. Phase 11.10 becomes `PASS / OWNER_ACCEPTED` only after candidate completion, candidate freeze, successful 11.10p execution and explicit accountable owner acceptance.

Phase 11.10 acceptance still does not authorize production. Phase 11.11 remains blocked until this acceptance exists.

### Phase 11.11 Independent external assurance

**Status:** `NOT STARTED`.

Fresh independent assurance must target the same immutable integrated candidate accepted in Phase 11.10. No historical Phase 9 assurance is transferable to the changed Phase 11 candidate.

### Phase 12

**Status:** `NOT STARTED`.

Phase 12 is the only future gate that can produce a new formal production GO/NO-GO decision for the integrated candidate.

## Evidence transfer rule

Historical Phase 8/9 acceptance remains candidate-bound and cannot be transferred automatically to the materially changed Phase 11 platform. The historical Phase 11.7 Cortex decision is also not rewritten to manufacture the later owner requirement.

## Governance and handling rules

Framework claims remain governed by explicit provenance-backed mappings. External service, workload identity, secret-provider, ingress, HA, observability, recovery, supply-chain, capacity, rollout, migration or frontend state does not establish local exploitability, compromise, case necessity or dissemination authority without separate attributable evidence.

- Exact-head evidence belongs only to the exact state tested.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Sensitive authentication material, TLS private keys, signing key material and unnecessary personal data do not belong in repository evidence.
- Human review/share approval and human case-handoff approval remain separate from technical execution.
- Cortex analyzer output is enrichment evidence only.
- Kubernetes placement, migration tooling and frontend integration do not collapse service licensing/authority boundaries.
- Signed provenance is not a declaration that an artifact is vulnerability-free or production-authorized.
- Application rollback is not automatic database rollback or data recovery.
- Historical immutable run records are never rewritten to manufacture later acceptance.
