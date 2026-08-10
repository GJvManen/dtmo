# Frontend UX Release Gate — DTMO 16.0.0rc6

## Scope

This gate evaluates the repository-controlled professional frontend baseline introduced in 16.0.0rc6. It does not substitute for genuine assistive-technology execution or external user acceptance.

## Required repository evidence

The final exact release head must demonstrate:

1. root console is discoverable at `/` and `/ui/console`;
2. Overview, Intelligence, Governance, Audit and Security work areas are present and navigable;
3. specialized Analyst, Share Approval, Auditor and CISO views remain available;
4. search, review, share approval, audit read and token revocation remain wired to existing governed API endpoints;
5. client-side permission presentation never replaces server-side RBAC enforcement;
6. review and external share approval remain separate actions and permissions;
7. audit evidence remains read-only and individual rendered events remain independently addressable by event ID;
8. local/dev/staging identity helper uses `sessionStorage`, not `localStorage`, and does not embed credentials;
9. UI responses retain CSP/no-store/anti-framing protections;
10. keyboard focus, skip navigation, responsive reflow, reduced motion, measurable contrast and live status semantics are retained;
11. semantic loading/success/empty/error/forbidden states remain machine-observable where historically accepted;
12. registered browser/accessibility regression workflows execute on the final exact head;
13. all registered workflows complete successfully before release acceptance.

## First exact-head result — failed

PR #112 exact head `0e6bc86b425b4e6511520bd6734f79baf7413d97` is **not accepted**. It produced 11 failing workflow-level RC9 gates (22 failing checks when fail-closed aggregate jobs are included): Analyst Search Browser E2E, Keyboard Navigation, Auditor Read-only Browser E2E, Responsive Layout, CISO Token Revocation Browser E2E, Text Spacing, Reflow, Contrast, Session Status, Text Resize and Supported Browsers.

Directly observed regressions included lost `empty`/`forbidden` semantic states, missing `aria-atomic=true`, missing `data-event-id` on rendered audit events, absent visible focus on the analyst search input, 390 px document width at a 360 px viewport and decorative backgrounds that made automated contrast evidence fail closed.

RUN-163 introduces a compatibility remediation that preserves the professional rc6 information architecture while restoring these previously accepted RC9 contracts. The remediation must itself pass a complete fresh exact-head matrix; no result from the failed head can be reused as PASS evidence.

## External evidence not satisfied here

This gate does **not** claim completion of:

- genuine VoiceOver behavior;
- genuine NVDA behavior;
- real staging deployment parity;
- independent penetration testing;
- external operational/stakeholder acceptance;
- production go/no-go.

## Governance invariants

RBAC, least privilege, separation of duties, privacy, provenance, append-only auditability and human share approval remain mandatory. A visual affordance or disabled control is not an authorization control; the server is authoritative.

## Current decision

`CI_VALIDATION_PENDING` for the RUN-163 remediation. PR #112 must not merge until every registered workflow succeeds on the final exact head.
