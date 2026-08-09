# RC9.10 — A11Y-001 Session-Status Remediation

Status: `PASS`

## Objective

Remediate the single deterministic blocker `A11Y-001` found by RC9.9: asynchronous principal/session resolution on the four accepted critical surfaces was not exposed as a programmatic status message.

## Accepted scope

Affected surfaces:

- governed share approval (`/ui/share-approval`);
- analyst intelligence search (`/ui/analyst-search`);
- CISO token revocation (`/ui/ciso-security`);
- auditor read-only evidence (`/ui/auditor`).

Each principal/session element carries `role="status"`, `aria-live="polite"` and `aria-atomic="true"`. The existing JavaScript continues to replace `Resolving authenticated principal…` with the backend-resolved subject and roles. The accepted regression evidence also proves that the role-authorized critical control becomes visible after the same real `/api/v1/ui/session` resolution.

## Acceptance evidence

PR #68 exact head `a962ddb158adf264737bf5da3bfea024767aba81` completed all 28 registered workflows successfully. Retained artifact `9038822061` has digest `sha256:49370bd7f46f80cbecde6248c6f9ee722eb8614ea4a98480b0069024e165efc1` and was independently inspected. JUnit recorded 1 test, 0 failures, 0 errors and 0 skips. Machine-readable evidence covers all four critical surfaces and records `principal_role_status`, `principal_aria_live_polite`, `principal_aria_atomic_true`, `async_session_text_resolved` and `rbac_governed_control_visible`; server logs show real `/api/v1/ui/session` 200 responses for every surface.

PR #68 merged with expected-head protection as `b1626913841f3ba373eeb52e8301fd41f314489a`.

## Governance invariants

- RBAC remains backend-derived from `/api/v1/ui/session`.
- No authorization decision moved into the browser.
- Separation of duties is unchanged.
- Human share approval remains separate and mandatory.
- No production personal data, credentials or live intelligence were introduced.
- Existing persistence, audit-chain and security gates remain authoritative.

## Claim boundary

This PASS closes only `A11Y-001` for its bounded programmatic-status semantics. It does not prove genuine VoiceOver/NVDA announcement behavior, product-wide WCAG 2.2 AA conformance, measured contrast, 200% resize, 320 CSS px reflow, text-spacing behavior or complete focus-order evidence. Those remain separate Phase-6 evidence items.

## Current decision

`PASS` for RC9.10 bounded scope. Phase 6 remains `IN PROGRESS`.
