# RC9.1 — Browser Share Approval E2E Gate

Status: `CI_VALIDATION_PENDING`

## Objective

Prove one highest-risk Phase-6 user journey in a real browser: intelligence review followed by separate human share approval. Browser-visible actions must derive from backend-resolved permissions, and backend separation-of-duties must fail closed when the reviewer attempts to approve their own review.

## Scope

The bounded journey covers Chromium execution against the real FastAPI application, a synthetic PostgreSQL candidate, backend-derived UI capability visibility, review by an authenticated human, blocked same-principal share approval, successful approval by a distinct publisher, hidden service-account decision controls, distinct persisted reviewer/approver identities, and retained JUnit/server-log/machine-readable evidence.

Responsive testing, keyboard-only coverage, broad WCAG 2.2 AA validation, analyst/CISO/auditor journey breadth and cross-browser coverage remain outside RC9.1.

## Governance invariants

- UI actions derive from backend principal/permission resolution.
- Possessing review and share permissions does not override resource-state separation of duties.
- The same human principal cannot review and approve sharing of the same item.
- A distinct authorized publisher may approve only after review.
- Service accounts cannot review or approve external sharing.
- Synthetic fixtures only; no production personal data.
- Missing, queued, failed or unexecuted browser CI is never PASS.

## Acceptance evidence required

PASS requires the exact final PR head to complete every repository-required regression workflow plus `RC9 Browser Share Approval E2E Gate` successfully. Retained `browser-share-approval-evidence` must be independently inspected and prove exact-head identity, Chromium execution, self-approval denial, distinct publisher approval, service-account control hiding and human share approval.

## RUN-20260809-093 evidence

Superseded head `5891fdc46b9076707467ca42b26553ecb67ea17e` executed 20 workflows. Eighteen succeeded. RC4 Quality Gate failed because the generic pytest job collected the browser E2E test without the dedicated database/browser environment; its actual failure was inability to resolve database host `postgres`. The dedicated RC9.1 gate also executed and failed separately during the browser journey.

The first release-wide deterministic failure was remediated by making the browser test module conditional on explicit `DTMO_E2E_BASE_URL`. The dedicated RC9.1 workflow sets that variable and therefore continues to execute the E2E test; generic RC4 pytest does not.

## RUN-20260809-094 remediation

The dedicated superseded-head browser run reached PostgreSQL migrations, Uvicorn startup and Chromium successfully, then failed on the first review request with `409 intelligence item not found`. The synthetic candidate had been flushed but not committed before the separately running application process attempted to read it.

The fixture seed now explicitly commits after obtaining the candidate UUID and before browser interaction. This is the only behavioral change in RUN-20260809-094. It addresses cross-process transaction visibility without weakening RBAC, separation of duties, privacy, provenance, auditability or human share approval.

## Current decision

`CI_VALIDATION_PENDING`. Fresh exact-head GitHub Actions and retained evidence are required; superseded-head results cannot authorize merge.
