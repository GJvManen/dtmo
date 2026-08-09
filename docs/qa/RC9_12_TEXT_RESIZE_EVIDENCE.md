# RC9.12 — 200% Text Resize Evidence

Status: `PASS`

## Objective

Produce bounded retained evidence for WCAG 2.2 SC 1.4.4 Resize Text on the four accepted critical surfaces: `/ui/share-approval`, `/ui/analyst-search`, `/ui/ciso-security`, and `/ui/auditor`.

## Accepted evidence

PR #72 exact head `e13373120db938e5395828ac124d0a7e3b2e1be0` passed all 30 registered workflows. Retained artifact `9039100766` (`browser-text-resize-evidence`, digest `sha256:c635614fac302fb398d510ed2a26ea9311ef67ae8f7d26b6bab13c9c091c6708`) was independently inspected.

JUnit reports 1 test, 0 failures, 0 errors and 0 skips. The retained machine-readable evidence is exact-head bound, covers all four critical surfaces, records 200% target resizing, shows 2.0x rendered scaling for sampled/comparable visible text, no detected clipping or horizontal page overflow at the bounded 1440x900 viewport, and visible/focusable governed critical controls. Server logs show real `/api/v1/ui/session` requests on all four surfaces; health evidence preserves `publication_gate: human-approval-required`.

PR #72 was merged with expected-head protection as `9826f9ec2c27f88a806b8fec787224654067b9fc`.

## Governance invariants

Backend-derived RBAC remains authoritative; separation of duties, auditability and separate human share approval are unchanged. No production data or credentials are used.

## Claim boundary

This PASS covers only the tested SC 1.4.4 200% text-resize behavior on these four critical surfaces in Chromium at 1440x900. It does not establish 320 CSS px reflow, text-spacing behavior, complete focus-order evidence, assistive-technology certification or product-wide WCAG 2.2 AA conformance.
