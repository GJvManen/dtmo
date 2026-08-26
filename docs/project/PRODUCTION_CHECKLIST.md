# DTMO Production Readiness Checklist

Last reconciled: **2026-08-26**  
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
| Phase 11.10c Command Center | `PASS / REPOSITORY_COMPLETE` | Accepted repository/browser Command Center evidence |
| Phase 11.10d Unified Intelligence Workspace | `PASS / REPOSITORY_COMPLETE` | Accepted repository/browser intelligence evidence |
| Phase 11.10e IntelOwl/Cortex integrated analysis | `PASS / REPOSITORY_COMPLETE` | Accepted repository/browser analysis evidence |
| Phase 11.10f OpenCTI graph/entity workspace | `PASS / REPOSITORY_COMPLETE` | Accepted repository/browser graph evidence |
| Phase 11.10g MISP Sharing & Exchange | `PASS / REPOSITORY_COMPLETE` | Accepted repository/browser governed exchange evidence |
| Phase 11.10h TheHive Investigations & Cases | `PASS / REPOSITORY_COMPLETE` | Accepted repository/browser governed case evidence |
| Phase 11.10i Vulnerability & Exposure Center | `PASS / REPOSITORY_COMPLETE` | Accepted repository/browser vulnerability evidence |
| Phase 11.10j Sources & Collection Control Center | `PASS / REPOSITORY_COMPLETE` | Accepted repository/browser collection-control evidence |
| Phase 11.10k Automation & Playbooks | `PASS / REPOSITORY_COMPLETE` | Accepted repository/browser automation evidence |
| Phase 11.10l Governance & Evidence Center | `PASS / REPOSITORY_COMPLETE` | Accepted repository/browser governance evidence |
| Phase 11.10m–11.10o recovery continuation | `PASS / REPOSITORY_COMPLETE` | Accepted repository/browser recovery continuation evidence |
| Phase 11.10q Functional Recovery Acceptance | `MERGED / OWNER-AUTHORIZED MERGE` | Accountable functional recovery acceptance |
| Post-11.10q framework-integration hardening | `PASS / REPOSITORY_COMPLETE` | Repository integration hardening evidence |
| Fresh candidate freeze | `NEXT / REQUIRED` | Candidate identity boundary |
| Phase 11.10p production-equivalent validation | `NOT YET EXECUTED FOR NEW CANDIDATE` | Future real-environment evidence |
| Phase 11.11 independent external assurance | `NOT STARTED` | Independent assurance |
| Phase 12 | `NOT STARTED` | Future production authorization |

Historical Phase 8/9 evidence remains candidate-bound and cannot be reused for the materially changed Phase 11 candidate.

## Evidence rules

- Repository CI, owner acceptance, production-equivalent validation, independent assurance and production authorization are separate evidence classes.
- Missing evidence is not implicit acceptance.
- Historical evidence is preserved rather than relabelled.
- Role-aware UI never substitutes for **server-side RBAC**.
- Human review and sharing approval remain separate human decisions; publication/share authority remains separate from TheHive case authority and technical execution.
- Analyzer, graph, correlation, exchange or case presence is evidence, not proof of local compromise.
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
- [x] Phase 11.10c canonical Command Center accepted and merged with expected-head protection.
- [x] Phase 11.10d Unified Intelligence Workspace accepted and merged with expected-head protection.
- [x] Phase 11.10e IntelOwl/Cortex integrated analysis accepted and merged with expected-head protection.
- [x] Phase 11.10f OpenCTI graph/entity workspace accepted and merged with expected-head protection.
- [x] Phase 11.10g MISP Sharing & Exchange accepted and merged with expected-head protection.
- [x] Phase 11.10h TheHive Investigations & Cases accepted as repository-complete.
- [x] Phase 11.10i Vulnerability & Exposure Center accepted as repository-complete.
- [x] Phase 11.10j Sources & Collection Control Center accepted as repository-complete.
- [x] Phase 11.10k Automation & Playbooks accepted as repository-complete.
- [x] Phase 11.10l Governance & Evidence Center accepted as repository-complete.
- [x] Phase 11.10m–11.10o recovery continuation accepted as repository-complete.
- [x] Phase 11.10q Functional Recovery Acceptance owner-authorized and merged.
- [x] Post-11.10q framework-integration hardening accepted as repository-complete.

## 3. Candidate-completion status

The repository-controlled functional recovery and hardening sequence is complete. This status is repository evidence only and does not authorize production-equivalent, external-assurance or production claims.

- [x] 11.10i Vulnerability & Exposure Center.
- [x] 11.10j Sources & Collection Control Center.
- [x] 11.10k Automation & Playbooks.
- [x] 11.10l Governance & Evidence Center.
- [x] 11.10m Operations & Administration recovery continuation.
- [x] 11.10n role-aware UX/accessibility recovery continuation.
- [x] 11.10o consolidation/full functional acceptance recovery continuation.
- [x] 11.10q Functional Recovery Acceptance merged with owner authorization.
- [x] Post-11.10q framework-integration hardening repository-complete.
- [ ] One immutable integrated candidate frozen after the accepted recovery/hardening baseline.

## 4. Fresh candidate freeze boundary

Before any new production-equivalent evidence is accepted, one immutable integrated candidate must be identified consistently. At minimum the candidate record must bind:

- [ ] exact deployed Git commit;
- [ ] immutable application image digest;
- [ ] expected migration head;
- [ ] deployment/GitOps revision;
- [ ] approved production-equivalent environment identifier;
- [ ] exact prior immutable application digest used for rollback;
- [ ] accountable owner/operator/reviewer;
- [ ] one consistent candidate fingerprint across all evidence.

Do not fill these fields from repository assumptions. Missing, placeholder, mutable-tag-only or mixed-candidate identity fails closed. Repository CI, staging-emulator evidence and historical Phase 8/9 evidence cannot substitute for a fresh candidate-bound production-equivalent run.

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

- [ ] Start only after Phase 11.10 is `PASS / OWNER_ACCEPTED` for the fresh immutable candidate.
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
