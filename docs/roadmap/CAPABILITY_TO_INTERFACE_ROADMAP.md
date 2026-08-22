# DTMO Capability-to-Interface Roadmap

Status: `ACTIVE / FUNCTIONAL REMEDIATION`

## Why this roadmap exists

The owner functional review of candidate `17e31a839a16a250a94b00a67b3ddd0a8c88fbbf` established that repository completeness and green CI did not equal usable product completeness. DTMO already contains substantially more backend capability than the canonical React workbench exposes. A large part of the platform remains hidden behind legacy `/ui/*` pages, direct APIs, manual UUID entry, feature flags, operator-only routes or isolated point workspaces.

The goal of Phase 11.10q is therefore not to add decorative screens. It is to expose the already-governed technical capability coherently through one canonical workbench, add missing operator workflows where the backend supports them, and identify genuinely missing backend functions separately.

## Architectural rule

The canonical user path remains:

`browser -> DTMO same-origin API -> governed DTMO service/persistence -> governed integration or evidence source`

The interface must never become a privileged direct client for MISP, OpenCTI, IntelOwl, Cortex, TheHive, Taranis, AIL or other upstream services. Existing RBAC, human review/share/publication authority, replay protection, provenance and fail-closed semantics remain authoritative.

## Existing technical capability that is currently under-exposed

The backend already mounts a broad control plane: intelligence search/detail and persistence, connector execution, source registry/bootstrap, graphical dashboard summary data, operations metrics, vulnerability analytics, framework governance, governance crosswalks, governance knowledge, MISP read/export, IntelOwl execution, OpenCTI entity mappings, TheHive handoff, RBAC administration, source administration, UX preferences, audit/CISO surfaces, severity/analytics experience and multiple legacy unified-console extensions.

Specific examples that must be reused rather than rebuilt:

- `/api/v1/dashboards/summary` already provides total intelligence, 24h volume, confidence, severity distribution, review status, source distribution, connector health and a seven-day trend;
- `/api/v1/operations/summary` already provides requests, in-flight requests, latency, active alerts, queue backlog, traces and connector runs;
- source control already supports catalog visibility, bootstrap registration, enable/disable, health, manual runs, provenance and circuit/isolation state;
- vulnerability analytics already projects CVSS v2/v3/v4, EPSS, KEV, vendors, products, CWEs and sightings from canonical evidence;
- framework governance already exposes versioned frameworks, explicit mappings, coverage, review state and provenance;
- RBAC administration already supports managed principals, immutable role catalog, role assignment, activation state and audit/token-reissue boundaries;
- AIL correlation logic already exists for exact-match investigation context across canonical intelligence, MISP and vulnerability context;
- MISP has governed read and export paths with distribution/TLP/replay/share-approval controls;
- IntelOwl and Cortex execution/history exist but are currently detached from the normal Threat Intelligence investigation flow;
- OpenCTI mappings/entities/revisions exist but discovery currently depends on manually knowing a canonical UUID.

## Product information architecture target

The canonical workbench will converge on eight user-facing domains:

1. **Command Center** — platform overview, actionable health, trends, framework integration status and work queues.
2. **Intelligence** — Threat Intelligence, IOC Explorer, correlations, enrichment, graph/entity context and pivots.
3. **Exposure** — vulnerability intelligence, prioritisation, KEV/EPSS/CVSS, sightings and affected technology context.
4. **Investigations** — TheHive cases/handoffs, evidence, status and controlled transitions.
5. **Sharing** — MISP read context, approval queue, export state, TLP/distribution and audit trail.
6. **Sources & Collection** — catalog, activation, schedules, health, collection runs, source provenance and onboarding.
7. **Governance & Assurance** — Normenkader IBP, MITRE ATT&CK, NIST CSF, CVSS context, mappings, coverage, evidence and audit.
8. **Operations & Administration** — runtime health, alerts, queues, storage/search state, RBAC, principals, connector configuration and preferences.

Legacy `/ui/*` implementations are treated as capability donors until their functionality is absorbed into the canonical workbench. They are not a reason to duplicate business logic.

## Delivery sequence

### 11.10q1 — Capability inventory and API/UI traceability

Build a machine-readable inventory of mounted routers, APIs, permissions, persistence models, legacy pages and React consumers. Every meaningful backend capability receives one status: `EXPOSED`, `PARTIAL`, `LEGACY_ONLY`, `API_ONLY`, `HIDDEN_BY_FLAG`, or `MISSING_UI_WORKFLOW`.

Acceptance: a traceability matrix can answer, for every mounted capability, where an operator uses it in the canonical interface or why it is intentionally not user-facing.

### 11.10q2 — Canonical data/bootstrap and integration readiness

Provide deterministic local-functional bootstrap content through governed repository-owned loaders. Bootstrap data must include representative intelligence, IOCs, CVEs, provenance, source states, OpenCTI mappings, enrichment history, MISP context, investigation references, governance mappings and operational states. It must be unmistakably labelled non-live/bootstrap and must never be accepted as production evidence.

Add an integration-readiness model that distinguishes: feature available, configured, credentials present/absent without secret disclosure, enabled, scheduled, last run, last success, degraded/isolated and externally unreachable/not tested.

Acceptance: a fresh local deployment is useful immediately for product evaluation without pretending that external services are live.

### 11.10q3 — Command Center 2.0 and visual analytics foundation

Move existing dashboard capability into the canonical React workbench. Add accessible visual components with table equivalents for:

- intelligence volume trend;
- severity distribution;
- source distribution;
- review/share queues;
- connector health and freshness;
- framework integration readiness;
- vulnerability risk distribution;
- active operational alerts;
- ingestion/processing activity.

The Command Center must show why an integration is disabled or unavailable and provide a governed pivot to its configuration or source-control surface when the user has permission.

Acceptance: no primary platform state should require opening a legacy dashboard page.

### 11.10q4 — Threat Intelligence Investigation Hub

Replace the current search-plus-detail island with a true investigation workspace. On selecting intelligence, show canonical metadata, provenance, source reliability, confidence, severity, education relevance, tags, CVEs, linked IOCs, vulnerability context, AIL correlations, available OpenCTI context, existing IntelOwl/Cortex history, MISP origin/share state and TheHive handoff state in one investigation view.

Provide one-click governed pivots to Analyze, Graph, Case and Share without manually copying UUIDs.

Acceptance: an analyst can start with one intelligence object and traverse all permitted related DTMO capabilities without retyping identifiers.

### 11.10q5 — IOC Explorer 2.0

Create a real IOC inventory rather than a renamed generic text search. Introduce canonical indicator projection from persisted intelligence/evidence with indicator type, normalized value, first/last seen, source count, source list, confidence, severity/context, TLP/handling where attributable, enrichment status, correlation count and linked intelligence count.

Views: recent IOCs, high-interest IOCs, by type, by source, correlated indicators, enriched/not-enriched and saved filter state. Support domain, IP, URL, hash, hostname/FQDN, CVE-linked and other explicitly supported indicator types.

Acceptance: IOC Explorer is populated from canonical persisted data and useful before the user enters a search query.

### 11.10q6 — Integrated Enrichment & Analysis

Embed IntelOwl and Cortex into the intelligence/IOC investigation flow. The UI should derive eligible observables from the selected object, show allowlisted analyzers, preserve handling/TLP controls and expose previous runs, partial/degraded status and persisted results.

Add batch-selection only where server-side permissions, limits and replay controls are explicit. No responder action is added merely because Cortex exists.

Acceptance: no manual UUID or observable copy/paste is needed for the common analysis journey.

### 11.10q7 — Knowledge Graph 2.0

Add graph discovery instead of requiring a known UUID. Provide graph entry from intelligence, IOC, actor/campaign/malware/entity search and recent mapped objects. Render persisted DTMO-to-OpenCTI mappings and any explicitly persisted relationship topology with filters by entity type, confidence, marking and time.

Support side-panel entity detail, revision history, provenance, external references and pivots back to canonical intelligence/IOCs. Never synthesize entity-to-entity relationships that are not persisted.

Acceptance: a populated deployment presents discoverable graph content without manual UUID entry.

### 11.10q8 — Vulnerability & Exposure Center 2.0

Promote existing vulnerability analytics fully into the canonical workbench. Expose CVSS v2/v3/v4, EPSS, KEV, vendor/product, CWE and sightings together with trends, risk bands, source provenance and links to related intelligence/IOCs.

Add filters and pivots: newly observed, KEV, high EPSS, critical CVSS, vendor/product, CWE, sighting type, correlated intelligence and education-relevant context. Explicitly distinguish threat intelligence from local asset exposure unless a real asset/exposure source exists.

Acceptance: existing vulnerability backend depth is visible and navigable without using legacy console pages.

### 11.10q9 — Sources, Collection and Framework Integrations

Unify source catalog, registration, enable/disable, scheduling, manual execution, last-success/failure, consecutive failures, isolation/circuit state, provenance and per-integration configuration readiness.

Surface CISA KEV, OpenCVE, Vulnerability-Lookup, MISP, AIL, Taranis and other supported catalog sources. IntelOwl, Cortex, OpenCTI and TheHive appear as framework integrations with capability-specific readiness even when they are not scheduled ingestion feeds.

Acceptance: the Command Center no longer shows unexplained `disabled`; operators can see the exact governed next action required to make a capability usable.

### 11.10q10 — Investigations, Sharing and Workflow Continuity

Bring TheHive handoff/case state and MISP governed sharing into the same object-centric workflow. Show review state, share approval, export eligibility, replay/previous export state, TLP/distribution constraints and case/handoff status on the selected intelligence object.

Add work queues for pending review, pending share approval, failed/degraded handoffs and items needing analyst action. Preserve separate authorities.

Acceptance: analysts can understand lifecycle state without switching conceptual models between disconnected screens.

### 11.10q11 — Governance, Audit and Administration 2.0

Expose the existing governance and administrative depth consistently in React:

- Normenkader IBP / MITRE / NIST / CVSS framework cards and explicit mapping detail;
- coverage and unmapped/pending/rejected mappings;
- provenance and evidence registry;
- audit/searchable decision history;
- managed principals and immutable role catalog;
- principal creation/activation/role assignment;
- security/CISO controls where authorized;
- source and integration administration;
- user display preferences.

Do not recreate custom roles if policy deliberately defines an immutable role catalog; instead make the limitation explicit and usable.

Acceptance: Administration becomes an actual control plane rather than a navigation page.

### 11.10q12 — Operations & Observability 2.0

Expose the existing operations summary and deeper health signals as operator-grade UI: request volume, latency, in-flight requests, active alerts, queue backlog, connector runs, trace context, storage integrity, search health, connector alerts and API errors.

Add time-window trends where persisted/observable data supports them, alert drill-downs, correlation/request IDs, runbook links and clear degraded-state explanations. Grafana may remain an advanced external observability tool, but basic operational understanding must not require separate Grafana authentication.

Acceptance: a platform operator can identify what is degraded, where, since when and what governed action/runbook applies from the DTMO workbench.

### 11.10q13 — Cross-workspace navigation, saved views and role-aware UX

Standardize deep links and contextual actions so canonical object IDs are passed internally rather than typed manually. Add breadcrumbs, recent objects, saved filters/views, role-aware action visibility, keyboard navigation, accessible chart alternatives, responsive behavior and consistent status vocabulary.

Acceptance: the platform behaves as one application rather than a collection of screens.

### 11.10q14 — Unmocked functional acceptance and owner retest

Replace mock-heavy critical browser acceptance with tests that start the real DTMO API/persistence stack, load governed bootstrap content, exercise same-origin APIs and verify real persisted state transitions. Mocks remain acceptable for isolated unit/component tests but not as the sole proof of functional completeness.

Minimum real journeys:

1. bootstrap -> source status -> ingest -> Command Center trend changes;
2. intelligence object -> IOC -> enrichment -> persisted history;
3. intelligence object -> OpenCTI mappings -> rendered graph/entity detail;
4. intelligence object -> TheHive handoff state;
5. reviewed/share-approved object -> governed MISP export preconditions;
6. CVE -> vulnerability analytics -> related intelligence pivot;
7. framework -> mapping detail -> evidence/provenance;
8. admin -> principal/role operation -> audited state;
9. operations -> induced controlled degraded condition -> visible alert/recovery.

Owner functional acceptance is required after these journeys pass. Green CI alone is not acceptance.

## Capability prioritisation

Priority A — product usability blockers: bootstrap/content, Command Center, IOC inventory, integrated Threat Intelligence, enrichment pivots, Knowledge Graph discovery, source/integration readiness.

Priority B — operational depth: vulnerability analytics, investigations, MISP sharing lifecycle, operations/alerts, RBAC and governance.

Priority C — productivity and polish: saved views, advanced filtering, cross-workspace navigation, accessibility refinement and personalization.

## Release consequence

Phase 11.11 remains stopped. The previous Phase 11.10p candidate is functionally rejected. Product-affecting 11.10q changes require a new immutable candidate, a fresh production-equivalent validation cycle, a fresh owner functional acceptance and only then new independent external assurance. Phase 12 remains blocked.
