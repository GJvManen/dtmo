# DTMO Design System Contract

Status: **Phase 11.10a — IN PROGRESS / TARGET DESIGN CONTRACT**

## Purpose

This document defines the visual, interaction and accessibility contract for the next-generation DTMO Unified Operations Workbench. Implementation follows in later bounded slices.

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
- system-preference default where appropriate;
- user preference without changing the meaning of security states.

Theme changes must not change severity or status semantics.

## 3. Semantic tokens

Implementation must use semantic tokens rather than feature-specific hard-coded colours. Required token families include:

- background/surface/elevated surface;
- text primary/secondary/muted;
- border/divider/focus;
- action primary/secondary/danger;
- status success/warning/error/neutral/info;
- severity informational/low/medium/high/critical;
- chart categorical and sequential tokens tested for contrast.

Exact colour values are selected and tested in the shell implementation slice.

## 4. Severity semantics

Canonical intelligence severity remains:

- `informational` — neutral/informational treatment;
- `low` — low-risk/green semantic treatment;
- `medium` — amber/orange treatment;
- `high` — red treatment;
- `critical` — highest-severity distinct treatment.

Colour is supplementary. Every presentation must include text, iconography, position, pattern or other non-colour meaning appropriate to the component.

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

`Healthy` must map to a defined check. Unknown or missing data must not be rendered as healthy.

## 6. Typography

The design system uses a legible sans-serif UI stack with a monospace stack for hashes, identifiers, queries and evidence references.

Hierarchy levels include:

- application title;
- workspace title;
- section title;
- card/widget title;
- body;
- compact metadata;
- code/identifier.

Text must remain usable at browser zoom and accepted text-resize levels.

## 7. Spacing and layout

Use an 8px-based spacing rhythm with smaller 4px increments for dense inline alignment. Page-local one-off spacing should be minimized.

The desktop shell targets:

- persistent navigation width approximately 240–280px;
- fluid main workspace;
- optional context rail approximately 320–400px;
- responsive collapse below defined breakpoints.

Exact dimensions remain implementation details so accessibility/reflow testing can drive adjustment.

## 8. Core component families

The target design-system layer includes:

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

Feature teams extend these through composition instead of cloning styles.

## 9. Data tables

High-density tables are first-class. They must support where applicable:

- sortable columns;
- accessible header semantics;
- filters;
- pagination/virtualization for large sets;
- persistent object identity links;
- compact severity/status/provenance columns;
- row keyboard navigation where appropriate;
- a mobile alternative when horizontal table use becomes unusable.

## 10. Charts and graph views

Visualizations always have a textual/table equivalent or accessible summary for critical information. Empty data produces an explicit empty state, not fabricated bars/points.

Geographic maps require attributable geographic data and may not infer victim location from unrelated IP/source metadata.

Graph nodes/edges must preserve entity type, relationship semantics, markings and confidence where relevant.

## 11. Forms and actions

Each context should have at most one visually dominant primary action. Destructive, external-share, privileged administrative and other high-impact actions require distinct visual treatment and explicit consequence text.

Disabled controls should explain why an action is unavailable where practical; hiding controls is allowed for clarity but never substitutes for authorization.

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

A spinner without context is not sufficient for long-running enrichment, analysis, collection or playbook jobs; those require explicit job state and progress where attributable.

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

## 14. Icons

Icons support recognition but never carry unique meaning without text/accessible name. Upstream product logos may identify service provenance where licensing/brand usage permits; DTMO navigation should prefer capability semantics rather than making vendor logos the sole information architecture.

## 15. Evidence and provenance presentation

Evidence panels distinguish:

- canonical DTMO state;
- upstream-derived observation;
- human decision;
- repository engineering evidence;
- production-equivalent/external evidence.

The UI must not visually collapse those evidence classes into a single generic 'verified' badge.

## 16. Design-reference boundary

Mockups, generated visuals and design-system examples are design artifacts only. They are not live screenshots and cannot be used as staging, production-equivalent or production evidence.

## 17. Implementation acceptance

Later frontend slices must demonstrate component-level automated tests, critical browser journeys, keyboard/focus behavior, responsive/reflow coverage and professional documentation before merge.