# DTMO Current Project State

Last reconciled: **2026-08-15**  
Software baseline: **16.0.0rc12 plus accepted post-RC13 and E8 repository enhancements**

## Executive summary

DTMO has completed the repository-controlled engineering baseline through Phase 7, the RC13 functional unified-console acceptance gate and the E8.1–E8.10 vulnerability/CTI product-evolution line. RC13 is explicitly `PASS / OWNER_ACCEPTED`; E8.1–E8.10 are `PASS / REPOSITORY_COMPLETE`.

The post-E8 candidate has been externally deployed and extensively tested by the accountable owner in an approved production-equivalent staging environment. This is `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE` for the deployment/staging fact itself.

The repository-side validation contracts for Phase 8.2 platform/identity, Phase 8.3 source-to-intelligence, Phase 8.4 operations/recovery and Phase 8.5 accountable staging acceptance are complete. Formal Phase 8 closure still requires the external evidence from those contracts to be completed and accepted against one immutable staging deployment identity, including exact deployed release/commit, image digests and runtime identity.

DTMO is therefore **not production ready**. The current progression is **Phase 8 external evidence completion and accountable acceptance → Phase 9 independent external assurance → Phase 10 formal production go/no-go**.

## Lifecycle position

| Stage | Status |
|---|---|
| Phases 1–7 | `PASS` |
| RC13 + owner retest | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Historical Phase 8.1 staging identity | `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE — HISTORICAL IDENTITY ONLY` |
| Post-E8 external deployment + approved staging | `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE` |
| Phase 8.2 | `REPOSITORY CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED` |
| Phase 8.3 | `REPOSITORY CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED` |
| Phase 8.4 | `REPOSITORY CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED` |
| Phase 8.5 | `REPOSITORY CONTRACT COMPLETE / EXTERNAL OWNER DECISION REQUIRED` |
| Phase 9 | `NOT COMPLETE / NEXT ASSURANCE TRACK AFTER PHASE 8 PASS` |
| Phase 10 | `NOT STARTED` |

## Accepted product capabilities

### Unified operator experience

DTMO provides one canonical application shell across Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance. The accepted product supports severity/classification semantics and filters, source/provenance context, governed source operations, native analytics, managed principals/roles/permissions and repository-backed governance knowledge.

### Vulnerability and CTI capabilities

The E8 baseline includes:

- OpenCVE vulnerability intelligence;
- CIRCL Vulnerability-Lookup and sightings;
- explainable vulnerability prioritization;
- governed vendor/product/CPE relevance;
- vulnerability analytics across Overview, Intelligence and Visual Analytics;
- governed read-only MISP integration;
- separately governed MISP outbound export with human review/share approval boundaries;
- governed AIL read/enrichment and correlation workspace;
- repository-backed vulnerability-management evidence mapping with explicit semantic boundaries for CVSS, EPSS, KEV, MITRE ATT&CK, MISP and AIL.

Repository completion proves the implementation and its controlled tests; it does not by itself prove live external-source completeness, production deployment, legal sharing authority, independent assurance or production approval.

## Data and persistence model

- **PostgreSQL** — canonical application, intelligence and RBAC state;
- **OpenSearch** — search/index representation;
- **S3-compatible object storage** — raw source/evidence objects;
- **Redis** — queue/cache/runtime coordination;
- **Prometheus/Grafana** — operational observability.

Durable source ingestion is not reported as successful before the canonical persistence boundary completes. Supporting stores and dashboards do not replace the canonical record or governance state.

## Security and authority model

The accepted baseline preserves server-side RBAC, least privilege, bearer-token trust validation, human/service-account separation, privileged Administration safeguards, request correlation, auditable security-relevant actions, provenance/confidence preservation, data minimization and explicit review/share approval boundaries.

No connector, successful import, CI result, analytics view, Administration privilege, Governance mapping or staging access automatically grants external publication authority. MISP and AIL behavior remains constrained by the documented source and sharing semantics.

## Governance and framework model

Framework relationships are explicit, versioned and provenance-backed. DTMO includes relationships to Normenkader IBP, MITRE ATT&CK and NIST CSF and uses CVSS as vulnerability-scoring context. E8.10 adds vulnerability-management evidence mapping, including Normenkader IBP SM.07 and supporting context.

A recorded mapping does not imply complete framework compliance, maturity, certification, local exploitability, compromise or remediation completion. Missing evidence is not inferred.

## Phase 8 current requirement

The repository-side contracts for Phases 8.2–8.5 are complete. The remaining work is external evidence completion and accountable acceptance against one immutable staging deployment identity.

The evidence package must bind, as applicable:

- approved environment and accountable owner;
- exact deployed release/commit and immutable image digests;
- runtime/infrastructure identity and configuration parity/deviations;
- IAM, service-account, secret-management, TLS/network and data-sanitization evidence;
- platform health, persistence, search/cache/storage and authorization validation;
- source-to-intelligence traceability and degraded behavior;
- operations, recovery, rollback and RTO/RPO observations;
- approved residual risk/deviations and absence of unresolved release-blocking staging findings;
- explicit accountable `PASS / OWNER_ACCEPTED` or `BLOCKED` Phase 8.5 decision.

This is the current **IN PROGRESS / NEXT** release-readiness objective.

## Phase 9 and Phase 10

Phase 9 requires independent external assurance against the accepted candidate. The expected scope includes penetration testing, hardening/configuration, IAM/secrets, representative load/stress, resilience/recovery, monitoring/incident-response readiness, relevant privacy/legal/governance review, finding remediation/retest and residual-risk disposition.

Phase 10 is the formal production go/no-go and has not started. It requires accepted Phase 8 and Phase 9 evidence plus accountable production-environment, operations, security, privacy/data, recovery/rollback and release/change approvals.

## Documentation and evidence boundary

Professional current-state documents describe the present controlled state. Immutable historical run records remain under `docs/development/` and may correctly contain older lifecycle terminology because they record what was true at that point in time.

Repository CI, local Docker Compose, staging emulators, synthetic fixtures and self-attestation remain supporting evidence only and cannot substitute for the external evidence classes explicitly required by Phase 8, Phase 9 or Phase 10.
