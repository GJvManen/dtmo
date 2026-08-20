# DTMO Roadmap — Production Readiness and Product Evolution

Last updated: **2026-08-20**

## Purpose

This roadmap separates production authorization from product evolution and platform industrialisation. Repository engineering, accountable functional acceptance, deployment-bound validation, independent assurance and production authorization remain distinct evidence classes.

## Current position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Repository-controlled engineering baseline | `PASS` |
| RC13 + owner retest | Unified-console functional acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | Vulnerability & CTI ecosystem integrations | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Production-equivalent validation | `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 9 | Independent external assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 10 | Formal production go/no-go | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11.1–11.9 | Service integrations, runtime and migration compatibility | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10 | Candidate completion + new production-equivalent validation | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` |
| Phase 11.10a | Frontend architecture/design contract | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10b | Canonical application shell | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10c | Command Center | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10d | Unified Intelligence Workspace | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10e | IntelOwl/Cortex integrated analysis | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10f | OpenCTI graph/entity workspace | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10g | MISP Sharing & Exchange | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10h | TheHive Investigations & Cases | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.10i | Vulnerability & Exposure Center | `NOT STARTED` |
| Phase 11.10p | Fresh production-equivalent validation | `NOT STARTED / CANDIDATE FREEZE REQUIRED` |
| Phase 11.11 | New independent external assurance | `NOT STARTED` |
| Phase 12 | New formal production go/no-go | `NOT STARTED` |

DTMO remains **not production authorized**. Phase 11 is `IN PROGRESS / ACTIVE` and remains the highest-priority programme.

## Historical readiness evidence

Phase 8 remains `PASS / OWNER_ACCEPTED` and Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate only. Those claims are historical and cannot be transferred to the materially changed Phase 11 candidate.

## Phase 11 platform industrialisation

The authoritative detailed programme is `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`. Phase 11.1–11.9 are `PASS / REPOSITORY_COMPLETE`. The accepted baseline includes Taranis AI, IntelOwl, OpenCTI, MISP, TheHive, Cortex, Kubernetes/Helm/GitOps, workload identity/external secrets, ingress/TLS/network segmentation, HA, observability, recovery, supply chain, capacity, upgrade/rollback and forward-first migration compatibility.

Repository acceptance of these controls does not establish production-equivalent behavior.

## Phase 11.10 — Candidate completion and validation

**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`

The Unified Operations Workbench materially changes the candidate. Phase 11.10 therefore completes the workbench first, freezes one immutable candidate, and only then performs the fresh production-equivalent exercise.

### Part A — 11.10a–11.10o candidate completion

1. 11.10a frontend architecture/design contract — `PASS / REPOSITORY_COMPLETE`;
2. 11.10b canonical application shell — `PASS / REPOSITORY_COMPLETE`;
3. 11.10c Command Center — `PASS / REPOSITORY_COMPLETE`;
4. 11.10d Unified Intelligence Workspace — `PASS / REPOSITORY_COMPLETE`;
5. 11.10e IntelOwl/Cortex integrated analysis — `PASS / REPOSITORY_COMPLETE`;
6. 11.10f OpenCTI graph/entity workspace — `PASS / REPOSITORY_COMPLETE`;
7. 11.10g MISP Sharing & Exchange — `PASS / REPOSITORY_COMPLETE`;
8. **11.10h TheHive Investigations & Cases — `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`**;
9. 11.10i Vulnerability & Exposure Center — `NOT STARTED`;
10. 11.10j Sources & Collection Control Center — `NOT STARTED`;
11. 11.10k Automation & Playbooks — `NOT STARTED`;
12. 11.10l Governance & Evidence Center — `NOT STARTED`;
13. 11.10m Operations & Administration — `NOT STARTED`;
14. 11.10n role-aware UX/accessibility — `NOT STARTED`;
15. 11.10o consolidation/full functional acceptance — `NOT STARTED`.

The canonical security path remains **browser → DTMO API → governed integration adapter → upstream service**. **Server-side RBAC**, provenance, human publication/share authority and separate TheHive case authority remain authoritative. `/ui/console` and earlier UI routes remain temporary **compatibility paths**.

### Accepted 11.10a–11.10g workbench baseline

The accepted workbench includes the frontend architecture, canonical React/TypeScript/Vite shell, Command Center, Unified Intelligence/IOC Explorer, Integrated Analysis, OpenCTI Graph/Entity and MISP Sharing/Exchange. Search projections do not become canonical truth; capability configuration does not become runtime health; IntelOwl/Cortex output does not prove local compromise; OpenCTI generic relationship topology is not inferred beyond persisted evidence; MISP transfer does not become publication/synchronization authority.

### Active 11.10h TheHive Investigations & Cases

The active slice makes `/workbench/investigations` functional by composing accepted Phase 11.6 TheHive case-handoff/persistence controls with a DTMO-owned canonical investigation read projection rather than adding a parallel case backend.

Frontend-facing state contract:

- `GET /api/v1/thehive/items/{item_id}/investigation` — canonical intelligence/provenance/handoff state protected by `read:intelligence`.

Existing governed action remains authoritative:

- `POST /api/v1/thehive/items/{item_id}/cases` — explicit human `handoff:case` mutation.

Service accounts cannot substitute for human case authority. Canonical provenance is required. The browser never receives TheHive credentials and does not call TheHive directly. TLP/PAP and authoritative source restrictions remain fail closed.

Durable `reserved`, `delivered`, `ambiguous` and `failed` handoff evidence is projected. `reserved` or `ambiguous` state requires manual reconciliation and blocks a blind new UI request. A delivered result proves only stable case identity at creation time.

The accepted Phase 11.6 persistence does not mirror TheHive alerts, tasks, case timeline, later upstream case state or responder results. Phase 11.10h therefore does not infer them. Configuration is not live TheHive health. Handoff/case presence does not prove external-share authority, downstream remediation or local compromise.

Authoritative evidence is `docs/architecture/PHASE11_10H_THEHIVE_INVESTIGATIONS_CASES.md`, `docs/user/THEHIVE_INVESTIGATIONS_WORKSPACE.md`, `docs/qa/PHASE11_10H_THEHIVE_INVESTIGATIONS_GATE.md`, the Phase 11.10h contract/API/browser tests and `.github/workflows/phase11-thehive-investigations.yml`.

Repository/browser acceptance **does not prove** live TheHive connectivity/health, license entitlement, upstream case completeness, responder execution, production-equivalent operation, independent assurance or production authorization.

### Part B — 11.10p fresh production-equivalent validation

After 11.10o acceptance, freeze one immutable integrated deployment identity. 11.10p requires fresh evidence for candidate identity, migration/compatibility, upgrade, exact prior-digest rollback plus post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity.

All external evidence must identify the **same immutable** candidate fingerprint and production-equivalent environment. Application rollback does not authorize automatic database down migration. Historical Phase 8/9 evidence cannot satisfy the gate. Missing, ambiguous, inaccessible, placeholder, historical-only or mixed-candidate evidence must **fail closed**.

The controlled package remains `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`, `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`, `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`, `tools/phase11_production_equivalent_validation.py`, `backend/tests/test_phase11_10_production_equivalent_validation.py` and `.github/workflows/phase11-production-equivalent-validation.yml`.

Repository CI and manifest validation support the gate but are not real-environment evidence. Phase 11.10 completes only when candidate completion and 11.10p evidence are explicitly `PASS / OWNER_ACCEPTED`.

## Phase 11.11 — New independent external assurance

**Status:** `NOT STARTED`

Run fresh independent assurance against the same immutable integrated candidate only after Phase 11.10 acceptance. Historical Phase 9 assurance cannot satisfy this gate.

## Phase 12 — Formal production GO/NO-GO

**Status:** `NOT STARTED`

Phase 12 begins only after accepted Phase 11.10 and Phase 11.11 evidence for the same release identity plus accountable production ownership, residual-risk, IAM/secrets/network/recovery/monitoring/privacy/legal/change prerequisites.

## Delivery discipline

Each material repository change requires one bounded PR with explicit acceptance criteria, exact-head CI, expected-head protection and synchronized professional documentation. Production-equivalent validation and independent assurance remain external evidence classes and cannot be manufactured by repository changes.

## Immediate sequence

1. Complete **Phase 11.10h TheHive Investigations & Cases** on one fully green exact head and merge with expected-head protection.
2. Only then start **11.10i Vulnerability & Exposure**.
3. Continue 11.10j–11.10o one green merged bounded PR at a time.
4. Freeze one immutable candidate and execute **11.10p**.
5. Run Phase 11.11 against that same candidate after explicit 11.10 acceptance.
6. Enter Phase 12 only after both evidence classes are accepted.
