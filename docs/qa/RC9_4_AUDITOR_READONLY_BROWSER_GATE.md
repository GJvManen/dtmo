# RC9.4 — Auditor Read-only Browser Gate

Status: `PASS`

## Objective

Prove one bounded critical auditor browser journey for persistent audit evidence, with browser-visible capability derived from backend RBAC and no mutation of audit records.

## Scope

The gate covers Chromium against the real FastAPI application, an authenticated `auditor` principal, backend-derived `read:audit` visibility, a real read-only `/api/v1/audit/events` endpoint backed by PostgreSQL, an analyst negative path, persistent audit-chain verification and before/after audit-rowcount equality.

Responsive behavior, keyboard-only navigation, cross-browser coverage, broad WCAG 2.2 AA validation, production identity-provider acceptance and external audit assurance are outside RC9.4.

## Governance invariants

- UI audit visibility derives from `/api/v1/ui/session` and the existing backend permission model.
- `/api/v1/audit/events` independently requires `read:audit`; hiding the UI is not treated as an authorization control.
- The auditor journey is read-only and cannot review intelligence, approve sharing, revoke tokens, publish intelligence or mutate audit records.
- Analyst direct access to the audit endpoint fails with HTTP 403.
- The browser reads real persisted audit records from PostgreSQL.
- The persistent audit chain verifies after the browser journey.
- Audit-row count before and after the read journey is identical.
- Synthetic fixture data is used; no production personal data is introduced.
- RBAC, separation of duties, privacy, provenance, auditability and separate human share approval remain unchanged.

## Accepted evidence

PR #57 exact head `487dbe1320a4ef820ff32f1c9ef8f8c7652a4868` completed all 23 registered workflows successfully. Retained artifact `9037246175`, digest `sha256:884950bf6789ecccedda51f0b2ff956a64328b30a9922ecf72414cc923707dc6`, is identity-bound to that exact head.

Independent inspection confirmed:

- Chromium executed against the real FastAPI target;
- UI permissions were backend-derived;
- `read:audit` was required;
- analyst audit control was hidden;
- direct analyst API access returned HTTP 403;
- auditor audit retrieval returned HTTP 200;
- persisted PostgreSQL audit records were rendered;
- the persistent audit chain verified;
- the browser read did not mutate audit row count;
- JUnit: 1 test, 0 failures, 0 errors, 0 skipped.

PR #57 was merged with expected-head protection as `c7877015869bf58dec3a5f2628d71c4b0c2cf97a`.

## Threat/CVE/vendor context

RC9.4 added no production dependency and no external intelligence provider. Playwright/Chromium remained test-only infrastructure. Existing dependency/security gates remained authoritative and all registered exact-head workflows succeeded.

## Current decision

`PASS`. RC9.4 is accepted. Phase 6 remains `IN PROGRESS` because keyboard navigation, responsive behavior, supported-browser breadth and broad WCAG 2.2 AA remain open.
