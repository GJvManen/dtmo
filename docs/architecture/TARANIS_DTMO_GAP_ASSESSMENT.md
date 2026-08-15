# Taranis AI ↔ DTMO Architecture & Gap Assessment

Status: **Phase 11.1 / ACTIVE**

## Executive decision

Taranis AI should be evaluated as the primary OSINT collection and analyst-workflow platform underneath/alongside DTMO, not as a wholesale replacement for DTMO. The preferred architecture is service-to-service integration through documented APIs and explicit data contracts.

Taranis currently provides a production-oriented service split with ingress, frontend, core API and worker services, PostgreSQL as the primary database, Redis-backed RQ workers, health endpoints, collector/bot/presenter/publisher workflows, an OpenAPI contract, IntelOwl integration and experimental MISP collaboration. DTMO should reuse these capabilities where they are stronger than continued bespoke implementation.

## Decision matrix

| Capability | DTMO decision | Target owner | Rationale / action |
|---|---|---|---|
| Education-sector governance | KEEP | DTMO | Core differentiator: Normenkader IBP and evidence semantics |
| Vulnerability prioritisation | KEEP | DTMO | Existing CVSS/EPSS/KEV/context model and explainability |
| Provenance policy / canonical evidence | KEEP | DTMO | Existing accepted canonical contracts |
| External-share approval | KEEP | DTMO | Preserve separate human review/share authority |
| Generic RSS/web OSINT collection | INTEGRATE / DEPRECATE DUPLICATION | Taranis | Use mature Taranis collectors and worker model |
| Analyst article/story workflow | INTEGRATE | Taranis | Use structured OSINT assessment workflow |
| Generic report/publisher engine | INTEGRATE | Taranis | Avoid bespoke publisher/report subsystem |
| Generic IOC enrichment | REPLACE BESPOKE EXPANSION | IntelOwl | Taranis already integrates IntelOwl |
| STIX knowledge graph | INTEGRATE | OpenCTI | Avoid building a graph platform inside DTMO |
| Community CTI exchange | CONSOLIDATE | MISP + DTMO policy | Single governed outbound policy |
| Incident/case management | INTEGRATE LATER | TheHive | DTMO should hand off, not become case-management suite |
| Additional analyzer runtime | OPTIONAL | Cortex | Add only if IntelOwl has demonstrated gaps |
| RBAC / authorization | FEDERATE, KEEP SERVER AUTHORITY | DTMO + platform IAM | Map identities; never trust UI visibility alone |
| SSO/OIDC | INDUSTRIALISE | Shared identity provider | One enterprise identity plane with workload identities |
| Secrets | INDUSTRIALISE | External secret manager | No cross-platform static secrets in repo/config |
| Observability | CONSOLIDATE | Shared platform | Central metrics/logs/traces/SLOs |
| Deployment | INDUSTRIALISE | Shared platform | Immutable, signed, production-equivalent topology |

## Taranis capability observations

Taranis exposes distinct ingress, frontend, core and worker services. Worker responsibilities include collectors, bots, presenters and publishers. PostgreSQL is the primary database and Redis is used for RQ worker/message coordination. An OpenAPI 3.1 specification is included. Core exposes a liveness endpoint and an operational health endpoint that reports dependencies and can fail with HTTP 503. These are useful production integration contracts.

Taranis supports an IntelOwl bot. The documented analyzer mapping covers CVE, IP, domain, URL, hash and email observables. The integration is disabled by default and supports explicit TLS verification, dedicated API tokens, analyzer readiness checks and probe-based runtime validation. This is a strong candidate to become DTMO's generic enrichment plane.

Taranis also documents experimental MISP story-level sharing. DTMO must not delegate its existing human share-approval boundary to that feature without a dedicated policy assessment.

## Initial canonical mapping

| Taranis concept | DTMO target | Mapping rule |
|---|---|---|
| source / collector | source catalogue + connector provenance | Preserve upstream source and collector identity separately |
| news item | canonical intelligence record | Keep original timestamp, URL/source, content/evidence reference and ingestion provenance |
| tags / IOC tags | structured indicators/context | Map only recognized typed values; retain raw tags as source context |
| story | investigation/intelligence collection context | Do not flatten story-level relationships into one record |
| report item | governed report/reference context | Preserve author/reviewer provenance where available |
| publication state | external reference only | Must not imply DTMO share approval |
| TLP/classification | DTMO classification/TLP | Reject unknown/less-restrictive transformations fail-closed |
| attachments | evidence/object references | Store immutable reference/hash where supported; avoid uncontrolled binary duplication |

## Identity and authorization boundary

The integration must distinguish human users, service accounts and machine-to-machine identities. DTMO server-side authorization remains authoritative for DTMO privileged actions. Taranis roles may be mapped to DTMO claims only through an explicit trust policy; no role-name equivalence is assumed.

Preferred target:

- enterprise OIDC/SSO for human identities;
- dedicated workload identity/token for Taranis -> DTMO;
- dedicated workload identity/token for DTMO -> OpenCTI/MISP/TheHive;
- secrets in an external secret manager;
- short-lived credentials where platform support allows;
- full audit correlation across service boundaries.

## Integration API direction

Phase 11.2 should start read-oriented and one-way:

`Taranis -> DTMO`

The first adapter should consume Taranis structured output through its documented REST/OpenAPI surface rather than database access. Direct cross-database coupling is rejected because it creates schema/version coupling and bypasses service authorization/audit boundaries.

Minimum adapter contract:

- stable upstream object ID;
- source/collector identity;
- observed/published/collected timestamps;
- title/content/summary as available;
- typed IOC/tag context;
- TLP/classification;
- upstream object URL/reference;
- evidence/attachment metadata;
- deterministic idempotency key;
- adapter version;
- correlation ID;
- no implicit review/share approval.

## Licensing boundary

Taranis AI is distributed under EUPL-1.2 while DTMO is Apache-2.0. Phase 11 therefore assumes service/API integration and independent deployment units. No Taranis source code should be copied or vendored into DTMO until a dedicated licensing assessment explicitly approves the intended use and distribution model.

## Proof-of-concept acceptance criteria

Phase 11.1 exits only when the Phase 11.2 PoC backlog is bounded by these criteria:

1. one Taranis item can be imported through an API adapter into DTMO canonical storage;
2. source provenance and upstream object ID survive round-trip retrieval;
3. replay is idempotent;
4. TLP/classification cannot become less restrictive silently;
5. malformed or unavailable Taranis responses fail closed and do not corrupt canonical state;
6. machine identity has only the minimum required DTMO ingest permission;
7. no Taranis publication state grants DTMO external-share authority;
8. audit/correlation links the upstream request to the created/updated DTMO record;
9. adapter health/freshness/timeout/failure-isolation are observable;
10. no secret is exposed to browser UI, logs, fixtures or repository evidence.

## Risks requiring explicit Phase 11 treatment

- duplicate source collection between Taranis and existing DTMO connectors;
- divergent classification/TLP semantics;
- user/role-model mismatch;
- cross-platform identifier collisions;
- hidden publication/sharing side effects;
- enrichment provider data/privacy constraints;
- operational complexity from too many overlapping services;
- licensing obligations if boundaries are blurred;
- availability coupling and queue backpressure;
- migration of existing DTMO source catalogue and historical provenance.

## Next implementation step

After this architecture assessment is accepted, start **Phase 11.2** with a minimal read-only Taranis -> DTMO adapter against the Taranis OpenAPI contract and synthetic fixtures. Do not enable production publication, direct database integration or bidirectional mutation in the first increment.
