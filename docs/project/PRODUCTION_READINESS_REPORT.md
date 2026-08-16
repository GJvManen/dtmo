# DTMO Production Readiness Report

Assessment date: **2026-08-16**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## 1. Executive conclusion

DTMO completed the repository engineering baseline, accountable functional acceptance, E8.1–E8.10 product evolution, Phase 8 production-equivalent staging acceptance and Phase 9 independent external assurance for the earlier candidate they covered.

Phase 10 concluded with **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

The project is in **Phase 11 — Platform Industrialisation**. Phase 11.1 Taranis architecture/contract and Phase 11.2 Taranis→DTMO canonical adapter are `PASS / REPOSITORY_COMPLETE`. The active bounded step is **Phase 11.3 IntelOwl enrichment integration**, beginning with contract acceptance before adapter implementation. A new Phase 12 production GO/NO-GO will be considered only after the integrated platform completes new production-equivalent validation and independent external assurance.

## 2. Readiness summary

| Readiness dimension | Current position | Decision |
|---|---|---|
| Engineering / CI | Exact-head engineering baseline accepted | `PASS` |
| Functional product | Unified console owner-accepted | `PASS / OWNER_ACCEPTED` |
| E8 vulnerability/CTI scope | Repository-complete | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Production-equivalent validation accepted for prior candidate | `PASS / OWNER_ACCEPTED` |
| Phase 9 | Independent assurance accepted for prior candidate | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | Production authorization decision | `NO-GO / BLOCKED` |
| Phase 11.1 | Taranis architecture/API/licensing boundary | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.2 | Taranis→DTMO canonical adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 | IntelOwl enrichment integration | `IN PROGRESS / CONTRACT BASELINE IN EXACT-HEAD VALIDATION` |
| Phase 12 | New production authorization decision | `NOT STARTED` |

## 3. Accepted DTMO product baseline

The accepted baseline includes the canonical operator shell across Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance; durable canonical intelligence/provenance; severity/classification and filtering; vulnerability analytics and prioritization; managed RBAC; explicit governance mappings; OpenCVE and CIRCL Vulnerability-Lookup; governed MISP read/export; governed AIL read/enrichment/correlation; and Normenkader IBP SM.07-oriented evidence mapping with explicit semantic boundaries.

Phase 11.2 additionally adds repository-accepted read-only Taranis collection, stable identity/replay, durable checkpointing/reconciliation, bounded detail/CTI retrieval, governed execution, canonical persistence/indexing and connector observability. This remains repository evidence, not live production-equivalent proof.

The governed UI-01 through UI-10 screenshots remain product documentation illustrations rather than production-state evidence.

## 4. Phase 10 decision rationale

Production authorization was not granted because the next platform generation should reduce custom implementation of generic OSINT and operations capabilities and adopt mature open-source subsystems behind explicit service boundaries.

The active architecture direction is:

- **Taranis AI** — repository-integrated OSINT collection, analyst assessment and structured reporting;
- **IntelOwl** — active generic IOC enrichment target;
- **OpenCTI** — STIX knowledge graph;
- **MISP** — consolidated governed exchange;
- **TheHive** — incident/case handoff;
- **Cortex** — conditional only where IntelOwl cannot satisfy a validated requirement;
- **DTMO** — education-sector CTI context, vulnerability prioritization, governance, canonical evidence semantics and governed sharing authority.

## 5. Security and governance posture

DTMO's established invariants remain mandatory through the integration programme: server-side RBAC and least privilege, human/service-principal separation, privileged Administration safeguards, correlation/audit, provenance/confidence preservation, data minimization and separate review/external-share authority.

The Phase 11.3 IntelOwl contract strengthens the enrichment boundary with a dedicated non-admin service identity, secret-backed API token, TLS verification, explicit observable/analyzer allowlists, fail-closed TLP/privacy controls, bounded rate-limit/retry behavior and analyzer/job/result provenance. IntelOwl external Connectors are excluded from the initial path. Analyzer/provider verdicts remain attributed context and do not become proof of local compromise.

No collector, publisher, enrichment engine, graph platform, case platform, CI result, staging acceptance or production authorization automatically grants external publication/share authority.

## 6. Architecture and licensing impact

The preferred pattern is service-to-service integration rather than source-code merger. No Taranis source is vendored into DTMO under the accepted boundary.

IntelOwl and pyIntelOwl are AGPL-3.0. The Phase 11.3 contract treats them as separate API/service components and does not vendor their source into DTMO. Any future embedding, modification, redistribution or operation of modified network-facing IntelOwl components requires explicit licensing review before architecture acceptance.

The target runtime remains a composed Kubernetes platform with Helm/value-driven configuration and GitOps promotion, hardened with immutable images, external secrets, workload identities, network policies, HA/recovery, observability and supply-chain controls.

## 7. Historical evidence effect

Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the prior accepted candidate. Those decisions remain valid historical evidence.

Because Phase 11 materially changes the platform, that evidence cannot authorize or independently assure the future integrated candidate. New production-equivalent validation in Phase 11.10 and new independent external assurance in Phase 11.11 are required before Phase 12.

## 8. Phase 11 active scope

The detailed programme is defined in `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`.

The current bounded objective is **Phase 11.3 IntelOwl contract acceptance**. `docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md` defines the v6.7-compatible API/service boundary, allowed observable classes, service identity/authentication, analyzer/playbook allowlisting, TLP/privacy, job/result provenance, rate-limit/failure semantics, no-share authority and AGPL service boundary.

A subsequent bounded implementation PR may begin only after this contract and all synchronized professional documentation pass exact-head CI.

## 9. Evidence boundaries

- Repository CI proves repository-controlled engineering claims within test scope.
- Contract-gate success proves the document/test boundary only; it is not live integration evidence.
- Owner acceptance and external assurance remain separate evidence classes.
- Historical run evidence remains immutable and scoped to the state it covered.
- A materially changed integrated platform requires fresh deployment-bound evidence.
- Restricted security/operational evidence should be referenced rather than copied when sensitive.
- Production authorization does not exist until a future Phase 12 `GO` is explicitly recorded.

## 10. Recommendation

Proceed only with Phase 11 priorities in the defined order. Accept the IntelOwl contract on fully green exact-head CI, then implement the bounded IntelOwl adapter with explicit analyzer allowlists and attributed results. Continue through OpenCTI, MISP, TheHive and integrated runtime industrialisation only after each preceding bounded gate is green. Freeze unrelated generic collector, enrichment, graph, SOAR/case-management and report-publishing development inside DTMO.