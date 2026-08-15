# DTMO Production Readiness Checklist

Last reconciled: **2026-08-15**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8 repository enhancements**

This checklist is the high-level control for the post-Phase-10 industrialisation programme and the future Phase 12 production authorization decision.

## Current lifecycle status

| Stage | Status | Evidence class |
|---|---|---|
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` | Repository-controlled product evolution |
| Phase 8 | `PASS / OWNER_ACCEPTED` | Accountable production-equivalent staging acceptance |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` | Independent external assurance |
| Phase 10 | `NO-GO / BLOCKED` | Accountable production decision |
| Phase 11 | `IN PROGRESS / ACTIVE` | Platform industrialisation |
| Phase 12 | `NOT STARTED` | Future production authorization |

The accepted Phase 8 and Phase 9 evidence remains scoped to the candidate it originally covered. It is historical prerequisite evidence for the industrialisation decision and must not be reused as production-equivalent validation or independent assurance for the materially changed Phase 11 integrated candidate.

## Evidence rules

A checklist item is complete only when its required evidence exists, is attributable and is reviewable. Repository CI, accountable acceptance, production-equivalent validation, independent assurance and production authorization are separate evidence classes. Historical evidence remains immutable and scoped to the state/deployment it actually covered.

## 1. Accepted historical baseline

- [x] Phases 1–7 repository engineering baseline.
- [x] RC13 functional owner acceptance.
- [x] E8.1–E8.10 repository-complete product evolution.
- [x] Phase 8 production-equivalent validation and accountable acceptance.
- [x] Phase 9 independent external assurance.

**Decision:** historical prerequisites remain accepted for the candidate they covered.

## 2. Phase 10 production decision

- [x] Accountable production decision recorded.
- [x] Production authorization denied for the current candidate.
- [x] Successor programme identified.

**Decision:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.

## 3. Phase 11.1 — Taranis AI architecture and gap assessment

- [x] Initial responsibility-boundary assessment created.
- [x] Keep / Integrate / Replace / Deprecate / Migrate capability matrix created.
- [x] Service-to-service integration is the default architecture.
- [x] Licensing boundary recorded: no Taranis source vendoring before review.
- [ ] Exact Taranis REST/OpenAPI endpoint inventory completed.
- [ ] Source/news/story/report schema mapping completed.
- [ ] Stable identifiers, replay and deduplication rules completed.
- [ ] Authentication/service-account/least-privilege model completed.
- [ ] Provenance, TLP and classification transformation rules completed.
- [ ] Polling versus SSE/event boundary decided.
- [ ] Duplicated DTMO generic collection functions identified for deprecation.
- [ ] Integration threat-model abuse cases completed.
- [ ] Licensing guidance for service integration/redistribution accepted.
- [ ] Phase 11.2 adapter contracts and rollback criteria accepted.

**Decision:** Phase 11.1 `IN PROGRESS / ACTIVE`.

## 4. Phase 11.2 — Taranis → DTMO canonical adapter

- [ ] API client/service identity implemented.
- [ ] News/source/story/report mapping implemented.
- [ ] Idempotency/replay/deduplication tested.
- [ ] Provenance and evidence retention tested.
- [ ] TLP/classification fail-closed handling tested.
- [ ] Degraded/partial failure behavior tested.
- [ ] Publishing authority remains separate from ingestion.
- [ ] Migration/rollback path tested.

## 5. Phase 11.3 — IntelOwl

- [ ] Dedicated service identity/token and TLS policy approved.
- [ ] CVE/IP/domain/URL/hash enrichment integrated.
- [ ] Email enrichment disabled unless privacy scope is explicitly approved.
- [ ] Analyzer identity/raw-result provenance retained.
- [ ] Rate-limit/quota/timeout/failure handling tested.
- [ ] Enrichment cannot be misrepresented as local exposure or compromise.

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

**Phase 10 is `NO-GO / BLOCKED`. Phase 11 is `IN PROGRESS / ACTIVE`. DTMO is not production authorized. Phase 12 is `NOT STARTED`.**