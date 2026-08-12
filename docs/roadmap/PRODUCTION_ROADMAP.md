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

RC13.1–RC13.5 and earlier owner acceptance remain historical evidence. Subsequent owner testing exposed additional defects and drove the bounded repair sequence below.

### Completed repair sequence

1. PR #159 repaired refresh behavior, empty-data truthfulness, Chrome interactions, Administration clarity, graph empty states and menu version clutter.
2. PR #160 repaired the canonical runtime image so `tools/provision_grafana_reader.py` is available to `grafana-db-provision`.
3. PR #161 removed duplicate default Prometheus datasource provisioning and added a real Grafana 13.1.0 runtime health gate.
4. PR #163 repaired the source-catalog secret-reference/bootstrap contract. Final exact head `4198f06e360929d3937065b8528237741cbe189a` completed every returned workflow successfully and merged with expected-head protection as `adc027143f1274c604a16446fe1ad2bdc7bc835f`.

The latest owner run had already confirmed the bounded startup path for #160 and #161. PR #163 now makes executable `env:VARIABLE` references consistent across catalog, registry and runtime, normalizes legacy `env://VARIABLE`, preserves external secret-manager references, rejects raw secrets and regression-tests supported catalog bootstrap for idempotency and disabled-by-default registration.

### Remaining RC13 acceptance

The accountable project owner must retest current merged `main` and verify:

1. local Compose startup remains successful;
2. Grafana remains healthy;
3. supported source catalog bootstrap works without HTTP 500 and remains idempotent;
4. bootstrapped sources remain disabled until explicitly enabled;
5. source validation/run controls behave truthfully;
6. `Alles vernieuwen` executes a real refresh and exposes loading/success/failure state;
7. empty canonical intelligence never produces a false `Data bijgewerkt` claim;
8. zero-only intelligence datasets render explicit empty states;
9. Chrome navigation and operator controls work without page/console errors;
10. governed Administration is the primary admin workspace;
11. after successful source ingestion with valid local configuration, Intelligence, Overview and analytics update truthfully;
12. authorization/publication boundaries remain unchanged.

The earlier MinIO credential symptom is not classified as a repository defect because the owner explicitly identified the local `.env` as incorrect and asked to skip that point.

Only explicit accountable owner acceptance closes RC13.

## Phase 8 — paused external staging gate

PR #157 remains valid historical/preparatory evidence. The external deployment identity record remains fail-closed and issue #158 remains open but paused.

No Phase 8 evidence may advance while RC13 awaits owner retest. After successful owner acceptance, Phase 8 may return to `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY` and issue #158 can resume.

Repository CI, Docker Compose and staging emulators cannot substitute for a real staging deployment or owner functional acceptance.

## Phase 9 — external assurance

Phase 9 covers independent penetration testing, representative load/stress validation, full backup/restoration in the production-equivalent environment, platform hardening, secrets-management acceptance and required operational/stakeholder approval.

## Phase 10 — production decision

Phase 10 is the formal production go/no-go and begins only after all prior gates are complete and reviewable.

## Exactly one next priority

**Issue #150 — accountable project-owner local Compose and functional-console retest of current merged `main`.**
