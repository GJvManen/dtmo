# RC9.8 — WCAG 2.2 AA Critical-Journey Gate

Status: `CI_VALIDATION_PENDING`

## Objective

Prove one bounded Phase-6 accessibility objective across the four already accepted critical journeys using an automated subset of applicable WCAG 2.2 AA checks.

## Scope

The dedicated Chromium gate evaluates governed share approval, analyst search, CISO token revocation and auditor read-only surfaces for declared document language, non-empty title, a main landmark, heading presence, duplicate IDs, image alternative attributes, accessible control names/labels, keyboard focusability and visible focus.

The gate uses the real `/api/v1/ui/session` path so capability visibility remains backend-derived. It introduces no production data and does not replace the already accepted backend authorization, persistence, separation-of-duties, responsive-layout or cross-browser gates.

## Claim boundary

This gate does **not** constitute product-wide WCAG 2.2 AA certification, assistive-technology certification, PDF/documentation accessibility certification or native-mobile accessibility certification. Manual accessibility review and criteria not automatable in this bounded gate remain separate evidence requirements.

## Governance invariants

- RBAC and role visibility remain backend-derived.
- Human share approval remains distinct from review.
- No production personal data or live intelligence is introduced.
- Existing accepted gates remain authoritative for backend authorization, persistence and audit-chain behavior.
- Missing, queued, failed or unexecuted CI is never PASS.

## Acceptance evidence required

PASS requires every registered repository workflow plus `RC9 WCAG Critical Journeys Gate` to complete successfully on the exact final PR head. Retained `browser-wcag-critical-journeys-evidence` must be independently inspected and prove exact-head identity, all four accepted surfaces, the declared automated checks, real backend-session RBAC and the explicit absence of a product-wide certification claim.

## Threat/CVE/vendor context

RC9.8 adds no production dependency, external connector, credential or provider. Chromium/Playwright remain existing test-only infrastructure. Existing dependency/security workflows remain authoritative for CVE and vendor-advisory evidence; any material advisory surfaced there blocks acceptance rather than being waived by this gate.

## Current decision

`CI_VALIDATION_PENDING` until exact-head GitHub Actions and retained evidence execute successfully.
