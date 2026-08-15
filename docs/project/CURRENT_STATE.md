# DTMO Current Project State

Last reconciled: **2026-08-15**  
Software baseline: **16.0.0rc12 plus accepted post-RC13 and E8 repository enhancements**

## Executive summary

DTMO has completed the repository-controlled engineering baseline through Phase 7, RC13 functional unified-console acceptance and the E8.1–E8.10 vulnerability/CTI product-evolution line. RC13 is `PASS / OWNER_ACCEPTED`; E8.1–E8.10 are `PASS / REPOSITORY_COMPLETE`.

Phase 8 production-equivalent validation and accountable acceptance are `PASS / OWNER_ACCEPTED`. Phase 9 independent external assurance is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`.

Phase 10 has now concluded with **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is not production authorized. The active programme is **Phase 11 — Platform Industrialisation**, followed by a new Phase 12 production GO/NO-GO for the materially changed integrated platform.

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
| Phase 12 | `NOT STARTED` |

## Accepted product capabilities

DTMO provides one canonical application shell across Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance. The accepted baseline includes severity/classification semantics and filters, source/provenance context, governed source operations, native analytics, managed principals/roles/permissions, repository-backed governance knowledge, OpenCVE, CIRCL Vulnerability-Lookup, vulnerability prioritization and vendor/product relevance, governed MISP read/export, governed AIL read/enrichment/correlation and vulnerability-management evidence mapping with explicit semantic boundaries for CVSS, EPSS, KEV, MITRE ATT&CK, MISP and AIL.

Repository completion proves implementation and controlled test behavior; it does not replace external evidence classes or legal/publication authority.

## Data and persistence model

- **PostgreSQL** — canonical application, intelligence and RBAC state;
- **OpenSearch** — search/index representation;
- **S3-compatible object storage** — raw source/evidence objects;
- **Redis** — queue/cache/runtime coordination;
- **Prometheus/Grafana** — operational observability.

These remain the accepted DTMO data boundaries until Phase 11 migration decisions explicitly replace or integrate them.

## Security and authority model

The accepted baseline preserves server-side RBAC, least privilege, bearer-token trust validation, human/service-account separation, privileged Administration safeguards, request correlation, auditable security-relevant actions, provenance/confidence preservation, data minimization and explicit review/share approval boundaries.

No connector, successful import, CI result, analytics view, Administration privilege, Governance mapping, staging acceptance, external assurance or platform integration automatically grants external publication authority.

## Governance and framework model

Framework relationships are explicit, versioned and provenance-backed. DTMO includes relationships to Normenkader IBP, MITRE ATT&CK and NIST CSF and uses CVSS as vulnerability-scoring context. E8.10 adds vulnerability-management evidence mapping, including Normenkader IBP SM.07 and supporting context.

A recorded mapping does not imply complete framework compliance, maturity, certification, local exploitability, compromise or remediation completion. Missing evidence is not inferred.

## Phase 10 decision

Phase 10 is complete as `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`. The accountable decision preserves the accepted Phase 8 and Phase 9 evidence as historical evidence for the candidate they covered, but it does not authorize production.

The no-go explicitly triggers a material architecture programme. Therefore previous staging and independent-assurance evidence cannot be reused as production authorization for the future integrated candidate.

## Phase 11 active programme

Phase 11 is the highest-priority development line. The fixed integration order is:

1. Taranis AI;
2. IntelOwl;
3. OpenCTI;
4. MISP consolidation;
5. TheHive;
6. Cortex only if IntelOwl cannot satisfy a validated requirement;
7. Kubernetes/Helm/GitOps and integrated runtime hardening;
8. migration/compatibility;
9. new production-equivalent validation;
10. new independent external assurance.

The current bounded objective is **Phase 11.1 Taranis AI architecture and gap assessment**. The architectural recommendation is to keep DTMO as the education-sector CTI/governance layer and integrate Taranis as the generic OSINT collection, analyst-assessment and structured-reporting subsystem through service APIs.

See:

- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`;
- `docs/architecture/TARANIS_PLATFORM_INTEGRATION_ASSESSMENT.md`.

## Licensing boundary

DTMO is Apache-2.0 and Taranis AI is EUPL-1.2. No Taranis source code is to be vendored into DTMO before an explicit licensing review. The default integration design is service-to-service through documented APIs.

## Evidence boundary

Professional current-state documents describe the present controlled state. Immutable historical run records under `docs/development/` remain scoped to what was true when they were created and are not rewritten to simulate later acceptance.

Phase 8 and Phase 9 remain accepted evidence for the prior candidate. Phase 11 requires fresh validation/assurance for the integrated platform. Phase 12 is the next production authorization decision and is currently `NOT STARTED`.