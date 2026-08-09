# RC9.11 — Measured WCAG 2.2 Contrast Evidence

Status: `PASS`

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

## Accepted evidence

PR #70 exact head `61fad60558a8700c8e80f6f657976aec1c0c081b` completed all 29 registered workflows successfully.

Retained artifact: `9038987343`.
Digest: `sha256:a82e08c90851b70c74b789d87be59607011827c8634286eab3a5dd7843aebd68`.
JUnit: 1 test, 0 failures, 0 errors, 0 skips.

The retained JSON is exact-head bound and records PASS for all measured text, UI-boundary and keyboard-focus-indicator contrast across the four critical surfaces. The artifact records real backend session RBAC and preserved separate human share approval.

PR #70 was merged with expected-head protection as `9e66e864056a95eed135004ad0c12ad4f8da919b`.

## Governance invariants

Backend-derived RBAC, separation of duties, auditability and separate human share approval remain unchanged. No production data or credentials are used.

## Claim boundary

This PASS covers only the measured contrast requirements on the four tested critical surfaces in Chromium. It does not establish product-wide WCAG 2.2 AA conformance, 200% resize, 320 CSS px reflow, text-spacing behavior, complete focus-order evidence or genuine assistive-technology behavior.
