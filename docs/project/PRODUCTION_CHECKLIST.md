# DTMO Production Readiness Checklist

Last reconciled: **2026-08-20**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

This checklist controls the post-Phase-10 industrialisation programme and future Phase 12 production authorization decision. DTMO is **not production authorized**.

## Current lifecycle status

| Stage | Status | Evidence class |
|---|---|---|
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` | Repository product evolution |
| Phase 8 | `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` | Historical accountable staging acceptance |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE` | Historical independent assurance |
| Phase 10 | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` | Accountable production decision |
| Phase 11 | `IN PROGRESS / ACTIVE` | Platform industrialisation |
| Phase 11.1–11.9 | `PASS / REPOSITORY_COMPLETE` | Integration/runtime/migration evidence |
| Phase 11.10 | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` | Candidate completion + future real-environment evidence |
| Phase 11.10a frontend architecture/design | `PASS / REPOSITORY_COMPLETE` | Repository architecture evidence |
| Phase 11.10b canonical application shell | `PASS / REPOSITORY_COMPLETE` | Repository/browser shell evidence |
| Phase 11.10c Command Center | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Repository/browser Command Center evidence |
| Phase 11.10d Unified Intelligence Workspace | `NOT STARTED` | Future product evidence |
| Phase 11.10p production-equivalent validation | `NOT STARTED / CANDIDATE FREEZE REQUIRED` | Future real-environment evidence |
| Phase 11.11 independent external assurance | `NOT STARTED` | Independent assurance |
| Phase 12 | `NOT STARTED` | Future production authorization |

Historical Phase 8/9 evidence remains candidate-bound and cannot be reused for the materially changed Phase 11 candidate.

## Evidence rules

- Repository CI, owner acceptance, production-equivalent validation, independent assurance and production authorization are separate evidence classes.
- Missing evidence is not implicit acceptance.
- Historical evidence is preserved rather than relabelled.
- Role-aware UI never substitutes for **server-side RBAC**.
- Human publication/share authority remains separate from TheHive case authority and technical execution.
- Repository/browser CI **does not prove** live upstream health or production-equivalent operation.
- Missing, placeholder, inaccessible, historical-only or mixed-candidate evidence must **fail closed**.

## 1. Accepted baseline

- [x] Phases 1–7 repository engineering baseline.
- [x] RC13 `PASS / OWNER_ACCEPTED`.
- [x] E8.1–E8.10 `PASS / REPOSITORY_COMPLETE`.
- [x] Phase 10 remains `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.
- [x] Phase 11.1–11.7b service/integration boundaries accepted.
- [x] Phase 11.8 runtime industrialisation accepted, including workload identity, external secret delivery, ingress/TLS, HA, observability, recovery, supply chain, capacity and upgrade/rollback.
- [x] Phase 11.9 migration/compatibility accepted with forward-first and no-automatic-down-migration boundaries.

## 2. Accepted Unified Operations Workbench foundation

- [x] Phase 11.10a frontend architecture/design contract accepted.
- [x] Canonical path is browser → DTMO API → governed integration adapter → upstream service.
- [x] Phase 11.10b React/TypeScript/Vite canonical `/workbench/` shell accepted.
- [x] Committed frontend dependency graph consumed with `npm ci`.
- [x] `/ui/console` retained only as a migration **compatibility path**.
- [x] Responsive navigation, keyboard command palette, context rail, light/dark semantics and CSP accepted.
- [x] Existing security, accessibility, integration and supply-chain regressions remained green on the accepted 11.10b exact head.

## 3. Active Phase 11.10c — Command Center

Implementation criteria:

- [x] Canonical read model implemented in `backend/dtmo/command_center.py`.
- [x] Server-authorized read API implemented at `/api/v1/command-center`.
- [x] Six operational KPI classes derived from canonical DTMO persistence.
- [x] Recent canonical intelligence is exposed without direct upstream browser calls.
- [x] Taranis, IntelOwl, OpenCTI, MISP, TheHive and Cortex capability state is visible.
- [x] Configuration state is separated from runtime observation; feature enablement is not a health claim.
- [x] Canonical-store failure returns `null` values / unavailable state rather than synthetic zeros.
- [x] Role-aware quick actions are derived from server-issued permissions.
- [x] Command Center remains read-only; review/share/case/connector/admin mutations retain separate authorization.
- [x] Dedicated repository and browser contracts added.
- [x] Dedicated `Phase 11 Command Center Gate` added.
- [ ] Final exact-head frontend `npm ci`, typecheck and production build are green.
- [ ] Final exact-head Command Center repository contract is green.
- [ ] Final exact-head browser acceptance is green.
- [ ] Existing security, accessibility, integration, migration, runtime and supply-chain regressions are all green for the same exact head.
- [ ] Professional current-state, evidence, QA and roadmap documentation is synchronized for the same head.
- [ ] Phase 11.10c merged with expected-head protection only after every registered exact-head workflow is `completed/success`.

Only after these items are complete may **Phase 11.10d Unified Intelligence Workspace** start.

## 4. Remaining candidate-completion sequence

- [ ] 11.10d Unified Intelligence Workspace.
- [ ] 11.10e IntelOwl/Cortex integrated analysis.
- [ ] 11.10f OpenCTI graph/entity workspace.
- [ ] 11.10g MISP Sharing & Exchange.
- [ ] 11.10h TheHive Investigations & Cases.
- [ ] 11.10i Vulnerability & Exposure Center.
- [ ] 11.10j Sources & Collection Control Center.
- [ ] 11.10k Automation & Playbooks.
- [ ] 11.10l Governance & Evidence Center.
- [ ] 11.10m Operations & Administration.
- [ ] 11.10n role-aware UX/accessibility.
- [ ] 11.10o consolidation/full functional acceptance and obsolete UI retirement.
- [ ] One immutable integrated candidate frozen after 11.10o acceptance.

## 5. Phase 11.10p — fresh production-equivalent validation

### Candidate and environment identity

- [ ] Approved production-equivalent environment identifier recorded.
- [ ] Accountable owner/operator/reviewer recorded.
- [ ] Exact Git commit and immutable application/supporting image digests recorded.
- [ ] Expected migration head and deployment/GitOps revision recorded.
- [ ] Exact prior immutable application digest recorded for rollback.
- [ ] Candidate fingerprint calculated and consistent across all evidence.

### Required evidence classes

- [ ] Migration/compatibility exercised on the candidate.
- [ ] Upgrade exercised and attributable to the same candidate.
- [ ] Health/readiness evidence captured.
- [ ] Representative saturation/capacity behavior captured.
- [ ] Recovery/continuity exercised with integrity/RPO/RTO observations where applicable.
- [ ] Rollback restores the **exact prior immutable** digest.
- [ ] Successful **post-rollback health** captured.
- [ ] Application rollback performs no **automatic database down migration**.
- [ ] No open release-blocking findings remain.
- [ ] Accountable review records `PASS / OWNER_ACCEPTED` only after all referenced evidence is inspected.

Repository-green status cannot satisfy these items.

## 6. Phase 11.11 — independent external assurance

- [ ] Start only after Phase 11.10 is `PASS / OWNER_ACCEPTED`.
- [ ] Assess the **same immutable** integrated candidate.
- [ ] Preserve independent assessor evidence and residual findings.
- [ ] Material candidate changes invalidate the assurance binding and require renewed validation/assurance as applicable.

## 7. Phase 12 — formal production decision

- [ ] Phase 11.10 accepted for the release candidate.
- [ ] Phase 11.11 accepted for the same candidate.
- [ ] Accountable operational owner identified.
- [ ] Residual risk and exceptions formally accepted or closed.
- [ ] Support/change/rollback authority documented.
- [ ] Formal production GO/NO-GO recorded.

Until all required Phase 12 decision evidence is accepted, DTMO remains **not production authorized**.
