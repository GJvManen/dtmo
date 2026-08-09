# RC9.4 — Auditor Read-only Browser Gate

Status: `CI_VALIDATION_PENDING`

## Objective

Prove one bounded critical auditor browser journey for persistent audit evidence, with browser-visible capability derived from backend RBAC and no mutation of audit records.

## Scope

The gate covers Chromium against the real FastAPI application, an authenticated `auditor` principal, backend-derived `read:audit` visibility, a real read-only `/api/v1/audit/events` endpoint backed by PostgreSQL, an analyst negative path, persistent audit-chain verification and before/after audit-rowcount equality.

Responsive behavior, keyboard-only navigation, cross-browser coverage, broad WCAG 2.2 AA validation, production identity-provider acceptance and external audit assurance are outside RC9.4.

## Governance invariants

- UI audit visibility derives from `/api/v1/ui/session` and the existing backend permission model.
- `/api/v1/audit/events` independently requires `read:audit`; hiding the UI is not treated as an authorization control.
- The auditor journey is read-only and cannot review intelligence, approve sharing, revoke tokens, publish intelligence or mutate audit records.
- Analyst direct access to the audit endpoint must fail with HTTP 403.
- The browser reads real persisted audit records from PostgreSQL.
- The persistent audit chain must verify after the browser journey.
- Audit-row count before and after the read journey must be identical.
- Synthetic fixture data is used; no production personal data is introduced.
- RBAC, separation of duties, privacy, provenance, auditability and separate human share approval remain unchanged.
- Missing, queued, failed or unexecuted CI is never PASS.

## Acceptance evidence required

PASS requires every repository-required workflow plus `RC9 Auditor Read-only Browser E2E Gate` to succeed on the exact final PR head. Retained `browser-auditor-readonly-evidence` must be independently inspected and prove exact-head identity, Chromium execution, backend-derived `read:audit`, analyst UI denial, analyst backend 403, persisted audit rendering, valid audit chain and no browser-induced audit mutation.

## Threat/CVE/vendor context

RC9.4 adds no production dependency and no external intelligence provider. Playwright/Chromium remain test-only infrastructure. Existing dependency/security gates remain authoritative; a material advisory discovered there blocks acceptance rather than being waived by this UX gate.

## Current decision

`CI_VALIDATION_PENDING` until exact-head GitHub Actions and retained evidence execute successfully.
