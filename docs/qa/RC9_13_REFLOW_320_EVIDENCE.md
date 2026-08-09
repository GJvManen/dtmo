# RC9.13 — 320 CSS px Reflow Evidence

Status: `CI_VALIDATION_PENDING`

## Objective

Produce bounded retained evidence for WCAG 2.2 SC 1.4.10 Reflow on the four accepted critical surfaces: `/ui/share-approval`, `/ui/analyst-search`, `/ui/ciso-security`, and `/ui/auditor`.

## Evidence method

The dedicated Chromium gate runs each critical surface at a 320x900 CSS-pixel viewport using the appropriate real backend-derived session role. It waits for the governed critical control, then verifies:

- document/body horizontal scroll width does not exceed the 320 CSS px viewport beyond a 1 px rounding tolerance;
- the main content region stays within the horizontal viewport;
- no visible descendant of `main` extends outside the horizontal viewport;
- all governed critical controls remain visible, horizontally contained and focusable.

The gate retains exact-head JSON with per-surface layout metrics/control boxes, JUnit and server logs and fails closed on missing or non-conforming evidence.

## Governance invariants

Backend-derived RBAC remains authoritative. Separation of duties, auditability and separate human share approval are unchanged. No business mutation, production credential or production data is used.

## Claim boundary

A PASS covers only the tested SC 1.4.10 behavior on these four critical surfaces in Chromium at 320x900 CSS px. No two-dimensional-content exception is used. This does not establish text-spacing conformance, complete focus-order evidence, genuine assistive-technology behavior or product-wide WCAG 2.2 AA conformance.

## Acceptance gate

PASS requires every registered workflow on the exact final PR head to complete successfully and retained `browser-reflow-320-evidence` to show zero horizontal overflow/off-viewport critical content with visible/focusable governed controls on all four surfaces. Missing, queued, failed, cancelled or unexecuted CI is not PASS.
