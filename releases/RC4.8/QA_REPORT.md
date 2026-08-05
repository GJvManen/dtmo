# DTMO RC4.8 — QA report

## Automated checks committed

| Gate | Evidence | Blocking |
|---|---|---:|
| Raw-object integrity | `test_intelligence_lake_preserves_and_verifies_raw_payload` | Yes |
| Knowledge-graph evidence and confidence | `test_graph_relationship_requires_evidence_and_confidence` | Yes |
| Separation of review and share approval | `test_rbac_separates_review_and_share_approval` | Yes |
| Evidence-required reporting | `test_reporting_refuses_evidence_free_claims` | Yes |
| Production security configuration | `test_production_security.py` | Yes |
| OpenSearch indexing contract | `test_search_service.py` | Yes |
| Existing FastAPI core tests | `backend/tests/test_core.py` | Yes |
| Ruff | GitHub Actions | Yes |
| strict MyPy | GitHub Actions | Yes |
| Pytest coverage threshold | GitHub Actions | Yes |
| Alembic upgrade/downgrade cycle | GitHub Actions migration job | Yes |
| Container build and smoke test | GitHub Actions | Yes |
| Dependency review | GitHub Actions on pull requests | Yes |

## Sprint QA summary

| Sprint | Implemented gate | State |
|---|---|---|
| RC4.1 | Platform health, logging, scheduler and container checks | Configured |
| RC4.2 | Persistence deduplication, UTC-aware models and publication invariant | Implemented |
| RC4.3 | Immutable raw data, MinIO adapter and checksum verification | Implemented |
| RC4.4 | Connector registration and health validation | Implemented |
| RC4.5 | Graph evidence, confidence and query-depth validation | Implemented |
| RC4.6 | Responsive SOC workspace | Implemented; browser acceptance pending |
| RC4.7 | RBAC and evidence-gated reporting | Implemented |
| RC4.8 | Cross-sprint regression, migrations, search and production config tests | Committed; CI pending |

## Additional implementation completed

- Initial Alembic migration for intelligence, provenance and connector-run tables.
- Dedicated Docker Compose migration service before API startup.
- Asynchronous database session management with rollback on failure.
- MinIO object-store adapter with explicit TLS configuration.
- OpenSearch index creation, document indexing and filtered search service.
- Manual `workflow_dispatch` trigger and PostgreSQL migration validation in CI.
- `pytest-asyncio` and explicit async test configuration.

## Release status

**CI VALIDATION PENDING**

No successful status checks are currently exposed for the latest commit. A missing status is not a pass. GitHub Actions must be enabled and complete successfully before `RC_READY` can be assigned.

## Remaining technical follow-up

- Connect persistence, lake and search services to authenticated FastAPI routes.
- Add browser-based accessibility and end-to-end tests.
- Add live connector contract tests with controlled credentials.
- Enable OpenSearch security and TLS in staging and production.
- Add backup and complete restoration automation.

## External production acceptance

Tracked in GitHub issue #1. These checks require an actual target environment and independent execution.
