# DTMO Frontend UX Architecture

Last updated: **2026-08-12**  
Baseline: **16.0.0rc12 / RC13 accepted**

## Purpose

The DTMO frontend is a single governed security-operations experience for analysts, administrators, security leadership, reviewers/share approvers and auditors. The browser improves orientation and workflow efficiency, but server-side authorization remains authoritative.

## Experience principles

1. **One canonical product** — normal work occurs in the unified DTMO console rather than disconnected URLs or second-login dashboards.
2. **Task first** — navigation reflects operator intent rather than internal service boundaries.
3. **Role-aware, never role-trusting** — UI visibility may adapt for clarity; authorization is enforced server-side.
4. **Truthful state** — loading, success, partial failure and empty-data states must accurately represent canonical application state.
5. **Evidence visible** — source provenance, governance state and audit context are first-class information.
6. **Progressive disclosure** — privileged/high-impact actions are separated from routine analysis.
7. **Accessible by default** — semantic controls, labels, focus, keyboard behavior, reflow and non-colour state cues are part of the product contract.
8. **No publication by convenience** — technical execution, Administration or analytics cannot silently create external-share authority.

## Canonical information architecture

The accepted console contains six primary work areas.

### Overview

Purpose: immediate situational awareness.

Contains:

- intelligence KPIs;
- source/runtime state;
- recent intelligence;
- native summaries/trends;
- unified `Alles vernieuwen` refresh action;
- explicit truthful empty-data states.

Planned enhancement: shared informational/low/medium/high severity filtering and accessible semantic colour treatment.

### Intelligence

Purpose: inspect recent canonical intelligence and investigation context.

Contains:

- durable PostgreSQL-backed intelligence records;
- source/provenance context;
- investigation/search support;
- structured record presentation.

Planned enhancement: the same shared severity filter contract as Overview, plus future framework mapping context.

### Sources & Catalog

Purpose: govern intelligence-source lifecycle and execution.

Contains:

- catalog/bootstrap state;
- source enable/disable controls;
- supported execution actions;
- execution feedback;
- source/runtime status.

Planned enhancement: governed manual source onboarding with explicit source type, endpoint, freshness/schedule, authentication mode/secret reference, owner, default-disabled state, validation/test-run and audit/RBAC controls.

### Visual Analytics

Purpose: turn canonical intelligence into visual analytical context.

Contains native views for:

- severity;
- source;
- connector/runtime state;
- review state;
- existing trend data where available.

Planned enhancements:

- shared accessible severity semantics;
- informational/low/medium/high filtering;
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
- meaningful empty states instead of pseudo-data visualizations.

### Severity semantics

The planned shared severity system must use a single taxonomy and remain accessible:

- informational — neutral/informational treatment;
- low — green semantic treatment;
- medium — yellow/amber semantic treatment;
- high — red semantic treatment;
- critical, if introduced/present — distinct highest-severity treatment.

Colour must never be the only indicator. Text labels, accessible names and/or symbols remain mandatory.

## Interaction model

### Refresh and loading

Refresh actions must:

- visibly enter a busy/loading state;
- execute the intended canonical reads;
- return controls to enabled state;
- expose partial failure rather than reporting false success;
- distinguish `no intelligence data` from successful populated refresh.

### Filtering

Filters should compose rather than replace context. Shared severity filters must use the same semantic values across Overview, Intelligence and later Visual Analytics.

Filtered totals, lists and charts must remain internally consistent, and zero results must display a truthful filtered-empty state.

### Privileged actions

Administration and other high-impact actions require explicit server-authorized actions, clear consequences and auditable results. The UI must not imply that hidden controls provide security; server authorization remains the enforcement point.

## Authentication and identity UX

Production authentication uses the configured external bearer-token/identity-provider trust model. Local/reference identity helpers are development conveniences only and must not replace production identity architecture.

Tokens/credentials must not be embedded in HTML, committed documentation or persistent browser storage as a production pattern.

## Analytics boundary

Native DTMO analytics are the normal product surface. Grafana remains separately secured for operations/advanced analysis and must not require anonymous access or become a normal-product authentication bypass.

## Accessibility contract

Phases 1–7, including the accepted accessibility/UX phase, are complete for the current engineering baseline. Continued product changes must preserve the existing keyboard, focus, contrast, reflow, text-size/spacing, responsive and supported-browser regression coverage.

Any enhancement affecting severity colours must explicitly test contrast and non-colour cues.

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
- no publication authority from UI convenience or technical execution.
