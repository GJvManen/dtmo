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
| RC13 | Functional unified-console acceptance | `REOPENED / BLOCKED_INTERNAL` |
| 8 | Real staging acceptance | `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST` |
| 9 | Independent external assurance | `NOT COMPLETE` |
| 10 | Production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

## RC13 — current reopened gate

RC13.1–RC13.5 and earlier owner acceptance remain historical evidence. Subsequent accountable owner testing controls the current decision.

### Completed repair sequence

1. PR #159 repaired refresh behavior, empty-data truthfulness, Chrome interactions, Administration clarity, graph empty states and menu version clutter.
2. PR #160 repaired the canonical runtime image so `tools/provision_grafana_reader.py` is available to `grafana-db-provision`.
3. PR #161 removed duplicate default Prometheus datasource provisioning and added a real Grafana 13.1.0 runtime health gate.
4. PR #163 repaired the source catalog secret-reference/bootstrap contract; final exact head `4198f06e360929d3937065b8528237741cbe189a` completed every returned workflow successfully and merged as `adc027143f1274c604a16446fe1ad2bdc7bc835f`.

The latest owner run confirms #160/#161/#163 on the observed path: startup proceeds, Grafana does not re-enter the former restart loop, and supported source catalog bootstrap returns `200 OK`.

### Current blocker — local object-store credential contract

The same fresh-clone run successfully fetched CISA KEV upstream data, then failed when raw evidence was written to the local object store with `InvalidAccessKeyId`.

Repository inspection confirmed a source-controlled local-development mismatch:

- API `.env.example` defaults before repair: `DTMO_MINIO_ACCESS_KEY=dtmo`, `DTMO_MINIO_SECRET_KEY=change-me-now`;
- AIStor local Compose identity: required `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`;
- no local provisioner created the `dtmo` identity.

A fresh-clone operator could therefore start the topology successfully but could not complete source-to-intelligence persistence with the shipped credential contract.

### Current bounded repair

Branch `rc13/local-objectstore-credential-contract`:

- aligns the effective local API object-store identity with the supplied local AIStor bootstrap identity;
- removes misleading runnable API object-store defaults from `.env.example`;
- marks the shared identity as a development-only topology exception;
- preserves distinct least-privilege `AISTOR_APP_ACCESS_KEY/AISTOR_APP_SECRET_KEY` requirements for the staging/production-equivalent model;
- tests both local consistency and staging separation;
- renders `docker compose config` in a dedicated exact-head gate and asserts the effective credentials match locally.

The repair is `PENDING_CI`. It is not accepted until every returned workflow on the final exact PR head is `completed/success`.

### Remaining RC13 acceptance after repair

The accountable project owner must retest current merged `main` and verify:

1. local Compose startup remains successful;
2. Grafana remains healthy;
3. source catalog bootstrap remains successful;
4. a supported source run fetches and persists raw evidence without object-store authentication failure;
5. source validation/run controls behave truthfully;
6. `Alles vernieuwen` executes a real refresh and exposes loading/success/failure state;
7. empty canonical intelligence never produces a false `Data bijgewerkt` claim;
8. zero-only intelligence datasets render explicit empty states;
9. Chrome navigation and operator controls work without page/console errors;
10. governed Administration is the primary admin workspace;
11. after successful source ingestion, Intelligence, Overview and analytics update truthfully;
12. authorization/publication boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

## Documentation status note

PR #164 was closed unmerged because its post-#163 `AWAITING_OWNER_RETEST` reconciliation became stale before merge when the new owner run exposed the object-store defect. Its branch-only RUN-201 never became authoritative on `main`.

The assistant tooling incident that briefly created and deleted an empty `dummy` file on `main` is documented in RUN-20260812-202. A GitHub compare from the #163 merge commit to the cleanup head returned no changed files.

## Phase 8 — paused external staging gate

PR #157 remains valid historical/preparatory evidence. The external deployment identity record remains fail-closed and issue #158 remains open but paused.

No Phase 8 evidence may advance while RC13 is blocked. After successful owner acceptance, Phase 8 may return to `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY` and issue #158 can resume.

Repository CI, Docker Compose and staging emulators cannot substitute for a real staging deployment or owner functional acceptance.

## Phase 9 — external assurance

Phase 9 covers independent penetration testing, representative load/stress validation, full backup/restoration in the production-equivalent environment, platform hardening, secrets-management acceptance and required operational/stakeholder approval.

## Phase 10 — production decision

Phase 10 is the formal production go/no-go and begins only after all prior gates are complete and reviewable.

## Exactly one next priority

**Issue #150 — complete the local object-store credential contract repair, require complete exact-head CI, merge, then resume accountable owner functional retesting.**
