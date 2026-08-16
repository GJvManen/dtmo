# DTMO Production Readiness Checklist

Last reconciled: **2026-08-16**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

This checklist is the high-level control for the post-Phase-10 industrialisation programme and the future Phase 12 production authorization decision.

## Current lifecycle status

| Stage | Status | Evidence class |
|---|---|---|
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` | Repository-controlled product evolution |
| Phase 8 | `PASS / OWNER_ACCEPTED` | Accountable production-equivalent staging acceptance |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` | Independent external assurance |
| Phase 10 | `NO-GO / BLOCKED` | Accountable production decision |
| Phase 11 | `IN PROGRESS / ACTIVE` | Platform industrialisation |
| Phase 11.1 | `PASS / REPOSITORY_COMPLETE` | Taranis architecture/contract |
| Phase 11.2 | `PASS / REPOSITORY_COMPLETE` | Taranis canonical adapter |
| Phase 11.3 contract | `PASS / REPOSITORY_COMPLETE` | IntelOwl service/API/security/licensing contract |
| Phase 11.3 adapter | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Bounded IntelOwl adapter |
| Phase 12 | `NOT STARTED` | Future production authorization |

The accepted Phase 8 and Phase 9 evidence remains scoped to the candidate it originally covered. It must not be reused as production-equivalent validation or independent assurance for the materially changed Phase 11 integrated candidate.

## Evidence rules

A checklist item is complete only when its required evidence exists, is attributable and is reviewable. Repository CI, accountable acceptance, production-equivalent validation, independent assurance and production authorization are separate evidence classes. Historical evidence remains immutable and scoped to the state/deployment it actually covered.

## 1. Accepted historical baseline

- [x] Phases 1–7 repository engineering baseline.
- [x] RC13 functional owner acceptance.
- [x] E8.1–E8.10 repository-complete product evolution.
- [x] Phase 8 production-equivalent validation and accountable acceptance.
- [x] Phase 9 independent external assurance.

## 2. Phase 10 production decision

- [x] Accountable production decision recorded.
- [x] Production authorization denied for the current candidate.
- [x] Successor programme identified.

**Decision:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.

## 3. Phase 11.1 — Taranis AI architecture and gap assessment

- [x] Responsibility boundary, capability matrix and service-to-service architecture accepted.
- [x] API/data-model/identity/RBAC/provenance/TLP/reconciliation contract accepted.
- [x] Licensing boundary recorded: no Taranis source vendoring before review.
- [x] Phase 11.2 acceptance criteria accepted.

**Decision:** Phase 11.1 `PASS / REPOSITORY_COMPLETE`.

## 4. Phase 11.2 — Taranis → DTMO canonical adapter

- [x] Read-only API client/service identity implemented.
- [x] News/story and detail/CTI mapping implemented.
- [x] Idempotency/replay/deduplication tested.
- [x] Durable checkpointing and bounded reconciliation tested.
- [x] Provenance and evidence retention tested.
- [x] TLP/classification fail-closed handling tested.
- [x] Governed scheduler/manual execution integrated.
- [x] Canonical persistence/indexing and connector observability integrated.
- [x] Publishing/share authority remains separate from ingestion.
- [x] Final exact-head CI and professional documentation gates passed.

**Decision:** Phase 11.2 `PASS / REPOSITORY_COMPLETE`. Live production-equivalent evidence remains future Phase 11.10 work.

## 5. Phase 11.3 — IntelOwl

### Contract gate — accepted

- [x] Official IntelOwl v6.7.0 baseline inspected and referenced.
- [x] Service-to-service/API boundary documented; no IntelOwl source vendored.
- [x] Dedicated non-admin service identity/token model documented.
- [x] TLS verification outside local development required.
- [x] Approved observable scope limited to CVE/IP/domain/URL/hash.
- [x] Email/generic personal data disabled pending explicit privacy/data-processing approval.
- [x] Explicit analyzer/playbook allowlisting required.
- [x] Analyzer/job/result provenance contract defined.
- [x] Rate-limit/quota/timeout/failure semantics defined.
- [x] TLP/privacy and external-disclosure controls defined.
- [x] IntelOwl external Connectors excluded from the initial enrichment path.
- [x] Enrichment cannot be represented as local exposure/compromise proof.
- [x] AGPL-3.0 service-boundary and licensing-review trigger recorded.
- [x] Exact-head contract CI and Professional Documentation Gate accepted.

**Decision:** Phase 11.3 contract `PASS / REPOSITORY_COMPLETE`.

### Adapter implementation — active exact-head gate

- [x] Runtime configuration and secret-backed API token implemented.
- [x] Production HTTPS and explicit analyzer allowlist enforced.
- [x] Approved observable/analyzer policy enforced before disclosure.
- [x] `connectors_requested=[]` prevents IntelOwl external Connector side effects in this path.
- [x] Bounded job submission and polling implemented.
- [x] Immutable upstream job-ID correlation enforced.
- [x] Analyzer identity/result provenance retained in normalized output.
- [x] Partial-success semantics implemented.
- [x] `429`/timeout/failure behavior covered by synthetic tests.
- [x] Unknown analyzer and malformed/oversized result handling fail closed.
- [x] Normalized authority metadata preserves no-share/no-local-compromise semantics.
- [ ] Full exact-head CI matrix green on the adapter head.
- [ ] Professional Documentation Gate green on that same exact head.

### Governed execution/persistence — next only after adapter merge

- [ ] Governed execution entry point and RBAC authorization integrated.
- [ ] Durable enrichment-history persistence implemented.
- [ ] Operational metrics/alerting/runbook state integrated.
- [ ] User/admin documentation updated if an operator-visible surface is introduced.
- [ ] Governed screenshot/visual added only if a real accepted operator surface exists.

## 6. Phase 11.4 — OpenCTI

- [ ] STIX 2.x import/export boundary implemented.
- [ ] Entity identity/deduplication policy accepted.
- [ ] ATT&CK and CTI relationship mapping tested.
- [ ] Provenance/confidence/marking preserved.
- [ ] DTMO does not duplicate a separate graph engine.

## 7. Phase 11.5 — MISP consolidation

- [ ] One authoritative inbound synchronization model accepted.
- [ ] Conflict/replay handling tested.
- [ ] DTMO governed outbound approval remains authoritative.
- [ ] Distribution/TLP/sharing-group handling remains fail-closed.
- [ ] Automated collectors/publishers cannot gain implicit external-share authority.

## 8. Phase 11.6 / 11.7 — TheHive and conditional Cortex

- [ ] TheHive intelligence-to-case handoff implemented and audited.
- [ ] Canonical CTI and case-state semantics remain separate.
- [ ] Cortex need explicitly assessed.
- [ ] Cortex remains absent unless a validated IntelOwl gap justifies it.

## 9. Phase 11.8 — Integrated runtime industrialisation

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

## 10. Phase 11.9 — Migration and compatibility

- [ ] Canonical intelligence migration tested.
- [ ] Source/catalog migration tested.
- [ ] Provenance/confidence/classification migration tested.
- [ ] Governance mappings preserved.
- [ ] MISP/AIL/OpenCVE/Vulnerability-Lookup compatibility dispositioned.
- [ ] User/role mapping dispositioned.
- [ ] Every deprecation has a replacement and rollback path.

## 11. Phase 11.10–11.11 — new validation and assurance

- [ ] Integrated candidate bound to one immutable deployment identity.
- [ ] New production-equivalent validation complete.
- [ ] New independent external assurance complete.
- [ ] Release-blocking findings remediated/retested or formally dispositioned.
- [ ] Residual risk accepted.

## 12. Phase 12 — formal production GO/NO-GO

- [ ] Phase 11 validation and external assurance accepted.
- [ ] Production environment/owner/support approved.
- [ ] Production IAM/secrets/network approved.
- [ ] Backup/recovery/rollback approved.
- [ ] Monitoring/on-call/incident-response handover approved.
- [ ] Privacy/data/legal/governance approval recorded.
- [ ] Change/release authorization and immutable production identity recorded.
- [ ] Formal accountable `GO` or `NO-GO / BLOCKED` decision recorded.

## Current release decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1 and 11.2 are repository-complete. The Phase 11.3 IntelOwl contract is repository-complete and the adapter is the active exact-head gate. DTMO is not production authorized. Phase 12 is `NOT STARTED`.**
