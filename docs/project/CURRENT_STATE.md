# DTMO Current Project State

Last reconciled: **2026-08-14**  
Release baseline: **16.0.0rc12 + accepted post-RC13 enhancements + E8 workstream**

## Executive summary

DTMO has completed its repository-controlled engineering baseline through Phase 7 and its functional unified-console acceptance gate (RC13). The accountable project owner has explicitly accepted that functional baseline and the targeted post-RC13 retest.

Phase 8.1 real-staging deployment identity/environment evidence was previously owner-verified for the deployment identity it covered. The repository also contains the Phase 8.2 platform/identity validation mechanism. Phase 8.2–8.5 remain the **IN PROGRESS / NEXT** production-readiness lifecycle, but external execution is intentionally paused while E8 materially changes the intended production candidate. Historical staging evidence is not relabelled as evidence for a newer candidate.

The active repository product line is **E8 — Vulnerability & CTI ecosystem integrations**. E8.1 through E8.5 are merged. E8.6 read-only MISP integration is active under issue #193. DTMO is **not production ready**: the materially updated candidate must later be rebound to an immutable staging deployment identity and complete remaining Phase 8 external acceptance, Phase 9 independent assurance and Phase 10 production go/no-go.

## Current phase position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Engineering, security, integrity/recovery, connectors, performance, accessibility/UX, observability/operations | `PASS` |
| RC13 + targeted post-RC13 owner retest | Functional unified-console acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.5 | Vulnerability integrations, relevance/prioritization, analytics and unified-console UX | `MERGED / REPOSITORY PASS` |
| E8.6 | Governed read-only MISP integration | `ACTIVE` |
| Phase 8.1 historical deployment identity | Real staging environment + immutable deployment identity for the candidate then deployed | `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE` |
| Phase 8.2–8.5 external execution | Deployed staging validation and accountable staging acceptance | `IN PROGRESS / NEXT — execution paused while E8 changes candidate` |
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
- durable commit-before-success ingestion behavior;
- vulnerability analytics based on governed OpenCVE evidence and Vulnerability-Lookup sightings;
- CVSS/EPSS/KEV/vendor/product/CWE/sighting filters and 24h/7d/30d windows;
- explicit vulnerability `ok`, `empty` and `degraded` states with raw-evidence provenance.

### Sources & Catalog

- curated/built-in source catalog and idempotent bootstrap;
- source enable/disable and supported execution;
- credentialed source support through logical/runtime secret references;
- governed manual source onboarding with validation/pretest and disabled-first activation;
- connector state/freshness/runtime evidence;
- optional OpenCVE and CIRCL Vulnerability-Lookup read integrations;
- E8.6 adds optional MISP read integration only after its own exact-head gate passes.

### Visual Analytics

- native severity/source/connector/review analytical views;
- configurable trend analysis;
- native vulnerability CVSS/EPSS/KEV/sighting/vendor/product/CWE facets and trends;
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

The targeted owner retest explicitly accepted the Governance framework/control mapping surface. E8 repository changes do not create new owner acceptance by implication.

## E8 delivery state

- **E8.1** OpenCVE vulnerability intelligence — merged.
- **E8.2** CIRCL Vulnerability-Lookup and sightings — merged.
- **E8.3** explainable vulnerability prioritization — merged.
- **E8.4** governed vendor/product/CPE relevance — merged.
- **E8.5.1** governed vulnerability analytics contract — merged.
- **E8.5.2** server-side evidence projection plus Overview, Intelligence and Visual Analytics UX — merged through PRs #199 and #200.
- **E8.6** governed read-only MISP integration — active.
- **E8.7–E8.10** not yet accepted.

Repository tests and synthetic browser fixtures for E8 are repository evidence only. They do not prove live-feed completeness, deployment, exploitability, compromise, owner acceptance, pentest acceptance or external-share authorization.

## Canonical data and persistence state

DTMO's application truth is layered:

- **PostgreSQL:** canonical intelligence/application/RBAC state;
- **OpenSearch:** search/index representation;
- **S3-compatible object storage:** raw source/evidence objects;
- **Redis:** queue/cache/runtime coordination;
- **Prometheus/Grafana:** operational observability.

A connector result is not durably successful until canonical PostgreSQL persistence completes. External platform state never replaces DTMO review, audit or authorization state.

## Security and governance state

The accepted baseline preserves server-side RBAC and least privilege, externally issued bearer-token trust validation, human/service-account separation, separation of duties, auditable privileged transitions, provenance/confidence preservation, privacy/data minimization, logical/runtime secret references, explicit human review and separate external-share approval.

No connector, successful import, CI job, analytics view, Administration capability, Governance mapping or staging access grants automatic publication authority. In particular, incoming MISP TLP/distribution/sharing-group restrictions are authoritative constraints; E8.6 import must not be interpreted as permission to redistribute.

## Framework mapping truth

Framework mapping is explicit and provenance-backed. The project does not infer mappings from free text, tags or semantic similarity. Individual mappings carry their own relation/coverage semantics and evidence; presence of a mapping does not imply complete framework compliance.

CVSS remains a vulnerability-scoring context rather than a DTMO compliance-control framework. MITRE ATT&CK mappings are threat/detection/classification relationships rather than compliance claims.

## Active workstream

**E8.6 — governed read-only MISP integration** is the active repository objective under issue #193.

The bounded slice must preserve MISP event/attribute/object/relationship UUIDs and source/time context, tags/taxonomies/galaxies and distribution/TLP constraints while remaining read-only. MISP credentials remain runtime-only. No E8.7 outbound sharing path is accepted by E8.6.

## Remaining production-readiness limitations

- E8.6–E8.10 are not yet fully accepted;
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

Stable professional documents describe the controlled current state. Operational chronology belongs under `docs/development/runs/`, GitHub issues/PRs and CI evidence. Environment and independent-assurance claims require evidence attributable to the relevant deployment/assessment identity.
