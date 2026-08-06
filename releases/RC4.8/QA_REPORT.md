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
| RC4.8 | Cross-sprint regression, migrations, search, security config, secured API routes and CI workflow contract | Committed; CI pending |

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

`RUN-20260806-012` isolated GitHub Actions execution from all DTMO application dependencies. The minimal canary was committed directly to `main` as `86c18aaa0fcd623d099c464f3bc4669392cc059b`, but the resulting commit exposed zero observable status contexts. This demonstrates that the current blocker is not caused by project tests, Python packaging, PostgreSQL, migrations, Docker, dependency review or aggregate gate logic.

The remaining blocker is repository/account Actions policy or integration-level check-run visibility. The connected integration cannot inspect or modify the repository Actions policy endpoint and cannot list generic push-triggered workflow runs, so it cannot safely resolve that external setting from this run.

## Release status

**CI VALIDATION PENDING — BLOCKED BY `CI-OPS-001`**

No successful status checks are currently exposed for either the RC4 workflow or the independent canary. A missing status is not a pass. GitHub Actions must be enabled and a canary plus the RC4 Quality Gate must complete successfully before `RC_READY` can be assigned.

## Required operational action

1. Open repository **Settings → Actions → General**.
2. Enable Actions for the repository and allow the GitHub-authored actions used by the workflows.
3. Manually dispatch **GitHub Actions Canary**.
4. Capture its run URL and successful conclusion.
5. Dispatch or push-trigger **RC4 Quality Gate** and attach its release-gate artifact to this report.

## Remaining technical follow-up

- Resolve `CI-OPS-001` and restore observable CI execution on `main`.
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

## External production acceptance

Tracked in GitHub issue #1. These checks require an actual target environment and independent execution.
