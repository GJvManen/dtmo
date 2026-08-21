# DTMO Evidence Index

Last updated: **2026-08-21**

## Purpose

This index maps current lifecycle stages to authoritative evidence classes and repository evidence chains. It is not a CI chronology. Historical workflow artifacts and external assurance remain bound to their original candidate.

## Current lifecycle

Phases 1–7 remain `PASS`; RC13 remains `PASS / OWNER_ACCEPTED`; E8.1–E8.10 remain `PASS / REPOSITORY_COMPLETE`. Phase 8 remains `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE`; Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`; Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**.

Phase 11.1–11.9 and Phase 11.10a–11.10k are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 remains **`IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`** with **Phase 11.10l Governance & Evidence** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 11.10m–11.10o, Phase 11.11 and Phase 12 are `NOT STARTED`; Phase 11.10p is `NOT STARTED / CANDIDATE FREEZE REQUIRED`. DTMO is **not production authorized**.

## Evidence hierarchy

1. **Repository-controlled engineering evidence** — exact-head CI, contracts, builds, browser tests, migrations and runtime contracts.
2. **Supply-chain evidence** — artifact hashes, SBOM, provenance and signing for the exact release subject.
3. **Accountable functional evidence** — explicit owner acceptance of product behavior.
4. **Real-environment evidence** — production-equivalent exercise bound to one immutable deployment identity.
5. **Independent assurance** — assessment independent from repository CI.
6. **Formal production authorization** — accountable GO/NO-GO for a specific candidate.

These classes are not interchangeable. Repository CI **does not prove** production-equivalent operation, independent assurance or production authorization.

## Accepted Phase 11 integration and industrialisation baseline

Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate governed service/licensing boundaries. Accepted Phase 11.1–11.9 evidence covers integration contracts plus runtime, workload identity/external secrets, ingress/TLS/network segmentation, HA/disruption, observability, backup/restore/recovery, supply-chain hardening, capacity, exercised upgrade/rollback and forward-first migration compatibility.

Accepted service implementation evidence includes `.github/workflows/phase11-thehive-handoff-implementation.yml`. That workflow is repository-controlled implementation evidence only: it does not establish live TheHive health, case-state truth beyond recorded handoff evidence, production-equivalent operation, external assurance or production authorization.

Accepted runtime and supply-chain workflow evidence remains explicitly indexed through:

- `.github/workflows/phase11-runtime-foundation.yml`;
- `.github/workflows/phase11-workload-identity-secrets.yml`;
- `.github/workflows/phase11-ingress-tls-network.yml`;
- `.github/workflows/phase11-ha-disruption.yml`;
- `.github/workflows/phase11-supply-chain-hardening.yml`;
- `.github/workflows/release-artifact-attestation.yml`;
- `.github/workflows/phase11-upgrade-rollback.yml`;
- `.github/workflows/phase11-migration-compatibility.yml`.

Application rollback does not authorize automatic database down migration. Configuration or CI success does not establish live service health, production-equivalent behavior or production authorization.

## Phase 11.10 candidate-completion evidence

For lifecycle discoverability, every bounded slice is explicitly indexed: **11.10a** Frontend Architecture & Design, **11.10b** Application Shell, **11.10c** Command Center, **11.10d** Unified Intelligence, **11.10e** IntelOwl/Cortex Integrated Analysis, **11.10f** OpenCTI Graph & Entity, **11.10g** MISP Sharing & Exchange, **11.10h** TheHive Investigations & Cases, **11.10i** Vulnerability & Exposure, **11.10j** Sources & Collection, **11.10k** Automation & Playbooks and **11.10l** Governance & Evidence. Slices 11.10a–11.10k are `PASS / REPOSITORY_COMPLETE`; 11.10l remains `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. This index records repository evidence state only and does not establish production-equivalent behavior, independent assurance or production authorization.

### 11.10a–11.10g

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted packages cover frontend architecture/design, canonical application shell, Command Center, Unified Intelligence, IntelOwl/Cortex integrated analysis, OpenCTI graph/entity and MISP Sharing & Exchange. Human review/share/publication authority remains separate; enrichment, topology and transfer evidence do not prove compromise or publication.

### 11.10h TheHive Investigations & Cases

**Status:** `PASS / REPOSITORY_COMPLETE`.

Authoritative evidence includes `backend/dtmo/thehive_handoff.py`, TheHive integration/persistence, `frontend/src/InvestigationsWorkspace.tsx`, architecture/user/QA material, deterministic tests and `.github/workflows/phase11-thehive-investigations.yml`. Case mutation remains explicit human `handoff:case` authority. Ambiguous handoff state fails closed; case identity does not prove compromise, remediation or later upstream case state.

### 11.10i Vulnerability & Exposure

**Status:** `PASS / REPOSITORY_COMPLETE`.

Authoritative evidence includes `frontend/src/ExposureWorkspace.tsx`, the canonical vulnerability analytics API projection, `docs/architecture/PHASE11_10I_VULNERABILITY_EXPOSURE.md`, `docs/user/VULNERABILITY_EXPOSURE_WORKSPACE.md`, `docs/qa/PHASE11_10I_VULNERABILITY_EXPOSURE_GATE.md`, deterministic tests and `.github/workflows/phase11-vulnerability-exposure.yml`. CVSS/EPSS/KEV are prioritization inputs, not proof of local exposure or compromise.

### 11.10j Sources & Collection

**Status:** `PASS / REPOSITORY_COMPLETE`.

Authoritative evidence includes `backend/dtmo/admin_sources.py`, `frontend/src/CollectionWorkspace.tsx`, architecture/user/QA material, deterministic contract/browser tests and `.github/workflows/phase11-sources-collection.yml`. Source credentials remain server-side references; validation/test/run evidence does not prove source truth, compromise or production health.

### 11.10k Automation & Playbooks

**Status:** `PASS / REPOSITORY_COMPLETE`.

Authoritative evidence includes `frontend/src/AutomationWorkspace.tsx`, governed connector execution contracts, architecture/user/QA material, deterministic tests and `.github/workflows/phase11-automation-playbooks.yml`. Automation never acquires human review/share/publication, case, remediation or production authority and does not prove source truth or compromise.

### 11.10l Governance & Evidence

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

Authoritative active evidence chain:

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

The Governance surface uses the explicit typed partial crosswalk already present in the repository. Normenkader IBP relationships include explicitly recorded control identifiers such as `ID.02`, `ID.05`, `SM.02`, `SM.04`, `SM.07`, `SM.11`, `OP.02`, `BC.03` and `GO.03` where implementation evidence exists. MITRE ATT&CK relationships are explicit threat/detection/classification context and are not inferred from free text. NIST CSF relationships are partial outcomes/categories. CVSS is `context-only` scoring semantics.

These mappings are **not** certification, complete compliance, semantic equivalence, proof of control effectiveness in an environment, local compromise, audit acceptance, independent assurance or production authorization. Unrecorded framework objects remain unmapped. Missing or inaccessible evidence must **fail closed**.

Governance visibility is read-oriented and grants no review, case, remediation, connector, external-share, publication, administration or production authority. Repository CI remains exact-head engineering evidence only.

### Candidate-completion order

After acceptance of 11.10l, the next bounded priorities remain 11.10m Operations & Administration, 11.10n role-aware UX/accessibility and 11.10o consolidation/full functional acceptance. No later slice may start while the active bounded PR is unaccepted.

## Phase 11.10p production-equivalent evidence

**Status:** `NOT STARTED / CANDIDATE FREEZE REQUIRED`.

After 11.10o, one immutable integrated candidate must be frozen. Fresh evidence must cover candidate identity, migration/compatibility, upgrade, rollback to the exact prior immutable digest plus post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity for the **same immutable candidate** and production-equivalent environment.

The authoritative repository execution chain remains explicit:

- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `tools/phase11_production_equivalent_validation.py`;
- `backend/tests/test_phase11_10_production_equivalent_validation.py`;
- `.github/workflows/phase11-production-equivalent-validation.yml`.

That later gate requires fresh evidence for candidate identity, migration/compatibility, upgrade, rollback, health, saturation and recovery for one immutable candidate. Missing, inaccessible, placeholder, historical-only or mixed-candidate evidence must **fail closed**. Repository workflow success alone is not production-equivalent evidence and does not authorize production.

Historical Phase 8/9 evidence is audit history only and cannot be reused as proof for the materially changed candidate.

## Phase 11.11 and Phase 12

Phase 11.11 independent external assurance is `NOT STARTED` and remains blocked until Phase 11.10 is explicitly `PASS / OWNER_ACCEPTED`. Phase 12 is `NOT STARTED`; only a formal accountable decision can authorize production.
