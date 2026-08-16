# DTMO Production Readiness Checklist

Last reconciled: **2026-08-16**  
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
| Phase 11.1 | `PASS / REPOSITORY_COMPLETE` | Taranis architecture/contract |
| Phase 11.2 | `PASS / REPOSITORY_COMPLETE` | Taranis canonical adapter |
| Phase 11.3 | `PASS / REPOSITORY_COMPLETE` | IntelOwl enrichment integration |
| Phase 11.4 | `PASS / REPOSITORY_COMPLETE` | OpenCTI contract, adapter and persistence integration |
| Phase 11.5 MISP consolidation contract | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | MISP service/API/licensing/identity/authority contract |
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

## 3. Phase 11.1–11.2 — Taranis

- [x] Service/API/licensing boundary accepted.
- [x] No Taranis source vendoring before licensing approval.
- [x] Canonical read adapter, provenance, checkpointing/reconciliation and governed execution accepted.
- [x] Publication/share authority remains separate.

**Decision:** `PASS / REPOSITORY_COMPLETE`.

## 4. Phase 11.3 — IntelOwl

- [x] Separate AGPL-3.0 service/API boundary accepted.
- [x] Bounded analyzer allowlists and privacy/TLP fail-closed behavior accepted.
- [x] Governed human execution and durable enrichment history accepted.
- [x] No-share/no-local-compromise invariants accepted.

**Decision:** `PASS / REPOSITORY_COMPLETE`.

## 5. Phase 11.4 — OpenCTI

- [x] Service/API/STIX/licensing contract accepted.
- [x] Read-only GraphQL/STIX adapter accepted.
- [x] Stable OpenCTI/STIX identity, markings, confidence and provenance preservation accepted.
- [x] Canonical mapping and immutable reconciliation persistence accepted.
- [x] PostgreSQL-before-checkpoint ordering and replay safety accepted.
- [x] Database no-share/no-local-compromise invariants accepted.
- [x] Exact-head CI and professional documentation accepted.

**Decision:** `PASS / REPOSITORY_COMPLETE`.

## 6. Phase 11.5 — MISP consolidation — active

### Contract slice

- [x] Reviewed MISP v2.5.44 baseline recorded.
- [x] Separate AGPL-3.0 service/API boundary defined; no MISP core source vendoring.
- [x] Existing governed `events/restSearch` inbound and human-approved unpublished `events/add` outbound paths identified as the only initial paths to consolidate.
- [x] Event/attribute/object UUID identity separation defined.
- [x] Distribution, sharing-group and TLP/tag restrictions preserved and non-broadening rule defined.
- [x] Ingestion cannot grant `share_approved`, publication authority or local-compromise proof.
- [x] Human review/share approval remains authoritative for outbound sharing.
- [x] Deterministic replay and uncertain-delivery fail-closed requirements defined.
- [x] Automatic MISP push/pull federation excluded from the contract slice.
- [x] Automatic OpenCTI↔MISP synchronization excluded from the contract slice.
- [x] Architecture, security, QA, evidence, roadmap and portal documentation reconciled.
- [ ] Full exact-head CI matrix green on the final contract head.
- [ ] Professional Documentation Gate green on that same exact head.
- [ ] Contract PR protected-merged with expected-head protection.

### Next bounded implementation slice — only after contract acceptance

- [ ] Single reconciled synchronization-state/persistence model implemented.
- [ ] Inbound identity/revision replay behavior persisted and tested.
- [ ] Outbound reservation/success/uncertain state persisted and tested.
- [ ] Authority enforcement uses existing human approval path rather than a parallel publisher.
- [ ] Operations/runbook and recovery behavior documented and tested.
- [ ] Phase 11.5 reconciled to `PASS / REPOSITORY_COMPLETE` only after all required slices are accepted.

## 7. Phase 11.6 — TheHive

- [ ] Start only after Phase 11.5 repository completion.
- [ ] Controlled intelligence-to-case handoff implemented and audited.
- [ ] Canonical CTI and case-state semantics remain separate.

## 8. Phase 11.7 — Cortex conditional decision

- [ ] IntelOwl capability-gap assessment performed.
- [ ] Cortex remains absent unless a validated gap justifies adoption.

## 9. Phase 11.8 — Integrated runtime industrialisation

- [ ] Kubernetes/Helm/GitOps model accepted.
- [ ] Workload identities/external secrets and TLS/network policy implemented.
- [ ] HA/recovery, observability, SBOM/scanning/signing/attestation accepted.
- [ ] Capacity, upgrade and rollback procedures tested.

## 10. Phase 11.9 — Migration and compatibility

- [ ] Canonical intelligence/provenance/classification/governance migration tested.
- [ ] Existing integration disposition documented with replacement and rollback paths.

## 11. Phase 11.10–11.11 — new validation and assurance

- [ ] One immutable integrated deployment identity established.
- [ ] New production-equivalent validation complete.
- [ ] New independent external assurance complete.
- [ ] Release-blocking findings remediated/retested or formally dispositioned.

## 12. Phase 12 — formal production GO/NO-GO

- [ ] Phase 11 validation and assurance accepted.
- [ ] Production ownership, IAM/secrets/network, recovery, monitoring/support and privacy/legal/governance approvals recorded.
- [ ] Formal accountable `GO` or `NO-GO / BLOCKED` decision recorded.

## Current release decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.4 are repository-complete. Phase 11.5 MISP consolidation contract validation is active. DTMO is not production authorized. Phase 12 is `NOT STARTED`.**
