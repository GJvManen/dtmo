# DTMO Current Project State

Last reconciled: **2026-08-14**  
Release baseline: **16.0.0rc12 + accepted post-RC13 enhancements + E8 workstream**

## Executive summary

DTMO has completed its repository-controlled engineering baseline through Phase 7 and its functional unified-console acceptance gate (RC13). The accountable project owner has explicitly accepted that functional baseline and the targeted post-RC13 retest.

Phase 8.1 real-staging deployment identity/environment evidence was previously owner-verified for the deployment identity it covered. Phase 8.2–8.5 remain the **IN PROGRESS / NEXT** production-readiness lifecycle. External execution is intentionally paused while E8 materially changes the intended production candidate; historical staging evidence is not relabelled as evidence for a newer candidate.

The active repository product line is **E8 — Vulnerability & CTI ecosystem integrations**. E8.1 through E8.7 are merged at repository level. E8.8 governed AIL Project read/enrichment is the active slice. DTMO is **not production ready**: the materially updated candidate must later be rebound to an immutable staging deployment identity and complete remaining Phase 8 external acceptance, Phase 9 independent assurance and Phase 10 production go/no-go.

## Current phase position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Engineering, security, integrity/recovery, connectors, performance, accessibility/UX, observability/operations | `PASS` |
| RC13 + targeted post-RC13 owner retest | Functional unified-console acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.7 | Vulnerability/CTI integrations, analytics, unified-console UX and governed MISP read/export | `MERGED / REPOSITORY PASS` |
| E8.8 | Governed AIL Project read/enrichment | `ACTIVE` |
| Phase 8.1 historical deployment identity | Real staging environment + immutable deployment identity for the candidate then deployed | `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE` |
| Phase 8.2–8.5 external execution | Deployed staging validation and accountable staging acceptance | `IN PROGRESS / NEXT — execution paused while E8 changes candidate` |
| Phase 9 | Independent external assurance | `NOT COMPLETE` |
| Phase 10 | Production go/no-go | `NOT STARTED` |

## Accepted product capabilities

### Overview and Intelligence

- canonical intelligence KPIs, recent intelligence and investigation/search support;
- shared accessible severity semantics and filtering;
- source/provenance context and durable commit-before-success ingestion;
- vulnerability analytics based on governed OpenCVE and Vulnerability-Lookup evidence;
- CVSS/EPSS/KEV/vendor/product/CWE/sighting filters and configurable time windows;
- explicit `ok`, `empty` and `degraded` evidence states.

### Sources & Catalog

- curated source catalog and idempotent bootstrap;
- source enable/disable, supported execution and runtime-secret references;
- governed manual onboarding with validation/pretest and disabled-first activation;
- optional OpenCVE, Vulnerability-Lookup and MISP read integrations;
- governed MISP outbound export under a separate feature flag, with human review/share approval and replay protection;
- AIL Project read/enrichment is active as a separate disabled-by-default, explicit-object integration and does not enable autonomous crawling.

### Visual Analytics

- native severity/source/connector/review analytical views;
- configurable trend analysis;
- vulnerability CVSS/EPSS/KEV/sighting/vendor/product/CWE facets and trends;
- canonical application analytics without requiring Grafana authentication for normal users;
- separately secured Grafana operations/advanced dashboards.

### Administration

- managed principals and governed role assignments;
- role-to-permission visibility/management;
- human/service-account separation;
- administrator self-management and final-active-admin protections;
- auditable privileged changes with request correlation.

### Governance

- authenticated repository-backed governance knowledge surface;
- versioned framework registry and explicit coverage/review states;
- provenance-backed DTMO control crosswalks;
- Normenkader IBP, MITRE ATT&CK and NIST CSF relationships;
- CVSS context with explicit claim boundaries;
- implementation-evidence and publication/share authority boundaries.

The targeted owner retest explicitly accepted the Governance framework/control mapping surface. Later E8 repository changes do not create new owner acceptance by implication.

## E8 delivery state

- **E8.1** OpenCVE vulnerability intelligence — merged.
- **E8.2** CIRCL Vulnerability-Lookup and sightings — merged.
- **E8.3** explainable vulnerability prioritization — merged.
- **E8.4** governed vendor/product/CPE relevance — merged.
- **E8.5.1** governed vulnerability analytics contract — merged.
- **E8.5.2** server-side evidence projection plus Overview, Intelligence and Visual Analytics UX — merged after repository-controlled acceptance gates.
- **E8.6** governed read-only MISP integration — merged after exact-head repository CI.
- **E8.7** governed MISP sharing/export — merged after exact-head repository CI.
- **E8.8** governed AIL Project read/enrichment — active.
- **E8.9–E8.10** not yet accepted.

Repository tests and synthetic browser/HTTP fixtures for E8 are repository evidence only. They do not prove live-feed completeness, deployment, exploitability, compromise, owner acceptance, pentest acceptance, successful external delivery or external-share authorization.

## Canonical data and persistence state

DTMO's application truth is layered:

- **PostgreSQL:** canonical intelligence/application/RBAC state;
- **OpenSearch:** search/index representation;
- **S3-compatible object storage:** raw source/evidence objects;
- **Redis:** queue/cache/runtime coordination;
- **Prometheus/Grafana:** operational observability.

A connector result is not durably successful until canonical PostgreSQL persistence completes. External platform state never replaces DTMO review, audit or authorization state.

## Security and governance state

The accepted baseline preserves server-side RBAC and least privilege, externally issued bearer-token trust validation, human/service-account separation, separation of duties, auditable privileged transitions, provenance/confidence preservation, privacy/data minimization, runtime secret handling, explicit human review and separate external-share approval.

No connector, successful import, CI job, analytics view, Administration capability, Governance mapping or staging access grants automatic publication authority. Incoming MISP restrictions remain authoritative. MISP export creates unpublished events only. The AIL integration is read-only and deliberately excludes crawler control, general paste-body import and autonomous investigation mutation.

## Framework mapping truth

Framework mapping is explicit and provenance-backed. The project does not infer mappings from free text, tags or semantic similarity. Individual mappings carry their own relation/coverage semantics and evidence; presence of a mapping does not imply complete framework compliance.

CVSS remains a vulnerability-scoring context rather than a DTMO compliance-control framework. MITRE ATT&CK mappings are threat/detection/classification relationships rather than compliance claims.

## Active workstream

**E8.8 — governed AIL Project read/enrichment** is the active repository objective under issue #193.

The bounded slice reads only explicitly configured AIL object global IDs through the authenticated object API. Supported extracted security indicators are projected into canonical DTMO indicators with source provenance. Returned raw AIL content, investigation titles and notes are not copied; only bounded investigation identifiers may be retained as context. Crawler creation, scheduling, execution, AIL imports and object/investigation mutation are outside the slice.

## Remaining production-readiness limitations

- E8.8–E8.10 are not yet fully accepted;
- the production candidate is still changing and must later be rebound to an updated immutable staging deployment identity;
- Phase 8.2 platform/identity validation remains IN PROGRESS / NEXT but execution is paused until the updated candidate is immutable;
- Phase 8.3 source-to-intelligence validation is not yet accepted for the final candidate;
- Phase 8.4 operational/recovery validation is not yet accepted for the final candidate;
- Phase 8.5 accountable staging acceptance is not yet recorded for the final candidate;
- Phase 9 independent penetration/security assurance is not complete;
- representative production-equivalent load/stress, hardening and residual-risk acceptance remain outstanding where required by the Phase 9 gate;
- Phase 10 formal production go/no-go has not started.

## Documentation and evidence boundary

Historical Phase 8.1 owner verification remains immutable evidence for the deployment identity it covered. It is not rewritten to cover later E8 commits. Environment-specific values remain governed by their approved evidence location and are not reconstructed from repository placeholders.

Stable professional documents describe the controlled current state. Operational chronology belongs under `docs/development/runs/`, GitHub issues/pull requests and CI evidence. Environment and independent-assurance claims require evidence attributable to the relevant deployment/assessment identity.
