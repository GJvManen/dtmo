# DTMO RC4.8 — QA report

## Automated checks committed

| Gate | Evidence | Blocking |
|---|---|---:|
| Raw-object integrity | `test_intelligence_lake_preserves_and_verifies_raw_payload` | Yes |
| Knowledge-graph evidence and confidence | `test_graph_relationship_requires_evidence_and_confidence` | Yes |
| Separation of review and share approval | `test_rbac_separates_review_and_share_approval` | Yes |
| Evidence-required reporting | `test_reporting_refuses_evidence_free_claims` | Yes |
| Existing FastAPI core tests | `backend/tests/test_core.py` | Yes |
| Ruff | GitHub Actions | Yes |
| strict MyPy | GitHub Actions | Yes |
| Pytest coverage threshold | GitHub Actions | Yes |
| Container build and smoke test | GitHub Actions | Yes |
| Dependency review | GitHub Actions on pull requests | Yes |

## Sprint QA summary

| Sprint | Implemented gate | State |
|---|---|---|
| RC4.1 | Platform health, logging, scheduler and container checks | Configured |
| RC4.2 | Persistence deduplication and publication invariant | Implemented |
| RC4.3 | Immutable raw data and checksum verification | Implemented |
| RC4.4 | Connector registration and health validation | Implemented |
| RC4.5 | Graph evidence, confidence and query-depth validation | Implemented |
| RC4.6 | Responsive SOC workspace | Implemented; browser acceptance pending |
| RC4.7 | RBAC and evidence-gated reporting | Implemented |
| RC4.8 | Cross-sprint regression suite | Committed; CI pending |

## Release status

**CI VALIDATION PENDING**

No successful status checks were available when this report was written. A missing status is not a pass. After the newest commit, GitHub Actions must complete and its results must be reviewed before `RC_READY` can be assigned.

## Known technical follow-up

- Generate and apply Alembic migrations from the persistence models.
- Add production S3/MinIO and graph-store adapters.
- Connect the frontend to authenticated API routes.
- Add browser-based accessibility and end-to-end tests.
- Add live connector contract tests with controlled credentials.
- Enable OpenSearch security and TLS in staging/production.

## External production acceptance

Tracked in GitHub issue #1. These checks require an actual target environment and independent execution.
