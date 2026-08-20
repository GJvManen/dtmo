# DTMO Unified Operations Workbench

Status: **Phase 11.10a PASS / REPOSITORY_COMPLETE; Phase 11.10b IN PROGRESS / CANONICAL SHELL IMPLEMENTATION**  
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

Phase 11.10b implements this shell foundation under `/workbench/`. The command palette is navigation-only in this slice, the context rail starts with an explicit no-selection state and later workspace routes do not fabricate feature data.

The Command Center additionally uses a KPI row, operational widgets and a workflow strip inspired by the approved graphical reference; that functional content remains Phase 11.10c scope.

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

## Command Center target

The Command Center provides a truthful operational picture, not decorative pseudo-data.

### KPI layer

Candidate metrics include:

- threats/new intelligence;
- IOC matches;
- active incidents/cases;
- high-risk vulnerabilities;
- system/integration health;
- pending human approvals.

Every metric must have a defined canonical source, freshness rule and empty/degraded state before implementation.

### Threat intelligence panel

May include:

- recent/high-priority intelligence;
- severity trend;
- campaign/actor activity;
- vulnerability exploitation context;
- education relevance;
- geographic context only when source data justifies it.

### Security operations panel

May include:

- open/in-progress cases;
- unassigned work;
- SLA warnings;
- pending enrichment/analysis;
- pending decision/approval;
- recently resolved work.

### Framework integration panel

Shows attributable health and activity for DTMO plus governed Taranis AI, IntelOwl, OpenCTI, MISP, TheHive and Cortex integration paths. Green status must mean a specifically defined health check, not assumed service availability.

### Quick actions

Role- and context-aware actions may include search, analyze IOC, create case, run source, start enrichment, prepare sharing, generate report and inspect system health. Server authorization remains authoritative.

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

## Integrated capability expectations

### Taranis AI

Collection/assessment capabilities remain an upstream service boundary but source, collection and canonicalization operations exposed to normal operators should be governed through DTMO Collection workspaces.

### IntelOwl

DTMO should expose analyzer selection, job state, normalized findings, provenance, partial failures and raw evidence references where permitted.

### OpenCTI

DTMO should expose entity/relationship exploration, graph expansion, filtering, markings/confidence and relationship provenance through the canonical workbench.

### MISP

DTMO should expose inbound events/matches/correlations and governed outbound draft/review/approval workflows. Technical connectivity never grants sharing authority.

### TheHive

DTMO should expose daily case, task, observable, assignment and timeline operations subject to accepted case-handoff authority.

### Cortex

DTMO should expose bounded analyzer execution and result history. Responders or autonomous side effects remain excluded until separately governed and explicitly accepted.

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

The same product can present different default workspaces for:

- Executive/security leadership;
- CISO;
- SOC analyst;
- CTI analyst;
- Incident responder;
- Administrator;
- Auditor.

Role-aware layout is for efficiency only; backend authorization remains authoritative.

## Visual direction

The target is a dense but calm SOC-grade interface:

- dark operations mode plus accessible light mode;
- clear hierarchy and restrained accent usage;
- high information density without decorative noise;
- semantic status and severity treatment;
- persistent context;
- compact tables/cards with drill-down;
- keyboard-first operation for analyst workflows;
- responsive layouts;
- truthful loading, empty and degraded states.

The design must not imitate a decorative 'Hollywood hacker' interface.

## Candidate-completion sequence

The interface programme is executed as bounded Phase 11.10 candidate-completion slices:

- 11.10a frontend architecture/design contract — `PASS / REPOSITORY_COMPLETE`;
- 11.10b canonical application shell — active;
- 11.10c Command Center;
- 11.10d Unified Intelligence Workspace;
- 11.10e IntelOwl/Cortex analysis;
- 11.10f OpenCTI graph/entity workspace;
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

This document is product/UX architecture. The graphical reference and repository documentation are not evidence of live integration, staging acceptance, production-equivalent validation or production authorization.
