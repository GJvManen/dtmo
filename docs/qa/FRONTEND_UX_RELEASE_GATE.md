# DTMO Frontend UX Release Gate

**Status:** `PASS` for the accepted functional baseline

## Objective

This gate defines the professional user-experience acceptance contract for the canonical DTMO console. It ensures product changes remain usable, understandable, accessible and aligned with server-side security/governance controls.

Historical browser failures, repair chronology and individual workflow identifiers are retained in `docs/development/` and CI evidence rather than this durable UX contract.

## Information architecture contract

The canonical product must present clear task-oriented navigation across:

- Overview;
- Intelligence;
- Sources & Catalog;
- Visual Analytics;
- Administration;
- Governance.

Users should not need knowledge of internal service URLs or separately authenticated operational tooling to complete normal product tasks.

## Interaction-state contract

Interactive views must provide machine- and human-observable states for:

- loading/busy;
- success;
- partial failure;
- empty/no data;
- filtered empty results;
- forbidden/unauthorized;
- validation errors.

False-success messaging is not acceptable. Zero-data analytical views should communicate absence of data rather than drawing misleading pseudo-graphs.

## Navigation and control contract

- Controls use appropriate semantic button/link/form behavior.
- Keyboard operation is supported.
- Visible focus is preserved.
- Refresh/navigation actions return to a usable enabled state after completion.
- Supported browser journeys must complete without unexpected page/console errors where the acceptance journey defines a zero-error boundary.
- Responsive navigation remains understandable on desktop, tablet and mobile layouts.

## Accessibility contract

Frontend UX changes must preserve accepted regression coverage for:

- keyboard navigation;
- focus order/visibility;
- contrast;
- reflow;
- text resize;
- text spacing;
- responsive layout;
- supported browsers;
- critical end-to-end journeys.

Accessible names intended only for assistive technology must remain semantically available even when excluded from visible geometry/layout calculations.

Colour is never the sole state indicator. Text labels, symbols or equivalent non-colour cues accompany semantic colour use.

## Security and governance contract

- Server-side RBAC is authoritative.
- Client-side visibility/disabled state is not an authorization control.
- Human and service-account authorities remain separated.
- Review and external-share approval remain distinct actions/permissions.
- Administration does not bypass privileged-action safeguards.
- Governance visibility does not create publication/share authority.
- Tokens/credentials are not embedded in frontend assets or persistent production browser storage.
- Security response headers remain enforced.

## Product clarity contract

### Overview

Must prioritize situational awareness, clear KPI meaning, source/runtime state, recent intelligence and truthful refresh/empty states.

### Intelligence

Must prioritize readable intelligence records, provenance/source context and investigation/filtering without obscuring canonical record state.

### Sources & Catalog

Must keep source lifecycle/execution distinct from general user/role administration.

### Visual Analytics

Must use interpretable native analytical views, explicit labels and truthful no-data states.

### Administration

Must clearly present governed principals/roles/permissions and privileged consequences.

### Governance

Must distinguish framework context, mapping coverage, evidence and authority boundaries; missing mappings remain visibly missing.

## Next UX evolution

The next planned UX slice adds a shared severity system across Overview and Intelligence:

- informational;
- low;
- medium;
- high;
- critical if present in the canonical dataset.

Semantic colour may support comprehension (for example green/amber/red), but labels/non-colour cues and WCAG-compliant contrast remain mandatory. Filters and their resulting KPI/list/chart states must remain internally consistent.

## Evidence rule

Every frontend/UX PR requires fresh exact-head CI. A new commit invalidates earlier evidence. This gate's current PASS does not create Phase 8, Phase 9 or production acceptance.
