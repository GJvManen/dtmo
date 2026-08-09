# RC9.7 — Supported-Browser Critical-Journey Gate

Status: `CI_VALIDATION_PENDING`

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

## Acceptance evidence required

PASS requires every registered repository workflow plus `RC9 Supported Browsers E2E Gate` to complete successfully on the exact final PR head. Retained `browser-supported-browsers-evidence` must be independently inspected and show Chromium, Firefox and WebKit execution, all four accepted surfaces, exact-head identity, real backend-session RBAC and no unsupported broad WCAG claim.

## Threat/CVE/vendor context

RC9.7 adds no production dependency, external connector, credential or production provider. Playwright browser engines remain test-only infrastructure. Existing dependency/security workflows remain authoritative for CVE and vendor-advisory evidence; any material advisory surfaced there blocks acceptance rather than being waived by this gate.

## Current decision

`CI_VALIDATION_PENDING` until exact-head GitHub Actions and retained evidence execute successfully.
