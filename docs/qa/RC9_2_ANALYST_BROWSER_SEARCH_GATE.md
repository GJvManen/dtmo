# RC9.2 — Analyst Browser Search Operational-State Gate

Status: `PASS`

## Objective

Prove one bounded critical analyst browser journey for intelligence search, with browser-visible capability derived from backend RBAC and explicit loading, empty, success and backend-error states.

## Accepted evidence

PR #53 exact head `ebc9a7ca2ebb1c0e9b55c057eaad82d3f04e5afd` completed all 21 registered workflows successfully.

Retained artifact `9036721912`, digest `sha256:308f98282c5520b3d96bc04f9b14c382dbdb83c1fc8817809c87ea03ce94a82e`, is identity-bound to the accepted head. Independent inspection confirms Chromium execution, backend-derived `read:intelligence` capability visibility, loading/empty/success states, and a real backend `503 search backend unavailable` path. JUnit: 1 test, 0 failures, 0 errors, 0 skips. Server evidence records `GET /api/v1/intelligence/search?q=error` returning 503.

PR #53 merged with expected-head protection as `22bf74bb6c5c367195a3e67b0c8db4ec0489a449`.

## Governance invariants

- UI search capability derives from `/api/v1/ui/session` and backend RBAC.
- Analyst search is read-only and cannot review, approve sharing or publish intelligence.
- Synthetic fixtures are used only for deterministic rendering states.
- The backend error path fails closed and fabricates no results.
- RBAC, separation of duties, privacy, provenance, auditability and separate human share approval remain unchanged.
- Issue #1 external production gates remain independent and open.

## Remaining Phase-6 scope

CISO/auditor journey breadth, responsive behavior, keyboard-only navigation, supported-browser breadth and WCAG 2.2 AA remain unaccepted.
