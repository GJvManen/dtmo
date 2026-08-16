# DTMO Production Readiness Report

Assessment date: **2026-08-16**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## 1. Executive conclusion

DTMO completed the repository engineering baseline, accountable functional acceptance, E8.1–E8.10 product evolution, Phase 8 production-equivalent staging acceptance and Phase 9 independent external assurance for the earlier candidate they covered.

Phase 10 concluded with **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

Phase 11.1–11.2 Taranis and Phase 11.3 IntelOwl are `PASS / REPOSITORY_COMPLETE`. Within Phase 11.4, the OpenCTI contract and bounded read-only GraphQL/STIX adapter are `PASS / REPOSITORY_COMPLETE`. The active bounded step is **OpenCTI canonical mapping/persistence + operational integration**, `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 12 remains dependent on fresh Phase 11.10 production-equivalent validation and Phase 11.11 independent external assurance.

## 2. Readiness summary

| Readiness dimension | Current position | Decision |
|---|---|---|
| Engineering / CI | Exact-head engineering baseline accepted through completed slices | `PASS` |
| Functional product | Unified console owner-accepted | `PASS / OWNER_ACCEPTED` |
| E8 vulnerability/CTI scope | Repository-complete | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Historical production-equivalent validation for prior candidate | `PASS / OWNER_ACCEPTED` |
| Phase 9 | Historical independent assurance for prior candidate | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | Production authorization decision | `NO-GO / BLOCKED` |
| Phase 11.1–11.2 | Taranis architecture + canonical adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 | IntelOwl enrichment integration | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.4 contract | OpenCTI service/API/STIX/identity/security/licensing | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.4 adapter | Read-only GraphQL/STIX identity adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.4 persistence | Canonical mapping/reconciliation/operational integration | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 12 | New production authorization decision | `NOT STARTED` |

## 3. Accepted DTMO product baseline

The accepted baseline includes the canonical operator shell, durable canonical intelligence/provenance, classification/filtering, vulnerability analytics/prioritization, managed RBAC, explicit governance mappings, OpenCVE, CIRCL Vulnerability-Lookup, governed MISP read/export, AIL read/enrichment/correlation and Normenkader IBP SM.07-oriented evidence mapping.

Phase 11.2 adds repository-accepted Taranis collection/canonicalization. Phase 11.3 adds repository-accepted IntelOwl enrichment and durable enrichment history. The accepted OpenCTI read adapter adds bounded GraphQL/STIX retrieval, stable identity/provenance preservation and durable checkpoint semantics.

The governed UI-01 through UI-10 screenshots remain documentation illustrations rather than production-state evidence. No OpenCTI screenshot is promoted because Phase 11.4 adds no accepted operator GUI surface.

## 4. Active Phase 11.4 persistence position

The active slice introduces `opencti_object_mappings` and immutable `opencti_mapping_revisions`. Current mapping state explicitly links a DTMO canonical item to OpenCTI internal identity and STIX identity while preserving entity type, parent types, markings, confidence, timestamps, external references and provenance.

Reconciliation uses SHA-256 canonical snapshot hashes. Unchanged replay is idempotent; changed attributed state adds an immutable revision. OpenCTI/STIX identity drift fails closed rather than being silently merged.

Database constraints enforce `external_share_authorized=false` and `local_compromise_proven=false`. Migration `0012_opencti_mapping_persistence` follows `0011_intelowl_enrichment_history`.

The persistence coordinator commits PostgreSQL before `commit_page(page)` advances the durable cursor. Database failure leaves the checkpoint unchanged; checkpoint failure after database commit remains replay-safe.

## 5. Security and governance posture

DTMO preserves server-side RBAC, least privilege, human/service separation, audit/correlation, provenance/confidence, data minimization and separate human review/external-share authority.

OpenCTI authorization failures, malformed markings/STIX, ambiguous identity mappings and checkpoint corruption fail closed. Administrator or `Bypass all capabilities` privilege is not broadened automatically.

OpenCTI entities, relationships, mappings, revisions and confidence values are attributed CTI context. They do not prove local exposure/exploitability/compromise, establish DTMO severity or grant external publication/share authority.

## 6. Architecture and licensing impact

The preferred pattern remains service-to-service integration rather than source-code merger. IntelOwl/pyIntelOwl remain separate AGPL-3.0 services. OpenCTI Community Edition is Apache-2.0; Enterprise Edition is separately licensed. No OpenCTI source is vendored and Enterprise-only dependencies require explicit entitlement/legal approval.

The target runtime remains a composed Kubernetes platform hardened later in Phase 11.8.

## 7. Historical evidence effect

Phase 8 and Phase 9 remain valid historical evidence for the prior candidate. Because Phase 11 materially changes the platform, those evidence classes cannot authorize or independently assure the future integrated candidate. New Phase 11.10 and 11.11 evidence is mandatory before Phase 12.

## 8. Active scope and documentation

The detailed programme is `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`.

The current bounded objective is the **Phase 11.4 OpenCTI persistence exact-head gate**. Authoritative documents include:

- `docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md`;
- `docs/integrations/OPENCTI_INTEGRATION.md`;
- `docs/operations/OPENCTI_INTEGRATION_RUNBOOK.md`;
- `docs/qa/PHASE11_4_OPENCTI_PERSISTENCE_GATE.md`;
- `docs/security/SECURITY_OVERVIEW.md`;
- `docs/evidence/EVIDENCE_INDEX.md`.

Phase 11.5 MISP consolidation remains blocked until this slice is protected-merged and Phase 11.4 is reconciled to `PASS / REPOSITORY_COMPLETE`.

## 9. Evidence boundaries

- Repository CI proves only repository-controlled engineering claims within test scope.
- Persistence-gate success is not live OpenCTI integration or deployment evidence.
- Owner acceptance and external assurance remain separate evidence classes.
- Historical run evidence remains immutable and scoped to the state it covered.
- Production authorization does not exist until a future Phase 12 `GO` is explicitly recorded.

## 10. Recommendation

Continue only with the active Phase 11.4 persistence PR. Merge it only on fully green exact-head CI with synchronized professional documentation and expected-head protection. After protected acceptance, reconcile Phase 11.4 to repository-complete and start exactly Phase 11.5 MISP consolidation.
