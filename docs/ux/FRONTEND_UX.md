# DTMO Frontend UX Architecture

Last updated: **2026-08-20**  
Baseline: **16.0.0rc12 / RC13 accepted / Phase 11.10a active**

## Purpose

The DTMO frontend is a single governed security-operations experience for analysts, administrators, security leadership, reviewers/share approvers and auditors. The browser improves orientation and workflow efficiency, but server-side authorization remains authoritative.

The accepted six-area console remains the current implemented product baseline. Phase 11.10a now defines the target **Unified Operations Workbench** architecture that will supersede the current layout incrementally through bounded 11.10b–11.10o implementation slices. The existing product remains canonical until replacement capability is actually implemented and accepted.

## Experience principles

1. **One canonical product** — normal work occurs in the unified DTMO console/workbench rather than disconnected URLs or second-login dashboards.
2. **Task first** — navigation reflects operator intent rather than internal service boundaries.
3. **Role-aware, never role-trusting** — UI visibility may adapt for clarity; authorization is enforced server-side.
4. **Truthful state** — loading, success, partial failure and empty-data states must accurately represent canonical application state.
5. **Evidence visible** — source provenance, governance state and audit context are first-class information.
6. **Progressive disclosure** — privileged/high-impact actions are separated from routine analysis.
7. **Accessible by default** — semantic controls, labels, focus, keyboard behavior, reflow and non-colour state cues are part of the product contract.
8. **No publication by convenience** — technical execution, Administration or analytics cannot silently create external-share authority.
9. **Object-centric continuity** — the selected intelligence object, IOC, CVE, case, source or entity remains available as context across related workflows.
10. **DTMO is the control plane** — normal browser workflows use the DTMO API and governed adapters instead of direct privileged browser calls to upstream services.

## Current implemented information architecture

The accepted console currently contains six primary work areas.

### Overview

Purpose: immediate situational awareness.

Contains:

- intelligence KPIs;
- source/runtime state;
- recent intelligence;
- native summaries/trends;
- unified `Alles vernieuwen` refresh action;
- explicit truthful empty-data states;
- shared informational/low/medium/high/critical severity filtering;
- accessible semantic severity colour treatment with text labels and counts.

The current E1/E2 severity experience is specified in [`SEVERITY_EXPERIENCE.md`](SEVERITY_EXPERIENCE.md).

### Intelligence

Purpose: inspect recent canonical intelligence and investigation context.

Contains:

- durable PostgreSQL-backed intelligence records;
- source/provenance context;
- investigation/search support;
- structured record presentation;
- the same shared severity filter contract as Overview.

Framework mapping remains a future first-class capability. The UI must not invent framework relationships from severity, tags or free text.

### Sources & Catalog

Purpose: govern intelligence-source lifecycle and execution.

Contains:

- catalog/bootstrap state;
- source enable/disable controls;
- supported execution actions;
- execution feedback;
- source/runtime status.

Planned enhancement: governed manual source onboarding with explicit source type, endpoint, freshness/schedule, authentication mode/secret reference, owner, default-disabled state, validation/test-run and audit/RBAC controls. Existing governed source-registry APIs must be reused rather than duplicated.

### Visual Analytics

Purpose: turn canonical intelligence into visual analytical context.

Contains native views for:

- severity;
- source;
- connector/runtime state;
- review state;
- existing trend data where available.

Planned enhancements:

- reuse the accepted shared severity semantics and filter state;
- configurable trend windows;
- clear distinction between volume trend and severity/risk trend;
- framework aggregation only when first-class mappings exist.

### Administration

Purpose: govern principals and role assignments.

Current controls include managed principal/role assignment lifecycle, service-account/human separation, administrator self-management protection, final-admin protection and auditable state changes.

Planned enhancement: richer role-to-permission management while preserving least privilege, separation of duties and review/share-approval boundaries.

### Governance

Purpose: present framework/governance coverage and evidence without overstating mappings.

Current surface presents explicit coverage states and repository-backed internal mappings. Planned enhancement: framework/version inventory, mapped/unmapped coverage, provenance/review status and drill-down built on the future first-class mapping model.

## Phase 11.10a target information architecture

The next-generation workbench is defined in:

- [`UNIFIED_OPERATIONS_WORKBENCH.md`](UNIFIED_OPERATIONS_WORKBENCH.md);
- [`INFORMATION_ARCHITECTURE.md`](INFORMATION_ARCHITECTURE.md);
- [`DESIGN_SYSTEM.md`](DESIGN_SYSTEM.md);
- [`../architecture/FRONTEND_ARCHITECTURE.md`](../architecture/FRONTEND_ARCHITECTURE.md);
- [`../architecture/UI_API_CONTRACT.md`](../architecture/UI_API_CONTRACT.md).

The target primary workspaces are:

- Command Center;
- Intelligence;
- Exposure;
- Investigations;
- Analysis;
- Sharing;
- Automation;
- Collection;
- Governance;
- Operations;
- Administration.

The target shell also includes a global command/status bar and a selected-object context rail/drawer. This is an architectural target only in 11.10a; it does not claim that the new shell or workspaces already exist.

## Canonical browser/API boundary

Normal product operations follow:

**browser → DTMO API → governed integration adapter → upstream service**.

The browser must not become a privileged direct client for Taranis AI, IntelOwl, OpenCTI, MISP, TheHive or Cortex. Advanced upstream administration may remain a separately authenticated escape hatch where genuinely required, but normal DTMO journeys must not depend on it.

## Object-centric interaction model

The future workbench should let an authorized user select one canonical object and traverse relevant functions without losing context. Depending on object type, the context surface may expose:

- canonical identity;
- severity/classification;
- confidence;
- provenance/markings;
- enrichment/analysis state;
- OpenCTI relationships;
- MISP correlations/sharing state;
- TheHive cases/tasks;
- vulnerability/exposure context;
- audit timeline;
- governed actions.

No unavailable fact may be inferred merely because an upstream service is configured.

## Visual system

The UI should communicate security state clearly without becoming alarmist or decorative.

Design requirements:

- calm, high-information layout;
- clear hierarchy and workspace headings;
- consistent KPI cards, tables and panels;
- responsive desktop/tablet/mobile behavior;
- explicit primary/secondary/danger actions;
- visible focus and keyboard-operable controls;
- status labels/icons in addition to colour;
- meaningful empty states instead of pseudo-data visualizations;
- dark operations mode and accessible light mode with identical semantic meaning;
- reusable semantic design tokens and component families;
- persistent context for analyst workflows.

### Severity semantics

The shared severity system uses the canonical intelligence taxonomy:

- informational — neutral/informational treatment;
- low — green semantic treatment;
- medium — yellow/amber semantic treatment;
- high — red semantic treatment;
- critical — distinct highest-severity treatment.

Colour is never the only indicator. Text labels, native checkbox labels, chart/table labels and counts remain mandatory. Severity is a classification dimension only; it is not itself a framework mapping.

## Interaction model

### Refresh and loading

Refresh actions must:

- visibly enter a busy/loading state;
- execute the intended canonical reads;
- return controls to enabled state;
- expose partial failure rather than reporting false success;
- distinguish `no intelligence data` from successful populated refresh.

Long-running enrichment, analysis, collection and automation jobs require explicit job state rather than an indefinite spinner.

### Filtering

Overview and Intelligence currently share one severity selection state. Filters compose rather than replace context.

Current rules:

- informational, low, medium, high and critical are selected by default;
- at least one severity remains selected;
- changing either filter surface synchronizes both surfaces;
- reset restores all severities;
- Overview filtered KPIs and severity distribution are derived from canonical PostgreSQL data;
- recent Intelligence is filtered server-side against canonical PostgreSQL records;
- search reuses the governed OpenSearch severity parameter when one severity is selected and applies the shared selected set to returned results when multiple values are active;
- zero results display an explicit filtered-empty state.

Future workbench filters may extend these dimensions but must retain explicit semantics and canonical sources.

### Privileged actions

Administration and other high-impact actions require explicit server-authorized actions, clear consequences and auditable results. The UI must not imply that hidden controls provide security; server authorization remains the enforcement point.

Playbook steps are classified as `AUTOMATIC`, `HUMAN APPROVAL REQUIRED`, `MANUAL` or `PROHIBITED`. A visual workflow never bypasses underlying authorization or approval boundaries.

## Authentication and identity UX

Production authentication uses the configured external bearer-token/identity-provider trust model. Local/reference identity helpers are development conveniences only and must not replace production identity architecture.

Tokens/credentials must not be embedded in HTML, committed documentation or persistent browser storage as a production pattern.

## Analytics boundary

Native DTMO analytics are the normal product surface. Grafana remains separately secured for operations/advanced analysis and must not require anonymous access or become a normal-product authentication bypass.

The workbench may surface canonical operational summaries derived from governed APIs, but it must not pretend that embedding an externally authenticated Grafana view converts Grafana into canonical DTMO product state.

## Accessibility contract

Phases 1–7, including the accepted accessibility/UX phase, are complete for the current engineering baseline. Continued product changes must preserve the existing keyboard, focus, contrast, reflow, text-size/spacing, responsive and supported-browser regression coverage.

The next-generation design targets WCAG 2.2 AA for supported critical journeys, reduced-motion behavior where animation is used, persistent non-colour status cues and accessible textual/table alternatives or summaries for critical chart/graph information.

## Security contract

The frontend must preserve:

- server-side RBAC;
- least privilege;
- service-account/human authority separation;
- review and external-share separation;
- read-only auditor behavior where applicable;
- CSP/no-store/anti-framing controls;
- provenance/evidence visibility without leaking raw secrets;
- no framework mapping inference;
- no publication authority from UI convenience or technical execution;
- no local-compromise inference from enrichment, graph presence or correlation;
- separate TheHive case authority and publication/share authority;
- governed DTMO API/adapters as the normal integration path.

## Migration and evidence boundary

The current console remains the implemented canonical baseline until each new workbench slice is implemented, tested and accepted. Legacy routes may coexist temporarily for compatibility but are not parallel product targets.

Phase 11.10a documentation and graphical references are repository design artifacts only. They do not prove new-frontend implementation, live-source connectivity, staging acceptance, production-equivalent validation, independent assurance or production authorization.
