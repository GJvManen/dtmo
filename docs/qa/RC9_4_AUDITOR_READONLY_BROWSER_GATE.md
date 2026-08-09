# RC9.4 — Auditor Read-only Browser Gate

Status: `PASS`

## Objective

Prove one bounded critical auditor browser journey for persistent audit evidence, with browser-visible capability derived from backend RBAC and no mutation of audit records.

## Accepted exact-head evidence

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

## Governance invariants

- UI audit visibility derives from `/api/v1/ui/session` and the existing backend permission model.
- `/api/v1/audit/events` independently requires `read:audit`; hiding the UI is not treated as authorization.
- The auditor journey is read-only and cannot review intelligence, approve sharing, revoke tokens, publish intelligence or mutate audit records.
- Synthetic fixture data is used; no production personal data is introduced.
- RBAC, separation of duties, privacy, provenance, auditability and separate human share approval remain unchanged.

## Current decision

`PASS` for RC9.4. This historical gate remains accepted; current project status is tracked in `docs/development/RUN_LOG.md` and `docs/roadmap/PRODUCTION_ROADMAP.md`.
