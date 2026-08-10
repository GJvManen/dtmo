# DTMO Frontend UX Architecture

## Purpose

DTMO 16.0.0rc6 establishes a coherent operator-facing experience for analysts, reviewers, share approvers, auditors and CISO/security users while preserving the platform's server-side authorization and governance controls.

## Experience principles

1. **Task first** — users navigate by operational intent: overview, intelligence, governance, audit and security.
2. **Role-aware, never role-trusting** — the browser may hide unavailable controls for clarity, but the server remains authoritative for RBAC decisions.
3. **Decision clarity** — review and external share approval are visibly separate steps and remain technically separate permissions.
4. **Evidence visibility** — audit and provenance information is presented as first-class operational information rather than diagnostic output.
5. **Progressive disclosure** — high-impact controls are separated from routine analysis and use explicit labels and consequences.
6. **Accessible by default** — semantic headings, native controls, skip navigation, visible focus, live status regions, reflow and reduced-motion behavior are built into the design system.
7. **No secret persistence** — local/dev/staging identity inputs use per-tab `sessionStorage`; production identity remains the configured server-side bearer-token/identity-provider path.

## Information architecture

The primary console is available at `/` and `/ui/console` and contains five work areas:

- **Overzicht** — runtime health, release/environment identity, connector state and governance summary.
- **Intelligence** — governed intelligence search and result triage.
- **Governance** — review followed by separately authorized external share approval.
- **Audit** — read-only recent audit evidence with event hashes.
- **Security** — privileged CISO controls such as token revocation.

Specialized role views remain available for focused workflows:

- `/ui/analyst-search`
- `/ui/share-approval`
- `/ui/auditor`
- `/ui/ciso-security`

All views use the shared `/ui/design-system.css` visual language.

## Visual system

The console uses a dense but calm security-operations layout with:

- persistent desktop navigation and compact mobile navigation;
- clear workspace headings and explanatory copy;
- status pills and KPI cards for current state;
- restrained surface elevation and borders rather than decorative effects;
- explicit primary, secondary, danger and ghost actions;
- consistent tables, cards, forms and inline status regions;
- responsive breakpoints for desktop, tablet and mobile use.

The design intentionally avoids relying on color alone: text labels, hierarchy and symbols accompany state colors.

## Interaction model

### Identity

The header exposes the active local/dev/staging test identity. Configuration opens in a modal dialog and is scoped to the current browser tab. Production authentication is not replaced by this UX helper.

### Intelligence search

Search is presented as a primary analyst action. Results appear as structured cards with title, summary and available metadata. The control is disabled client-side when the session lacks `read:intelligence`; server authorization remains authoritative.

### Governed decisions

Review and external sharing are separate cards and separate endpoints. The interface communicates separation of duties before the high-impact action. The server continues to reject unauthorized or self-approved decisions.

### Audit evidence

Audit evidence is displayed as a read-only table with action, principal, decision, resource and event hash. The view does not expose mutation controls.

### Security operations

Token revocation is isolated in a security-specific work area and requires `revoke:tokens` for a human principal.

## Accessibility contract

Repository-controlled frontend validation covers structure and browser behavior, including keyboard interaction, focus visibility, responsive reflow, critical journeys, text resize/spacing and supported browsers. Genuine VoiceOver/NVDA execution remains an external Phase 6 evidence requirement and is not claimed complete by this release.

## Security contract

The frontend does not alter these invariants:

- server-side RBAC is authoritative;
- service accounts do not receive human publication authority;
- human share approval remains separate from review;
- audit evidence remains read-only in the auditor surface;
- credentials/tokens are not embedded in HTML or source-controlled documentation;
- CSP, no-store behavior and anti-framing controls remain applied to UI responses.

## External test focus for rc6

External UX validation should assess:

- orientation and navigation without prior DTMO knowledge;
- clarity of current platform and connector state;
- analyst search efficiency and result comprehension;
- ability to distinguish review from share approval;
- error/loading/empty-state comprehension;
- mobile/tablet reflow;
- keyboard-only use;
- genuine VoiceOver and NVDA behavior;
- comprehension of privileged security operations.

Findings should be recorded with browser/assistive-technology versions, target release identity and reproducible steps.
