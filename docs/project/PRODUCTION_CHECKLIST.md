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
| Phase 11.6 TheHive handoff contract | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Repository contract/policy evidence |
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

## 4. Phase 11.6 — TheHive — active contract slice

- [x] Reviewed TheHive 5.5.16 baseline recorded.
- [x] Public API v1 (`/api/v1`) selected; deprecated public API v0 excluded.
- [x] TheHive remains a separate StrangeBee service; no upstream source vendoring.
- [x] TheHive 5.3+ Community/Gold/Platinum activation requirement recorded as a deployment prerequisite for continued write operation.
- [x] `POST /api/v1/case` identified only as a future mutation candidate.
- [x] Automatic case creation explicitly excluded.
- [x] Human case-handoff approval defined as separate from DTMO publication/share approval.
- [x] Dedicated server-side RBAC and least-privilege non-human TheHive identity required for later runtime implementation.
- [x] Stable DTMO canonical identity, handoff/idempotency identity, TheHive case identity and organization context required for reconciliation.
- [x] Mutable title/tag/assignee values excluded as identity.
- [x] TLP/PAP/access mappings must preserve the strongest authoritative source restriction.
- [x] Ambiguous mutation delivery blocks blind replay.
- [x] Attachments, raw source bodies, credentials, private enrichment and unrelated personal data excluded by default.
- [x] TheHive case lifecycle explicitly separated from canonical CTI truth, local-compromise proof and DTMO share authority.
- [x] Responders, Cortex execution, automatic MISP→TheHive automation, external sharing and administration excluded.
- [x] Architecture, integration, operations/runbook, security, QA, evidence and roadmap documentation added/reconciled.
- [ ] Dedicated TheHive contract gate green on final exact head.
- [ ] RC4 Quality Gate green on final exact head.
- [ ] Professional Documentation Gate green on final exact head.
- [ ] Contract PR protected-merged with expected-head protection.
- [ ] Phase 11.6 contract reconciled to `PASS / REPOSITORY_COMPLETE` after protected merge.

A later bounded implementation PR must add the minimum human-authorized case-handoff adapter and durable mutation reservation/reconciliation state. Live deployment remains blocked on actual license entitlement, credentials/organization scope, privacy/handling approval and later deployment-bound validation.

## 5. Phase 11.7 — Cortex conditional decision

- [ ] IntelOwl capability-gap assessment performed after Phase 11.6.
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

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.5 are `PASS / REPOSITORY_COMPLETE`. Phase 11.6 TheHive handoff-contract exact-head validation is active. DTMO is not production authorized. Phase 12 is `NOT STARTED`.**
