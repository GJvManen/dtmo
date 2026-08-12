# DTMO Production Readiness Roadmap

## Purpose

This roadmap separates **repository-controlled engineering acceptance**, **functional product acceptance** and **external staging/assurance/production approval**. A phase is complete only when its own evidence boundary is satisfied.

## Current status — 2026-08-12

| Phase | Scope | Status |
|---|---|---|
| 1 | CI and workflow integrity | `PASS` |
| 2 | Application security and identity | `PASS` |
| 3 | Data integrity and recovery | `PASS` |
| 4 | Connector reliability and provenance | `PASS` |
| 5 | Performance and scalability | `PASS` |
| 6 | Accessibility and operational UX | `PASS` |
| 7 | Observability and incident operations | `PASS` |
| RC13 | Functional unified-console acceptance | `AWAITING_OWNER_RETEST_AFTER_REPAIR` |
| 8 | Real staging acceptance | `PAUSED_PENDING_RC13_OWNER_RETEST` |
| 9 | Independent external assurance | `NOT COMPLETE` |
| 10 | Production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

## RC13 — current owner-retest gate

RC13.1–RC13.5 and earlier owner acceptance remain historical evidence. Subsequent accountable owner testing controls the current decision.

### Completed repair sequence

1. PR #159 repaired refresh behavior, empty-data truthfulness, Chrome interactions, Administration clarity, graph empty states and menu version clutter.
2. PR #160 repaired the canonical runtime image so `tools/provision_grafana_reader.py` is available to `grafana-db-provision`.
3. PR #161 removed duplicate default Prometheus datasource provisioning and added a real Grafana runtime health gate.
4. PR #163 repaired the source catalog secret-reference/bootstrap contract and was later owner-observed with bootstrap `200 OK`.
5. PR #165 repaired the local object-store credential contract; exact head `48688977836cf3305b9d90c064e945de00eefb49` completed every returned workflow successfully and merged as `65440afea6cfa3c3300b25d577d746432cc95700`.
6. PR #167 repaired canonical connector commit visibility; exact head `bf18ef2c499edcf8399d1f91b80190937538fdce` completed every returned workflow successfully and merged as `e9a0926f9e13b603be759a7d7036058685ebc3cc`.

### PR #167 acceptance boundary

The canonical console and dashboard summary derive intelligence data from PostgreSQL `IntelligenceItem` rows. PR #167 fixes the transaction lifecycle so a connector can no longer report successful canonical ingestion before the database session generator completes its post-`yield` commit. Commit failures propagate.

The dedicated `RC13 Canonical Connector Commit Visibility Gate` covers commit-before-return, commit-failure propagation, connector ingestion, source-to-intelligence console behavior and graphical dashboard contracts.

Repository acceptance is complete for this repair. Accountable functional owner retesting is still required.

### Remaining RC13 acceptance

The accountable project owner must retest current merged `main` and verify:

1. local Compose startup and Grafana remain healthy;
2. source catalog bootstrap remains successful;
3. a supported source run fetches and persists raw evidence;
4. canonical intelligence is durably committed to PostgreSQL;
5. recent Intelligence appears in the canonical console;
6. Overview KPIs and dashboard metrics update truthfully;
7. native severity/source/trend/review graphics render from the ingested dataset;
8. `Alles vernieuwen` executes a real refresh and re-enables;
9. Chrome navigation/operator controls remain functional;
10. governed Administration remains the primary admin workspace;
11. true empty datasets still render explicit empty states;
12. authorization/publication boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

## Documentation status note

PR #166 was closed unmerged because newer owner evidence made its post-#165 reconciliation stale; branch-only RUN-203 never became authoritative on `main`. RUN-204 remains immutable evidence of the blocker that led to PR #167. RUN-205 records the post-#167 merge state separately.

## Phase 8 — paused external staging gate

PR #157 remains valid historical/preparatory evidence. The external deployment identity record remains fail-closed and issue #158 remains open but paused.

No Phase 8 evidence may advance while RC13 awaits accountable owner retesting. After explicit owner acceptance, Phase 8 may return to `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY` and issue #158 can resume.

Repository CI, Docker Compose and staging emulators cannot substitute for a real staging deployment or owner functional acceptance.

## Phase 9 — external assurance

Phase 9 covers independent penetration testing, representative load/stress validation, full backup/restoration in the production-equivalent environment, platform hardening, secrets-management acceptance and required operational/stakeholder approval.

## Phase 10 — production decision

Phase 10 is the formal production go/no-go and begins only after all prior gates are complete and reviewable.

## Exactly one next priority

**Issue #150 — run accountable owner functional retesting on current merged `main` containing PR #167.**