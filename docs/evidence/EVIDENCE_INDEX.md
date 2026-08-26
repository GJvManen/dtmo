# DTMO Evidence Index

Last updated: **2026-08-26**

## Purpose

This index maps the current DTMO lifecycle to authoritative evidence classes and repository evidence chains. It is not a CI chronology. Repository-controlled engineering evidence, owner functional acceptance, production-equivalent evidence, independent external assurance and formal production authorization remain separate evidence classes and are never interchangeable.

## Current lifecycle

| Stage | Evidence status |
|---|---|
| Phases 1–7 | `PASS / REPOSITORY_COMPLETE` |
| RC13 historical owner retest | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE ONLY` |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE ONLY` |
| Phase 10 | `NO-GO / BLOCKED — HISTORICAL PLATFORM INDUSTRIALISATION DECISION` |
| Phase 11.1–11.9 | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10a–11.10o | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10q Functional Recovery Acceptance | `MERGED / OWNER-AUTHORIZED` |
| Phase 11.10p | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` |
| Phase 11.11 | `NOT STARTED / BLOCKED UNTIL FRESH PRODUCTION-EQUIVALENT PASS` |
| Phase 12 | `NOT STARTED / BLOCKED UNTIL 11.10p AND 11.11 ACCEPTED` |

DTMO remains **not production authorized**. Phase 11 remains **IN PROGRESS**. Historical Phase 8 and Phase 9 evidence remains attributable only to the historical candidate and cannot be reused for the materially changed current candidate.

## Evidence hierarchy

1. **Repository-controlled engineering evidence** — exact-head CI, deterministic contracts, builds, browser tests, migrations, runtime contracts and bounded repository-controlled integration emulators.
2. **Supply-chain evidence** — immutable artifact hashes, SBOM, provenance and signing for the exact release subject.
3. **Accountable functional evidence** — explicit owner acceptance of product behavior.
4. **Production-equivalent evidence** — accountable observations from an approved production-equivalent environment bound to one immutable deployment identity.
5. **Independent external assurance** — assessment independent from repository CI and bound to the same accepted immutable candidate.
6. **Formal production authorization** — accountable GO/NO-GO for a specific candidate after all prerequisite evidence is accepted.

Repository CI does **not** establish production-equivalent operation, penetration-test success, independent external assurance or production authorization.

## Phase 11 integration and industrialisation baseline

Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate governed service/licensing boundaries. Accepted Phase 11.1–11.9 repository evidence covers integration contracts plus runtime, workload identity/external secrets, ingress/TLS/network segmentation, HA/disruption, observability, backup/restore/recovery, supply-chain hardening, capacity, upgrade/rollback and forward-first migration compatibility.

Application rollback does not authorize automatic database down migration. Connector execution, repository-controlled emulation or CI success does not prove upstream source truth, compromise, remediation success, production-equivalent behavior or production authorization.

Representative repository evidence remains indexed through:

- `.github/workflows/phase11-runtime-foundation.yml`;
- `.github/workflows/phase11-workload-identity-secrets.yml`;
- `.github/workflows/phase11-ingress-tls-network.yml`;
- `.github/workflows/phase11-ha-disruption.yml`;
- `.github/workflows/phase11-supply-chain-hardening.yml`;
- `.github/workflows/release-artifact-attestation.yml`;
- `.github/workflows/phase11-upgrade-rollback.yml`;
- `.github/workflows/phase11-migration-compatibility.yml`.

## Phase 11.10 candidate-completion and functional-recovery evidence

Phase 11.10a–11.10o are `PASS / REPOSITORY_COMPLETE`. They cover the canonical frontend architecture and application shell, Command Center, Unified Intelligence, IntelOwl/Cortex integrated analysis, OpenCTI graph/entity workspace, MISP Sharing & Exchange, TheHive Investigations & Cases, Vulnerability & Exposure, Sources & Collection, Automation & Playbooks, Governance & Evidence, Operations & Administration, role-aware UX/accessibility and consolidation/full functional acceptance contracts.

Phase 11.10q is `MERGED / OWNER-AUTHORIZED`. The later repository-controlled functional recovery slices additionally proved real same-origin journeys for Administration, Threat Intelligence, IOC Explorer, Knowledge Graph, Vulnerability & Exposure, Investigations and Analysis & Enrichment without promoting repository-controlled emulators or fixtures to live-source evidence.

The accepted functional boundaries remain mandatory:

- no primary recovered workflow requires `/ui/*` legacy compatibility paths;
- RBAC and separation of duties remain enforced server-side;
- provenance and immutable raw-evidence binding remain visible where applicable;
- external review/share/publication authority remains explicit human authority and is not inferred from enrichment or case state;
- local compromise is never inferred solely from IOC, enrichment, graph, vulnerability or upstream-case evidence;
- credentials remain server-side and are not exposed to the browser;
- missing, ambiguous or unauthorized state fails closed.

The authoritative functional-recovery record is `docs/roadmap/FUNCTIONAL_RECOVERY_ACCEPTANCE.md`. Repository browser evidence remains repository evidence only and does not establish production-equivalent behavior or external assurance.

## Phase 11.10p — source candidate freeze and production-equivalent evidence

**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`.

The synchronized repository source selected for the next candidate is the immutable Git commit:

`71bd9d08c0005d30c3db632cd2b938b042b64b9a`

That SHA is a **source-candidate identity only**. The convenience branch `phase11-10p-candidate-freeze` currently points to the same commit, but the branch name is mutable and is not itself accepted as an immutable deployment identity.

At the time this index was synchronized, no claim is made that this source commit has already been built into the production-equivalent application image or deployed to an approved production-equivalent environment. Phase 11.10p therefore remains open.

Before execution can begin, the accountable production-equivalent exercise must record and verify all of the following for the exact deployed candidate:

- production-equivalent environment identifier;
- accountable owner, validation operator and security/release reviewer;
- exact deployed Git commit, which must reconcile to the selected source candidate or trigger a refreeze;
- immutable application image digest (`sha256:`);
- immutable supporting image digests;
- expected migration head;
- deployment/GitOps revision;
- exact approved prior immutable application image digest for rollback;
- candidate fingerprint derived from the immutable identity material.

Fresh evidence must then cover immutable candidate identity, migration/compatibility, upgrade, rollback to the exact prior immutable digest plus post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity for the **same candidate fingerprint and production-equivalent environment**.

The authoritative execution package remains:

- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `tools/phase11_production_equivalent_validation.py`;
- `backend/tests/test_phase11_10_production_equivalent_validation.py`;
- `.github/workflows/phase11-production-equivalent-validation.yml`.

The evidence template intentionally remains fail closed while identity fields, observations or accountable review data are `REQUIRED`/`PENDING`. Missing, inaccessible, placeholder, historical-only, synthetic-only or mixed-candidate evidence must not be accepted.

## Phase 11.11 and Phase 12

Phase 11.11 independent external assurance is `NOT STARTED` and remains blocked until fresh Phase 11.10p production-equivalent evidence for one immutable candidate is explicitly accepted. Independent assurance must target that same immutable candidate; historical Phase 9 evidence cannot satisfy the new gate.

Phase 12 is `NOT STARTED`. A production GO requires fresh accepted production-equivalent evidence and fresh accepted independent external assurance for the same release identity, together with accountable production ownership, residual-risk acceptance and explicit rollback authority.

## Claim boundary

This index records repository lifecycle and evidence attribution. It does not manufacture environment observations. The frozen source SHA above is not by itself a deployed image digest, deployment revision, production-equivalent validation result, penetration-test result, external-assurance result or production authorization.
