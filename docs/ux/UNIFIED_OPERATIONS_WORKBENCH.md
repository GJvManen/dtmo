# DTMO Unified Operations Workbench

Status: **Phase 11.10a–11.10e PASS / REPOSITORY_COMPLETE; Phase 11.10f IN PROGRESS / OPENCTI GRAPH & ENTITY**  
Visual reference: approved next-generation command-center concept (design target only, not evidence).

## Purpose

The Unified Operations Workbench is the canonical DTMO browser experience. It converts the integrated DTMO framework into one professional operational product instead of exposing only a fraction of each underlying capability through disconnected views.

The workbench is task- and object-oriented. Users should normally operate DTMO without having to decide which upstream platform UI to visit.

## Target shell

The workbench follows a stable four-zone composition:

- **left navigation** for functional domains;
- **top command/status bar** for global search, candidate/environment state, notifications and principal context;
- **main workspace** for the current operational task;
- **right context rail** for selected-object facts and governed actions.

Phase 11.10b accepted this shell foundation under `/workbench/`. The command palette is navigation-only, the context rail starts with an explicit no-selection state and workspace routes do not fabricate feature data.

Phase 11.10c accepted the Command Center. Phase 11.10d accepted Threat Intelligence and IOC Explorer. Phase 11.10e accepted Analysis & Enrichment with persisted IntelOwl/Cortex evidence and human-triggered execution. Phase 11.10f is the active migration of OpenCTI graph/entity context into the same shell.

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
7. correlate with MISP and existing canonical intelligence;
8. create or link a TheHive case when human-authorized;
9. complete investigation tasks;
10. prepare a governed sharing package;
11. obtain separate human publication/share approval;
12. review evidence, timeline and audit state.

The normal journey remains inside DTMO.

## Accepted functional workspaces

### Command Center

Phase 11.10c provides a truthful operational picture using canonical read models. Missing canonical data produces unavailable/null state rather than synthetic zero values. Integration configuration never becomes an automatic `healthy` claim.

### Unified Intelligence Workspace

Phase 11.10d provides `/workbench/intelligence` and `/workbench/intelligence/iocs`. Indexed search is a discovery projection; selected detail comes separately from canonical DTMO persistence. Search/detail failures **fail closed**. Both routes require server-side `read:intelligence` and grant no mutation authority.

### Integrated Analysis Workspace

Phase 11.10e provides `/workbench/analysis`. It combines persisted IntelOwl and Cortex evidence against one canonical object. Capability/allowlist state is not runtime health. Read access requires `read:intelligence`; human-triggered analyzer execution requires server-side `review:intelligence`.

Cortex responders, automatic analyzer discovery and automatic IntelOwl fallback remain excluded. Analyzer output does not prove local compromise and grants no external-share/publication authority.

## Active OpenCTI Graph / Entity Workspace

Phase 11.10f makes `/workbench/intelligence/graph` functional through DTMO-owned read APIs:

- `/api/v1/opencti/capabilities`;
- `/api/v1/opencti/items/{item_id}/graph`;
- `/api/v1/opencti/entities/{mapping_id}`.

The browser never receives OpenCTI credentials and does not call OpenCTI `/graphql` directly. Server-side `read:intelligence` remains authoritative.

The accepted Phase 11.4 persistence model stores stable OpenCTI/STIX mappings and immutable mapping revisions. It does not currently durably store generic OpenCTI entity-to-entity relationship topology. Therefore the visual graph draws only proven `canonical-mapping` edges from the selected DTMO canonical item to persisted OpenCTI mappings.

The workspace must not infer a malware→campaign, actor→tool, indicator→infrastructure or other upstream relationship merely because two nodes are present. Missing topology evidence must **fail closed**.

An empty mapping graph means only that DTMO has no persisted OpenCTI mapping evidence for that item. It does not prove OpenCTI has no related knowledge. Graph presence, confidence and markings do not prove local exposure, exploitability, compromise, attribution certainty or remediation state.

The entity detail surface exposes stable OpenCTI/STIX identity, entity type, markings, confidence, external references, snapshot identity and immutable revision history where recorded. Existing `external_share_authorized=false` and `local_compromise_proven=false` boundaries remain intact.

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

The right context rail may expose attributable counts/status from IntelOwl, Cortex, OpenCTI, MISP and TheHive without requiring a separate upstream login. Until a bounded feature slice supplies attributable data, missing facts are not inferred.

The object-centric experience began with 11.10d; 11.10e added analysis and 11.10f adds read-only persisted OpenCTI graph/entity context. Later 11.10g–11.10h slices add exchange and case capabilities without bypassing the DTMO API boundary.

## Integrated capability expectations

### Taranis AI

Collection/assessment remains an upstream service boundary; normal operator workflows should be governed through DTMO Collection surfaces.

### IntelOwl

Phase 11.10e exposes explicit analyzer selection, job state and persisted bounded enrichment history. IntelOwl results do not grant publication/share authority or prove local compromise.

### OpenCTI

Phase 11.10f exposes persisted entity identity, STIX type, markings, confidence, provenance and immutable revisions in a graph/entity workspace. Only relationships supported by DTMO persistence may be displayed as relationships.

### MISP

DTMO should expose inbound events/matches/correlations and governed outbound draft/review/approval workflows. Technical connectivity never grants sharing authority. This is Phase 11.10g scope.

### TheHive

DTMO should expose daily case, task, observable, assignment and timeline operations subject to accepted case-handoff authority.

### Cortex

Phase 11.10e exposes bounded analyzer execution and durable result history. Responders or autonomous side effects remain excluded until separately governed and explicitly accepted.

### Vulnerability intelligence

CVE/KEV/CVSS/EPSS and education relevance should be correlated with actors, campaigns, IOCs, cases and affected technology where attributable data exists.

## Workflow/automation target

The future playbook surface uses explicit execution classes: `AUTOMATIC`, `HUMAN APPROVAL REQUIRED`, `MANUAL` and `PROHIBITED`. No graphical workflow may bypass RBAC, case authority, publication/share approval or other server-side controls.

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
- 11.10e IntelOwl/Cortex integrated analysis — `PASS / REPOSITORY_COMPLETE`;
- 11.10f OpenCTI graph/entity workspace — active;
- 11.10g MISP Sharing & Exchange — next after 11.10f acceptance/merge;
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

This document is product/UX architecture. The graphical reference and repository documentation are not evidence of live integration, staging acceptance, production-equivalent validation or production authorization. Repository/browser CI for 11.10f does not prove live OpenCTI health/completeness, local exposure or compromise, independent assurance or production authorization.
