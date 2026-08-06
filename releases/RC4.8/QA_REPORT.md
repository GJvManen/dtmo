# DTMO RC4.8 — QA report

## Automated checks committed

| Gate | Evidence | Blocking |
|---|---|---:|
| Raw-object integrity | `test_intelligence_lake_preserves_and_verifies_raw_payload` | Yes |
| Knowledge-graph evidence and confidence | `test_graph_relationship_requires_evidence_and_confidence` | Yes |
| Separation of review and share approval | `test_rbac_separates_review_and_share_approval` | Yes |
| Evidence-required reporting | `test_reporting_refuses_evidence_free_claims` | Yes |
| Production security configuration | `test_production_security.py` | Yes |
| API-key and role resolution | `test_api_auth.py` | Yes |
| Secured API route exposure | OpenAPI contract assertion in `test_api_auth.py` | Yes |
| OpenSearch indexing contract | `test_search_service.py` | Yes |
| CI workflow contract | `test_ci_workflow_contract.py` | Yes |
| Existing FastAPI core tests | `backend/tests/test_core.py` | Yes |
| Ruff | GitHub Actions | Yes |
| strict MyPy | GitHub Actions | Yes |
| Pytest coverage threshold | GitHub Actions | Yes |
| Alembic upgrade/downgrade cycle | GitHub Actions migration job | Yes |
| Container build and smoke test | GitHub Actions | Yes |
| Dependency review | GitHub Actions on pull requests | Yes |

## Integrated data flow

The versioned API now orchestrates:

1. API-key authentication;
2. subject and role resolution;
3. route-level RBAC;
4. request and provenance validation;
5. raw object landing in MinIO/S3 storage;
6. SHA-256 receipt generation;
7. candidate persistence in PostgreSQL;
8. provenance persistence;
9. OpenSearch indexing;
10. an explicit response containing review, share-approval and indexing state.

The ingestion contract cannot set `review_status=reviewed` or `share_approved=true`.

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
| RC4.8 | Cross-sprint regression, migrations, search, security config, secured API routes and CI workflow contract | Committed; full CI gate pending |

## Additional implementation completed

- Initial Alembic migration for intelligence, provenance and connector-run tables.
- Dedicated Docker Compose migration service before API startup.
- Asynchronous database session management with rollback on failure.
- MinIO object-store adapter with explicit TLS configuration.
- OpenSearch index creation, document indexing and filtered search service.
- Authenticated principal resolution and route-level RBAC.
- Versioned ingestion and search API routes.
- API and architecture documentation.
- Manual `workflow_dispatch` trigger and PostgreSQL migration validation in CI.
- Regression protection for release-critical workflow triggers, jobs and commands.
- `pytest-asyncio` and explicit async test configuration.
- A dependency-free GitHub Actions execution canary at `.github/workflows/actions-canary.yml`.

## Latest PDCA gate outcome

`RUN-20260806-013` confirms that basic GitHub Actions execution has been restored. The repository owner reported `GitHub Actions Canary #5` as green on 2026-08-06. This resolves `CI-OPS-001` for the bounded infrastructure objective and demonstrates that Actions can execute repository workflows.

The connected integration does not expose generic push/manual runs, so this evidence is recorded as operator-confirmed rather than API-fetched. The result is sufficient to close the basic execution blocker, but not sufficient to approve RC4.8.

## Release status

**CI EXECUTION RESTORED — FULL RC4 QUALITY GATE PENDING**

The canary has passed, but `RC_READY` is not assigned. The complete `RC4 Quality Gate` must still finish successfully, including workflow contracts, lint, strict MyPy, tests with the coverage threshold, migrations, container smoke testing, pull-request dependency review where applicable, and the aggregate `release-gate`.

## Required next action

Run **RC4 Quality Gate** on `main`. Record the workflow result and verify that the aggregate `release-gate` is green. Any failed job remains release-blocking and must be fixed before RC4.8 can receive `RC_READY`.

## Remaining technical follow-up

- Execute and validate the complete RC4 Quality Gate.
- Add a transactional outbox and retry worker for OpenSearch indexing.
- Add durable audit events for ingestion, review and share approval.
- Add browser-based accessibility and end-to-end tests.
- Add live connector contract tests with controlled credentials.
- Integrate an enterprise identity provider or identity-aware proxy.
- Enable OpenSearch security and TLS in staging and production.
- Add backup and complete restoration automation.

## Documentation evidence

- `docs/api/INTELLIGENCE_API.md`
- `docs/architecture/ADR-0001-SECURED-INTELLIGENCE-INGESTION.md`
- `docs/development/runs/RUN-20260805-002.md`
- `docs/development/runs/RUN-20260806-003.md`
- `docs/development/runs/RUN-20260806-012.md`
- `docs/development/runs/RUN-20260806-013.md`

## External production acceptance

Tracked in GitHub issue #1. These checks require an actual target environment and independent execution.
