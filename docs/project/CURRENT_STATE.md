# DTMO Current Project State

Last reconciled: **2026-08-12**  
Release baseline: **16.0.0rc12**

## Executive summary

DTMO has completed its repository-controlled engineering baseline through Phase 7 and its functional unified-console acceptance gate (RC13). The accountable project owner has explicitly accepted the current functional product.

The project is therefore ready to enter **Phase 8 real production-equivalent staging validation**, but it is **not production ready**. Independent external assurance and formal production go/no-go remain outstanding.

## Current phase position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Engineering, security, integrity/recovery, connectors, performance, accessibility/UX, observability/operations | `PASS` |
| RC13 | Functional unified-console acceptance | `PASS / OWNER_ACCEPTED` |
| Phase 8 | Real staging acceptance | `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY` |
| Phase 9 | Independent external assurance | `NOT COMPLETE` |
| Phase 10 | Production go/no-go | `NOT STARTED` |

## Product capabilities available in the accepted baseline

### Overview

- intelligence KPIs;
- source/runtime status;
- recent intelligence;
- native analytical summaries and trend representation;
- truthful no-data/empty-state behavior;
- unified refresh behavior.

### Intelligence

- canonical recent intelligence from PostgreSQL application state;
- provenance/source context;
- OpenSearch-backed investigation/search support;
- normalized supported source types and references;
- durable commit-before-success ingestion behavior.

### Sources & Catalog

- curated/built-in source catalog;
- catalog bootstrap and idempotent registration;
- source enable/disable operations;
- supported source execution;
- credentialed source support through logical secret references;
- connector state/freshness/runtime evidence.

Manual source onboarding through the product UI/API is a planned post-RC13 enhancement.

### Visual Analytics

- native severity/source/connector/review analytical views;
- zero-data truthful empty states;
- canonical application analytics without requiring Grafana authentication for normal users;
- separately secured Grafana operations/advanced dashboards.

Richer severity colours, shared filtering and configurable trend analysis are planned enhancements.

### Administration

- managed principals and role assignments;
- human/service-account role separation;
- administrator self-management protection;
- final-active-admin protection;
- auditable privileged changes with request correlation.

A richer role-to-permission administration model is planned.

### Governance

- authenticated repository-backed governance knowledge surface;
- explicit framework coverage states;
- repository provenance for internal mappings;
- publication/share authority boundaries.

First-class external framework crosswalks remain deliberately incomplete until explicit provenance-backed mapping datasets are implemented.

## Canonical data and persistence state

DTMO's application truth is intentionally layered:

- **PostgreSQL:** canonical intelligence/application/RBAC state;
- **OpenSearch:** search/index representation;
- **S3-compatible object storage:** raw source/evidence objects;
- **Redis:** queue/cache/runtime coordination;
- **Prometheus/Grafana:** operational observability.

A connector result is not considered durably successful until canonical PostgreSQL persistence completes. Search-index or raw-object success alone does not substitute for canonical application truth.

## Security and governance state

The accepted baseline preserves:

- server-side RBAC and least privilege;
- externally issued bearer-token trust validation;
- human/service-account separation;
- separation of duties;
- tamper-evident/auditable privileged state transitions;
- provenance and confidence preservation;
- privacy/data minimization;
- logical secret references instead of raw credential values;
- explicit human review and separate external-share approval;
- no automatic publication authority from connectors, CI, analytics, Administration, Governance or staging access.

## Framework mapping state

The current governance truth model is intentionally conservative:

| Framework | Current state | Meaning |
|---|---|---|
| Normenkader IBP | `UNMAPPED` | no complete first-class control crosswalk yet |
| MITRE ATT&CK | `UNMAPPED` | no complete first-class technique crosswalk yet |
| CVSS | `CONTEXT_ONLY` | severity context exists, but first-class score/vector mapping is not yet implemented |
| DTMO internal governance | `MAPPED_INTERNAL` | repository-backed mappings to explicit project evidence |

The next mapping architecture must record framework/version, control/technique identifier, provenance, confidence/status and review state. Missing mappings must remain visible and must never be inferred from free text or tags.

## Active production-readiness workstream

**Phase 8.1** is the single active production-readiness gate.

It requires a real approved production-equivalent staging environment and an immutable deployment identity tied to:

- environment and accountable owner;
- approved reachable access path;
- exact deployed commit/release;
- immutable application/supporting image digests;
- infrastructure/runtime inventory;
- configuration parity;
- separate least-privilege application identities;
- TLS/network controls;
- controlled staging data and no-production-credential confirmation;
- deployment/change and rollback records;
- deployment-time security/CVE/vendor-advisory review.

## Active product-enhancement workstream

GitHub issue #171 tracks the post-RC13 product roadmap. Delivery order:

1. shared accessible severity semantics and filters for Overview + Intelligence;
2. governed manual source onboarding;
3. richer Visual Analytics and trend analysis;
4. first-class framework mapping data/API model;
5. deeper Administration role/permission management;
6. deeper framework-oriented Governance evidence surface.

These enhancements do not reopen RC13 and do not themselves satisfy Phase 8 evidence requirements.

## Known limitations

- DTMO has not yet completed real production-equivalent staging acceptance.
- Independent penetration testing/external assurance is not yet complete.
- Formal production go/no-go has not started.
- First-class Normenkader IBP and MITRE ATT&CK crosswalks are not implemented.
- CVSS is not yet a complete first-class structured mapping model.
- Manual arbitrary source onboarding is not yet available through the canonical Sources & Catalog UI.
- Administration does not yet expose the planned full role/permission management matrix.

## Documentation and evidence boundary

Stable professional documents describe the platform and controlled current state. Operational chronology belongs under `docs/development/runs/`, GitHub issues/PRs and CI evidence.

Historical run records remain immutable point-in-time evidence, but they must not replace architecture, security, product or governance documentation.
