# DTMO Evidence Index

Last updated: **2026-08-17**

## Purpose

This index maps lifecycle stages to evidence classes and authoritative professional documentation. It is not a CI chronology. Exact run/commit/job history remains in immutable operational records, pull requests and CI artifacts.

**Current lifecycle:** Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1–11.7b are `PASS / REPOSITORY_COMPLETE` with the original Phase 11.7 Cortex decision retained as a historical baseline; Phase 11.8a Kubernetes/Helm/GitOps runtime foundation is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`; Phase 12 is `NOT STARTED`. DTMO is not production authorized. Historical Phase 8/9 evidence remains candidate-bound.

## Authoritative current-state sources

- `README.md`
- `docs/README.md`
- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`
- `docs/architecture/PHASE11_8_RUNTIME_FOUNDATION.md`
- `docs/administration/KUBERNETES_RUNTIME_CONFIGURATION.md`
- `docs/operations/PHASE11_8_RUNTIME_FOUNDATION_RUNBOOK.md`
- `docs/qa/PHASE11_8_RUNTIME_FOUNDATION_GATE.md`
- `deploy/helm/dtmo/Chart.yaml`
- `deploy/helm/dtmo/values.yaml`
- `deploy/helm/dtmo/templates/runtime.yaml`
- `deploy/gitops/phase11-8/values.yaml`
- `backend/tests/test_phase11_8_runtime_foundation.py`
- `.github/workflows/phase11-runtime-foundation.yml`
- `docs/architecture/CORTEX_DECISION_GATE.md`
- `docs/architecture/CORTEX_DTMO_INTEGRATION_CONTRACT.md`
- `docs/integrations/CORTEX_ANALYZER_CONNECTOR.md`
- `docs/operations/CORTEX_ANALYZER_RUNBOOK.md`
- `docs/qa/PHASE11_7B_CORTEX_CONNECTOR_GATE.md`
- `docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md`
- `docs/security/SECURITY_OVERVIEW.md`
- `docs/qa/QA_AND_RELEASE_GATES.md`
- `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`

## Evidence hierarchy

1. **Repository-controlled engineering evidence** — exact-head CI, contracts, migrations and synthetic integration/runtime tests.
2. **Accountable functional evidence** — explicit owner acceptance of product behavior.
3. **Real-environment evidence** — production-equivalent validation bound to an immutable deployment identity.
4. **Independent assurance evidence** — external assessment independent from repository CI.
5. **Formal production authorization** — accountable GO/NO-GO for a specific candidate.
6. **Platform-integration evidence** — service contracts, adapters, mappings, migrations, Helm/GitOps contracts and interoperability evidence; never production authorization by itself.

## Lifecycle evidence map

### Phases 1–7

**Status:** `PASS`.

### RC13 and E8

Accepted historical repository/owner evidence remains unchanged and is not upgraded by Phase 11 work.

### Phase 8–9

**Status:** accepted for the earlier candidate only. These records are historical and cannot satisfy Phase 11.10 or 11.11.

### Phase 10

**Status:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.

### Phase 11.1–11.6

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers Taranis, IntelOwl, OpenCTI, MISP and TheHive service boundaries, identity/provenance preservation, durable reconciliation/state, fail-closed authority controls and human publication/share/case-handoff authority. These are repository engineering claims only.

### Phase 11.7 Cortex decision

**Status:** `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE`.

The accepted point-in-time record concluded that Cortex was not adopted under the requirement set then available because no validated IntelOwl capability gap existed. That claim remains preserved.

### Phase 11.7b Cortex analyzer connector

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers the later attributable owner-required analyzer-only connector, including separate service/API identity, API-key authentication, explicit analyzer/datatype/TLP validation, stable job identity, bounded result import and explicit no-share/no-local-compromise metadata. Live provider permissions, lawful disclosure and runtime behavior remain deployment evidence.

### Phase 11.8a Kubernetes/Helm/GitOps runtime foundation

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

The bounded repository evidence target covers:

- governed Helm chart and GitOps-owned environment values;
- mandatory immutable image digest with render failure when absent;
- no embedded secret material in Git-owned values and explicit `existingSecret` consumption;
- non-root UID/GID 10001, `RuntimeDefault` seccomp, read-only root filesystem, dropped capabilities and no privilege escalation;
- disabled service-account token automounting;
- resource requests/limits and `/health` readiness/liveness probes;
- two application replicas and PodDisruptionBudget foundation;
- default-deny NetworkPolicy with same-namespace/DNS allowances and explicit external CIDR configuration;
- synchronized architecture, administration, operations, QA, current-state, roadmap, README, documentation portal and evidence material.

Dedicated repository evidence is:

- `backend/tests/test_phase11_8_runtime_foundation.py`;
- `.github/workflows/phase11-runtime-foundation.yml`;
- `docs/qa/PHASE11_8_RUNTIME_FOUNDATION_GATE.md`.

A green 11.8a gate does **not** prove live Kubernetes admission, CNI enforcement, cloud IAM, external-secret controller permissions, stateful/multi-zone HA, ingress/TLS, centralized observability, backup/restore, recovery objectives, SBOM/vulnerability scanning, image signing, provenance attestations, capacity, exercised upgrades/rollbacks, production-equivalent validation, independent assurance or production authorization.

### Remaining Phase 11.8

Subsequent bounded PRs must independently establish the deferred HA, secrets/workload identity, network/TLS, observability, recovery, supply-chain, capacity and upgrade/rollback controls. 11.9 does not start until the required 11.8 controls are accepted.

### Phase 11.9

Migration and compatibility evidence follows completed Phase 11.8 runtime industrialisation.

### Phase 11.10–11.11

Fresh production-equivalent validation and fresh independent assurance must target the same immutable integrated candidate. Historical Phase 8/9 evidence cannot satisfy these gates.

### Phase 12

**Status:** `NOT STARTED`.

## Evidence transfer rule

Historical Phase 8/9 acceptance remains candidate-bound and cannot be transferred automatically to the materially changed Phase 11 platform. The historical Phase 11.7 Cortex decision is also not rewritten to manufacture the later owner requirement.

## Governance and handling rules

Framework claims remain governed by explicit provenance-backed mappings. External service or Kubernetes runtime state does not establish local exploitability, compromise, case necessity or dissemination authority without separate attributable evidence.

- Exact-head evidence belongs only to the exact state tested.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Credentials/tokens and unnecessary personal data do not belong in repository evidence.
- Human review/share approval and human case-handoff approval remain separate from technical execution.
- Cortex analyzer output is enrichment evidence only.
- Kubernetes placement does not collapse service licensing/authority boundaries.
- Historical immutable run records are never rewritten to manufacture later acceptance.
