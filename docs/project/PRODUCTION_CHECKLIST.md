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
| Phase 11.10 production-equivalent validation | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` | Real-environment evidence |
| Phase 11.11 independent external assurance | `NOT STARTED` | Independent assurance |
| Phase 12 | `NOT STARTED` | Future production authorization |

Historical Phase 8/9 evidence remains candidate-bound and is not reused for the materially changed Phase 11 integrated candidate.

## Evidence rules

Repository CI, release signing, accountable acceptance, production-equivalent validation, independent assurance and production authorization are separate evidence classes. Missing mandatory evidence is not implicit acceptance. Sensitive evidence is retained in approved restricted storage rather than committed to Git.

## 1. Accepted baseline

- [x] Phases 1–7 repository engineering baseline.
- [x] RC13 functional owner acceptance (`PASS / OWNER_ACCEPTED`).
- [x] E8.1–E8.10 repository-complete product evolution (`PASS / REPOSITORY_COMPLETE`).
- [x] Historical Phase 8 and Phase 9 evidence preserved in original scope.
- [x] Phase 10 decision remains `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.
- [x] Phase 11.1–11.7b service/integration boundaries accepted.
- [x] Phase 11.8 integrated runtime industrialisation accepted, including workload identity, external secret, ingress/TLS, HA, observability, recovery, supply chain, capacity and upgrade/rollback controls.
- [x] Phase 11.9 migration/compatibility accepted with forward-first and no-automatic-down-migration boundaries.
- [x] Human publication/share authority, separate TheHive case authority, provenance, RBAC, least privilege and fail-closed evidence preserved.

## 2. Active Phase 11.10 — production-equivalent validation

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
- [ ] Representative intended API/UI behavior succeeds.
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
- [ ] Evidence references point to fresh external evidence rather than repository CI, emulators or historical Phase 8/9 records.
- [ ] Validation timestamps and observers are attributable.
- [ ] No unresolved release-blocking finding remains.
- [ ] Deviations are closed or explicitly accepted by an accountable owner.
- [ ] Evidence manifest validates without fail-open exceptions.
- [ ] Referenced evidence has been manually reviewed.
- [ ] Accountable owner records `PASS / OWNER_ACCEPTED`.

## 3. Explicitly deferred until Phase 11.10 acceptance

- [ ] Phase 11.11 fresh independent external assurance against the same immutable candidate.
- [ ] Remediation/retest of any Phase 11.11 release-blocking findings.
- [ ] Phase 12 formal production GO/NO-GO.

## 4. Fail-closed conditions

Phase 11.10 remains blocked if candidate identity is incomplete, a mutable tag substitutes for an immutable digest, any required evidence class is absent or not `PASS`, evidence belongs to another candidate/environment, historical Phase 8/9 evidence is reused, rollback does not restore the exact prior digest, post-rollback health is missing, or release-blocking findings remain unresolved.

## 5. Service and authority boundaries

Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate service/licensing boundaries. Validation execution grants no publication/share, case-handoff or responder authority and does not prove local compromise.

## Current release decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.9 are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 is `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`. Phase 11.11 and Phase 12 are `NOT STARTED`. DTMO is not production authorized.**
