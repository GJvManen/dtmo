# DTMO Evidence Index

Last updated: **2026-08-18**

## Purpose

This index maps lifecycle stages to evidence classes and authoritative professional documentation. It is not a CI chronology. Exact run/commit/job history remains in immutable operational records, pull requests and CI artifacts.

**Current lifecycle:** Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate only; Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1–11.8e are `PASS / REPOSITORY_COMPLETE`, with the original Phase 11.7 Cortex decision retained as a historical baseline; Phase 11.8f backup/restore/recovery hardening is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`; Phase 12 is `NOT STARTED`. DTMO is not production authorized. Historical Phase 8/9 evidence remains candidate-bound and cannot satisfy Phase 11.10/11.11.

## Authoritative current-state sources

- `README.md`
- `docs/README.md`
- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`
- `docs/architecture/PHASE11_8_RUNTIME_FOUNDATION.md`
- `docs/architecture/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS.md`
- `docs/architecture/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION.md`
- `docs/architecture/PHASE11_8D_HA_DISRUPTION.md`
- `docs/architecture/PHASE11_8E_OBSERVABILITY_HARDENING.md`
- `docs/architecture/PHASE11_8F_RECOVERY_HARDENING.md`
- `docs/administration/KUBERNETES_RUNTIME_CONFIGURATION.md`
- `docs/administration/WORKLOAD_IDENTITY_EXTERNAL_SECRETS.md`
- `docs/administration/INGRESS_TLS_NETWORK_SEGMENTATION.md`
- `docs/operations/PHASE11_8_RUNTIME_FOUNDATION_RUNBOOK.md`
- `docs/operations/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_RUNBOOK.md`
- `docs/operations/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION_RUNBOOK.md`
- `docs/operations/PHASE11_8D_HA_DISRUPTION_RUNBOOK.md`
- `docs/operations/PHASE11_8E_OBSERVABILITY_RUNBOOK.md`
- `docs/operations/PHASE11_8F_RECOVERY_RUNBOOK.md`
- `docs/qa/PHASE11_8_RUNTIME_FOUNDATION_GATE.md`
- `docs/qa/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_GATE.md`
- `docs/qa/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION_GATE.md`
- `docs/qa/PHASE11_8D_HA_DISRUPTION_GATE.md`
- `docs/qa/PHASE11_8E_OBSERVABILITY_GATE.md`
- `docs/qa/PHASE11_8F_RECOVERY_GATE.md`
- `deploy/helm/dtmo/Chart.yaml`
- `deploy/helm/dtmo/values.yaml`
- `deploy/helm/dtmo/templates/runtime.yaml`
- `deploy/helm/dtmo/templates/external-secret.yaml`
- `deploy/helm/dtmo/templates/ingress.yaml`
- `deploy/helm/dtmo/templates/observability.yaml`
- `backend/tests/test_phase11_8_runtime_foundation.py`
- `backend/tests/test_phase11_8b_workload_identity_secrets.py`
- `backend/tests/test_phase11_8c_ingress_tls_network_segmentation.py`
- `backend/tests/test_phase11_8d_ha_disruption.py`
- `tests/test_phase11_8e_observability_contract.py`
- `tests/test_phase11_8f_recovery_contract.py`
- `.github/workflows/phase11-runtime-foundation.yml`
- `.github/workflows/phase11-workload-identity-secrets.yml`
- `.github/workflows/phase11-ingress-tls-network.yml`
- `.github/workflows/phase11-ha-disruption.yml`
- `.github/workflows/phase11-observability-hardening.yml`
- `.github/workflows/phase11-recovery-hardening.yml`
- `docs/architecture/CORTEX_DECISION_GATE.md`
- `docs/architecture/CORTEX_DTMO_INTEGRATION_CONTRACT.md`
- `docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md`
- `.github/workflows/phase11-thehive-handoff-implementation.yml`
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

RC13 remains `PASS / OWNER_ACCEPTED`; accepted historical repository/owner evidence remains unchanged and is not upgraded by Phase 11 work.

### Phase 8–9

Phase 8 remains `PASS / OWNER_ACCEPTED` and Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate only. These records are historical and cannot satisfy Phase 11.10 or 11.11.

### Phase 10

**Status:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.

### Phase 11.1–11.7b

**Status:** `PASS / REPOSITORY_COMPLETE` except the original 11.7 decision, which remains `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE`.

Accepted repository evidence covers Taranis, IntelOwl, OpenCTI, MISP, TheHive and the later bounded Cortex analyzer connector. The accepted TheHive implementation evidence includes the repository workflow `.github/workflows/phase11-thehive-handoff-implementation.yml`; this reference preserves the historical repository-evidence chain and does not imply live TheHive deployment evidence. Service identity/licensing boundaries, provenance, RBAC, human publication/share authority and fail-closed semantics remain authoritative.

### Phase 11.8a Runtime foundation

**Status:** `PASS / REPOSITORY_COMPLETE`.

Protected exact-head acceptance established governed Helm/GitOps configuration, mandatory immutable image digests, existing-secret consumption without secret material in Git, non-root/read-only runtime hardening, disabled service-account token automounting, resource/probe defaults, application PDB foundation and default-deny NetworkPolicy. This is repository engineering evidence only.

### Phase 11.8b Workload identity and external secret delivery

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers provider-neutral ServiceAccount identity annotations, continued service-account-token automount disablement, opt-in ExternalSecret rendering, explicit SecretStore/ClusterSecretStore reference, explicit target Secret, explicit per-variable remote mappings and no identity credential or secret value in Git.

Dedicated repository evidence is `backend/tests/test_phase11_8b_workload_identity_secrets.py`, `.github/workflows/phase11-workload-identity-secrets.yml` and `docs/qa/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_GATE.md`.

### Phase 11.8c Ingress/TLS and network segmentation

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers fail-closed optional ingress, mandatory explicit ingress class/host/TLS Secret reference, TLS-only enablement, `ClusterIP` application service exposure, mandatory NetworkPolicy and ingress-controller reachability constrained by both explicit namespace and pod selectors.

Dedicated repository evidence is `backend/tests/test_phase11_8c_ingress_tls_network_segmentation.py`, `.github/workflows/phase11-ingress-tls-network.yml` and `docs/qa/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION_GATE.md`.

Repository acceptance does **not** prove DNS ownership, certificate validity, ingress-controller installation/admission, external routing, cloud load-balancer/WAF policy, CNI enforcement or production availability.

### Phase 11.8d HA and disruption hardening

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence requires at least two DTMO replicas and defaults to three, spreads application replicas across availability-zone and hostname topology domains with fail-closed `DoNotSchedule` constraints, requires host anti-affinity, preserves a non-zero PodDisruptionBudget and defines explicit graceful termination. PostgreSQL, Redis, OpenSearch and object-storage HA remain deployment-specific stateful requirements rather than inferred repository capabilities.

Dedicated repository evidence is `backend/tests/test_phase11_8d_ha_disruption.py`, `.github/workflows/phase11-ha-disruption.yml` and `docs/qa/PHASE11_8D_HA_DISRUPTION_GATE.md`.

Repository acceptance does **not** prove live multi-zone placement, node/zone failure survival, stateful quorum/failover, provider replication or storage durability.

### Phase 11.8e Observability hardening

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence establishes opt-in metrics discovery through the ServiceMonitor contract, structured JSON logging and opt-in tracing/OTLP configuration. Dedicated evidence is `tests/test_phase11_8e_observability_contract.py`, `.github/workflows/phase11-observability-hardening.yml` and `docs/qa/PHASE11_8E_OBSERVABILITY_GATE.md`.

This acceptance does **not** prove live metric ingestion, log completeness, trace continuity, alert delivery, retention, SLO attainment or production observability.

### Phase 11.8f Backup, restore and recovery hardening

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

The bounded repository evidence target defines PostgreSQL, Redis, OpenSearch and object storage as explicit recovery domains and requires accountable backup ownership, retention, restore verification, recovery-exercise cadence and measurable RPO/RTO evidence. Backup success or achieved recovery objectives are never inferred from repository CI or configuration.

Dedicated repository evidence is `tests/test_phase11_8f_recovery_contract.py`, `.github/workflows/phase11-recovery-hardening.yml`, `docs/architecture/PHASE11_8F_RECOVERY_HARDENING.md`, `docs/operations/PHASE11_8F_RECOVERY_RUNBOOK.md` and `docs/qa/PHASE11_8F_RECOVERY_GATE.md`.

A green repository gate does **not** prove successful live backups, point-in-time recovery, achieved RPO/RTO, provider durability, disaster failover, production-equivalent behavior, independent assurance or production authorization. Missing deployment-bound recovery evidence remains fail closed.

### Remaining Phase 11.8

Subsequent bounded PRs must independently establish supply-chain, capacity and upgrade/rollback controls. 11.9 does not start until the required 11.8 controls are accepted.

### Phase 11.9

Migration and compatibility evidence follows completed Phase 11.8 runtime industrialisation.

### Phase 11.10–11.11

Fresh production-equivalent validation and fresh independent assurance must target the same immutable integrated candidate. Historical Phase 8/9 evidence cannot satisfy these gates.

### Phase 12

**Status:** `NOT STARTED`.

## Evidence transfer rule

Historical Phase 8/9 acceptance remains candidate-bound and cannot be transferred automatically to the materially changed Phase 11 platform. The historical Phase 11.7 Cortex decision is also not rewritten to manufacture the later owner requirement.

## Governance and handling rules

Framework claims remain governed by explicit provenance-backed mappings. External service, workload identity, secret-provider, ingress, HA, observability, recovery configuration or Kubernetes runtime state does not establish local exploitability, compromise, case necessity or dissemination authority without separate attributable evidence.

- Exact-head evidence belongs only to the exact state tested.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Credentials/tokens, TLS private keys and unnecessary personal data do not belong in repository evidence.
- Human review/share approval and human case-handoff approval remain separate from technical execution.
- Cortex analyzer output is enrichment evidence only.
- Kubernetes placement, workload identity, network reachability, observability and recovery configuration do not collapse service licensing/authority boundaries.
- Historical immutable run records are never rewritten to manufacture later acceptance.
