# DTMO Current Project State

Last reconciled: **2026-08-16**  
Software baseline: **16.0.0rc12 plus accepted post-RC13, E8 and Phase 11 repository enhancements**

## Executive summary

DTMO has completed the repository-controlled engineering baseline through Phase 7, RC13 functional unified-console acceptance and the E8.1–E8.10 vulnerability/CTI product-evolution line. RC13 is `PASS / OWNER_ACCEPTED`; E8.1–E8.10 are `PASS / REPOSITORY_COMPLETE`.

Phase 8 production-equivalent validation and accountable acceptance are `PASS / OWNER_ACCEPTED`. Phase 9 independent external assurance is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate they covered.

Phase 10 concluded with **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is not production authorized. The active programme is **Phase 11 — Platform Industrialisation**, followed by a new Phase 12 production GO/NO-GO for the materially changed integrated platform.

Phase 11.1 Taranis architecture/contract and Phase 11.2 Taranis→DTMO canonical adapter are **`PASS / REPOSITORY_COMPLETE`**. The Phase 11.3 IntelOwl contract and bounded service/API adapter are accepted. The active bounded objective is now **governed IntelOwl execution, durable enrichment-history persistence and operational integration**, currently requiring exact-head repository validation.

## Lifecycle position

| Stage | Status |
|---|---|
| Phases 1–7 | `PASS` |
| RC13 + owner retest | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | `PASS / OWNER_ACCEPTED` |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11 | `IN PROGRESS / ACTIVE` |
| Phase 11.1 Taranis architecture/contract | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.2 Taranis adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 IntelOwl contract | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 IntelOwl adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 governed execution/persistence | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 12 | `NOT STARTED` |

## Accepted product capabilities

DTMO provides one canonical application shell across Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance. The accepted baseline includes severity/classification semantics and filters, source/provenance context, governed source operations, native analytics, managed principals/roles/permissions, repository-backed governance knowledge, OpenCVE, CIRCL Vulnerability-Lookup, vulnerability prioritization and vendor/product relevance, governed MISP read/export, governed AIL read/enrichment/correlation and vulnerability-management evidence mapping with explicit semantic boundaries for CVSS, EPSS, KEV, MITRE ATT&CK, MISP and AIL.

Phase 11.2 additionally provides the repository-complete Taranis read-only canonical integration: news/story collection, durable checkpointing/reconciliation, detail/CTI retrieval, governed execution, canonical persistence/indexing and connector observability. Repository completion proves implementation and controlled test behavior only; it does not replace deployment, external-assurance or production-authorization evidence classes.

The accepted IntelOwl adapter validates approved observable classes, analyzer allowlists and handling before disclosure; disables IntelOwl external connector side effects in the submitted job; correlates results to immutable upstream job IDs; rejects unknown analyzers, oversized/malformed results and job-identity mismatches; marks partial analyzer success explicitly; and records that enrichment does not grant external-share authority or prove local compromise.

The active Phase 11.3 slice extends that adapter with a human-authorized `REVIEW_INTELLIGENCE` execution boundary, durable immutable enrichment records linked to canonical intelligence, a read-only enrichment-history endpoint and database-enforced no-share/no-compromise invariants. Every requested analyzer is conservatively treated as an external disclosure boundary in this slice, so restricted handling fails closed before network disclosure.

## Data and persistence model

- **PostgreSQL** — canonical application, intelligence, RBAC and IntelOwl enrichment-history state;
- **OpenSearch** — search/index representation;
- **S3-compatible object storage** — raw source/evidence objects;
- **Redis** — queue/cache/runtime coordination;
- **Prometheus/Grafana** — operational observability.

Migration `0011_intelowl_enrichment_history` introduces `intelowl_enrichment_records`. Each record preserves canonical item identity, IntelOwl job identity, observable/handling decision inputs, requested analyzers, partial/terminal status, attributed reports, raw normalized result, requesting human subject and explicit `external_share_authorized=false` / `local_compromise_proven=false` authority markers. `(item_id, job_id)` is unique to prevent duplicate persistence of the same upstream job.

These remain repository-controlled boundaries only. They do not establish live provider connectivity, production-equivalent durability or operational acceptance.

## Security and authority model

The accepted baseline preserves server-side RBAC, least privilege, bearer-token trust validation, human/service-account separation, privileged Administration safeguards, request correlation, auditable security-relevant actions, provenance/confidence preservation, data minimization and explicit review/share approval boundaries.

Taranis is integrated read-only and cannot grant DTMO publication/share authority. IntelOwl follows the same principle: enrichment jobs, analyzer verdicts, tags, evaluations or upstream connector capabilities cannot become DTMO external-share approval or proof of local compromise. The adapter sends an empty IntelOwl connector request and preserves `external_share_authorized=false` and `local_compromise_proven=false` in normalized and persisted provenance.

Governed IntelOwl execution requires the human `REVIEW_INTELLIGENCE` permission. The current service-account role does not hold that permission, preventing autonomous invocation through the governed endpoint. Read-only history requires `READ_INTELLIGENCE`.

Production configuration for IntelOwl fails closed unless the integration uses HTTPS, a runtime API token and an explicit analyzer allowlist. Email/personal-data enrichment remains excluded by default pending explicit privacy/data-processing approval. Restricted handling such as `red`, `tlp:red` and `review-required` is treated as non-disclosable to the separate IntelOwl service/analyzer boundary.

No connector, successful import, enrichment result, CI result, analytics view, Administration privilege, Governance mapping, staging acceptance, external assurance or platform integration automatically grants external publication authority.

## Governance and framework model

Framework relationships are explicit, versioned and provenance-backed. DTMO includes relationships to Normenkader IBP, MITRE ATT&CK and NIST CSF and uses CVSS as vulnerability-scoring context. E8.10 adds vulnerability-management evidence mapping, including Normenkader IBP SM.07 and supporting context.

A recorded mapping does not imply complete framework compliance, maturity, certification, local exploitability, compromise or remediation completion. Missing evidence is not inferred.

## Phase 10 decision

Phase 10 is complete as `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`. The accountable decision preserves the accepted Phase 8 and Phase 9 evidence as historical evidence for the candidate they covered, but it does not authorize production.

The no-go explicitly triggered a material architecture programme. Therefore previous staging and independent-assurance evidence cannot be reused as production authorization for the future integrated candidate.

## Phase 11 active programme

Phase 11 is the highest-priority development line. The fixed integration order is:

1. Taranis AI — repository-complete through Phase 11.2;
2. IntelOwl — active Phase 11.3 governed execution/persistence objective;
3. OpenCTI;
4. MISP consolidation;
5. TheHive;
6. Cortex only if IntelOwl cannot satisfy a validated requirement;
7. Kubernetes/Helm/GitOps and integrated runtime hardening;
8. migration/compatibility;
9. new production-equivalent validation;
10. new independent external assurance.

The current bounded objective is **Phase 11.3 governed IntelOwl execution, durable persistence and operational integration**. Phase 11.4 OpenCTI remains blocked until this slice is fully green, merged and Phase 11.3 is reconciled as repository-complete.

See:

- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`;
- `docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md`;
- `docs/integrations/INTELOWL_INTEGRATION.md`.

## Licensing boundary

DTMO remains a separate service consumer of upstream platform components. Taranis AI remains behind the accepted service-to-service boundary and its source is not vendored into DTMO.

IntelOwl and pyIntelOwl are AGPL-3.0. Phase 11.3 keeps IntelOwl behind a service/API boundary and does not vendor IntelOwl or pyIntelOwl source into DTMO. Any future embedding, modification, redistribution or operation of modified network-facing IntelOwl components requires explicit licensing review before acceptance.

## Evidence boundary

Professional current-state documents describe the present controlled state. Immutable historical run records under `docs/development/` remain scoped to what was true when they were created and are not rewritten to simulate later acceptance.

Repository/CI evidence for this slice can prove only code/configuration, migration and synthetic persistence behavior. It cannot prove live IntelOwl connectivity, deployed service-account permissions, provider credentials, analyzer quality, privacy approval, production-equivalent behavior, independent assurance or production authorization. New Phase 11.10 validation and Phase 11.11 independent assurance are required for the materially changed integrated platform before Phase 12 can consider production authorization.
