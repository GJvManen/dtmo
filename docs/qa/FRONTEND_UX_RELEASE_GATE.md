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

## Validation history

PR #112 initial exact head `0e6bc86b425b4e6511520bd6734f79baf7413d97` is **not accepted**. It produced 11 failing workflow-level RC9 gates (22 failing checks when fail-closed aggregate jobs are included).

RUN-163 through RUN-165 progressively restored the accepted frontend contracts. RUN-166 validation head `b33f270b201527249f847107863ee1184954f352` completed 46/48 registered workflows successfully. RC9 Reflow and RC9 Contrast were confirmed green, demonstrating the RUN-166 product fixes were effective.

The only failures on `b33f270b201527249f847107863ee1184954f352` were:

- RC9 Text Spacing Accessibility Gate;
- RC9 Text Resize Accessibility Gate.

Each workflow includes a primary evidence job and a fail-closed aggregate job, so GitHub surfaces these as four failed checks.

Decoded logs show one shared cause: the intentional `.sr-only` label for Analyst intelligence search was included in visual clipping geometry. The label is required for accessible naming and must remain available to assistive technology. RUN-167 therefore corrects the visual-evidence scope: `.sr-only` nodes are excluded only from rendered text geometry measurements. The label is not removed or made `aria-hidden`.

A complete fresh exact-head matrix is required after RUN-167. No result from a prior failed head can be reused as release PASS evidence.

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

`CI_VALIDATION_PENDING` for RUN-167. PR #112 must not merge until every registered workflow succeeds on one final exact head.
