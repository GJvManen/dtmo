# DTMO Production Readiness Checklist

Last reconciled: **2026-08-20**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

This checklist controls the post-Phase-10 industrialisation programme and future Phase 12 production authorization decision.

## Current lifecycle status

| Stage | Status | Evidence class |
|---|---|---|
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` | Repository product evolution |
| Phase 8 | `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` | Historical accountable staging acceptance |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE` | Historical independent assurance |
| Phase 10 | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` | Accountable production decision |
| Phase 11 | `IN PROGRESS / ACTIVE` | Platform industrialisation |
| Phase 11.1–11.8 | `PASS / REPOSITORY_COMPLETE` | Accepted integrations/runtime controls |
| Phase 11.9 migration/compatibility | `PASS / REPOSITORY_COMPLETE` | Repository migration/compatibility evidence |
| Phase 11.10 candidate completion + production-equivalent validation | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` | Repository/functional + real-environment evidence |
| Phase 11.10a frontend architecture/design contract | `PASS / REPOSITORY_COMPLETE` | Accepted repository architecture evidence |
| Phase 11.10b canonical application shell | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Repository build/browser shell evidence |
| Phase 11.10c Command Center | `NOT STARTED` | Future functional product evidence |
| Phase 11.10p production-equivalent validation | `NOT STARTED / CANDIDATE FREEZE REQUIRED` | Future real-environment evidence |
| Phase 11.11 independent external assurance | `NOT STARTED` | Independent assurance |
| Phase 12 | `NOT STARTED` | Future production authorization |

Historical Phase 8/9 evidence remains candidate-bound and is not reused for the materially changed Phase 11 integrated candidate. DTMO is not production authorized.

## Evidence rules

Repository CI, release signing, accountable acceptance, production-equivalent validation, independent assurance and production authorization are separate evidence classes. Missing mandatory evidence is not implicit acceptance. Sensitive evidence is retained in approved restricted storage rather than committed to Git. Repository shell CI **does not prove** live upstream behavior or production-equivalent operation.

## 1. Accepted baseline

- [x] Phases 1–7 repository engineering baseline.
- [x] RC13 functional owner acceptance (`PASS / OWNER_ACCEPTED`).
- [x] E8.1–E8.10 repository-complete product evolution (`PASS / REPOSITORY_COMPLETE`).
- [x] Historical Phase 8 and Phase 9 evidence preserved in original scope.
- [x] Phase 10 decision remains `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.
- [x] Phase 11.1–11.7b service/integration boundaries accepted.
- [x] Phase 11.8 integrated runtime industrialisation accepted, including workload identity, external secret, ingress/TLS, HA, observability, recovery, supply chain, capacity and upgrade/rollback controls.
- [x] Phase 11.9 migration/compatibility accepted with forward-first and no-automatic-down-migration boundaries.
- [x] Human publication/share authority, separate TheHive case authority, provenance, server-side RBAC, least privilege and fail-closed evidence preserved.

## 2. Accepted Phase 11.10a — frontend architecture/design contract

- [x] `docs/architecture/FRONTEND_ARCHITECTURE.md` accepted.
- [x] `docs/architecture/UI_API_CONTRACT.md` accepted.
- [x] `docs/ux/UNIFIED_OPERATIONS_WORKBENCH.md` accepted.
- [x] `docs/ux/INFORMATION_ARCHITECTURE.md` accepted.
- [x] `docs/ux/DESIGN_SYSTEM.md` accepted.
- [x] Normal product trust path documented as browser → DTMO API → governed integration adapter → upstream service.
- [x] Server-side RBAC remains authoritative; role-aware rendering is not authorization.
- [x] Human publication/share authority remains separate from technical execution.
- [x] TheHive case authority remains separate from publication/share authority.
- [x] Enrichment, graph presence and correlation do not establish local compromise.
- [x] Dark/light theme semantics, severity labels and non-colour accessibility defined.
- [x] Loading, empty, stale, partial-failure and error states defined.
- [x] Design mockups explicitly classified as non-operational evidence.
- [x] Dedicated exact-head Phase 11 Frontend Architecture Gate accepted.
- [x] Professional documentation synchronized for the accepted 11.10a baseline.

## 3. Active Phase 11.10b — canonical application shell

- [x] Separately built React/TypeScript/Vite frontend structure added under `frontend/`.
- [x] Direct frontend dependencies exact-pinned.
- [x] npm lockfile committed as the authoritative dependency graph.
- [x] Supported workflow and Docker build configured to consume the committed lockfile with `npm ci` rather than regenerate resolution.
- [x] Canonical `/workbench/` route implemented through the DTMO origin.
- [x] `/ui/console` retained only as a temporary **compatibility path**.
- [x] Task-oriented primary navigation, top bar and navigation-only command palette implemented.
- [x] Context rail implements explicit no-selection state rather than inferred object truth.
- [x] Dark/light semantic shell tokens and responsive/mobile shell layout implemented.
- [x] Skip link, visible focus, keyboard navigation and reduced-motion handling implemented at shell level.
- [x] Canonical index configured with strict same-origin CSP; hashed assets use immutable caching.
- [x] Node/npm kept in a frontend Docker build stage; only built assets enter the Python runtime image.
- [x] Repository/browser tests and dedicated `Phase 11 Application Shell Gate` added.
- [ ] Final exact-head `npm ci` proves the committed dependency graph is consumed unchanged.
- [ ] Final exact-head frontend production dependency audit is green.
- [ ] Final exact-head TypeScript/Vite build and deterministic asset-hash evidence are green.
- [ ] Final exact-head browser acceptance proves root routing, canonical navigation, command palette, context rail and mobile navigation.
- [ ] Existing container supply-chain, security, accessibility, integration and regression workflows are fully green for the same exact head.
- [ ] All professional current-state, roadmap, QA and evidence documents are synchronized on the final head.
- [ ] Phase 11.10b is merged with expected-head protection only after all registered exact-head workflows are completed/success.

11.10b acceptance permits only **11.10c Command Center** to start.

## 4. Remaining candidate-completion sequence

- [ ] 11.10c Command Center.
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

## 5. Phase 11.10p — production-equivalent validation

The following items remain mandatory but are deliberately deferred until candidate freeze.

### Environment and candidate identity

- [ ] Approved production-equivalent environment identifier recorded.
- [ ] Accountable owner, validation operator and security/release reviewer recorded.
- [ ] Exact deployed 40-character Git commit recorded.
- [ ] Application image recorded by immutable `sha256:` digest.
- [ ] Supporting images recorded by immutable digest where applicable.
- [ ] Expected migration head recorded.
- [ ] GitOps/deployment revision recorded.
- [ ] Exact prior immutable application digest recorded for rollback.
- [ ] Candidate fingerprint calculated before evidence acceptance.
- [ ] No production credential reuse or unsanitized production-data use unless separately authorized.

### Migration and compatibility

- [ ] Forward migration reaches the expected accepted migration head.
- [ ] No duplicate, missing, disconnected or ambiguous migration state is observed.
- [ ] Rolling application/schema overlap remains backward compatible.
- [ ] Destructive schema evolution follows expand/migrate/contract where applicable.
- [ ] Representative read/write behavior succeeds through the exercised transition.
- [ ] Application rollback does not trigger automatic database down migration.

### Upgrade

- [ ] Upgrade from the exact approved prior digest to the candidate digest is exercised.
- [ ] Governed rolling-update behavior preserves readiness/availability as designed.
- [ ] Workload identity, secret delivery, ingress/TLS and service boundaries remain intact.
- [ ] Post-upgrade health/readiness evidence is captured.

### Health and readiness

- [ ] Application health succeeds in the production-equivalent environment.
- [ ] Readiness includes required dependency readiness rather than process liveness only.
- [ ] Representative intended API/UI behavior succeeds, including the accepted Unified Operations Workbench critical journeys.
- [ ] Metrics, logs and audit/correlation remain available to authorized reviewers.

### Saturation and capacity

- [ ] Approved representative workload profile recorded.
- [ ] Latency, error rate, queue/backlog and resource observations captured.
- [ ] Planned capacity/headroom or first constrained resource identified.
- [ ] Degraded behavior is visible and does not fabricate intelligence.
- [ ] Deviations from the capacity envelope are recorded and dispositioned.

### Recovery

- [ ] Approved failure/recovery path exercised.
- [ ] Required stateful dependencies recover according to the exercised design.
- [ ] Data-integrity checks succeed.
- [ ] Observed RPO/RTO recorded where applicable.
- [ ] Post-recovery health/readiness succeeds.
- [ ] Monitoring/audit continuity is reviewed.

### Exact prior-digest rollback

- [ ] Application is rolled back to the exact approved prior immutable digest.
- [ ] Database is not automatically down-migrated.
- [ ] Prior application remains compatible with the retained schema under the accepted Phase 11.9 contract.
- [ ] Post-rollback health/readiness succeeds.
- [ ] Representative read/write behavior succeeds after rollback.

### Evidence consolidation and acceptance

- [ ] All seven required evidence classes are present and `PASS`.
- [ ] Every evidence item uses the same candidate fingerprint and environment.
- [ ] Evidence references point to fresh external evidence rather than repository CI, emulators, design mockups or historical Phase 8/9 records.
- [ ] Validation timestamps and observers are attributable.
- [ ] No unresolved release-blocking finding remains.
- [ ] Deviations are closed or explicitly accepted by an accountable owner.
- [ ] Evidence manifest validates without fail-open exceptions.
- [ ] Referenced evidence has been manually reviewed.
- [ ] Accountable owner records `PASS / OWNER_ACCEPTED`.

## 6. Explicitly deferred until Phase 11.10 acceptance

- [ ] Phase 11.11 fresh independent external assurance against the same immutable candidate.
- [ ] Remediation/retest of any Phase 11.11 release-blocking findings.
- [ ] Phase 12 formal production GO/NO-GO.

## 7. Fail-closed conditions

Phase 11.10 remains blocked if candidate-completion work is incomplete, candidate identity is incomplete, a mutable tag substitutes for an immutable digest, any required 11.10p evidence class is absent or not `PASS`, evidence belongs to another candidate/environment, historical Phase 8/9 evidence is reused, rollback does not restore the exact prior digest, post-rollback health is missing, or release-blocking findings remain unresolved.

Phase 11.10b specifically remains blocked if the committed lockfile cannot be consumed unchanged, the canonical shell/browser gate is not green, a browser path bypasses DTMO server authorization, compatibility routes become parallel feature targets, synthetic operational data is presented as live, or any registered exact-head workflow is incomplete/failed.

## 8. Service and authority boundaries

Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate service/licensing boundaries. Frontend integration, validation execution and automation grant no publication/share, case-handoff or responder authority and do not prove local compromise.

## Current release decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.9 and 11.10a are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 is `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`; 11.10b is active. 11.10c, Phase 11.11 and Phase 12 are `NOT STARTED`. DTMO is not production authorized.**
