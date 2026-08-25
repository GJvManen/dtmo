# Phase 11.10q — Functional Completeness Remediation Audit

Status: **IN PROGRESS / OWNER FUNCTIONAL REJECTION**

## Why this phase exists

The integrated candidate at `17e31a839a16a250a94b00a67b3ddd0a8c88fbbf` passed repository gates but was rejected during functional owner review. Green CI did not establish that the workbench contained useful data, populated graph context, active framework integrations or operator-grade visual analytics.

Phase 11.11 external assurance is therefore superseded until functional completeness is restored and a new immutable candidate is produced.

## Confirmed blocking findings

### FQ-01 — Framework integrations disabled by default

`backend/dtmo/config.py` defaults the major integration feature flags to `False` and their API bases to empty strings. `backend/dtmo/command_center.py` correctly converts those values into `disabled` / `configuration-required` states. This is fail-closed from a security perspective, but the shipped/default operational experience is functionally empty and does not guide an operator through activation/readiness.

Required remediation:
- expose a clear integration inventory and activation/readiness model in the Command Center;
- distinguish disabled-by-policy, not-configured, configured, reachable, ingesting and degraded states;
- provide operator-safe activation/configuration guidance without exposing secrets to the browser;
- ensure supported integrations can be enabled through documented deployment configuration and are visible in one place.

### FQ-02 — IOC Explorer is not a real IOC workspace

`frontend/src/UnifiedIntelligenceWorkspace.tsx` reuses the generic intelligence search path and only changes labels for IOC mode. Before a user submits a query, no indicator content is loaded. There is no indicator inventory, type distribution, recent indicators, source distribution, enrichment status or pivot workflow.

Required remediation:
- add a first-class IOC read model and API;
- populate indicator rows from canonical persisted intelligence/provenance;
- support IP/domain/URL/hash/CVE/other observable facets;
- add useful initial content, filters, counts and pivots without synthetic demo data;
- link indicators directly to intelligence detail, enrichment and graph context.

### FQ-03 — Threat Intelligence and enrichment platforms are fragmented

`frontend/src/UnifiedIntelligenceWorkspace.tsx` and `frontend/src/AnalysisWorkspace.tsx` are separate manual UUID-driven flows. Analysts must copy a canonical item ID into the analysis workspace and manually enter observables before IntelOwl/Cortex can be used.

Required remediation:
- integrate enrichment history and available actions into intelligence object detail;
- extract/present canonical observables from persisted intelligence;
- provide governed one-click pivots into IntelOwl/Cortex for authorized users;
- return enrichment results into the same investigation context;
- preserve explicit review authority and server-side credentials.

### FQ-04 — Knowledge Graph is empty unless mappings already exist

`frontend/src/OpenCTIGraphWorkspace.tsx` requires a manually supplied canonical UUID and renders only already-persisted DTMO-to-OpenCTI mappings. It does not provide a populated landing view, discover graphable objects, or make empty mapping coverage operationally visible.

Required remediation:
- provide graphable-item discovery from canonical intelligence;
- persist and expose OpenCTI mapping coverage for eligible objects;
- surface mapping/collection status and last successful observation;
- support navigation from intelligence and IOC objects directly into graph context;
- render only attributable persisted relationships and remain fail-closed where topology is absent.

### FQ-05 — Browser graph acceptance is fixture-driven

`backend/tests/test_phase11_10f_opencti_graph_browser.py` intercepts and fulfils capability, graph and entity endpoints with static JSON. This validates browser rendering but cannot establish that the deployed application has populated graph data.

Required remediation:
- retain deterministic component tests, but add an unmocked functional journey over seeded/canonical repository-controlled persisted data;
- separately exercise real same-origin APIs and persistence;
- acceptance must fail if expected canonical content is not actually available.

### FQ-06 — Operator-grade charts/trends are absent from the canonical frontend

`frontend/package.json` contains React, React Router and React Query but no charting/visualization dependency. The OpenCTI workspace uses a bespoke SVG node rendering, but there is no reusable chart system for Command Center / intelligence / source / vulnerability / operations trends.

Required remediation:
- add an accessible visualization layer;
- provide meaningful time-series and distribution charts sourced from canonical APIs;
- include text/table equivalents and non-color cues;
- no synthetic values may be used to make dashboards appear populated.

## Framework-wide audit scope

Before acceptance, audit and reconcile all canonical workspaces:

1. Command Center — operational summary, integration inventory, trends, recent intelligence and collection state.
2. Threat Intelligence — populated initial view, search, provenance, observables, enrichment and pivots.
3. IOC Explorer — first-class indicator inventory and filters.
4. Analysis & Enrichment — IntelOwl/Cortex integration inside analyst workflow.
5. Knowledge Graph — graphable-object discovery and persisted OpenCTI mapping coverage.
6. Sources & Collection — usable source inventory, activation state, run status, freshness and ingestion counts.
7. Vulnerability & Exposure — populated vulnerability intelligence, prioritization and trend views.
8. Investigations — TheHive case visibility/handoff continuity.
9. MISP Sharing — candidate/review/share state and attributable transfer history.
10. Automation & Playbooks — enabled playbooks, execution history and authority state.
11. Governance & Evidence — framework mappings and evidence remain functional.
12. Operations & Administration — health, jobs, roles and mutation authority remain usable.

## Data/content acceptance rule

A workspace is not functionally complete merely because it renders an empty state correctly. For the repository-controlled functional candidate, canonical bootstrap/seed data must exercise representative object types and cross-workspace relationships without pretending to be live external evidence. The UI must clearly label repository-controlled sample/bootstrap content as such when used for local functional acceptance.

Live connector state must remain attributable and must never be fabricated. Production-equivalent and external-assurance claims remain separate later gates.

## New acceptance sequence

1. complete Phase 11.10q functional remediation;
2. conduct owner functional retest against the integrated application;
3. freeze a **new** immutable candidate;
4. repeat fresh production-equivalent validation for that candidate;
5. only then restart Phase 11.11 independent external assurance;
6. Phase 12 remains blocked until all prior gates are accepted.
