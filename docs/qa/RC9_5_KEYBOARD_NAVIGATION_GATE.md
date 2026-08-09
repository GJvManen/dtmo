# RC9.5 — Keyboard Navigation Accessibility Gate

Status: `CI_VALIDATION_PENDING`

## Objective

Prove one bounded keyboard-only accessibility gate across the four accepted critical browser journeys: governed share approval, analyst search, CISO token revocation and auditor read-only evidence.

## Scope

The dedicated Chromium gate validates that every interactive control on those accepted surfaces can be reached using sequential keyboard navigation, receives a visible focus indicator and can be activated with keyboard input only. Business-operation HTTP calls are intercepted with synthetic responses so RC9.5 evaluates keyboard/browser behavior without duplicating or mutating the already accepted governance, security and audit fixtures. `/api/v1/ui/session` remains real, so capability visibility still derives from backend RBAC.

Responsive behavior, supported-browser breadth and broad WCAG 2.2 AA validation remain outside RC9.5.

## Governance invariants

- No pointing-device interaction is used by the RC9.5 browser test.
- Backend-derived role/capability visibility remains real; the gate does not bypass `/api/v1/ui/session`.
- Business API calls are intercepted only inside the browser test to avoid side effects; RC9.1–RC9.4 remain authoritative for backend authorization and persistence behavior.
- Share review and human share approval remain distinct governed decisions.
- No production personal data or live intelligence is introduced.
- RBAC, separation of duties, privacy, provenance and auditability remain unchanged.
- Missing, queued, failed or unexecuted CI is never PASS.

## Acceptance evidence required

PASS requires every repository-required workflow plus `RC9 Keyboard Navigation E2E Gate` to succeed on the exact final PR head. Retained `browser-keyboard-navigation-evidence` must be independently inspected and prove exact-head identity, Chromium execution, keyboard-only input, no pointing-device use, visible focus, control reachability and keyboard activation across all four accepted surfaces.

## Threat/CVE/vendor context

RC9.5 adds no production dependency, external provider or connector. Playwright/Chromium remain test-only infrastructure. Existing dependency/security gates remain authoritative; a material advisory discovered there blocks acceptance rather than being waived by this accessibility gate.

## Current decision

`CI_VALIDATION_PENDING` until exact-head GitHub Actions and retained evidence execute successfully.
