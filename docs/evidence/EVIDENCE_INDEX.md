# DTMO Evidence Index

Last updated: **2026-08-18**

## Purpose

This index maps lifecycle stages to evidence classes and authoritative professional documentation. It is not a CI chronology. Exact run/commit/job history remains in immutable operational records, pull requests and CI artifacts.

**Current lifecycle:** Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate only; Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1–11.8f are `PASS / REPOSITORY_COMPLETE`, with the original Phase 11.7 Cortex decision retained as a historical baseline; Phase 11.8g software supply-chain hardening is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`; Phase 12 is `NOT STARTED`. DTMO is not production authorized. Historical Phase 8/9 evidence remains candidate-bound and cannot satisfy Phase 11.10/11.11.

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
- `docs/operations/PHASE11_8G_SUPPLY_CHAIN_RUNBOOK.md`
- `docs/qa/PHASE11_8G_SUPPLY_CHAIN_GATE.md`
- `backend/tests/test_phase11_8g_supply_chain_contract.py`
- `.github/workflows/phase11-supply-chain-hardening.yml`
- `.github/workflows/release-artifact-attestation.yml`
- `docs/architecture/CORTEX_DECISION_GATE.md`
- `docs/architecture/CORTEX_DTMO_INTEGRATION_CONTRACT.md`
- `docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md`
- `.github/workflows/phase11-thehive-handoff-implementation.yml`
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

Accepted repository evidence covers Taranis, IntelOwl, OpenCTI, MISP, TheHive and the later bounded Cortex analyzer connector. The accepted TheHive implementation evidence includes the repository workflow `.github/workflows/phase11-thehive-handoff-implementation.yml`; this reference preserves the historical repository-evidence chain and does not imply live TheHive deployment evidence. Service identity/licensing boundaries, provenance, RBAC, human publication/share authority and fail-closed semantics remain authoritative.

### Phase 11.8a–11.8e

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers the governed Helm/GitOps runtime foundation, workload identity/external-secret delivery, TLS ingress/network segmentation, application HA/disruption controls and opt-in observability boundaries. The accepted workload-identity and secret-delivery evidence includes `.github/workflows/phase11-workload-identity-secrets.yml`; this preserves the accepted repository-evidence chain and does not imply live cloud IAM, external secret retrieval, rotation, revocation or production deployment evidence. The accepted ingress/TLS/network-segmentation evidence includes `.github/workflows/phase11-ingress-tls-network.yml`; this preserves the accepted repository-evidence chain and does not imply live certificate issuance, ingress enforcement, network-policy enforcement or production deployment evidence. The accepted HA/disruption evidence includes `.github/workflows/phase11-ha-disruption.yml`; this preserves the accepted repository-evidence chain and does not imply live availability-zone survival, stateful quorum/failover, storage durability or production HA evidence. These controls remain repository engineering evidence and do not prove live provider enforcement, production availability or production authorization.

### Phase 11.8f Backup, restore and recovery hardening

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence defines PostgreSQL, Redis, OpenSearch and object storage as explicit recovery domains and requires accountable backup ownership, retention, restore verification, recovery-exercise cadence and measurable RPO/RTO evidence boundaries. Repository acceptance does not prove successful live backups, PITR, achieved recovery objectives, provider durability or disaster failover.

Dedicated evidence remains `tests/test_phase11_8f_recovery_contract.py`, `.github/workflows/phase11-recovery-hardening.yml`, `docs/architecture/PHASE11_8F_RECOVERY_HARDENING.md`, `docs/operations/PHASE11_8F_RECOVERY_RUNBOOK.md` and `docs/qa/PHASE11_8F_RECOVERY_GATE.md`.

### Phase 11.8g Software supply-chain hardening

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

The bounded repository evidence target requires exact-head build identity, Python and container CycloneDX SBOM generation, Python dependency auditing, container `HIGH`/`CRITICAL` known-vulnerability scanning, SHA-256 artifact identities and a governed release path for cryptographically signed provenance and SBOM attestations.

Dedicated repository evidence is `backend/tests/test_phase11_8g_supply_chain_contract.py`, `.github/workflows/phase11-supply-chain-hardening.yml`, `.github/workflows/release-artifact-attestation.yml`, `docs/security/PHASE11_8G_SUPPLY_CHAIN_HARDENING.md`, `docs/operations/PHASE11_8G_SUPPLY_CHAIN_RUNBOOK.md` and `docs/qa/PHASE11_8G_SUPPLY_CHAIN_GATE.md`.

A green PR gate proves the repository mechanism and the exact-head scan outputs only. It does **not** prove that a future release artifact has already received a signed attestation, that a registry/deployment environment has verified that attestation, that all vulnerabilities are absent, or that production-equivalent validation, independent assurance or production authorization has occurred. Missing supply-chain evidence fails closed.

### Remaining Phase 11.8

Subsequent bounded PRs must independently establish capacity and upgrade/rollback controls. Phase 11.9 does not start until all required 11.8 controls are accepted.

### Phase 11.9

Migration and compatibility evidence follows completed Phase 11.8 runtime industrialisation.

### Phase 11.10–11.11

Fresh production-equivalent validation and fresh independent assurance must target the same immutable integrated candidate. Historical Phase 8/9 evidence cannot satisfy these gates.

### Phase 12

**Status:** `NOT STARTED`.

## Evidence transfer rule

Historical Phase 8/9 acceptance remains candidate-bound and cannot be transferred automatically to the materially changed Phase 11 platform. The historical Phase 11.7 Cortex decision is also not rewritten to manufacture the later owner requirement.

## Governance and handling rules

Framework claims remain governed by explicit provenance-backed mappings. External service, workload identity, secret-provider, ingress, HA, observability, recovery or supply-chain state does not establish local exploitability, compromise, case necessity or dissemination authority without separate attributable evidence.

- Exact-head evidence belongs only to the exact state tested.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Sensitive authentication material, TLS private keys, signing key material and unnecessary personal data do not belong in repository evidence.
- Human review/share approval and human case-handoff approval remain separate from technical execution.
- Cortex analyzer output is enrichment evidence only.
- Kubernetes placement, workload identity, network reachability, observability, recovery and artifact-attestation configuration do not collapse service licensing/authority boundaries.
- Signed provenance is not a declaration that an artifact is vulnerability-free or production-authorized.
- Historical immutable run records are never rewritten to manufacture later acceptance.
