# Taranis AI → DTMO Platform Integration Assessment

Assessment date: **2026-08-15**  
Assessment state: **`PHASE 11.1 / ACTIVE`**

## Executive conclusion

Taranis AI is a strong candidate to become the upstream OSINT collection, analyst-assessment and structured-reporting subsystem for the next DTMO platform generation. DTMO should not be replaced wholesale and Taranis source code should not be copied into DTMO. The recommended architecture is a service-to-service integration in which Taranis owns generic OSINT collection and analyst workflow while DTMO remains authoritative for education-sector CTI context, vulnerability prioritization, governance evidence and governed external-sharing decisions.

The current upstream project exposes a central REST core, a Flask/HTMX frontend, RQ workers for collectors/bots/presenters/publishers, PostgreSQL/SQLite support with PostgreSQL primary, Redis, an SSE broker, Nginx ingress, OpenAPI documentation, operational health endpoints and deployment material for Docker Compose, Kubernetes, Helm and ArgoCD. It also includes an existing IntelOwl integration path and experimental MISP collaboration.

## Why integrate rather than reimplement

DTMO already has strong canonical intelligence, provenance, vulnerability analytics, governance mappings, RBAC, governed MISP export and education-sector semantics. Taranis brings capabilities that are generic and operationally expensive to reproduce independently:

- web/RSS/email and other OSINT collectors;
- worker/queue-based acquisition and processing;
- analyst refinement from unstructured news to structured stories/reports;
- presenters/publishers and report generation;
- deployment packaging beyond a single application container;
- existing enrichment hooks;
- a broader OSINT-oriented contributor ecosystem.

The integration therefore reduces duplicate engineering while retaining DTMO's differentiating governance and education focus.

## Recommended responsibility boundary

| Capability | Decision | Authoritative component | Rationale |
|---|---|---|---|
| Generic web/RSS/OSINT collection | **Replace / integrate** | Taranis AI | Mature collector/worker model; stop expanding duplicate DTMO generic crawlers |
| Education-sector curated source policy | **Keep** | DTMO | Governance, classification and sector relevance remain DTMO concerns |
| Source provenance | **Integrate** | Both, normalized by DTMO | Preserve upstream collection identity while retaining DTMO canonical evidence rules |
| Unstructured article processing | **Replace / integrate** | Taranis AI | Native OSINT/news workflow |
| Analyst story/report workflow | **Integrate** | Taranis AI + DTMO | Taranis structures OSINT; DTMO adds sector risk/governance context |
| Canonical education CTI record | **Keep** | DTMO | Existing persistence/provenance/governance boundary |
| Vulnerability prioritization | **Keep** | DTMO | CVSS/EPSS/KEV/vendor relevance and governance semantics are established |
| Generic IOC enrichment | **Replace future custom work** | IntelOwl | Taranis already has an integration path; avoid building a second generic analyzer engine |
| STIX knowledge graph | **Integrate** | OpenCTI | Avoid implementing a new graph engine inside DTMO |
| External CTI exchange | **Consolidate** | MISP + DTMO approval | MISP is exchange fabric; DTMO remains authority for governed outbound approval |
| Incident/case management | **Integrate later** | TheHive | Keep response cases separate from canonical CTI truth |
| Analyzer orchestration beyond IntelOwl | **Defer** | Cortex only if justified | Avoid duplicate enrichment stacks |
| Governance/framework mapping | **Keep** | DTMO | Normenkader IBP, ATT&CK and evidence relationships are DTMO differentiators |
| Administration/RBAC | **Integrate identities, keep policy boundary** | DTMO + platform IdP | Cross-service SSO/workload identity required; DTMO permissions remain authoritative for DTMO actions |
| Publishing/report delivery | **Integrate selectively** | Taranis for generic reports; DTMO for governed CTI sharing | Publishing capability must not bypass DTMO share authority |
| Platform deployment | **Adopt/harden** | Kubernetes/Helm/GitOps | Taranis upstream already provides a useful foundation; integrated topology still requires DTMO hardening |

## Taranis architecture observations

### Application services

Taranis documents four main service roles:

- `ingress` — Nginx reverse proxy;
- `frontend` — Flask/HTMX/Tailwind REST frontend;
- `core` — central backend and REST API;
- `worker` — RQ workers for collectors, bots, presenters and publisher functions.

Supporting services include PostgreSQL/SQLite, Redis and an SSE broker.

### Production-platform signals

Upstream deployment material currently includes:

- raw Kubernetes manifests;
- a Kubernetes optional-bot overlay;
- a Helm chart;
- an ArgoCD example;
- explicit secret/config placeholders;
- Kubernetes network-policy material;
- liveness/readiness checks;
- pinned-production-image guidance;
- SBOM attestations for published application images and CycloneDX SBOM release artifacts.

These are positive platform signals but are not, by themselves, DTMO production evidence. DTMO must validate the composed deployment, pin immutable images and add its own operational/security requirements.

### AI/NLP boundary

Taranis has consolidated several NLP/AI functions behind an optional `llm-bot` workload for summarization, title generation, NER, story clustering, sentiment and cybersecurity classification. For DTMO this must remain an optional, governed enrichment path. Model output must retain provenance and must never autonomously create compliance, compromise or external-sharing claims.

### IntelOwl

The existing Taranis IntelOwl bot can submit IOC types including CVE, IP, domain, URL, hash and email to configured analyzers. This makes IntelOwl the preferred first enrichment integration for DTMO rather than a new custom analyzer framework.

Security requirements for the DTMO target:

- dedicated service identity/token;
- secrets externalized from repository and screenshots;
- TLS verification outside local development;
- provider keys governed separately;
- email observables enabled only with approved privacy/data-processing scope;
- raw analyzer output preserved or referenced for provenance;
- enrichment semantics explicitly distinguished from local exposure or compromise.

### MISP

Taranis supports experimental Story-level MISP collaboration. DTMO already has governed read/export semantics. The target integration must therefore converge on one authority model instead of enabling two independent publication paths.

DTMO's existing rules remain the safer baseline:

- outbound sharing requires separate human approval;
- distribution/TLP is fail-closed;
- export creates an unpublished event unless separately authorized;
- service accounts do not gain autonomous share authority.

## Data-model mapping hypothesis

This is the starting contract for detailed 11.1 mapping and must be validated against the Taranis API before implementation.

| Taranis concept | DTMO target | Integration rule |
|---|---|---|
| source / collector | source catalogue + connector provenance | Stable upstream identity maps to a DTMO source record; collector execution is not itself canonical intelligence |
| news item | raw evidence + candidate canonical intelligence | Preserve original content reference, collection time and source identity |
| story | intelligence collection / assessed context | Do not automatically collapse multiple source items into one unsupported fact |
| report item / report | governed analytic product reference | Report content may enrich DTMO context but must preserve underlying evidence links |
| tag / IOC | observable/context | Normalize type/value; retain extraction origin and confidence |
| user/role | external identity/role mapping | Do not copy privilege semantics blindly; map through SSO/IdP and explicit service permissions |
| publisher action | publication intent | Must not become DTMO share approval |

## Trust boundaries introduced by integration

1. **Taranis → DTMO API boundary** — untrusted external-service input until schema, provenance and authorization checks pass.
2. **Taranis → IntelOwl boundary** — observable data leaves the collection system and may reach external analyzer providers.
3. **DTMO ↔ OpenCTI boundary** — graph/entity synchronization must preserve source identity, marking and confidence.
4. **DTMO → MISP boundary** — governed external sharing; highest authority sensitivity.
5. **DTMO → TheHive boundary** — intelligence becomes an operational case input but does not change canonical truth automatically.
6. **Shared identity/secrets boundary** — no shared superuser token across services; prefer workload identities and dedicated scopes.

## Licensing boundary

DTMO is distributed under Apache-2.0. Taranis AI is distributed under EUPL-1.2. This assessment does not provide a legal compatibility opinion. It establishes a conservative engineering rule:

> Integrate through documented APIs/services and do not vendor, copy or relicense Taranis source code into DTMO until a specific licensing review approves that action.

This also improves upgradeability and keeps upstream security fixes consumable.

## Deployment target

The preferred target is a composed Kubernetes platform with Helm/value-driven configuration and GitOps promotion. Taranis upstream deployment material can seed that design, but production DTMO requirements add:

- immutable image digests;
- external secrets management and rotation;
- SSO/OIDC and workload identity;
- explicit namespace/network-policy design;
- PostgreSQL HA/recovery objectives;
- Redis durability appropriate to RQ semantics;
- durable evidence/object storage;
- centralized audit/log/metric collection;
- backup and restore across all stateful services;
- SBOM/signing/vulnerability-policy gates;
- capacity, upgrade and rollback tests.

## Phase 11.1 gaps to close before coding the adapter

The next bounded work items are:

1. enumerate Taranis REST/OpenAPI endpoints required for source, news item, story, report and identity reads;
2. map exact request/response schemas to DTMO canonical models;
3. identify stable upstream identifiers and replay/deduplication keys;
4. define authentication, service account and least-privilege requirements;
5. define TLP/classification/provenance transformations;
6. decide polling versus event-driven/SSE integration boundaries;
7. identify which existing DTMO generic source code becomes deprecated after adapter acceptance;
8. produce threat-model abuse cases for malformed upstream data, replay, privilege escalation and publication bypass;
9. confirm licensing guidance for service integration and redistribution documentation;
10. define 11.2 contract tests and migration rollback criteria.

## Phase 11.1 exit decision

The current recommendation is **`PROCEED WITH SERVICE-TO-SERVICE TARANIS INTEGRATION`**, subject to the detailed API/data-model, identity and licensing checks above. No existing DTMO production `GO` is implied by this recommendation.

The immediate implementation priority after this assessment is the **Taranis → DTMO canonical adapter contract**, not additional generic DTMO collectors or UI features.