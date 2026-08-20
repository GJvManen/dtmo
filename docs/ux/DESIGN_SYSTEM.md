# DTMO Design System Contract

Status: **Phase 11.10a — PASS / REPOSITORY_COMPLETE; Phase 11.10b — ACTIVE SHELL BASELINE**

## Purpose

This document is the accepted visual, interaction and accessibility contract for the DTMO Unified Operations Workbench. Phase 11.10b implements the reusable application-shell baseline; feature-specific components and complete role-aware accessibility acceptance remain bounded later slices.

## 1. Design principles

1. **Operational clarity before decoration** — dense information is acceptable when hierarchy remains clear.
2. **Semantic consistency** — the same state means the same thing in cards, tables, graphs, badges and filters.
3. **Progressive disclosure** — routine information is immediately visible; raw evidence and high-impact actions are deliberate drill-downs.
4. **Accessible by default** — keyboard, focus, reflow, contrast and non-colour cues are part of the component contract.
5. **Truthful state** — loading, empty, partial failure, stale and error states are distinct.
6. **Authority visible** — approval, sharing, case and administrative boundaries are understandable at the point of action.
7. **No synthetic operational truth** — placeholder/demo values are never presented as live product data.

## 2. Theme model

DTMO supports:

- **dark operations mode** as a first-class high-density workspace theme;
- **light mode** with equivalent semantic contrast and hierarchy;
- user preference without changing the meaning of security states;
- future system-preference alignment where accepted without weakening deterministic rendering.

Phase 11.10b implements dark/light semantic themes and persists only the non-sensitive theme preference. Theme changes never change severity or status semantics.

## 3. Semantic tokens

Implementation uses semantic tokens rather than feature-specific hard-coded state colours. Required token families include:

- background/surface/elevated surface;
- text primary/secondary/muted;
- border/divider/focus;
- action primary/secondary/danger;
- status success/warning/error/neutral/info;
- severity informational/low/medium/high/critical;
- chart categorical and sequential tokens tested for contrast when chart components are introduced.

Phase 11.10b establishes shell tokens for background, surfaces, text, borders, accent, success, warning, error and focus. Feature slices extend these through shared composition rather than page-local styling.

## 4. Severity semantics

Canonical intelligence severity remains:

- `informational` — neutral/informational treatment;
- `low` — low-risk/green semantic treatment;
- `medium` — amber/orange treatment;
- `high` — red treatment;
- `critical` — highest-severity distinct treatment.

Colour is supplementary. Every presentation must include text, iconography, position, pattern or another non-colour cue appropriate to the component.

Severity is not the same as confidence, TLP/PAP, exploitability, local exposure, case priority or framework mapping.

## 5. Status semantics

Operational status uses explicit labels such as:

- Healthy;
- Degraded;
- Unavailable;
- Running;
- Pending;
- Needs approval;
- Failed;
- Stale;
- Unknown.

`Healthy` must map to a defined check. Unknown or missing data must not be rendered as healthy. The Phase 11.10b shell therefore reports unavailable/unknown shell state explicitly rather than inferring platform health.

## 6. Typography

The design system uses a legible sans-serif UI stack with a monospace stack for hashes, identifiers, queries and evidence references.

Hierarchy levels include application title, workspace title, section title, card/widget title, body, compact metadata and code/identifier.

Text must remain usable at browser zoom and accepted text-resize levels.

## 7. Spacing and layout

Use an 8px-based spacing rhythm with smaller 4px increments for dense inline alignment. Page-local one-off spacing should be minimized.

The desktop shell targets:

- persistent navigation approximately 240–280px;
- fluid main workspace;
- optional context rail approximately 320–400px;
- responsive collapse below defined breakpoints.

Phase 11.10b implements these proportions with responsive breakpoints that collapse navigation and context into mobile-safe drawers.

## 8. Core component families

The target shared layer includes:

- AppShell;
- NavigationGroup / NavigationItem;
- TopBar;
- GlobalSearch / CommandPalette;
- ContextRail / Drawer;
- PageHeader;
- KPI card;
- Surface/Panel;
- StatusBadge;
- SeverityBadge;
- DataTable;
- FilterBar;
- Tabs;
- Timeline;
- EmptyState;
- LoadingSkeleton;
- ErrorState / PartialFailureState;
- ConfirmationDialog;
- ApprovalPanel;
- Form controls;
- Toast/notification;
- Graph/Chart container;
- Evidence/provenance block;
- Audit metadata block.

Phase 11.10b implements the shell, navigation, top bar, navigation-only command palette, context rail, generic surfaces and truthful empty/degraded shell states. Feature-specific component families are implemented only by their bounded slices.

## 9. Data tables

High-density tables remain first-class and must support, where applicable, sortable columns, accessible header semantics, filters, pagination/virtualization, persistent object identity links, compact severity/status/provenance, keyboard use and a usable mobile alternative.

Data tables are not part of the 11.10b shell acceptance and must not be populated with demo operational data merely to make a route look complete.

## 10. Charts and graph views

Visualizations always require a textual/table equivalent or accessible summary for critical information. Empty data produces an explicit empty state, not fabricated bars/points.

Geographic maps require attributable geographic data and may not infer victim location from unrelated IP/source metadata. Graph nodes/edges must preserve entity type, relationship semantics, markings and confidence where relevant.

Chart and graph implementations remain later bounded feature work.

## 11. Forms and actions

Each context should have at most one visually dominant primary action. Destructive, external-share, privileged administrative and other high-impact actions require distinct treatment and explicit consequence text.

Disabled controls should explain why an action is unavailable where practical; hiding controls is allowed for clarity but never substitutes for **server-side RBAC** or other server authorization.

The 11.10b command palette intentionally exposes navigation only and cannot execute governed high-impact actions.

## 12. Loading, empty and degraded states

Every data-bearing component must define:

- loading;
- populated;
- genuinely empty;
- filtered empty;
- stale;
- partial failure;
- full failure;
- unauthorized/forbidden where relevant.

A spinner without context is not sufficient for long-running enrichment, analysis, collection or playbook jobs; those require explicit attributable job state and progress.

Phase 11.10b establishes truthful shell states and explicitly avoids synthetic metrics, cases, vulnerabilities, connector state or approval state.

## 13. Accessibility

Minimum contract:

- WCAG 2.2 AA target for supported critical journeys;
- semantic HTML and landmarks;
- skip link;
- visible focus;
- keyboard operability;
- logical focus order;
- labels and descriptions for controls;
- contrast-compliant themes;
- text resize and spacing resilience;
- responsive reflow;
- reduced motion support;
- ARIA only where native semantics are insufficient;
- status changes announced appropriately without excessive noise.

Phase 11.10b implements the shell-level skip link, focus treatment, keyboard navigation, Ctrl/Cmd+K palette, responsive navigation/context behavior, semantic status labels and reduced-motion handling. Full role-aware and feature-specific WCAG 2.2 AA acceptance remains Phase 11.10n and final consolidation in 11.10o.

## 14. Icons

Icons support recognition but never carry unique meaning without text or an accessible name. Upstream product logos may identify service provenance where licensing/brand usage permits; DTMO navigation prefers capability semantics rather than vendor ownership.

## 15. Evidence and provenance presentation

Evidence panels distinguish:

- canonical DTMO state;
- upstream-derived observation;
- human decision;
- repository engineering evidence;
- production-equivalent/external evidence.

The UI must not visually collapse those evidence classes into a single generic `verified` state.

## 16. Design-reference boundary

Mockups, generated visuals and design-system examples are design artifacts only. They are not live screenshots and cannot be used as staging, production-equivalent or production evidence.

The Phase 11.10b shell implementation and browser CI are repository engineering evidence only; they do not prove live upstream integrations, production-equivalent operation, independent assurance or production authorization.

## 17. Implementation acceptance

Phase 11.10a is `PASS / REPOSITORY_COMPLETE`. Phase 11.10b applies the first shared shell baseline and may become `PASS / REPOSITORY_COMPLETE` only after exact-head build/browser, dependency/supply-chain, accessibility-regression and professional-documentation gates are fully green.

Later frontend slices must continue demonstrating component-level automated tests, critical browser journeys, keyboard/focus behavior, responsive/reflow coverage and professional documentation before merge.
