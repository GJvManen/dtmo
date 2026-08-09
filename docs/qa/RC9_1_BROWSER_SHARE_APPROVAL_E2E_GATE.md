# RC9.1 — Browser Share Approval E2E Gate

Status: `CI_VALIDATION_PENDING`

## Objective

Prove one highest-risk Phase-6 user journey in a real browser: intelligence review followed by separate human share approval. Browser-visible actions must derive from backend-resolved permissions, and backend separation-of-duties must fail closed when the reviewer attempts to approve their own review.

## Scope

The bounded journey covers:

- Chromium browser execution against the real FastAPI application;
- a synthetic candidate intelligence record persisted in PostgreSQL;
- backend-derived UI capability visibility;
- review by an authenticated human principal;
- attempted self-approval by the same principal returning a governed conflict;
- successful share approval by a different authorized publisher;
- service-account approval controls remaining hidden;
- final persisted `review_status=reviewed` and `share_approved=true` with distinct `reviewed_by` and `share_approved_by` principals;
- retained JUnit, server-log and machine-readable browser evidence.

Responsive testing, keyboard-only coverage, broad WCAG 2.2 AA validation, analyst/CISO/auditor journey breadth and cross-browser coverage are explicitly outside RC9.1.

## Governance invariants

- UI actions are derived from the backend principal and permission model; the browser does not invent roles or permissions.
- Permission to review/share does not override resource-state separation of duties.
- The same human principal cannot review and then approve sharing of the same intelligence item.
- A publisher distinct from the reviewer may approve sharing only after review.
- Service accounts cannot review or approve external sharing.
- Synthetic fixtures only; no production personal data is used.
- Missing, queued, failed or unexecuted browser CI is never PASS.

## Acceptance evidence required

PASS requires the exact final PR head to complete all repository-required regression workflows plus `RC9 Browser Share Approval E2E Gate` successfully. Retained `browser-share-approval-evidence` must be independently inspected and prove the exact head, Chromium execution, self-approval denial, distinct publisher approval, service-account control hiding and human share-approval requirement.

## Threat/CVE/vendor context

RC9.1 introduces Playwright only as a test dependency and Chromium only in the dedicated CI job. No production runtime dependency or live intelligence provider is added. A dependency/security scan remains part of the existing release-wide gates; any material browser automation or dependency advisory discovered there blocks acceptance rather than being waived by this UI test.

## Current decision

`CI_VALIDATION_PENDING` until exact-head GitHub Actions and retained evidence execute successfully.
