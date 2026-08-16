# DTMO Production Readiness Report

Assessment date: **2026-08-16**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## 1. Executive conclusion

DTMO completed the repository engineering baseline, accountable functional acceptance, E8.1–E8.10 product evolution, Phase 8 production-equivalent staging acceptance and Phase 9 independent external assurance for the earlier candidate they covered.

Phase 10 concluded with **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

Phase 11.1–11.2 Taranis and Phase 11.3 IntelOwl are `PASS / REPOSITORY_COMPLETE`. The active bounded step is **Phase 11.4 OpenCTI service/API/STIX/data-model/identity/security/licensing contract validation**, `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. A future Phase 12 production decision remains dependent on fresh Phase 11.10 production-equivalent validation and Phase 11.11 independent external assurance for the materially changed integrated candidate.

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
| Phase 11.4 contract | OpenCTI service/API/STIX/identity/security/licensing | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 12 | New production authorization decision | `NOT STARTED` |

## 3. Accepted DTMO product baseline

The accepted baseline includes the canonical operator shell, durable canonical intelligence/provenance, classification/filtering, vulnerability analytics/prioritization, managed RBAC, explicit governance mappings, OpenCVE, CIRCL Vulnerability-Lookup, governed MISP read/export, AIL read/enrichment/correlation and Normenkader IBP SM.07-oriented evidence mapping.

Phase 11.2 adds repository-accepted Taranis collection/canonicalization with stable identity, replay, durable checkpointing/reconciliation, detail/CTI retrieval, governed execution and observability.

Phase 11.3 adds repository-accepted IntelOwl enrichment with pre-disclosure policy checks, bounded job execution, immutable job identity, explicit partial success, human `REVIEW_INTELLIGENCE` execution, durable enrichment history and no-share/no-local-compromise invariants.

The governed UI-01 through UI-10 screenshots remain documentation illustrations rather than production-state evidence. No OpenCTI screenshot is promoted for the contract slice because no accepted OpenCTI operator surface exists yet.

## 4. Phase 11.4 OpenCTI architecture position

OpenCTI is designated as the separate STIX knowledge-graph service; DTMO remains authoritative for education-sector relevance, vulnerability/local-exposure semantics, governance, review and publication/share authority.

The contract reviews OpenCTI `7.260811.0`, distinguishes Community Edition Apache-2.0 from separately licensed Enterprise Edition functionality, and bounds GraphQL, STIX 2.1, TAXII 2.1 and access-controlled stream interfaces.

A dedicated non-human OpenCTI identity must use minimum capabilities and only required markings. OpenCTI/STIX identities remain distinct from DTMO canonical UUIDs and are mapped with markings/TLP/PAP, confidence, source references, timestamps and provenance.

The first adapter after contract acceptance is read-oriented. Connector registration, MISP synchronization, arbitrary GraphQL mutation, external enrichment, TheHive case creation, report publication and security/marking administration are outside the initial boundary.

## 5. Security and governance posture

DTMO preserves server-side RBAC, least privilege, human/service separation, privileged-action safeguards, audit/correlation, provenance/confidence, data minimization and separate human review/external-share authority.

OpenCTI `401`/`403`, unknown markings and malformed/unsupported STIX fail closed. Administrator or `Bypass all capabilities` privilege is not broadened automatically to make an integration succeed. Future pagination/stream processing must be restart-safe and idempotent, advancing durable cursor/checkpoint state only after accepted persistence.

OpenCTI entities, relationships, confidence and graph presence are attributed CTI context. They do not prove local exposure/exploitability/compromise, establish DTMO severity or grant external publication/share authority.

## 6. Architecture and licensing impact

The preferred pattern is service-to-service integration rather than source-code merger. Taranis source is not vendored into DTMO. IntelOwl/pyIntelOwl remain separate AGPL-3.0 services.

OpenCTI Community Edition is Apache-2.0; OpenCTI Enterprise Edition is subject to a separate license. The Phase 11.4 contract does not vendor OpenCTI source and does not authorize Enterprise Edition-only dependencies without explicit entitlement/legal approval.

The target runtime remains a composed Kubernetes platform with Helm/value-driven configuration and GitOps promotion, hardened later in Phase 11.8.

## 7. Historical evidence effect

Phase 8 and Phase 9 remain valid historical evidence for the prior candidate. Because Phase 11 materially changes the platform, those evidence classes cannot authorize or independently assure the future integrated candidate. New Phase 11.10 and 11.11 evidence is mandatory before Phase 12.

## 8. Active scope and documentation

The detailed programme is `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`.

The current bounded objective is the **Phase 11.4 OpenCTI contract exact-head gate**. Authoritative documents include:

- `docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md`;
- `docs/integrations/OPENCTI_INTEGRATION.md`;
- `docs/operations/OPENCTI_INTEGRATION_RUNBOOK.md`;
- `docs/qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md`;
- `docs/security/SECURITY_OVERVIEW.md`.

After protected acceptance, the next bounded PR is the read-only OpenCTI STIX/identity adapter with pagination/reconciliation and provenance preservation. Phase 11.5 MISP consolidation remains blocked until Phase 11.4 is repository-complete.

## 9. Evidence boundaries

- Repository CI proves only repository-controlled engineering claims within test scope.
- Contract gate success is not live OpenCTI integration or deployment evidence.
- Owner acceptance and external assurance remain separate evidence classes.
- Historical run evidence remains immutable and scoped to the state it covered.
- A materially changed integrated platform requires fresh deployment-bound evidence.
- Production authorization does not exist until a future Phase 12 `GO` is explicitly recorded.

## 10. Recommendation

Continue only with the active Phase 11.4 contract PR. Merge it only on fully green exact-head CI with synchronized professional documentation and expected-head protection. Then begin exactly one bounded read-only OpenCTI adapter PR. Do not start Phase 11.5 before Phase 11.4 repository completion.
