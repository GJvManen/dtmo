# RC9.11 — Measured WCAG 2.2 Contrast Evidence

Status: `CI_VALIDATION_PENDING`

## Objective

Produce bounded retained rendered-contrast evidence for the four accepted critical surfaces covering WCAG 2.2 SC 1.4.3 Contrast (Minimum) and the required UI-component/focus-indicator portions of SC 1.4.11 Non-text Contrast.

Covered surfaces: `/ui/share-approval`, `/ui/analyst-search`, `/ui/ciso-security`, `/ui/auditor`.

## Standards and thresholds

Primary normative source: W3C WCAG 2.2.
- normal text: >= 4.5:1;
- large-scale text: >= 3:1;
- UI-component visual boundary/state information: >= 3:1 against adjacent colors;
- visible focus indicator measured by this gate: >= 3:1 against adjacent rendered colors.

Large-scale text is classified by the gate at >=24 CSS px normal weight or >=18.5 CSS px bold (>=700), following W3C G18/G145 guidance.

References:
- https://www.w3.org/TR/WCAG22/#contrast-minimum
- https://www.w3.org/TR/WCAG22/#non-text-contrast
- https://www.w3.org/WAI/WCAG22/Techniques/general/G18
- https://www.w3.org/WAI/WCAG22/Techniques/general/G145.html

## Evidence method

The dedicated Chromium gate resolves the real backend session for each role, waits for the governed critical control, measures visible text foreground/background contrast, measures interactive component fill/border contrast against adjacent background, keyboard-tabs through every visible interactive control and measures the rendered focus outline against adjacent colors, then retains exact-head JSON plus JUnit and server logs. Transparent backgrounds are composited to the effective page background; unsupported background-image cases fail closed.

## Governance invariants

Backend-derived RBAC, separation of duties, auditability and separate human share approval remain unchanged. No production data or credentials are used.

## Claim boundary

A PASS covers only these measured contrast requirements on the four tested critical surfaces in Chromium. It does not establish product-wide WCAG 2.2 AA conformance, 200% resize, 320 CSS px reflow, text-spacing behavior, complete focus-order evidence or genuine assistive-technology behavior.

## Acceptance gate

PASS requires every registered exact-head workflow to succeed and retained `browser-contrast-evidence` to show zero text, UI-boundary or focus-indicator failures across all four surfaces. Missing, queued, failed, cancelled or unexecuted CI is not PASS.
