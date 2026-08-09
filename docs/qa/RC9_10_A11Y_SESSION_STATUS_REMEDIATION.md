# RC9.10 — A11Y-001 Session-Status Remediation

Status: `CI_VALIDATION_PENDING`

## Objective

Remediate the single deterministic blocker `A11Y-001` found by RC9.9: asynchronous principal/session resolution on the four accepted critical surfaces was not exposed as a programmatic status message.

## Scope

Affected surfaces:

- governed share approval (`/ui/share-approval`);
- analyst intelligence search (`/ui/analyst-search`);
- CISO token revocation (`/ui/ciso-security`);
- auditor read-only evidence (`/ui/auditor`).

Each principal/session element now carries `role="status"`, `aria-live="polite"` and `aria-atomic="true"`. The existing JavaScript continues to replace `Resolving authenticated principal…` with the backend-resolved subject and roles. The regression gate additionally proves that the role-authorized critical control becomes visible after the same real `/api/v1/ui/session` resolution.

## Governance invariants

- RBAC remains backend-derived from `/api/v1/ui/session`.
- No authorization decision is moved into the browser.
- Separation of duties is unchanged.
- Human share approval remains separate and mandatory.
- No production personal data, credentials or live intelligence are introduced.
- Existing persistence, audit-chain and security gates remain authoritative.

## Acceptance evidence required

PASS requires every registered workflow on the exact final PR head to complete successfully and retained `browser-a11y-session-status-evidence` to be independently inspected. Evidence must show all four surfaces, the three status semantics, resolved asynchronous identity text, visible RBAC-authorized control, real backend session RBAC and preserved human share approval.

Missing, queued, failed, cancelled or unexecuted CI is not PASS.

## Claim boundary

This remediation closes only `A11Y-001` if evidenced. It does not prove genuine VoiceOver/NVDA announcement behavior, product-wide WCAG 2.2 AA conformance, measured contrast, 200% resize, 320 CSS px reflow, text-spacing behavior or complete focus-order evidence. Those remain separate Phase-6 evidence items.

## Threat / CVE / vendor context

This change introduces no dependency, connector, credential or provider. Threat intelligence, education-sector incident history, CVE data and vendor advisories do not alter the bounded accessibility remediation. Existing security and dependency workflows remain authoritative.

## Current decision

`CI_VALIDATION_PENDING` until exact-head CI and retained browser evidence complete successfully.
