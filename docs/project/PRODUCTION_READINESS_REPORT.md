# DTMO Production Readiness Report

Assessment date: **2026-08-16**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## 1. Executive conclusion

DTMO completed the repository engineering baseline, accountable functional acceptance, E8.1–E8.10 product evolution, Phase 8 production-equivalent staging acceptance and Phase 9 independent external assurance for the earlier candidate they covered.

Phase 10 concluded with **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

The project is in **Phase 11 — Platform Industrialisation**. Phase 11.1 Taranis architecture/contract, Phase 11.2 Taranis→DTMO canonical adapter, the Phase 11.3 IntelOwl contract and the bounded IntelOwl adapter are `PASS / REPOSITORY_COMPLETE`. The active bounded step is governed IntelOwl execution, durable enrichment-history persistence and operational integration, `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. A new Phase 12 production GO/NO-GO will be considered only after the integrated platform completes fresh Phase 11.10 production-equivalent validation and Phase 11.11 independent external assurance.

## 2. Readiness summary

| Readiness dimension | Current position | Decision |
|---|---|---|
| Engineering / CI | Exact-head engineering baseline accepted through completed slices | `PASS` |
| Functional product | Unified console owner-accepted | `PASS / OWNER_ACCEPTED` |
| E8 vulnerability/CTI scope | Repository-complete | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Production-equivalent validation accepted for prior candidate | `PASS / OWNER_ACCEPTED` |
| Phase 9 | Independent assurance accepted for prior candidate | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | Production authorization decision | `NO-GO / BLOCKED` |
| Phase 11.1 | Taranis architecture/API/licensing boundary | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.2 | Taranis→DTMO canonical adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 contract | IntelOwl service/API/security/licensing contract | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 adapter | Bounded IntelOwl enrichment adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 execution/persistence | Human execution + immutable enrichment history | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 12 | New production authorization decision | `NOT STARTED` |

## 3. Accepted DTMO product baseline

The accepted baseline includes the canonical operator shell across Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance; durable canonical intelligence/provenance; severity/classification and filtering; vulnerability analytics and prioritization; managed RBAC; explicit governance mappings; OpenCVE and CIRCL Vulnerability-Lookup; governed MISP read/export; governed AIL read/enrichment/correlation; and Normenkader IBP SM.07-oriented evidence mapping with explicit semantic boundaries.

Phase 11.2 additionally adds repository-accepted read-only Taranis collection, stable identity/replay, durable checkpointing/reconciliation, bounded detail/CTI retrieval, governed execution, canonical persistence/indexing and connector observability.

The accepted Phase 11.3 adapter adds pre-disclosure observable/TLP/analyzer policy checks, explicit exclusion of IntelOwl external Connectors, bounded polling, immutable job identity, result-size/analyzer validation and explicit partial-success/provenance semantics.

The active execution/persistence slice adds a human `REVIEW_INTELLIGENCE` execution endpoint, a read-only `READ_INTELLIGENCE` history endpoint and migration `0011_intelowl_enrichment_history`. Durable records are linked to canonical intelligence, deduplicated by `(item_id, job_id)`, preserve requesting human and analyzer/job attribution, and are database-constrained so enrichment cannot grant external-share authority or establish local compromise.

The governed UI-01 through UI-10 screenshots remain product documentation illustrations rather than production-state evidence. No new IntelOwl screenshot is promoted because this slice introduces an API/repository workflow rather than a separately accepted GUI surface.

## 4. Phase 10 decision rationale

Production authorization was not granted because the next platform generation should reduce custom implementation of generic OSINT and operations capabilities and adopt mature open-source subsystems behind explicit service boundaries.

The active architecture direction is Taranis AI for collection/assessment, IntelOwl for IOC enrichment, OpenCTI for STIX knowledge graph, MISP for governed exchange, TheHive for case handoff, Cortex only if a validated IntelOwl gap exists, and DTMO for education-sector CTI context, vulnerability prioritization, governance, canonical evidence semantics and governed sharing authority.

## 5. Security and governance posture

DTMO's established invariants remain mandatory through the integration programme: server-side RBAC and least privilege, human/service-principal separation, privileged Administration safeguards, correlation/audit, provenance/confidence preservation, data minimization and separate review/external-share authority.

For governed IntelOwl execution, every requested analyzer is conservatively treated as an external disclosure target. Restricted handling (`red`, `tlp:red`, `review-required`) fails closed before disclosure. The request still sends `connectors_requested=[]`. Unknown analyzers, job-identity mismatches and malformed/oversized results fail closed. Analyzer/provider verdicts remain attributed context and do not become proof of local compromise.

Durable enrichment history is treated as governed intelligence evidence and follows the classification/retention model in `docs/governance/DATA_CLASSIFICATION_RETENTION.md`. Repository CI does not prove production retention, deletion, backup propagation or recovery.

No collector, publisher, enrichment engine, graph platform, case platform, CI result, staging acceptance or production authorization automatically grants external publication/share authority.

## 6. Architecture and licensing impact

The preferred pattern is service-to-service integration rather than source-code merger. No Taranis source is vendored into DTMO under the accepted boundary.

IntelOwl and pyIntelOwl are AGPL-3.0. Phase 11.3 treats them as separate API/service components and does not vendor their source into DTMO. Any future embedding, modification, redistribution or operation of modified network-facing IntelOwl components requires explicit licensing review before architecture acceptance.

The target runtime remains a composed Kubernetes platform with Helm/value-driven configuration and GitOps promotion, hardened with immutable images, external secrets, workload identities, network policies, HA/recovery, observability and supply-chain controls.

## 7. Historical evidence effect

Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the prior accepted candidate. Those decisions remain valid historical evidence.

Because Phase 11 materially changes the platform, that evidence cannot authorize or independently assure the future integrated candidate. New production-equivalent validation in Phase 11.10 and new independent external assurance in Phase 11.11 are required before Phase 12.

## 8. Phase 11 active scope

The detailed programme is defined in `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`.

The current bounded objective is **Phase 11.3 governed IntelOwl execution/persistence exact-head acceptance**. The accepted contract remains `docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md`; `docs/integrations/INTELOWL_INTEGRATION.md` documents the implementation; `docs/security/INTELOWL_TRUST_BOUNDARY.md`, `docs/operations/INTELOWL_ENRICHMENT_RUNBOOK.md`, `docs/user/INTELOWL_ENRICHMENT_WORKFLOW.md` and `docs/qa/PHASE11_3_INTELOWL_GOVERNED_EXECUTION_GATE.md` define the active security, operations, user and QA boundaries.

OpenCTI remains blocked until this exact-head slice is green, merged and Phase 11.3 is reconciled as repository-complete.

## 9. Evidence boundaries

- Repository CI proves repository-controlled engineering claims within test scope.
- Contract/adapter/execution gate success is not live integration or deployment evidence.
- Owner acceptance and external assurance remain separate evidence classes.
- Historical run evidence remains immutable and scoped to the state it covered.
- A materially changed integrated platform requires fresh deployment-bound evidence.
- Restricted security/operational evidence should be referenced rather than copied when sensitive.
- Production authorization does not exist until a future Phase 12 `GO` is explicitly recorded.

## 10. Recommendation

Continue only with Phase 11 priorities in the defined order. Merge the governed IntelOwl execution/persistence slice only on fully green exact-head CI with synchronized professional documentation. Reconcile Phase 11.3 as repository-complete after merge, then start Phase 11.4 OpenCTI. Continue through later Phase 11 steps only after each preceding bounded gate is accepted.
