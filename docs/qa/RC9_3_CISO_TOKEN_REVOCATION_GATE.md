# RC9.3 — CISO Token Revocation Browser Gate

Status: `CI_VALIDATION_PENDING`

## Objective

Prove one bounded critical CISO browser journey for security-token revocation, with browser-visible capability derived from backend RBAC, direct backend denial for a non-authorized analyst, Redis-backed revocation state, and persistent audit-chain evidence.

## Scope

The gate covers Chromium against the real FastAPI application, an authenticated `ciso` principal, backend-derived `revoke:tokens` capability visibility, an authenticated `analyst` negative path, the real `/api/v1/security/tokens/revoke` endpoint, Redis token-state persistence, and PostgreSQL audit-chain persistence.

Responsive behavior, keyboard-only navigation, cross-browser coverage, broad WCAG 2.2 AA validation, auditor journey breadth, production identity-provider acceptance and production secrets management are outside RC9.3.

## Governance invariants

- UI revocation capability derives from `/api/v1/ui/session` and the backend permission model.
- An analyst cannot see the revocation control and a direct browser API request must still return `403`.
- A CISO may revoke a token only through the existing governed backend endpoint.
- Revocation must be persisted in Redis and accompanied by an immutable audit-chain event in PostgreSQL.
- The audit event must identify the human CISO principal, action, token resource, allow decision, request ID and revocation provenance.
- Token revocation does not alter intelligence review, share approval or publication behavior.
- RBAC, separation of duties, privacy, provenance, auditability and separate human share approval remain mandatory.
- Missing, queued, failed or unexecuted CI is never PASS.

## Acceptance evidence required

PASS requires the exact final PR head to complete every repository-required workflow plus `RC9 CISO Token Revocation Browser E2E Gate` successfully. Retained `browser-ciso-token-revocation-evidence` must be independently inspected and prove exact-head identity, Chromium execution, analyst UI denial, analyst backend `403`, successful CISO revocation, Redis state and persistent audit-chain verification.

## Threat/CVE/vendor context

RC9.3 adds no production dependency and no external intelligence source. Redis, PostgreSQL and Playwright/Chromium are already part of the existing platform/test architecture. Existing dependency, container, secrets and quality gates remain authoritative; any material finding blocks acceptance rather than being waived by this UX gate.

## Current decision

`CI_VALIDATION_PENDING` until exact-head GitHub Actions and retained evidence execute successfully.
