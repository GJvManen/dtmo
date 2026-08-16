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
| Phase 11.4 OpenCTI contract | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | OpenCTI service/API/STIX/identity/security/licensing contract |
| Phase 12 | `NOT STARTED` | Future production authorization |

The accepted Phase 8 and Phase 9 evidence remains scoped to the candidate it originally covered and is not reused for the materially changed Phase 11 integrated candidate.

## Evidence rules

A checklist item is complete only when its required evidence exists, is attributable and is reviewable. Repository CI, accountable acceptance, production-equivalent validation, independent assurance and production authorization are separate evidence classes. Historical evidence remains immutable.

## 1. Accepted historical baseline

- [x] Phases 1–7 repository engineering baseline.
- [x] RC13 functional owner acceptance.
- [x] E8.1–E8.10 repository-complete product evolution.
- [x] Phase 8 production-equivalent validation and accountable acceptance for the earlier candidate.
- [x] Phase 9 independent external assurance for the earlier candidate.

## 2. Phase 10 production decision

- [x] Accountable production decision recorded.
- [x] Production authorization denied.
- [x] Phase 11 successor programme identified.

**Decision:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.

## 3. Phase 11.1–11.2 — Taranis

- [x] Responsibility/service/licensing contract accepted.
- [x] No Taranis source vendoring before licensing approval.
- [x] Read-only canonical adapter implemented.
- [x] Stable identity, provenance and fail-closed TLP handling implemented.
- [x] Durable checkpointing/reconciliation and bounded pagination implemented.
- [x] Detail/CTI retrieval and governed execution integrated.
- [x] Canonical persistence/indexing and observability integrated.
- [x] Publication/share authority remains separate.
- [x] Exact-head CI and professional documentation accepted.

**Decision:** Phase 11.1 and 11.2 `PASS / REPOSITORY_COMPLETE`.

## 4. Phase 11.3 — IntelOwl

- [x] IntelOwl v6.7.0 contract/API/licensing baseline accepted.
- [x] Separate service/API boundary; no IntelOwl source vendored.
- [x] Dedicated non-admin identity, runtime-secret token and production TLS boundary accepted.
- [x] Observable/analyzer allowlists and privacy/TLP fail-closed controls implemented.
- [x] External IntelOwl Connectors excluded from the enrichment path.
- [x] Bounded job execution, immutable job identity and result validation implemented.
- [x] Unknown/malformed/oversized result handling fails closed.
- [x] Partial-success state and provenance preserved.
- [x] Governed human `REVIEW_INTELLIGENCE` execution endpoint implemented.
- [x] Durable enrichment-history persistence and read-only history access implemented.
- [x] Database constraints preserve no-share/no-local-compromise invariants.
- [x] Exact-head CI and professional documentation accepted.

**Decision:** Phase 11.3 `PASS / REPOSITORY_COMPLETE`.

## 5. Phase 11.4 — OpenCTI contract — active

- [x] Official OpenCTI `7.260811.0` baseline inspected and recorded.
- [x] Community Edition Apache-2.0 and separate Enterprise Edition licensing distinction recorded.
- [x] Service/API boundary defined; no OpenCTI source vendoring authorized.
- [x] GraphQL, STIX 2.1, TAXII 2.1 and access-controlled stream surfaces bounded.
- [x] Dedicated least-privilege non-human identity model defined.
- [x] Administrator/`Bypass all capabilities` and connector privileges excluded from routine integration.
- [x] OpenCTI/STIX and DTMO canonical identity domains explicitly separated/mapped.
- [x] Marking/TLP/PAP, confidence and provenance preservation rules defined.
- [x] Unknown/malformed marking and STIX semantics fail closed.
- [x] Restart-safe pagination/stream replay and checkpoint requirements defined.
- [x] Connector/MISP/enrichment/case/publication side effects excluded from the first path.
- [x] Graph context cannot grant DTMO publication/share authority or prove local compromise.
- [x] Architecture, integration, security, operations, QA, evidence and roadmap documentation updated.
- [ ] Full exact-head CI matrix green on the final OpenCTI contract head.
- [ ] Professional Documentation Gate green on that same exact head.
- [ ] Contract PR protected-merged with expected-head protection.

### Next Phase 11.4 slice — only after contract merge

- [ ] Read-only OpenCTI STIX/identity adapter implemented.
- [ ] Bounded pagination/reconciliation and durable checkpointing implemented.
- [ ] Provenance/confidence/marking preservation tested against synthetic contracts.
- [ ] Operational failure/replay behavior documented and tested.

## 6. Phase 11.5 — MISP consolidation

- [ ] One authoritative inbound synchronization model accepted.
- [ ] Conflict/replay handling tested.
- [ ] DTMO governed outbound approval remains authoritative.
- [ ] Distribution/TLP/sharing-group handling remains fail-closed.
- [ ] Automated components cannot gain implicit external-share authority.

## 7. Phase 11.6 / 11.7 — TheHive and conditional Cortex

- [ ] TheHive intelligence-to-case handoff implemented and audited.
- [ ] Canonical CTI and case-state semantics remain separate.
- [ ] Cortex need explicitly assessed.
- [ ] Cortex remains absent unless a validated IntelOwl gap justifies it.

## 8. Phase 11.8 — Integrated runtime industrialisation

- [ ] Kubernetes deployment model accepted.
- [ ] Helm/value-driven configuration accepted.
- [ ] GitOps promotion model accepted.
- [ ] Immutable images/digests enforced.
- [ ] External secrets/rotation and workload identity implemented.
- [ ] Network policies/TLS ingress implemented.
- [ ] PostgreSQL HA/recovery objectives tested.
- [ ] Redis durability/HA appropriate to queue semantics tested.
- [ ] Durable evidence/object storage tested.
- [ ] Central logging/audit/metrics/alerting tested.
- [ ] SBOM/scanning/signing/attestation gates accepted.
- [ ] Capacity, upgrade and rollback procedures tested.

## 9. Phase 11.9 — Migration and compatibility

- [ ] Canonical intelligence/source/provenance/classification/governance migration tested.
- [ ] Existing E8 integration disposition documented.
- [ ] User/role mapping dispositioned.
- [ ] Every deprecation has a replacement and rollback path.

## 10. Phase 11.10–11.11 — new validation and assurance

- [ ] Integrated candidate bound to one immutable deployment identity.
- [ ] New production-equivalent validation complete.
- [ ] New independent external assurance complete.
- [ ] Release-blocking findings remediated/retested or formally dispositioned.
- [ ] Residual risk accepted.

## 11. Phase 12 — formal production GO/NO-GO

- [ ] Phase 11 validation and external assurance accepted.
- [ ] Production environment/owner/support approved.
- [ ] Production IAM/secrets/network approved.
- [ ] Backup/recovery/rollback approved.
- [ ] Monitoring/on-call/incident-response handover approved.
- [ ] Privacy/data/legal/governance approval recorded.
- [ ] Change/release authorization and immutable production identity recorded.
- [ ] Formal accountable `GO` or `NO-GO / BLOCKED` decision recorded.

## Current release decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.3 are repository-complete. The Phase 11.4 OpenCTI contract is the active exact-head gate. DTMO is not production authorized. Phase 12 is `NOT STARTED`.**
