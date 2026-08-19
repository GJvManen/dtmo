# DTMO Evidence Index

Last updated: **2026-08-19**

## Purpose

This index maps lifecycle stages to evidence classes and authoritative professional documentation. It is not a CI chronology. Exact run/commit/job history remains in immutable operational records, pull requests and CI artifacts.

**Current lifecycle:** Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate only; Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1–11.8h are `PASS / REPOSITORY_COMPLETE`; Phase 11.8i exercised upgrade/rollback is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`; Phase 12 is `NOT STARTED`. DTMO is not production authorized. Historical Phase 8/9 evidence remains candidate-bound and cannot satisfy Phase 11.10/11.11.

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
- `docs/security/PHASE11_8G_SUPPLY_CHAIN_HARDENING.md`
- `docs/architecture/PHASE11_8H_CAPACITY_RESOURCE_PLANNING.md`
- `docs/architecture/PHASE11_8I_UPGRADE_ROLLBACK.md`
- `docs/operations/PHASE11_8I_UPGRADE_ROLLBACK_RUNBOOK.md`
- `docs/qa/PHASE11_8I_UPGRADE_ROLLBACK_GATE.md`
- `backend/tests/test_phase11_8i_upgrade_rollback.py`
- `tools/phase11_upgrade_rollback_exercise.py`
- `.github/workflows/phase11-upgrade-rollback.yml`
- `docs/security/SECURITY_OVERVIEW.md`
- `docs/qa/QA_AND_RELEASE_GATES.md`
- `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`

## Evidence hierarchy

1. **Repository-controlled engineering evidence** — exact-head CI, contracts, SBOMs, vulnerability scans, migrations and synthetic integration/runtime tests.
2. **Release supply-chain evidence** — artifact hashes plus signed provenance/SBOM attestations for the exact release subject.
3. **Accountable functional evidence** — explicit owner acceptance of product behavior.
4. **Real-environment evidence** — production-equivalent validation bound to an immutable deployment identity.
5. **Independent assurance evidence** — external assessment independent from repository CI.
6. **Formal production authorization** — accountable GO/NO-GO for a specific candidate.

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

Accepted repository evidence covers Taranis, IntelOwl, OpenCTI, MISP, TheHive and the later bounded Cortex analyzer connector. The accepted TheHive implementation evidence includes `.github/workflows/phase11-thehive-handoff-implementation.yml`; this preserves the historical repository-evidence chain and does not imply live TheHive deployment evidence. Service identity/licensing boundaries, provenance, RBAC, human publication/share authority and fail-closed semantics remain authoritative.

### Phase 11.8a–11.8e
**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers the governed Helm/GitOps runtime foundation, workload identity/external-secret delivery, TLS ingress/network segmentation, application HA/disruption controls and opt-in observability boundaries. Historical accepted workflow references remain `.github/workflows/phase11-workload-identity-secrets.yml`, `.github/workflows/phase11-ingress-tls-network.yml` and `.github/workflows/phase11-ha-disruption.yml`. These references preserve repository evidence only and do not imply live cloud IAM, secret retrieval, certificate issuance, CNI enforcement, zone survival or production deployment evidence.

### Phase 11.8f Backup, restore and recovery hardening
**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence defines PostgreSQL, Redis, OpenSearch and object storage as explicit recovery domains and requires accountable backup ownership, retention, restore verification, recovery-exercise cadence and measurable RPO/RTO evidence boundaries. Dedicated evidence remains `tests/test_phase11_8f_recovery_contract.py`, `.github/workflows/phase11-recovery-hardening.yml`, `docs/architecture/PHASE11_8F_RECOVERY_HARDENING.md`, `docs/operations/PHASE11_8F_RECOVERY_RUNBOOK.md` and `docs/qa/PHASE11_8F_RECOVERY_GATE.md`. Repository acceptance does not prove successful live backups, PITR, achieved recovery objectives, provider durability or disaster failover.

### Phase 11.8g Software supply-chain hardening
**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted evidence covers exact-head Python/container SBOM generation, Python dependency auditing, container `HIGH`/`CRITICAL` vulnerability scanning, SHA-256 artifact identities, minimal-runtime boundaries and a governed release path for cryptographically signed provenance and SBOM attestations. Dedicated evidence includes `backend/tests/test_phase11_8g_supply_chain_contract.py`, `.github/workflows/phase11-supply-chain-hardening.yml`, `.github/workflows/release-artifact-attestation.yml`, `docs/security/PHASE11_8G_SUPPLY_CHAIN_HARDENING.md`, `docs/operations/PHASE11_8G_SUPPLY_CHAIN_RUNBOOK.md` and `docs/qa/PHASE11_8G_SUPPLY_CHAIN_GATE.md`. Acceptance does not claim that a future release artifact has already been signed, admitted or deployed.

### Phase 11.8h Capacity and resource planning
**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence establishes explicit CPU/memory requests and limits, bounded autoscaling, stabilization behavior and saturation evidence thresholds. `docs/architecture/PHASE11_8H_CAPACITY_RESOURCE_PLANNING.md` remains authoritative for the capacity trust boundary. Repository acceptance does not prove production sizing, workload demand, provider headroom or SLO attainment.

### Phase 11.8i Exercised upgrade and rollback
**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

The bounded evidence target requires two different SHA-256 immutable image identities, an upgrade transition from baseline to candidate, rollback to the exact prior baseline digest, safe RollingUpdate controls, preserved revision history, finite progress/min-ready bounds, mandatory post-upgrade and post-rollback health evidence, human change authority and an explicit prohibition on automatic database down migration.

Dedicated repository evidence is `backend/tests/test_phase11_8i_upgrade_rollback.py`, `tools/phase11_upgrade_rollback_exercise.py`, `.github/workflows/phase11-upgrade-rollback.yml`, `docs/architecture/PHASE11_8I_UPGRADE_ROLLBACK.md`, `docs/operations/PHASE11_8I_UPGRADE_ROLLBACK_RUNBOOK.md` and `docs/qa/PHASE11_8I_UPGRADE_ROLLBACK_GATE.md`.

The machine-readable artifact `phase11-8i-upgrade-rollback-evidence` must bind to the exact pull-request head and show baseline → candidate → exact baseline. A green repository exercise does **not** prove live-cluster rollback, stateful recovery, production-equivalent continuity, independent assurance or production authorization. Missing immutable identity, rollback compatibility, health evidence or attributable change authority must **fail closed**.

### Phase 11.9
Migration and compatibility evidence starts only after accepted 11.8i exact-head evidence.

### Phase 11.10–11.11
Fresh production-equivalent validation and fresh independent assurance must target the same immutable integrated candidate. Phase 11.10 must include new upgrade, rollback, health, saturation and recovery evidence. Historical Phase 8/9 evidence cannot satisfy these gates.

### Phase 12
**Status:** `NOT STARTED`.

## Evidence transfer rule

Historical Phase 8/9 acceptance remains candidate-bound and cannot be transferred automatically to the materially changed Phase 11 platform. The historical Phase 11.7 Cortex decision is also not rewritten to manufacture the later owner requirement.

## Governance and handling rules

Framework claims remain governed by explicit provenance-backed mappings. External service, workload identity, secret-provider, ingress, HA, observability, recovery, supply-chain, capacity or rollout state does not establish local exploitability, compromise, case necessity or dissemination authority without separate attributable evidence.

- Exact-head evidence belongs only to the exact state tested.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Sensitive authentication material, TLS private keys, signing key material and unnecessary personal data do not belong in repository evidence.
- Human review/share approval and human case-handoff approval remain separate from technical execution.
- Cortex analyzer output is enrichment evidence only.
- Kubernetes placement, workload identity, network reachability, observability, recovery, artifact-attestation, capacity and rollout configuration do not collapse service licensing/authority boundaries.
- Signed provenance is not a declaration that an artifact is vulnerability-free or production-authorized.
- Application rollback is not automatic database rollback or data recovery.
- Historical immutable run records are never rewritten to manufacture later acceptance.
