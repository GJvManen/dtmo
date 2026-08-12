# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Current runs

- [RUN-20260812-204 — RC13 owner retest: source load not visible in canonical interface](runs/RUN-20260812-204.md) — newest accountable owner evidence: source loading appears to work but Intelligence, metrics and graphics remain empty; repository inspection confirms an early-return transaction defect can skip the canonical PostgreSQL commit; bounded repair is `PENDING_CI`.
- [RUN-20260812-202 — RC13 owner retest: catalog repaired, local object-store credential contract blocked](runs/RUN-20260812-202.md) — historical point-in-time evidence that led to PR #165.
- [RUN-20260812-200 — RC13 source catalog bootstrap secret-reference blocker](runs/RUN-20260812-200.md) — historical point-in-time record of the catalog bootstrap HTTP 500 repaired by PR #163.
- [RUN-20260812-199 — RC13 post-#161 status reconciliation](runs/RUN-20260812-199.md) — historical point-in-time record after PR #161 merged.
- [RUN-20260812-198 — RC13 Grafana datasource provisioning runtime failure](runs/RUN-20260812-198.md) — historical duplicate-default datasource failure repaired by PR #161.
- [RUN-20260812-197 — RC13 local Compose startup packaging blocker](runs/RUN-20260812-197.md) — historical missing runtime provisioner defect repaired by PR #160.
- [RUN-20260812-196 — RC13 reopened owner-retest usability repair](runs/RUN-20260812-196.md) — historical console defects repaired by PR #159.

RUN-201 and RUN-203 existed only on unmerged/superseded documentation branches and never became authoritative on `main`. Historical run records that did reach `main` remain immutable.

## Historical evidence rule

Historical run records remain immutable point-in-time evidence. Newer evidence may change the current decision without rewriting earlier records.

## Current decision

- Phases 1–7: `PASS`.
- PR #159 console usability: repository-controlled `PASS`; merged `b4fffecc47f87b1edab8258514eaa130d949c195`.
- PR #160 Compose runtime packaging: repository-controlled `PASS`; merged `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`.
- PR #161 Grafana datasource provisioning: repository-controlled `PASS`; merged `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`.
- PR #163 source catalog bootstrap: repository-controlled `PASS`; merged `adc027143f1274c604a16446fe1ad2bdc7bc835f`; later owner-observed bootstrap `200 OK`.
- PR #165 local object-store credential contract: repository-controlled `PASS`; exact head `48688977836cf3305b9d90c064e945de00eefb49`; complete returned workflow matrix success; merged `65440afea6cfa3c3300b25d577d746432cc95700`.
- newest owner retest: source loading appears successful but canonical UI intelligence/metrics/graphics remain empty.
- confirmed repository root cause: `ingest_connector_record()` could return before `Database.session()` resumed past `yield` and executed its commit.
- targeted canonical connector commit/console-visibility repair: `PENDING_CI`.
- RC13 overall: `REOPENED / BLOCKED_INTERNAL`; issue #150 remains open.
- Phase 8: `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`.
- Phase 9: `NOT COMPLETE`.
- Phase 10: `NOT STARTED`.

Repository CI and local runtime evidence do not manufacture accountable owner acceptance. DTMO is not production ready.

## Exactly one next priority

**Complete the canonical connector commit/console-visibility repair, require complete exact-head CI, merge, then resume accountable project-owner RC13 retesting.**
