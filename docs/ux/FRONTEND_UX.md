# DTMO Frontend UX Architecture

Last updated: **2026-08-12**  
Baseline: **16.0.0rc12 / RC13 accepted + post-RC13 severity UX**

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
8. **No publication by convenience** — technical execution, filtering, Administration or analytics cannot silently create external-share authority.

## Canonical information architecture

The accepted console contains six primary work areas.

### Overview

Purpose: immediate situational awareness.

Contains:

- intelligence KPIs;
- source/runtime state;
- recent intelligence;
- native analytical summaries and trend representation;
- unified `Alles vernieuwen` refresh action;
- explicit truthful empty-data states;
- shared severity filtering for `informational`, `low`, `medium`, `high` and `critical`;
- accessible semantic severity colours with visible labels/non-colour cues.

When a severity is selected, intelligence-derived KPI totals, 24-hour counts, confidence, trend, severity distribution, source/review aggregation and recent canonical intelligence use the same canonical PostgreSQL predicate. Connector health deliberately remains operational and unfiltered.

### Intelligence

Purpose: inspect recent canonical intelligence and investigation context.

Contains:

- durable PostgreSQL-backed recent intelligence records;
- source/provenance context;
- governed OpenSearch-backed investigation/search support;
- normalized supported source types and references;
- the same shared severity selection as Overview.

The selected severity composes with existing search rather than replacing it. A zero-result filtered list or search states which severity produced the empty result.

Severity does **not** imply framework mapping. Future framework context remains a separate provenance-backed data contract.

### Sources & Catalog

Purpose: govern intelligence-source lifecycle and execution.

Contains:

- catalog/bootstrap state;
- source enable/disable controls;
- supported execution actions;
- execution feedback;
- source/runtime status.

Planned enhancement: governed manual source onboarding in the canonical UI with explicit source type, endpoint, freshness/schedule, authentication mode/secret reference, owner, default-disabled state, validation/test-run and audit/RBAC controls. The backend governed source-registry API already exists and remains the canonical control plane.

### Visual Analytics

Purpose: turn canonical intelligence into visual analytical context.

Contains native views for:

- severity;
- source;
- connector/runtime state;
- review state;
- existing trend data where available.

Planned enhancements:

- reuse of the shared severity semantics/filter contract in the broader analytics surface;
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

The UI communicates security state clearly without becoming alarmist or decorative.

Design requirements:

- calm, high-information layout;
- clear hierarchy and workspace headings;
- consistent KPI cards, tables and panels;
- responsive desktop/tablet/mobile behavior;
- explicit primary/secondary/danger actions;
- visible focus and keyboard-operable controls;
- status labels/icons in addition to colour;
- meaningful empty states instead of pseudo-data visualizations.

### Shared severity semantics

The current shared severity system uses one canonical taxonomy:

| Severity | Semantic treatment | Non-colour cue |
|---|---|---|
| `informational` | neutral / blue-grey | visible `Informational` label and accessible name |
| `low` | green | visible `Low` label and accessible name |
| `medium` | yellow / amber | visible `Medium` label and accessible name |
| `high` | red | visible `High` label and accessible name |
| `critical` | distinct deep red / high-contrast treatment | visible `Critical` label and accessible name |

Colour is never the only indicator. Cards, legend entries, chart labels and table alternatives retain textual severity meaning.

`critical` is never silently collapsed into `high`.

## Interaction model

### Refresh and loading

Refresh actions must:

- visibly enter a busy/loading state;
- execute the intended canonical reads;
- return controls to enabled state;
- expose partial failure rather than reporting false success;
- distinguish `no intelligence data` from successful populated refresh.

The default `Alle severities` state preserves the accepted RC13 refresh/empty-state lifecycle. A persisted non-default severity preference may trigger an automatic filtered refresh after load.

### Shared severity filtering

The Overview and Intelligence selectors represent one browser-session preference stored in `sessionStorage` as a non-secret UI preference.

Changing either selector:

1. updates both controls;
2. refreshes dashboard intelligence aggregates with the selected severity;
3. refreshes recent canonical intelligence with the same severity;
4. reuses the existing governed search severity parameter when an active query exists;
5. renders a filter-aware empty state when no records match.

The filter is read-side only. It does not mutate intelligence, source state, review state, framework mappings or publication state.

### Privileged actions

Administration and other high-impact actions require explicit server-authorized actions, clear consequences and auditable results. The UI must not imply that hidden controls provide security; server authorization remains the enforcement point.

## Authentication and identity UX

Production authentication uses the configured external bearer-token/identity-provider trust model. Local/reference identity helpers are development conveniences only and must not replace production identity architecture.

Tokens/credentials must not be embedded in HTML, committed documentation or persistent browser storage as a production pattern.

## Analytics boundary

Native DTMO analytics are the normal product surface. Grafana remains separately secured for operations/advanced analysis and must not require anonymous access or become a normal-product authentication bypass.

The post-RC13 shared severity filter intentionally updates Overview and Intelligence first. Broader Visual Analytics filter/trend enrichment remains a separate bounded product slice so analytics changes do not bypass the proven console contract.

## Accessibility contract

Phases 1–7, including the accepted accessibility/UX phase, are complete for the current engineering baseline. Continued product changes must preserve the existing keyboard, focus, contrast, reflow, text-size/spacing, responsive and supported-browser regression coverage.

Severity UI changes require dedicated browser evidence for:

- keyboard-operable native selects;
- visible severity labels;
- non-colour cues;
- explicit critical treatment;
- truthful filtered empty states;
- zero browser page/console errors in the dedicated Chrome journey.

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
- no publication authority from filtering, UI convenience or technical execution.
