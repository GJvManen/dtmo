# DTMO Current Project State

Last reconciled: **2026-08-12**

## Executive summary

DTMO `16.0.0rc12` has accepted repository-controlled engineering through Phase 7. Repository-controlled RC13 repairs through PR #167 are complete and exact-head green.

PR #167 repaired the built-in connector transaction boundary that could return before the PostgreSQL session generator completed its post-`yield` commit. Exact head `bf18ef2c499edcf8399d1f91b80190937538fdce` completed every returned workflow with `completed/success`; the PR merged with expected-head protection as `e9a0926f9e13b603be759a7d7036058685ebc3cc`.

**RC13 = `AWAITING_OWNER_RETEST_AFTER_REPAIR`.**

**Phase 8 = `PAUSED_PENDING_RC13_OWNER_RETEST`.**

DTMO remains **not production ready**.

## Phase status

| Phase | Status |
|---|---|
| 1. CI and workflow integrity | `PASS` |
| 2. Application security and identity | `PASS` |
| 3. Data integrity and recovery | `PASS` |
| 4. Connector reliability and provenance | `PASS` |
| 5. Performance and scalability | `PASS` |
| 6. Accessibility and operational UX | `PASS` |
| 7. Observability and incident operations | `PASS` |
| RC13. Functional unified-console acceptance | `AWAITING_OWNER_RETEST_AFTER_REPAIR` |
| 8. Real staging acceptance | `PAUSED_PENDING_RC13_OWNER_RETEST` |
| 9. Independent external assurance | `NOT COMPLETE` |
| 10. Production go/no-go | `NOT STARTED` |

## Valid recent repair evidence

- PR #159 console usability: repository-controlled `PASS`; merged `b4fffecc47f87b1edab8258514eaa130d949c195`.
- PR #160 Compose runtime packaging: repository-controlled `PASS`; merged `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`.
- PR #161 Grafana datasource provisioning: repository-controlled `PASS`; merged `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`.
- PR #163 source catalog secret-reference/bootstrap: repository-controlled `PASS`; merged `adc027143f1274c604a16446fe1ad2bdc7bc835f`; later owner-observed bootstrap `200 OK`.
- PR #165 local object-store credential contract: repository-controlled `PASS`; exact head `48688977836cf3305b9d90c064e945de00eefb49`; merged `65440afea6cfa3c3300b25d577d746432cc95700`.
- PR #167 canonical connector commit/console visibility: repository-controlled `PASS`; exact head `bf18ef2c499edcf8399d1f91b80190937538fdce`; complete returned workflow matrix `completed/success`; merged `e9a0926f9e13b603be759a7d7036058685ebc3cc`.

Historical evidence is not rewritten; newer accountable owner evidence controls the current readiness decision.

## PR #167 repair boundary

The canonical console and dashboard endpoints read PostgreSQL `IntelligenceItem` rows. Before PR #167, `ingest_connector_record()` returned from inside `async for session in database.session()`, while `Database.session()` executes `commit()` only after its `yield`. This could allow raw landing/indexing and construction of an inserted/indexed receipt without a durable canonical PostgreSQL row becoming visible to the console.

PR #167 now:

1. retains the persistence receipt while the database session generator completes;
2. returns connector success only after the canonical commit path completes;
3. propagates commit failure rather than reporting success;
4. regression-tests commit-before-return and commit-failure behavior;
5. keeps connector ingestion, source-to-intelligence console and graphical dashboard contracts together in the `RC13 Canonical Connector Commit Visibility Gate`.

Repository CI proves this controlled repair contract. It does not itself establish accountable owner acceptance on the local end-to-end environment.

## Required owner retest

Verify on current merged `main` containing PR #167:

1. local Compose startup and Grafana remain healthy;
2. source catalog bootstrap remains successful;
3. a supported source run fetches and lands raw evidence;
4. canonical PostgreSQL intelligence is durably committed;
5. recent Intelligence becomes visible in the unified console;
6. Overview KPIs and dashboard summary increase truthfully;
7. severity/source/trend/review graphics render from those records;
8. `Alles vernieuwen` refreshes and re-enables correctly;
9. Chrome navigation/operator controls and Administration remain functional;
10. empty states remain truthful when datasets are actually empty;
11. authorization/publication boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

## Documentation status

PR #166 was closed unmerged because newer owner evidence made its reconciliation stale. Its branch-only RUN-203 never became authoritative on `main`. RUN-20260812-204 remains immutable point-in-time evidence of the blocker that led to PR #167. This post-merge state is recorded separately in RUN-20260812-205.

## Phase 8 boundary

The Phase 8 intake/deployment identity record from PR #157 remains fail-closed preparatory evidence. Issue #158 remains paused. No real staging, pentest or production-readiness progression is allowed until RC13 receives explicit owner acceptance.

## Security and governance boundaries

Credentialed integrations store logical secret references only; raw secret values remain forbidden. Production bearer tokens remain externally issued. RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, analytics, Administration, Governance, CI or staging access cannot authorize publication.

## Exactly one current priority

**Run the accountable project-owner RC13 local functional retest on current merged `main` containing PR #167.**