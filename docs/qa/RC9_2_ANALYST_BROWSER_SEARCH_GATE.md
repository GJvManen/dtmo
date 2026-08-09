# RC9.2 — Analyst Browser Search Operational-State Gate

Status: `CI_VALIDATION_PENDING`

## Objective

Prove one bounded critical analyst browser journey for intelligence search, with browser-visible capability derived from backend RBAC and explicit loading, empty, success and backend-error states.

## Scope

The gate covers Chromium against the real FastAPI application, an authenticated `analyst` principal, backend-derived `read:intelligence` capability visibility, deterministic loading/empty/success browser behavior, and an actual backend `503 search backend unavailable` error path when OpenSearch is intentionally absent from the bounded browser environment.

Responsive behavior, keyboard-only navigation, cross-browser coverage, broad WCAG 2.2 AA validation, CISO/auditor journey breadth and production OpenSearch acceptance are outside RC9.2.

## Governance invariants

- UI search capability derives from `/api/v1/ui/session` and the backend permission model.
- The analyst browser principal is human and receives only its configured role permissions.
- Search is read-only and cannot review, approve sharing or publish intelligence.
- Synthetic browser fixtures are used for deterministic empty/success rendering.
- The real backend error path remains fail-closed and does not fabricate results.
- RBAC, separation of duties, privacy, provenance, auditability and separate human share approval remain unchanged.
- Missing, queued, failed or unexecuted CI is never PASS.

## Acceptance evidence required

PASS requires the exact final PR head to complete all repository-required workflows plus `RC9 Analyst Search Browser E2E Gate` successfully. Retained `browser-analyst-search-evidence` must be independently inspected and prove exact-head identity, Chromium execution, backend-derived read permission, loading/empty/success states and the backend 503 error state.

## Threat/CVE/vendor context

RC9.2 adds no production dependency and no live intelligence provider. Playwright/Chromium were already present as test-only infrastructure from RC9.1. Existing dependency/security gates remain authoritative; a material advisory discovered there blocks acceptance rather than being waived by this UX gate.

## Current decision

`CI_VALIDATION_PENDING` until exact-head GitHub Actions and retained evidence execute successfully.
