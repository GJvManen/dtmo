# RC9.7 — Supported-Browser Critical-Journey Gate

Status: `PASS`

## Objective

Prove one bounded Phase-6 browser-compatibility objective across the four already accepted critical journeys in Chromium, Firefox and WebKit.

## Scope

The dedicated gate runs governed share approval, analyst search, CISO token revocation and auditor read-only journeys independently in each supported browser. `/api/v1/ui/session` remains real, so capability visibility continues to derive from backend RBAC. Business-operation HTTP calls are synthetic inside this compatibility test to avoid duplicating or mutating the accepted RC9.1–RC9.4 persistence/security fixtures.

## Governance invariants

- RBAC and role visibility remain backend-derived.
- Share review and human share approval remain distinct decisions.
- No production personal data or live intelligence is introduced.
- Synthetic business responses are confined to browser compatibility testing.
- Existing accepted gates remain authoritative for backend authorization, persistence and audit-chain behavior.
- Missing, queued, failed or unexecuted CI is never PASS.

## Acceptance evidence

PR #63 exact head `6da6f5b6d2e65c7b6be99697f564eb76d5d1ec51` completed all 26 registered workflows successfully, including `RC9 Supported Browsers E2E Gate`.

Retained artifact `9038307443`, digest `sha256:fab6f3c93359cb5f3effd363bbb86c99dc632a5c6b3a78f006ad5e07f92d1d86`, was independently inspected and proves:

- exact-head identity;
- Chromium, Firefox and WebKit execution;
- all four accepted critical surfaces;
- 3 browser-specific JUnit cases with 0 failures, 0 errors and 0 skips;
- real backend `/api/v1/ui/session` calls for each surface in each browser;
- preserved `human-approval-required` publication gate;
- synthetic business-operation calls only inside the compatibility test;
- no product-wide or broad WCAG 2.2 AA claim.

PR #63 was merged using expected-head protection as `1e886ac3fbb1d6711a7bfe191aeaff919d648451`.

## Threat/CVE/vendor context

RC9.7 adds no production dependency, external connector, credential or production provider. Playwright browser engines remain test-only infrastructure. Existing dependency/security workflows remain authoritative for CVE and vendor-advisory evidence; any material advisory surfaced there blocks acceptance rather than being waived by this gate.

## Current decision

`PASS` for the bounded supported-browser critical-journey objective. Phase 6 remains `IN PROGRESS`; broad WCAG 2.2 AA validation remains a separate later objective.
