# DTMO Unified Operations Workbench

Status: **Phase 11.10a–11.10g PASS / REPOSITORY_COMPLETE; Phase 11.10h IN PROGRESS / THEHIVE INVESTIGATIONS & CASES**  
Visual reference: approved next-generation command-center concept (design target only, not evidence).

## Purpose

The Unified Operations Workbench is the canonical DTMO browser experience. It converts the integrated DTMO framework into one professional operational product instead of exposing only a fraction of each underlying capability through disconnected views. The workbench is task- and object-oriented; users should normally operate DTMO without having to decide which upstream platform UI to visit.

## Target shell

The workbench follows a stable four-zone composition:

- **left navigation** for functional domains;
- **top command/status bar** for global search, candidate/environment state, notifications and principal context;
- **main workspace** for the current operational task;
- **right context rail** for selected-object facts and governed actions.

Phase 11.10b accepted this shell foundation under `/workbench/`. Phase 11.10c accepted the Command Center. Phase 11.10d accepted Threat Intelligence and IOC Explorer. Phase 11.10e accepted Analysis & Enrichment. Phase 11.10f accepted persisted OpenCTI graph/entity context. Phase 11.10g accepted governed MISP Sharing & Exchange. Phase 11.10h is the active migration of TheHive Investigations & Cases into the same shell.

## Primary journey

The end-state journey is:

**Collect → Normalize → Enrich → Correlate → Investigate → Respond → Share → Learn**.

A representative analyst journey is:

1. receive or discover intelligence;
2. inspect provenance and severity;
3. select an IOC/entity/CVE;
4. run IntelOwl enrichment where authorized;
5. run bounded Cortex analysis where authorized;
6. inspect attributable OpenCTI graph/entity evidence;
7. correlate with MISP and canonical intelligence;
8. create a TheHive case through explicit human `handoff:case` authority when canonical provenance and handling prerequisites are satisfied;
9. reconcile any uncertain/ambiguous handoff before further case mutation;
10. prepare a governed sharing package;
11. record independent human review and separate external-share approval;
12. export an approved canonical revision as an unpublished MISP event where authorized;
13. review attributable DTMO evidence and audit state.

The normal journey remains inside DTMO.

## Accepted functional workspaces

### Command Center

Phase 11.10c provides a truthful operational picture using canonical read models. Missing canonical data produces unavailable/null state rather than synthetic zero values. Integration configuration never becomes an automatic `healthy` claim.

### Unified Intelligence Workspace

Phase 11.10d provides `/workbench/intelligence` and `/workbench/intelligence/iocs`. Indexed search is a discovery projection; selected detail comes separately from canonical DTMO persistence. Search/detail failures **fail closed**. Both routes require server-side `read:intelligence` and grant no mutation authority.

### Integrated Analysis Workspace

Phase 11.10e provides `/workbench/analysis`. Capability/history reads require `read:intelligence`; human-triggered IntelOwl/Cortex analyzer execution requires `review:intelligence`. Cortex responders, autonomous side effects and local-compromise inference remain excluded.

### OpenCTI Graph / Entity Workspace

Phase 11.10f provides `/workbench/intelligence/graph` through DTMO-owned read APIs. The browser never receives OpenCTI credentials and does not call OpenCTI `/graphql` directly. Only attributable persisted `canonical-mapping` relationships are rendered because the accepted DTMO persistence boundary does not durably store generic OpenCTI entity-to-entity topology. Missing topology evidence **fails closed**.

### MISP Sharing & Exchange Workspace

Phase 11.10g provides `/workbench/sharing` without introducing a parallel sharing authority. The canonical flow is **inspect canonical state → human review → separate human share approval → unpublished MISP export**. The browser uses DTMO APIs only; server-side RBAC remains authoritative; source handling restrictions and replay evidence fail closed; the accepted exporter creates `published=false` events and exposes no MISP Publish or Synchronize action.

## Active TheHive Investigations & Cases Workspace

Phase 11.10h makes `/workbench/investigations` functional while preserving the accepted Phase 11.6 case-handoff authority and persistence boundary.

The browser uses DTMO APIs only:

- `GET /api/v1/thehive/items/{item_id}/investigation` for canonical intelligence, provenance and durable handoff state;
- `POST /api/v1/thehive/items/{item_id}/cases` for an explicit human-authorized case handoff.

Canonical reads require `read:intelligence`; case mutation requires `handoff:case`. Service accounts cannot substitute for human case authority. The browser never receives TheHive credentials or organization authorization.

Canonical provenance is required before mutation. TLP/PAP and authoritative source restrictions fail closed. Durable `reserved`, `delivered`, `ambiguous` and `failed` evidence is presented. A `reserved` or `ambiguous` handoff requires **manual reconciliation** and the canonical workspace blocks a blind new case request.

A delivered handoff proves only the stable case identity returned at creation time and persisted by DTMO. The accepted Phase 11.6 persistence does not mirror generic TheHive alerts, tasks, case timeline, later case state or responder results, so Phase 11.10h does not fabricate them or treat their absence as evidence.

Configuration does not establish live TheHive health. Handoff/case presence does not grant external-share authority or prove responder execution, downstream remediation or local compromise.

## Object-centric workspace

Every compatible canonical object should open a shared context model with tabs such as Overview, Evidence, Enrichment, Relationships/Graph, Vulnerabilities/Exposure, Cases/Tasks, Sharing and Timeline/Audit where those facts are attributable.

The right context rail may expose attributable counts/status from IntelOwl, Cortex, OpenCTI, MISP and TheHive without requiring a separate upstream login. Until a bounded feature slice supplies attributable data, missing facts are not inferred.

The object-centric experience began with 11.10d; 11.10e added analysis, 11.10f added persisted OpenCTI graph/entity context, 11.10g added governed sharing/exchange, and 11.10h adds canonical investigation plus durable TheHive handoff/reconciliation evidence.

## Integrated capability expectations

### Taranis AI
Collection/assessment remains an upstream service boundary; normal operator workflows should be governed through DTMO Collection surfaces.

### IntelOwl
Phase 11.10e exposes explicit analyzer selection, job state and persisted bounded enrichment history. Results do not grant publication/share authority or prove local compromise.

### OpenCTI
Phase 11.10f exposes persisted entity identity, STIX type, markings, confidence, provenance and immutable revisions. Only relationships supported by DTMO persistence are displayed as relationships.

### MISP
Phase 11.10g exposes governed review, independent share approval, authoritative handling restrictions, replay state and unpublished export. Technical connectivity never grants sharing or publication authority.

### TheHive
Phase 11.10h exposes canonical investigation context, explicit human case handoff and durable reconciliation evidence. It deliberately does not invent alerts, tasks, observables, assignment or timeline state that the accepted DTMO persistence does not store/read back.

### Cortex
Phase 11.10e exposes bounded analyzer execution and durable result history. Responders or autonomous side effects remain excluded until separately governed and explicitly accepted.

## Workflow/automation target

The future playbook surface uses explicit execution classes: `AUTOMATIC`, `HUMAN APPROVAL REQUIRED`, `MANUAL` and `PROHIBITED`. No graphical workflow may bypass RBAC, case authority, review/share approval or other server-side controls.

## Role-aware defaults

The same product can present different default workspaces for Executive/security leadership, CISO, SOC analyst, CTI analyst, Incident responder, Administrator and Auditor. Role-aware layout is for efficiency only; backend authorization remains authoritative.

## Visual direction

The target is a dense but calm SOC-grade interface with dark operations mode plus accessible light mode, clear hierarchy, semantic status/severity treatment, persistent context, compact drill-down surfaces, keyboard-first operation, responsive layouts and truthful loading/empty/degraded states.

## Candidate-completion sequence

The interface programme is executed as bounded Phase 11.10 candidate-completion slices:

- 11.10a frontend architecture/design contract — `PASS / REPOSITORY_COMPLETE`;
- 11.10b canonical application shell — `PASS / REPOSITORY_COMPLETE`;
- 11.10c Command Center — `PASS / REPOSITORY_COMPLETE`;
- 11.10d Unified Intelligence Workspace — `PASS / REPOSITORY_COMPLETE`;
- 11.10e IntelOwl/Cortex integrated analysis — `PASS / REPOSITORY_COMPLETE`;
- 11.10f OpenCTI graph/entity workspace — `PASS / REPOSITORY_COMPLETE`;
- 11.10g MISP Sharing & Exchange — `PASS / REPOSITORY_COMPLETE`;
- 11.10h TheHive Investigations & Cases — active;
- 11.10i Vulnerability & Exposure — next after 11.10h acceptance/merge;
- 11.10j Sources & Collection;
- 11.10k Automation & Playbooks;
- 11.10l Governance & Evidence;
- 11.10m Operations & Administration;
- 11.10n role-aware UX/accessibility;
- 11.10o consolidation/full functional acceptance;
- 11.10p fresh production-equivalent exercise against the frozen integrated candidate.

Phase 11.11 remains blocked until 11.10p is explicitly accepted.

## Evidence boundary

This document is product/UX architecture. Repository/browser CI for 11.10h can validate same-origin API usage, human case authority, handling/reconciliation semantics and fail-closed browser behavior. It does **not prove** live TheHive health, upstream case completeness, responder execution, production-equivalent validation, independent assurance or production authorization. DTMO remains **not production authorized**.
