# DTMO Current Project State

Last reconciled: **2026-08-12**

## Executive summary

DTMO `16.0.0rc12` has accepted repository-controlled engineering through Phase 7. Repository-controlled RC13 repairs through PR #165 remain valid.

PR #165 repaired the local AIStor/object-store credential contract and completed every returned workflow on exact head `48688977836cf3305b9d90c064e945de00eefb49`; it merged with expected-head protection as `65440afea6cfa3c3300b25d577d746432cc95700`.

The subsequent accountable owner retest reports a new internal blocker: source loading appears to succeed, but ingested intelligence is not visible in the canonical interface. Intelligence, Overview KPIs, metrics and native graphics therefore remain empty.

Repository inspection confirms a transaction-boundary defect in the built-in connector ingestion path. `ingest_connector_record()` returned from inside an `async for session in database.session()` body, while `Database.session()` performs its `commit()` only after the generator resumes beyond `yield`. The early return can therefore skip the durable canonical PostgreSQL commit even when raw landing/indexing has already occurred.

**RC13 = `REOPENED / BLOCKED_INTERNAL`.**

**Phase 8 = `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`.**

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
| RC13. Functional unified-console acceptance | `REOPENED / BLOCKED_INTERNAL` |
| 8. Real staging acceptance | `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST` |
| 9. Independent external assurance | `NOT COMPLETE` |
| 10. Production go/no-go | `NOT STARTED` |

## Valid recent repair evidence

- PR #159 console usability: repository-controlled `PASS`; merged as `b4fffecc47f87b1edab8258514eaa130d949c195`.
- PR #160 Compose runtime packaging: repository-controlled `PASS`; merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`.
- PR #161 Grafana datasource provisioning: repository-controlled `PASS`; merged as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`.
- PR #163 source catalog secret-reference/bootstrap: repository-controlled `PASS`; merged as `adc027143f1274c604a16446fe1ad2bdc7bc835f`; later owner-observed bootstrap `200 OK`.
- PR #165 local object-store credential contract: repository-controlled `PASS`; exact head `48688977836cf3305b9d90c064e945de00eefb49`; merged as `65440afea6cfa3c3300b25d577d746432cc95700`.

Historical evidence is not rewritten; newer owner-observed evidence controls the current readiness decision.

## Current RC13 blocker — canonical connector persistence visibility

The canonical UI and dashboard endpoints read `IntelligenceItem` rows from PostgreSQL:

- `/api/v1/console/recent-intelligence` returns recent `IntelligenceItem` records;
- `/api/v1/dashboards/summary` derives totals, source/severity/review distributions and the seven-day trend from the same model.

The built-in CISA path fetches and parses records, then calls `ingest_connector_record()`. Before repair that function returned immediately from the body of `async for session in database.session()`. Because `Database.session()` commits after its `yield`, the generator did not reach the commit path before connector success was returned.

The existing connector-pipeline test mocked `ingest_connector_record()` and therefore verified call counts/receipt fields but not durable canonical commit visibility.

## Current bounded repair

Branch `rc13/canonical-connector-commit-visibility`:

- preserves the persistence receipt while the async session generator runs to completion;
- returns a successful connector receipt only after the session commit path has completed;
- propagates a commit failure instead of reporting successful insertion;
- adds regression tests for commit-before-return and commit-failure propagation;
- adds `RC13 Canonical Connector Commit Visibility Gate` covering the new regression test plus the connector pipeline, source-to-intelligence console contract and graphical dashboard contract.

The repair is `PENDING_CI`. No repository pass is claimed until every returned workflow on the final exact PR head is `completed/success`.

## Documentation status

PR #166 was closed unmerged after this newer owner evidence made its post-#165 owner-retest-pending reconciliation stale. Its branch-only RUN-203 is not authoritative on `main`.

## Remaining owner acceptance after repair

After the repair is exact-head green and merged, verify on current `main`:

1. local Compose startup and Grafana remain healthy;
2. source catalog bootstrap remains successful;
3. a real supported source run fetches and lands raw evidence;
4. canonical PostgreSQL intelligence is durably committed;
5. recent Intelligence becomes visible in the unified console;
6. Overview KPIs and dashboard summary increase truthfully;
7. severity/source/trend/review graphics render from those records;
8. `Alles vernieuwen` refreshes and re-enables correctly;
9. Chrome navigation/operator controls and Administration remain functional;
10. empty states remain truthful when datasets are actually empty;
11. authorization/publication boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

## Phase 8 boundary

The Phase 8 intake/deployment identity record from PR #157 remains fail-closed preparatory evidence. Issue #158 remains paused. No real staging, pentest or production-readiness progression is allowed while RC13 is blocked.

## Security and governance boundaries

Credentialed integrations store logical secret references only; raw secret values remain forbidden. Production bearer tokens remain externally issued. RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, analytics, Administration, Governance, CI or staging access cannot authorize publication.

## Exactly one current priority

**Complete the canonical connector commit/console-visibility repair, require complete exact-head CI, merge, then resume accountable project-owner RC13 local functional retesting.**
