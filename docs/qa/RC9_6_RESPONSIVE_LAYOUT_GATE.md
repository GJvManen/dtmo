# RC9.6 — Responsive Layout Browser Gate

Status: `PASS`

## Objective

Prove one bounded responsive-layout gate across the four accepted critical browser surfaces at representative mobile, tablet and desktop viewports.

## Scope

The dedicated Chromium gate covers governed share approval, analyst search, CISO token revocation and auditor read-only evidence at 360×800, 768×1024 and 1440×900 viewports. It verifies that the document and body do not create blocking horizontal overflow and that every visible interactive control remains inside the viewport with a minimum 24 px rendered width and height.

The gate uses the real `/api/v1/ui/session` endpoint so role/capability visibility remains backend-derived. It performs no business mutation and introduces no production data.

Supported-browser breadth and broad WCAG 2.2 AA validation remain outside RC9.6.

## Governance invariants

- Backend-derived RBAC capability visibility remains real.
- The responsive test performs no review, share approval, token revocation or audit mutation.
- RC9.1–RC9.5 remain authoritative for backend authorization, separation of duties, persistence and keyboard behavior.
- Human share approval remains separate from review.
- No production personal data or live intelligence is introduced.
- Privacy, provenance and auditability remain unchanged.
- Missing, queued, failed or unexecuted CI is never PASS.

## Acceptance evidence

PR #61 exact head `7e75f45fca15dc11be3a3c10d2d26797bdcdf92a` passed 25/25 registered workflows, including `RC9 Responsive Layout E2E Gate` and all regression gates.

Retained artifact `browser-responsive-layout-evidence`:

- artifact id: `9038042763`;
- digest: `sha256:9a0f218d68ea82a6cd564c923e8b5e90ec6550a43de853999faee87be8bfa62c`;
- exact head: `7e75f45fca15dc11be3a3c10d2d26797bdcdf92a`;
- decision: `pass`;
- browser: Chromium;
- viewports: 360×800, 768×1024, 1440×900;
- surfaces: share approval, analyst search, CISO token revocation, auditor read-only;
- blocking horizontal overflow: false;
- interactive controls within viewport: true;
- minimum rendered control dimension: 24 px;
- backend session RBAC real: true;
- business mutations executed: false;
- cross-browser claimed: false;
- broad WCAG 2.2 AA claimed: false.

JUnit reports 1 test, 0 failures, 0 errors and 0 skips. Retained server logs show successful health, UI and real `/api/v1/ui/session` requests across the representative viewports. Health evidence retains `publication_gate: human-approval-required`.

PR #61 was merged with expected-head protection as `a21cd14033f89a9294b060ef7bd071f7f026b281`.

## Threat/CVE/vendor context

RC9.6 adds no production dependency, external provider or connector. Playwright/Chromium remain test-only infrastructure. Existing security and dependency gates remain authoritative; any material advisory surfaced by them blocks later release acceptance rather than being waived by this responsive-layout gate.

## Current decision

`PASS` for this bounded responsive-layout objective only. Phase 6 remains `IN PROGRESS`; supported-browser breadth and broad WCAG 2.2 AA remain open.
