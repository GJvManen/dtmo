# DTMO Platform Industrialisation Roadmap

Last updated: **2026-08-25**  
Programme state: **`ACTIVE — FRESH CANDIDATE VALIDATION`**

## Purpose and release truth

Phase 10's historical decision was `NO-GO / PLATFORM INDUSTRIALISATION REQUIRED`. Phase 11 delivered the successor industrialisation programme. Historical Phase 8 production-equivalent validation and Phase 9 external assurance remain valid only for their earlier candidate and cannot be transferred to the materially changed integrated workbench candidate.

DTMO remains **not production authorized**.

## Programme status

| Scope | Status |
|---|---|
| 11.1–11.9 integrations/runtime/migration | `PASS / REPOSITORY_COMPLETE` |
| 11.10a–11.10p repository candidate-completion contracts | `PASS / REPOSITORY_COMPLETE` |
| 11.10q functional completeness remediation | `MERGED / OWNER-AUTHORIZED` |
| Fresh immutable candidate freeze | `NEXT` |
| Fresh production-equivalent validation | `NOT YET ACCEPTED / FRESH EVIDENCE REQUIRED` |
| 11.11 independent external assurance | `BLOCKED UNTIL PRODUCTION-EQUIVALENT PASS` |
| Phase 12 formal production GO/NO-GO | `BLOCKED` |

## Accepted industrialisation baseline

### 11.1–11.7b governed service integrations

Taranis AI, IntelOwl, OpenCTI, MISP, TheHive and Cortex are integrated through DTMO-owned server-side contracts. Browser access does not become privileged upstream access. Credentials remain server-side. Enrichment output is evidence rather than a compromise verdict. MISP transport is separate from human review/share/publication authority. TheHive case handoff remains separately authorized. Graph topology is not inferred beyond persisted evidence.

### 11.8 runtime industrialisation

**Status:** `PASS / REPOSITORY_COMPLETE`

The repository baseline covers Kubernetes/Helm/GitOps, workload identity/external secret delivery, ingress/TLS/network segmentation, HA/disruption handling, observability, backup/recovery, software supply-chain controls, capacity planning and upgrade/rollback contracts. Repository acceptance does not itself prove production-equivalent behavior.

### 11.9 migration and compatibility

**Status:** `PASS / REPOSITORY_COMPLETE`

The accepted contract requires a connected Alembic chain, forward-first migration, rolling compatibility and expand/migrate/contract handling for destructive change. Ambiguity remains fail closed.

## 11.10 Unified Operations Workbench and functional recovery

**Status:** `MERGED / OWNER-AUTHORIZED`

The candidate-completion programme delivered the canonical application shell, Command Center, Unified Intelligence, IOC Explorer, Analysis & Enrichment, OpenCTI Graph, MISP Sharing & Exchange, TheHive Investigations, Vulnerability & Exposure, Sources & Collection, Automation & Playbooks, Governance & Evidence, Operations & Administration, role-aware UX/accessibility and consolidation/full functional acceptance contracts.

Phase 11.10q then addressed the owner's 2026-08-24 functional rejection. The final PR #316 head was `a2dff382d7d08d9058db0d0540c9ef1af172090a`. The owner explicitly directed merge after exact-head pull-request CI reported zero failed workflows, and PR #316 was merged as `e0a6019f561eaedade250093225ca22d9c937e8b` on 2026-08-25.

The recovery work includes canonical framework readiness/configuration, source bootstrap/control, Threat Intelligence population/default discovery, IOC inventory/pivots, Knowledge Graph discovery/population, Exposure population/filtering, object-driven Analysis/Investigations/Sharing, executable and observable Automation/Playbooks, Command Center readiness/trends, canonical operational telemetry, and unmocked same-origin repository browser acceptance.

The accepted security/evidence boundaries remain mandatory:

- server-side RBAC is authoritative;
- provenance must remain attributable;
- human review/share/publication authority is never inferred from technical access;
- case handoff remains separately authorized;
- missing or ambiguous state fails closed;
- credentials remain server-side;
- connector/run health is not source truth, compromise evidence, remediation success or production authorization;
- repository-controlled sample/bootstrap/browser evidence is not live, staging, production-equivalent or independent-assurance evidence.

## Fresh candidate freeze and production-equivalent validation

**Status:** `NEXT / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`

After documentation synchronization, freeze one immutable `main` commit as the next integrated candidate. The exact candidate identity must be carried through every production-equivalent artifact.

Required evidence includes candidate/deployment identity, migration compatibility, upgrade, rollback to the exact prior immutable digest with post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity. Application rollback never authorizes automatic database down migration.

The controlled package remains:

- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `tools/phase11_production_equivalent_validation.py`;
- `backend/tests/test_phase11_10_production_equivalent_validation.py`;
- `.github/workflows/phase11-production-equivalent-validation.yml`.

Historical Phase 8/9 evidence cannot satisfy the new validation. Missing, mixed-candidate, inaccessible, placeholder or historical-only evidence must fail closed. Repository CI can validate the evidence contract but cannot manufacture the real environment observations.

## Phase 11.11 — new independent external assurance

**Status:** `BLOCKED / WAITING FOR FRESH PRODUCTION-EQUIVALENT PASS`

Fresh independent assurance starts only after the newly frozen integrated candidate passes production-equivalent validation and must target the same immutable candidate identity.

## Phase 12 — production GO/NO-GO

**Status:** `BLOCKED`

A production `GO` requires accepted production-equivalent and independent-assurance evidence for the same candidate plus accountable ownership, residual-risk acceptance, support/change/rollback authority and the remaining IAM, secrets, network, recovery, monitoring, privacy and legal prerequisites.

## Immediate sequence

1. Keep authoritative documentation synchronized on `main`.
2. Freeze the synchronized `main` head as one immutable candidate.
3. Execute the fresh production-equivalent validation package against that exact candidate.
4. If validation changes code or configuration, invalidate the freeze, remediate the root cause and freeze a new candidate.
5. After explicit production-equivalent acceptance, restart Phase 11.11 external assurance for that same candidate.
6. Enter Phase 12 only after both fresh evidence classes are accepted.
