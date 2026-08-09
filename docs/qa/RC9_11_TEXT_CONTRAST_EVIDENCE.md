# RC9.11 — Measured WCAG 2.2 Text Contrast Evidence

Status: `CI_VALIDATION_PENDING`

## Objective

Produce bounded, independently retained rendered-text contrast evidence for WCAG 2.2 Success Criterion 1.4.3 across the four accepted critical browser surfaces.

Covered surfaces:
- governed share approval (`/ui/share-approval`);
- analyst intelligence search (`/ui/analyst-search`);
- CISO token revocation (`/ui/ciso-security`);
- auditor read-only evidence (`/ui/auditor`).

## Standard and thresholds

Primary normative source: W3C WCAG 2.2 SC 1.4.3 Contrast (Minimum).

- normal text: minimum 4.5:1;
- large-scale text: minimum 3:1;
- large-scale boundary used by the gate: rendered font size >= 24 CSS px at normal weight, or >= 18.5 CSS px at bold weight (>=700), following W3C G18/G145 guidance.

References:
- https://www.w3.org/TR/WCAG22/#contrast-minimum
- https://www.w3.org/WAI/WCAG22/Techniques/general/G18
- https://www.w3.org/WAI/WCAG22/Techniques/general/G145.html

## Evidence method

The dedicated Chromium gate:
1. resolves a real backend `/api/v1/ui/session` for the appropriate role on each surface;
2. waits for the role-authorized critical control to become visible;
3. enumerates visible rendered textual elements in the critical page content;
4. reads computed text color, font size, font weight and background colors;
5. composites transparent background layers against the page canvas;
6. calculates WCAG relative luminance and contrast ratio;
7. applies the correct 4.5:1 or 3:1 threshold per rendered text size/weight;
8. fails closed on any measured violation;
9. retains every measurement, exact head SHA, JUnit output and server log.

A background image encountered on a measured text element is treated as unsupported by this bounded measurement implementation and fails closed rather than being silently accepted.

## Governance invariants

- backend-derived RBAC remains authoritative;
- no authorization decision moves into the browser;
- separation of duties is unchanged;
- separate human share approval remains mandatory;
- no production data or credentials are used.

## Claim boundary

PASS for this gate, if evidenced, covers only SC 1.4.3 rendered text contrast on these four critical surfaces in the tested Chromium rendering. It does not establish SC 1.4.11 non-text contrast, product-wide WCAG 2.2 AA conformance, assistive-technology certification, 200% resize, 320 CSS px reflow, text-spacing behavior or complete focus-order evidence.

## Acceptance gate

PASS requires:
- every registered workflow on the exact final PR head completes successfully;
- retained `browser-text-contrast-evidence` is present and exact-head bound;
- JUnit has zero failures/errors/skips;
- all retained text measurements meet their applicable threshold;
- real backend session RBAC and human share approval are explicitly preserved.

Missing, queued, failed, cancelled or unexecuted CI is not PASS.
