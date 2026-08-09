# RC9.8 — WCAG 2.2 AA Critical-Journey Gate

Status: `PASS`

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

## Acceptance evidence

PR #65 exact head `34d2cce17372843cb51229648d1e5e62a66e4c04` completed all 27 registered workflows successfully, including `RC9 WCAG Critical Journeys Gate`.

Retained artifact `9038468839` (`sha256:c0ded460c73d6c10c8bb61fb4334711ef9f2723924034337b3b7a828b01eb97a`) was independently inspected and was unexpired and bound to the exact PR head. Its JUnit report contained 1 test, 0 failures, 0 errors and 0 skips. Its machine-readable evidence recorded the four accepted surfaces and the following automated checks: document language, document title, main landmark, heading presence, duplicate IDs, image alt attributes, control accessible names, keyboard focusability and visible focus. Server logs showed successful real `/api/v1/ui/session` requests for every covered surface.

The artifact also explicitly recorded that product-wide WCAG 2.2 AA certification and assistive-technology certification are not claimed, backend session RBAC is real, human share approval is preserved and no production data was used.

PR #65 was merged with expected-head protection as `5ca5c5e2cffde0700dde8b5aabd6ee3940f1b9c8`.

## Threat/CVE/vendor context

RC9.8 adds no production dependency, external connector, credential or provider. Chromium/Playwright remain existing test-only infrastructure. Existing dependency/security workflows remain authoritative for CVE and vendor-advisory evidence; all registered workflows succeeded on the exact accepted head.

## Current decision

`PASS` for this bounded automated critical-journey accessibility gate only. Phase 6 remains `IN PROGRESS` because the roadmap requires WCAG 2.2 AA compliance and no blocking accessibility defects, while manual/non-automatable accessibility evidence remains outstanding.
