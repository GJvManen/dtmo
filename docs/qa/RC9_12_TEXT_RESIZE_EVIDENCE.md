# RC9.12 — 200% Text Resize Evidence

Status: `CI_VALIDATION_PENDING`

## Objective

Produce bounded retained evidence for WCAG 2.2 SC 1.4.4 Resize Text on the four accepted critical surfaces: `/ui/share-approval`, `/ui/analyst-search`, `/ui/ciso-security`, and `/ui/auditor`.

## Evidence method

The dedicated Chromium gate resolves the real backend session for each role, captures rendered baseline text sizes, applies a 200% root text size, then verifies that comparable visible text reaches at least 1.95x baseline size. It additionally checks for clipping of visible text/control content, horizontal page overflow in the tested desktop viewport, and continued visibility/focusability of each critical governed control.

The gate retains exact-head JSON, JUnit and server logs and fails closed on missing or below-threshold evidence.

## Governance invariants

Backend-derived RBAC remains authoritative; separation of duties, auditability and separate human share approval are unchanged. No production data or credentials are used.

## Claim boundary

A PASS covers only the tested SC 1.4.4 200% text-resize behavior on these four critical surfaces in Chromium at 1440x900. It does not establish 320 CSS px reflow, text-spacing behavior, complete focus-order evidence, assistive-technology certification or product-wide WCAG 2.2 AA conformance.

## Acceptance gate

PASS requires every registered workflow on the exact final PR head to complete successfully and retained `browser-text-resize-evidence` to show 200% scaling, no detected clipping/horizontal page overflow, and visible/focusable critical controls on all four surfaces. Missing, queued, failed, cancelled or unexecuted CI is not PASS.
