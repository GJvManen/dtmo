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

## RC13 — current gate

RC13.1–RC13.5 and earlier owner acceptance remain historical evidence. Subsequent accountable owner testing controls the current decision.

### Repository-controlled repair sequence

1. PR #159 repaired refresh behavior, empty-data truthfulness, Chrome interactions, Administration clarity, graph empty states and menu version clutter.
2. PR #160 repaired the canonical runtime image so `tools/provision_grafana_reader.py` is available to `grafana-db-provision`.
3. PR #161 removed duplicate default Prometheus datasource provisioning and added a real Grafana 13.1.0 runtime health gate.
4. PR #163 repaired the source catalog secret-reference/bootstrap contract; exact head `4198f06e360929d3937065b8528237741cbe189a` completed every returned workflow successfully and merged as `adc027143f1274c604a16446fe1ad2bdc7bc835f`; later owner testing observed bootstrap `200 OK`.
5. PR #165 repaired the local object-store credential contract; exact head `48688977836cf3305b9d90c064e945de00eefb49` completed every returned workflow successfully and merged with expected-head protection as `65440afea6cfa3c3300b25d577d746432cc95700`.

There is no current repository-controlled RC13 blocker. Repository CI still does not establish owner acceptance.

### Remaining RC13 acceptance

The accountable project owner must retest current merged `main` and verify:

1. local Compose startup remains successful;
2. Grafana remains healthy;
3. supported source catalog bootstrap remains successful and idempotent;
4. bootstrapped sources remain disabled by default until explicitly enabled;
5. a supported source run fetches and persists raw evidence without object-store authentication failure;
6. source validation/run controls behave truthfully;
7. `Alles vernieuwen` executes a real refresh and exposes loading/success/failure state;
8. empty canonical intelligence never produces a false `Data bijgewerkt` claim;
9. zero-only intelligence datasets render explicit empty states;
10. Chrome navigation and operator controls work without page/console errors;
11. governed Administration is the primary admin workspace;
12. after successful source ingestion, Intelligence, Overview and analytics update truthfully;
13. authorization/publication boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

### Object-store security boundary

PR #165 aligns credentials only in local-development Compose. Staging/production-equivalent deployments continue to require a distinct least-privilege `AISTOR_APP_ACCESS_KEY/AISTOR_APP_SECRET_KEY` identity separate from AIStor root/admin credentials.

## Documentation status note

RUN-20260812-202 remains immutable point-in-time evidence from before #165 exact-head completion. A later reconciliation record captures the current post-merge status rather than rewriting historical evidence.

PR #164 was closed unmerged because newer owner evidence superseded its status before merge; its branch-only RUN-201 never became authoritative on `main`.

## Phase 8 — paused external staging gate

PR #157 remains valid historical/preparatory evidence. The external deployment identity record remains fail-closed and issue #158 remains open but paused.

No Phase 8 evidence may advance until RC13 is explicitly owner-accepted. After successful owner acceptance, Phase 8 may return to `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY` and issue #158 can resume.

Repository CI, Docker Compose and staging emulators cannot substitute for a real staging deployment or owner functional acceptance.

## Phase 9 — external assurance

Phase 9 covers independent penetration testing, representative load/stress validation, full backup/restoration in the production-equivalent environment, platform hardening, secrets-management acceptance and required operational/stakeholder approval.

## Phase 10 — production decision

Phase 10 is the formal production go/no-go and begins only after all prior gates are complete and reviewable.

## Exactly one next priority

**Issue #150 — run the accountable owner functional retest on current merged `main` containing PR #165.**
