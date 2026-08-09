# RC9.6 — Responsive Layout Browser Gate

Status: `CI_VALIDATION_PENDING`

## Objective

Prove one bounded responsive-layout gate across the four accepted critical browser surfaces at representative mobile, tablet and desktop viewports.

## Scope

The dedicated Chromium gate covers governed share approval, analyst search, CISO token revocation and auditor read-only evidence at 360×800, 768×1024 and 1440×900 viewports. It verifies that the document and body do not create blocking horizontal overflow and that every visible interactive control remains inside the viewport with a minimum 24 px rendered width and height.

The gate uses the real `/api/v1/ui/session` endpoint so role/capability visibility remains backend-derived. It performs no business mutation and introduces no production data.

Supported-browser breadth and broad WCAG 2.2 AA validation remain outside RC9.6.

## Governance invariants

- Backend-derived RBAC capability visibility remains real.
- The responsive test performs no review, share approval, token revocation or audit mutation.
- RC9.1–RC9.4 remain authoritative for backend authorization, separation of duties and persistence behavior.
- Human share approval remains separate from review.
- No production personal data or live intelligence is introduced.
- Privacy, provenance and auditability remain unchanged.
- Missing, queued, failed or unexecuted CI is never PASS.

## Acceptance evidence required

PASS requires every repository-required workflow plus `RC9 Responsive Layout E2E Gate` to succeed on the exact final PR head. Retained `browser-responsive-layout-evidence` must be independently inspected and prove exact-head identity, Chromium execution, all three representative viewport classes, all four accepted critical surfaces, no blocking horizontal overflow and viewport-contained interactive controls.

## Threat/CVE/vendor context

RC9.6 adds no production dependency, external provider or connector. Playwright/Chromium remain test-only infrastructure. Existing security and dependency gates remain authoritative; any material advisory surfaced by them blocks acceptance rather than being waived by this responsive-layout gate.

## Current decision

`CI_VALIDATION_PENDING` until exact-head GitHub Actions and retained evidence execute successfully.
