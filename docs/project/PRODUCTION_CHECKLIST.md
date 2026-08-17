# DTMO Production Readiness Checklist

Last reconciled: **2026-08-17**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

This checklist is the high-level control for the post-Phase-10 industrialisation programme and the future Phase 12 production authorization decision.

## Current lifecycle status

| Stage | Status | Evidence class |
|---|---|---|
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` | Repository-controlled product evolution |
| Phase 8 | `PASS / OWNER_ACCEPTED` | Historical accountable staging acceptance |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` | Historical independent assurance |
| Phase 10 | `NO-GO / BLOCKED` | Accountable production decision |
| Phase 11 | `IN PROGRESS / ACTIVE` | Platform industrialisation |
| Phase 11.1–11.5 | `PASS / REPOSITORY_COMPLETE` | Accepted Taranis, IntelOwl, OpenCTI and MISP boundaries |
| Phase 11.6 TheHive contract | `PASS / REPOSITORY_COMPLETE` | Accepted repository service/API/authority contract |
| Phase 11.6 TheHive implementation | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Repository adapter/state evidence |
| Phase 12 | `NOT STARTED` | Future production authorization |

Historical Phase 8/9 evidence remains candidate-bound and is not reused for the materially changed Phase 11 integrated candidate.

## Evidence rules

Repository CI, accountable acceptance, production-equivalent validation, independent assurance and production authorization are separate evidence classes. Missing mandatory evidence is not implicit acceptance.

## 1. Accepted historical baseline

- [x] Phases 1–7 repository engineering baseline.
- [x] RC13 functional owner acceptance.
- [x] E8.1–E8.10 repository-complete product evolution.
- [x] Phase 8 acceptance for the earlier candidate.
- [x] Phase 9 independent assurance for the earlier candidate.

## 2. Phase 10 production decision

- [x] Accountable decision recorded as `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.
- [x] Production authorization denied.
- [x] Phase 11 successor programme active.

## 3. Phase 11.1–11.5 accepted integration baseline

- [x] Taranis service/API/licensing boundary and canonical adapter accepted.
- [x] IntelOwl bounded enrichment integration accepted.
- [x] OpenCTI graph contract, adapter and persistence integration accepted.
- [x] MISP consolidation contract and synchronization-state/authority implementation accepted.
- [x] Human publication/share authority remains separate from integrated service identities.
- [x] Historical Phase 8/9 evidence remains candidate-bound.

**Decision:** `PASS / REPOSITORY_COMPLETE`.

## 4. Phase 11.6 — TheHive

### Contract baseline

- [x] TheHive 5.5.16/API v1 baseline recorded.
- [x] Separate StrangeBee service and deployment-specific licensing boundary accepted.
- [x] Human case-handoff authority separated from publication/share authority.
- [x] Stable DTMO↔TheHive identity, fail-closed handling, data minimization and no-blind-replay contract accepted.
- [x] Responders, Cortex, automatic MISP→TheHive, external sharing and administration excluded.
- [x] Contract PR protected-merged with expected-head protection.

**Decision:** `PASS / REPOSITORY_COMPLETE`.

### Active bounded handoff implementation

- [x] Dedicated `handoff:case` permission implemented and kept separate from `approve:share`.
- [x] Service accounts excluded from human handoff authority.
- [x] `POST /api/v1/case` is the only accepted external mutation.
- [x] Feature disabled by default.
- [x] Canonical item and repository provenance required before mutation.
- [x] Deterministic severity/TLP/PAP mapping implemented; unknown values fail closed.
- [x] Requested TLP cannot broaden a known authoritative TLP tag.
- [x] Authoritative MISP distribution/sharing-group restrictions block handoff until a deployment-approved TheHive access mapping exists.
- [x] Payload minimized to approved case fields; attachments/raw bodies/credentials/private enrichment/unrelated personal data excluded.
- [x] Migration `0014_thehive_handoff_state` added after `0013_misp_synchronization_state`.
- [x] Durable reservation committed before external mutation.
- [x] Stable request/item/case/organization identities persisted.
- [x] `reserved`, `delivered`, `ambiguous`, `failed` states implemented.
- [x] Timeout/network/malformed-success identity becomes `ambiguous` and blocks blind replay.
- [x] Persisted delivered outcome minimized to case identity, case number and organization.
- [x] Database constraints enforce no external-share authority and no local-compromise proof.
- [x] Production configuration requires HTTPS, runtime token and explicit organization when feature-enabled.
- [x] Architecture, integration, operations, security, user/admin, QA, evidence, roadmap and portal documentation reconciled.
- [ ] Dedicated TheHive Handoff Implementation Gate green on final exact head.
- [ ] RC4 Quality Gate green on final exact head.
- [ ] Professional Documentation Gate green on final exact head.
- [ ] Implementation PR protected-merged with expected-head protection.
- [ ] Phase 11.6 reconciled to `PASS / REPOSITORY_COMPLETE` after protected merge.

Live deployment remains blocked on actual Community/Gold/Platinum entitlement, effective runtime credentials/service permissions, organization scope, privacy/handling approval and later deployment-bound validation.

## 5. Phase 11.7 — Cortex conditional decision

- [ ] IntelOwl capability-gap assessment performed only after Phase 11.6 acceptance.
- [ ] Cortex remains absent unless a validated gap justifies adoption.

## 6. Phase 11.8 — Integrated runtime industrialisation

- [ ] Kubernetes/Helm/GitOps model accepted.
- [ ] Workload identities/external secrets and TLS/network policy implemented.
- [ ] HA/recovery, observability, SBOM/scanning/signing/attestation accepted.
- [ ] Capacity, upgrade and rollback procedures tested.

## 7. Phase 11.9 — Migration and compatibility

- [ ] Canonical intelligence/provenance/classification/governance migration tested.
- [ ] Existing integration disposition documented with replacement and rollback paths.

## 8. Phase 11.10–11.11 — new validation and assurance

- [ ] One immutable integrated deployment identity established.
- [ ] New production-equivalent validation complete.
- [ ] New independent external assurance complete.
- [ ] Release-blocking findings remediated/retested or formally dispositioned.

## 9. Phase 12 — formal production GO/NO-GO

- [ ] Phase 11 validation and assurance accepted.
- [ ] Production ownership, IAM/secrets/network, recovery, monitoring/support and privacy/legal/governance approvals recorded.
- [ ] Formal accountable `GO` or `NO-GO / BLOCKED` decision recorded.

## Current release decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.5 and the Phase 11.6 contract are `PASS / REPOSITORY_COMPLETE`. The Phase 11.6 bounded TheHive handoff implementation is in exact-head validation. DTMO is not production authorized. Phase 12 is `NOT STARTED`.**
