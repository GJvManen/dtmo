# Phase 11.10n — Role-aware UX & Accessibility

Status: **IN PROGRESS / REPOSITORY-CONTROLLED IMPLEMENTATION**

## Objective

Phase 11.10n makes the canonical DTMO application shell explicitly role-aware and accessible without weakening any accepted server-side authorization, provenance, audit, separation-of-duties or fail-closed boundary established through Phase 11.10m.

This slice is a presentation and interaction-authority layer. It does **not** move authorization into the browser, does not infer permissions from navigation visibility, and does not convert repository CI or visual evidence into production-equivalent evidence. Phase 10 remains **NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED**.

## Authority boundary

The canonical trust path remains:

`authenticated browser -> DTMO same-origin API -> server-side identity/RBAC/policy enforcement -> attributable response`

The browser may use server-returned role/capability context to adapt navigation, affordances, explanatory copy and disabled/hidden controls. That context is advisory for UX only. Every protected read or mutation remains authorized server-side at request time.

Required boundaries:

- hidden or disabled UI never substitutes for server authorization;
- a visible control never proves that the current principal may execute the action;
- service accounts never receive human-only review/share/publication authority through client presentation logic;
- self-management and separation-of-duties protections remain server-side;
- unavailable or unknown capability state fails closed and is presented as unavailable rather than guessed;
- request identifiers, provenance and existing auditability remain intact for governed mutations.

## Role-aware experience

The application shell and canonical workspaces must present only contextually relevant navigation and actions for the authenticated principal while preserving discoverability of why an action is unavailable.

Role-aware behavior includes:

- navigation items and action affordances derived from explicit server-provided capability context;
- read-only users receiving non-mutating surfaces without misleading enabled controls;
- administrators receiving governed administration affordances only when server context exposes them;
- analyst/investigator workflows preserving human review and share/publication boundaries;
- explicit unavailable/insufficient-authority states rather than silent disappearance where explanation improves usability;
- consistent role and permission semantics across canonical routes.

No client-side role string comparison may mint new authority or bypass canonical server policy.

## Accessibility acceptance

The canonical shell and Phase 11 workspaces must continue to satisfy the accepted accessibility contract and extend it to role-aware states. Deterministic browser acceptance must cover, at minimum:

- keyboard-only navigation and visible focus order;
- semantic landmarks, labels and accessible names for navigation, controls and state;
- sufficient contrast and non-color-only communication of severity, disabled state and authority state;
- text resize, reflow and text-spacing resilience;
- role-aware controls remaining understandable when disabled, unavailable or read-only;
- status and validation feedback exposed to assistive technology without requiring visual-only interpretation;
- supported-browser behavior for critical role-aware journeys.

Accessibility fixes must not weaken authorization or expose secrets, service credentials or restricted data in the DOM merely to improve presentation.

## Evidence and acceptance

Repository acceptance requires deterministic contract tests, Chromium/browser accessibility and role-aware journey tests, a dedicated exact-head workflow, synchronized professional documentation, and one final unchanged head for which every registered workflow is `completed/success`.

Repository CI is engineering evidence only. Screenshots and browser tests do not prove production identity-provider behavior, production authorization, staging acceptance, independent assurance or production readiness.

## Next boundary

After accepted Phase 11.10n, exactly the next bounded priority is **Phase 11.10o consolidation / full functional acceptance**. Phase 11.10p production-equivalent validation remains prohibited until Phase 11.10a–11.10o are complete and one immutable candidate is frozen.
