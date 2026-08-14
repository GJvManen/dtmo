# DTMO Current Project State

Last reconciled: **2026-08-14**  
Release baseline: **16.0.0rc12 + accepted post-RC13 enhancements**

## Executive summary

DTMO has completed its repository-controlled engineering baseline through Phase 7 and its functional unified-console acceptance gate (RC13). The accountable project owner has explicitly accepted the current functional product, including the targeted post-RC13 owner retest.

The accountable project owner has also checked and verified the **real staging deployment identity and Phase 8.1 environment evidence**. DTMO is therefore progressing within Phase 8, with **Phase 8.2 platform and identity validation** as the next active objective.

DTMO is **not production ready**. Full Phase 8 deployed-environment acceptance, independent Phase 9 assurance and Phase 10 production go/no-go remain outstanding.

## Current phase position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Engineering, security, integrity/recovery, connectors, performance, accessibility/UX, observability/operations | `PASS` |
| RC13 + targeted post-RC13 owner retest | Functional unified-console acceptance | `PASS / OWNER_ACCEPTED` |
| Phase 8.1 | Real staging environment + immutable deployment identity | `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE` |
| Phase 8.2–8.5 | Deployed staging validation and accountable staging acceptance | `IN PROGRESS / NEXT` |
| Phase 9 | Independent external assurance | `NOT COMPLETE` |
| Phase 10 | Production go/no-go | `NOT STARTED` |

## Accepted product capabilities

### Overview and Intelligence

- canonical intelligence KPIs and recent intelligence;
- shared accessible severity semantics and filtering;
- accepted high-contrast recent-intelligence presentation;
- source/provenance context;
- configurable analytical trends and truthful empty states;
- OpenSearch-backed investigation/search support;
- durable commit-before-success ingestion behavior.

### Sources & Catalog

- curated/built-in source catalog and idempotent bootstrap;
- source enable/disable and supported execution;
- credentialed source support through logical secret references;
- governed manual source onboarding with validation/pretest and disabled-first activation;
- connector state/freshness/runtime evidence.

### Visual Analytics

- native severity/source/connector/review analytical views;
- configurable trend analysis;
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
- visible provenance-backed DTMO control crosswalks;
- Normenkader IBP control relationships;
- MITRE ATT&CK threat/detection/classification context;
- NIST CSF relationships;
- CVSS context with explicit claim boundaries;
- implementation-evidence references and publication/share authority boundaries.

The targeted owner retest explicitly accepted the Governance framework/control mapping surface.

## Canonical data and persistence state

DTMO's application truth is layered:

- **PostgreSQL:** canonical intelligence/application/RBAC state;
- **OpenSearch:** search/index representation;
- **S3-compatible object storage:** raw source/evidence objects;
- **Redis:** queue/cache/runtime coordination;
- **Prometheus/Grafana:** operational observability.

A connector result is not durably successful until canonical PostgreSQL persistence completes.

## Security and governance state

The accepted baseline preserves server-side RBAC and least privilege, externally issued bearer-token trust validation, human/service-account separation, separation of duties, auditable privileged transitions, provenance/confidence preservation, privacy/data minimization, logical secret references, explicit human review and separate external-share approval.

No connector, CI job, analytics view, Administration capability, Governance mapping or staging access grants automatic publication authority.

## Framework mapping truth

Framework mapping is explicit and provenance-backed. The project does not infer mappings from free text, tags or semantic similarity. Individual mappings carry their own relation/coverage semantics and evidence; presence of a mapping does not imply complete framework compliance.

CVSS remains a vulnerability-scoring context rather than a DTMO compliance-control framework. MITRE ATT&CK mappings are threat/detection/classification relationships rather than compliance claims.

## Active production-readiness workstream

**Phase 8.2 — platform and identity validation** is now the single active production-readiness objective.

Validation must remain bound to the same owner-verified staging deployment identity and cover:

- application health/readiness;
- database migrations/connectivity;
- OpenSearch, Redis and object-storage availability;
- authentication and authorization;
- human/service-account separation;
- privileged Administration controls;
- audit/correlation behavior;
- operational metrics and separately authenticated Grafana.

A redeployment changes the immutable evidence identity and requires a new binding rather than mixing evidence across deployments.

## Remaining production-readiness limitations

- Phase 8.2 platform/identity validation is not yet accepted;
- Phase 8.3 source-to-intelligence validation is not yet accepted;
- Phase 8.4 operational/recovery validation is not yet accepted;
- Phase 8.5 accountable staging acceptance is not yet recorded;
- Phase 9 independent penetration/security assurance is not complete;
- representative production-equivalent load/stress, hardening and residual-risk acceptance remain outstanding where required by the Phase 9 gate;
- Phase 10 formal production go/no-go has not started.

## Documentation and evidence boundary

The Phase 8.1 owner-verification decision is retained as an immutable development run record. Environment-specific values remain governed by their approved evidence location and are not reconstructed from repository placeholders.

Stable professional documents describe the controlled current state. Operational chronology belongs under `docs/development/runs/`, GitHub issues/PRs and CI evidence. Environment and independent-assurance claims require evidence attributable to the relevant deployment/assessment identity.
