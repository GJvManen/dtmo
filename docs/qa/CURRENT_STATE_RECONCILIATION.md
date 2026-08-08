# Current-State Documentation Reconciliation Gate

Status: `CI_VALIDATION_PENDING`

## Control objective

Ensure the repository's human-visible current-state documentation accurately reflects the implementation, workflows, accepted evidence and open work actually present on `main`.

## Verified repository facts

- RC8.2 API-read performance workflow exists on `main` at `.github/workflows/api-read-performance.yml`.
- RC8.3 OpenSearch search-read performance workflow exists on `main` at `.github/workflows/search-read-performance.yml`.
- RC8.4 ingestion-performance workflow exists on `main` at `.github/workflows/ingestion-performance.yml`.
- RC8.1 through RC8.4 have accepted mainline evidence and merge history.
- PR #42 / RC8.5 remains open and therefore is not an accepted mainline capability.
- Prior `README.md` content was stale, describing RC7.2 as active and Phase 5 as not started.

## Reconciled documentation

- `README.md` now states the current Phase 5 position.
- `docs/project/CURRENT_STATE.md` provides roadmap, runtime/governance and CI/evidence Mermaid graphs.
- Workflow inventory distinguishes mainline RC8.2–RC8.4 from pending RC8.5.
- Accepted bounded RC8.2–RC8.4 measurements are summarized without claiming the independent external load/stress gate.
- Security and governance invariants remain explicit.

## Acceptance rule

This reconciliation becomes `PASS` only after required GitHub Actions execute successfully on the exact documentation PR head. Configured, queued, cancelled, missing or unexecuted workflows are not PASS.

No product behavior, RBAC, separation of duties, privacy, provenance, auditability or human share-approval control is modified by this gate.