# DTMO Unified Operations Workbench

Status: **Phase 11.10a–11.10d PASS / REPOSITORY_COMPLETE; Phase 11.10e IN PROGRESS / INTEGRATED ANALYSIS**  
Visual reference: approved next-generation command-center concept (design target only, not evidence).

## Purpose

The Unified Operations Workbench is the target canonical DTMO browser experience. It converts the already integrated DTMO framework into one professional operational product instead of exposing only a fraction of each underlying capability through disconnected views.

The workbench is task- and object-oriented. Users should normally operate DTMO without having to decide which upstream platform UI to visit.

## Target shell

The workbench follows a stable four-zone composition:

- **left navigation** for functional domains;
- **top command/status bar** for global search, candidate/environment state, notifications and principal context;
- **main workspace** for the current operational task;
- **right context rail** for selected-object facts and governed actions.

Phase 11.10b accepted this shell foundation under `/workbench/`. The command palette is navigation-only in the accepted shell, the context rail starts with an explicit no-selection state and later workspace routes do not fabricate feature data.

Phase 11.10c accepted the first functional workspace: the Command Center. Its KPI layer, recent-intelligence view, integration capability view, role-aware navigation and workflow orientation use attributable DTMO read models and explicit degraded/unavailable states.

Phase 11.10d accepted the functional migration of Threat Intelligence and IOC Explorer. It reuses governed DTMO search and canonical-detail/provenance APIs rather than introducing direct browser-to-upstream access or a second intelligence backend.

Phase 11.10e is the active functional migration of Analysis & Enrichment. It combines persisted IntelOwl enrichment and analyzer-only Cortex evidence against one canonical DTMO object, while retaining human-triggered execution and server-side authorization.

## Primary journey

The end-state journey is:

**Collect → Normalize → Enrich → Correlate → Investigate → Respond → Share → Learn**.

A representative analyst journey is:

1. receive or discover intelligence;
2. inspect provenance and severity;
3. select an IOC/entity/CVE;
4. run IntelOwl enrichment where authorized;
5. run bounded Cortex analysis where authorized;
6. inspect OpenCTI relationships;
7. correlate with MISP and existing canonical intelligence;
8. create or link a TheHive case when human-authorized;
9. complete investigation tasks;
10. prepare a governed sharing package;
11. obtain separate human publication/share approval;
12. review evidence, timeline and audit state.

The normal journey remains inside DTMO.

## Command Center

The accepted Phase 11.10c Command Center provides a truthful operational picture, not decorative pseudo-data.

### KPI layer

The implemented canonical read model includes total intelligence objects, high/critical intelligence, new intelligence in the preceding 24 hours, candidate intelligence pending review, reviewed intelligence awaiting a separate external-share decision and intelligence with education relevance of at least 80. A missing canonical datastore produces `unavailable`/`null`, not synthetic zero values.

### Threat intelligence panel

Phase 11.10c includes recent canonical intelligence with source, severity, education relevance, review state and discovery time. Phase 11.10d provides the deeper governed intelligence discovery/investigation workspace.

### Framework integration panel

Phase 11.10c shows governed capability/configuration state for Taranis AI, IntelOwl, OpenCTI, MISP, TheHive and Cortex. A feature flag or configured API base never means `healthy`. Persisted connector execution may be shown only as attributable runtime observation and is not promoted to a general upstream-health claim.

### Quick actions

Phase 11.10c exposes role-aware navigation based on server-issued permissions. Visibility is usability only. Review, analysis, source execution, case handoff, sharing and administration remain separately server-authorized.

## Unified Intelligence Workspace

Phase 11.10d provides accepted functional `/workbench/intelligence` and `/workbench/intelligence/iocs` routes.

The workspace deliberately separates two evidence layers:

1. **discovery projection** — `/api/v1/intelligence/search` returns indexed search results;
2. **canonical investigation** — `/api/v1/intelligence/{item_id}/workspace` returns the selected DTMO object and provenance from canonical persistence.

The interface exposes explicit query submission, severity, minimum education relevance and result-limit filters. It does not fabricate demonstration intelligence before search. A search failure is shown as unavailable rather than as an empty dataset, and a canonical-detail failure does not reconstruct missing object fields from the search result.

Both routes remain read-only and use server-side `read:intelligence`. Search or selection grants no review, publication/share approval, connector/analyzer execution, case mutation or administration authority.

## Integrated Analysis Workspace

Phase 11.10e provides the active `/workbench/analysis` slice.

The workspace keeps analysis object-centric:

- one canonical intelligence item can be selected directly or deep-linked using `?item=<uuid>`;
- `GET /api/v1/analysis/capabilities` shows explicit configured IntelOwl/Cortex observable/analyzer allowlists without making a runtime-health claim;
- `GET /api/v1/analysis/items/{item_id}/history` combines persisted IntelOwl and Cortex evidence;
- the existing IntelOwl execution path remains governed by `review:intelligence`;
- `POST /api/v1/analysis/items/{item_id}/cortex` executes one explicit analyzer-only Cortex job and persists bounded evidence;
- read-only principals can inspect history but execution controls are not presented as authorized.

Cortex responders, automatic analyzer discovery and automatic IntelOwl fallback are deliberately excluded. Durable Cortex evidence carries no external-share authority and does not prove local compromise. Failures remain explicit and **fail closed** rather than producing synthetic successful analysis.

## Object-centric workspace

Every compatible canonical object should open a shared context model with tabs such as:

- Overview;
- Evidence;
- Enrichment;
- Relationships/Graph;
- Vulnerabilities/Exposure;
- Cases/Tasks;
- Sharing;
- Timeline/Audit.

The right context rail may expose counts/status from IntelOwl, Cortex, OpenCTI, MISP and TheHive without requiring a separate upstream login. Until a bounded feature slice supplies attributable data, the rail must state that no object is selected rather than infer facts.

The object-centric intelligence experience began with **Phase 11.10d Unified Intelligence Workspace**. Phase 11.10e adds governed analysis; later 11.10f–11.10h slices add graph, exchange and case capabilities without bypassing the DTMO API boundary.

## Integrated capability expectations

### Taranis AI

Collection/assessment capabilities remain an upstream service boundary but source, collection and canonicalization operations exposed to normal operators should be governed through DTMO Collection workspaces.

### IntelOwl

Phase 11.10e exposes explicit analyzer selection, job state and persisted bounded enrichment history through the DTMO workbench. IntelOwl results do not grant publication/share authority or prove local compromise.

### OpenCTI

DTMO should expose entity/relationship exploration, graph expansion, filtering, markings/confidence and relationship provenance through the canonical workbench in 11.10f.

### MISP

DTMO should expose inbound events/matches/correlations and governed outbound draft/review/approval workflows. Technical connectivity never grants sharing authority.

### TheHive

DTMO should expose daily case, task, observable, assignment and timeline operations subject to accepted case-handoff authority.

### Cortex

Phase 11.10e exposes bounded analyzer execution and durable result history. Responders or autonomous side effects remain excluded until separately governed and explicitly accepted.

### Vulnerability intelligence

CVE/KEV/CVSS/EPSS and education relevance should be correlated with actors, campaigns, IOCs, cases and affected technology where attributable data exists.

## Workflow/automation target

The future playbook surface uses explicit execution classes:

- `AUTOMATIC`;
- `HUMAN APPROVAL REQUIRED`;
- `MANUAL`;
- `PROHIBITED`.

No graphical workflow may bypass RBAC, case authority, publication/share approval or other server-side controls.

## Role-aware defaults

The same product can present different default workspaces for Executive/security leadership, CISO, SOC analyst, CTI analyst, Incident responder, Administrator and Auditor. Role-aware layout is for efficiency only; backend authorization remains authoritative.

## Visual direction

The target is a dense but calm SOC-grade interface with dark operations mode plus accessible light mode, clear hierarchy, semantic status/severity treatment, persistent context, compact drill-down surfaces, keyboard-first operation, responsive layouts and truthful loading/empty/degraded states. The design must not imitate a decorative 'Hollywood hacker' interface.

## Candidate-completion sequence

The interface programme is executed as bounded Phase 11.10 candidate-completion slices:

- 11.10a frontend architecture/design contract — `PASS / REPOSITORY_COMPLETE`;
- 11.10b canonical application shell — `PASS / REPOSITORY_COMPLETE`;
- 11.10c Command Center — `PASS / REPOSITORY_COMPLETE`;
- 11.10d Unified Intelligence Workspace — `PASS / REPOSITORY_COMPLETE`;
- 11.10e IntelOwl/Cortex integrated analysis — active;
- 11.10f OpenCTI graph/entity workspace — next after 11.10e acceptance/merge;
- 11.10g MISP Sharing & Exchange;
- 11.10h TheHive Investigations & Cases;
- 11.10i Vulnerability & Exposure;
- 11.10j Sources & Collection;
- 11.10k Automation & Playbooks;
- 11.10l Governance & Evidence;
- 11.10m Operations & Administration;
- 11.10n role-aware UX/accessibility;
- 11.10o consolidation/full functional acceptance;
- 11.10p fresh production-equivalent exercise against the frozen integrated candidate.

Phase 11.11 remains blocked until 11.10p is explicitly accepted.

## Evidence boundary

This document is product/UX architecture. The graphical reference and repository documentation are not evidence of live integration, staging acceptance, production-equivalent validation or production authorization. Repository/browser CI for 11.10e does not prove live IntelOwl/Cortex availability, analyzer/provider authorization or service health.
