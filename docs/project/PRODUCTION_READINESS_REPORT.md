# DTMO Production Readiness Report

Assessment date: **2026-08-15**  
Software baseline: **16.0.0rc12 plus accepted post-RC13 and E8 repository enhancements**

## 1. Executive conclusion

DTMO completed the repository engineering baseline, accountable functional acceptance, E8.1–E8.10 product evolution, Phase 8 production-equivalent staging acceptance and Phase 9 independent external assurance.

Phase 10 has concluded with **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

The project has entered **Phase 11 — Platform Industrialisation**. A new Phase 12 production GO/NO-GO will be considered only after the integrated platform completes new production-equivalent validation and independent external assurance.

## 2. Readiness summary

| Readiness dimension | Current position | Decision |
|---|---|---|
| Engineering / CI | Exact-head engineering baseline accepted | `PASS` |
| Functional product | Unified console owner-accepted | `PASS / OWNER_ACCEPTED` |
| E8 vulnerability/CTI scope | Repository-complete | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Production-equivalent validation accepted for prior candidate | `PASS / OWNER_ACCEPTED` |
| Phase 9 | Independent assurance accepted for prior candidate | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | Production authorization decision | `NO-GO / BLOCKED` |
| Phase 11 | Integrated platform industrialisation | `IN PROGRESS / ACTIVE` |
| Phase 12 | New production authorization decision | `NOT STARTED` |

## 3. Accepted DTMO product baseline

The accepted baseline includes the canonical operator shell across Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance; durable canonical intelligence/provenance; severity/classification and filtering; vulnerability analytics and prioritization; managed RBAC; explicit governance mappings; OpenCVE and CIRCL Vulnerability-Lookup; governed MISP read/export; governed AIL read/enrichment/correlation; and Normenkader IBP SM.07-oriented evidence mapping with explicit semantic boundaries.

The governed UI-01 through UI-10 screenshots remain product documentation illustrations rather than production-state evidence.

## 4. Phase 10 decision rationale

Production authorization was not granted because the next platform generation should reduce custom implementation of generic OSINT and operations capabilities and adopt mature open-source subsystems behind explicit service boundaries.

The active architecture direction is:

- **Taranis AI** — OSINT collection, analyst assessment and structured reporting;
- **IntelOwl** — generic IOC enrichment;
- **OpenCTI** — STIX knowledge graph;
- **MISP** — consolidated governed exchange;
- **TheHive** — incident/case handoff;
- **Cortex** — conditional only where IntelOwl cannot satisfy a validated requirement;
- **DTMO** — education-sector CTI context, vulnerability prioritization, governance, canonical evidence semantics and governed sharing authority.

## 5. Security and governance posture

DTMO's established invariants remain mandatory through the integration programme: server-side RBAC and least privilege, human/service-principal separation, privileged Administration safeguards, correlation/audit, provenance/confidence preservation, data minimization and separate review/external-share authority.

No collector, publisher, enrichment engine, graph platform, case platform, CI result, staging acceptance or production authorization automatically grants external publication/share authority.

## 6. Architecture and licensing impact

The preferred pattern is service-to-service integration rather than source-code merger. DTMO is Apache-2.0 and Taranis AI is EUPL-1.2; no Taranis source code is to be copied into DTMO before an explicit licensing review.

The target runtime is a composed Kubernetes platform with Helm/value-driven configuration and GitOps promotion, hardened with immutable images, external secrets, workload identities, network policies, HA/recovery, observability and supply-chain controls.

## 7. Historical evidence effect

Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the prior accepted candidate. Those decisions remain valid historical evidence.

Because Phase 11 materially changes the platform, that evidence cannot authorize or independently assure the future integrated candidate. New production-equivalent validation and new independent external assurance are required before Phase 12.

## 8. Phase 11 active scope

The detailed programme is defined in `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`.

The current bounded objective is **Phase 11.1 Taranis AI architecture and gap assessment**, covering API/data-model mapping, provenance, identities/RBAC, deployment boundaries, licensing, migration risks and acceptance criteria for the canonical adapter.

The detailed initial assessment is `docs/architecture/TARANIS_PLATFORM_INTEGRATION_ASSESSMENT.md`.

## 9. Evidence boundaries

- Repository CI proves repository-controlled engineering claims within test scope.
- Owner acceptance and external assurance remain separate evidence classes.
- Historical run evidence remains immutable and scoped to the state it covered.
- A materially changed integrated platform requires fresh deployment-bound evidence.
- Restricted security/operational evidence should be referenced rather than copied when sensitive.
- Production authorization does not exist until a future Phase 12 `GO` is explicitly recorded.

## 10. Recommendation

Proceed only with Phase 11 priorities in the defined order. Freeze unrelated generic collector, enrichment, graph, SOAR/case-management and report-publishing development inside DTMO. Complete the Taranis architecture/API/data-model assessment first, then implement the adapter and continue through IntelOwl, OpenCTI, MISP, TheHive and integrated runtime industrialisation before new validation and assurance.