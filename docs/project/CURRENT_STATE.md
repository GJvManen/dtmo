# DTMO Current Project State

Last reconciled: **2026-08-15**  
Software baseline: **16.0.0rc12 plus accepted post-RC13 and E8 repository enhancements**

## Executive summary

DTMO has completed the repository-controlled engineering baseline through Phase 7, RC13 functional unified-console acceptance and the E8.1–E8.10 vulnerability/CTI product-evolution line. RC13 is `PASS / OWNER_ACCEPTED`; E8.1–E8.10 are `PASS / REPOSITORY_COMPLETE`.

The accountable owner reports Phase 8.2 platform/identity validation, Phase 8.3 source-to-intelligence validation, Phase 8.4 operations/recovery/rollback validation and Phase 8.5 accountable production-equivalent staging acceptance complete. Phase 8 is therefore `PASS / OWNER_ACCEPTED`. Phase 9 independent external assurance is also reported complete and accepted as `PASS / EXTERNAL_ASSURANCE_ACCEPTED`.

DTMO is now in **Phase 10 formal production go/no-go**. It is **not production authorized** until an accountable Phase 10 `GO` decision is explicitly recorded.

## Lifecycle position

| Stage | Status |
|---|---|
| Phases 1–7 | `PASS` |
| RC13 + owner retest | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8.2–8.4 | `PASS` |
| Phase 8.5 | `PASS / OWNER_ACCEPTED` |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | `IN PROGRESS / DECISION REQUIRED` |

## Accepted product capabilities

DTMO provides one canonical application shell across Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance. The accepted baseline includes severity/classification semantics and filters, source/provenance context, governed source operations, native analytics, managed principals/roles/permissions, repository-backed governance knowledge, OpenCVE, CIRCL Vulnerability-Lookup, vulnerability prioritization and vendor/product relevance, governed MISP read/export, governed AIL read/enrichment/correlation and vulnerability-management evidence mapping with explicit semantic boundaries for CVSS, EPSS, KEV, MITRE ATT&CK, MISP and AIL.

Repository completion proves implementation and controlled test behavior; it does not replace external evidence classes or legal/publication authority.

## Data and persistence model

- **PostgreSQL** — canonical application, intelligence and RBAC state;
- **OpenSearch** — search/index representation;
- **S3-compatible object storage** — raw source/evidence objects;
- **Redis** — queue/cache/runtime coordination;
- **Prometheus/Grafana** — operational observability.

Durable source ingestion is not reported as successful before the canonical persistence boundary completes. Supporting stores and dashboards do not replace the canonical record or governance state.

## Security and authority model

The accepted baseline preserves server-side RBAC, least privilege, bearer-token trust validation, human/service-account separation, privileged Administration safeguards, request correlation, auditable security-relevant actions, provenance/confidence preservation, data minimization and explicit review/share approval boundaries.

No connector, successful import, CI result, analytics view, Administration privilege, Governance mapping, staging acceptance or production authorization automatically grants external publication authority.

## Governance and framework model

Framework relationships are explicit, versioned and provenance-backed. DTMO includes relationships to Normenkader IBP, MITRE ATT&CK and NIST CSF and uses CVSS as vulnerability-scoring context. E8.10 adds vulnerability-management evidence mapping, including Normenkader IBP SM.07 and supporting context.

A recorded mapping does not imply complete framework compliance, maturity, certification, local exploitability, compromise or remediation completion. Missing evidence is not inferred.

## Phase 8 and Phase 9 acceptance

Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` based on accountable external acceptance facts. Detailed external/restricted evidence should remain in approved evidence locations and be referenced rather than copied into public repository documentation when it contains sensitive operational information.

Repository CI, local Docker Compose, staging emulators and synthetic fixtures remain supporting engineering evidence only. They are not retrospectively promoted to external staging or independent-assurance evidence.

## Phase 10 current requirement

Phase 10 is the active **IN PROGRESS / DECISION REQUIRED** release-readiness objective. The decision package must confirm:

- approved production environment, accountable service owner and support model;
- immutable production release identity and image digests;
- IAM, service identities, secrets-management and network approval;
- backup, restore, recovery and rollback approval;
- monitoring, alerting, on-call and escalation approval;
- incident-response/security-operations handover;
- privacy, data-handling, legal and governance approval;
- open-finding statement and accountable residual-risk disposition;
- formal production release/change authorization;
- go-live window and rollback authority.

Missing required approval, unresolved release-blocking findings or a material release-identity mismatch results in `NO-GO / BLOCKED` until corrected and, where required, revalidated.

## Documentation and evidence boundary

Professional current-state documents describe the present controlled state. Immutable historical run records under `docs/development/` remain scoped to what was true when they were created and are not rewritten to simulate later acceptance.

Phase 10 production authorization is a distinct accountable decision. DTMO must not be represented as production authorized before an explicit `GO` is recorded.