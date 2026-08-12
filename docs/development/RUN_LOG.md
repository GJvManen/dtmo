# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Current runs

- [RUN-20260812-198 — RC13 Grafana datasource provisioning runtime failure](runs/RUN-20260812-198.md) — post-#160 owner retest progressed beyond the packaging repair but Grafana entered a restart loop because duplicate Prometheus provisioning files were both marked default; targeted repair is `PENDING_CI`.
- [RUN-20260812-197 — RC13 local Compose startup packaging blocker](runs/RUN-20260812-197.md) — historical point-in-time record of the missing runtime provisioner defect repaired and merged by PR #160.
- [RUN-20260812-196 — RC13 reopened owner-retest usability repair](runs/RUN-20260812-196.md) — historical point-in-time record of the owner-observed console defects that led to PR #159.
- [RUN-20260812-195 — RC13 owner acceptance and Phase 8.1 external deployment identity](runs/RUN-20260812-195.md) — historical point-in-time record: earlier owner acceptance closed RC13 and opened Phase 8 before the subsequent owner retest found new blockers.
- [RUN-20260811-194 — RC13.5 exact-head acceptance and owner-retest transition](runs/RUN-20260811-194.md) — historical point-in-time record in which RC13 awaited owner retest.
- [RUN-20260811-193 — RC13.4 acceptance and RC13.5 full browser acceptance](runs/RUN-20260811-193.md) — historical RC13.5 implementation record.
- [RUN-20260811-190 — Functional console acceptance reopened](runs/RUN-20260811-190.md) — first owner-observed functional blockers inserted RC13 and paused Phase 8.

## Historical evidence rule

Historical run records remain immutable point-in-time evidence. Newer evidence may change the current decision without rewriting the original run record.

## Current decision

- Phases 1–7: `PASS`.
- PR #159 console repair exact-head workflow matrix: historical repository-controlled `PASS`; merged as `b4fffecc47f87b1edab8258514eaa130d949c195`.
- PR #160 Compose runtime packaging repair exact-head workflow matrix: repository-controlled `PASS`; merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`.
- accountable project-owner post-#160 RC13 retest: `BLOCKED_BY_GRAFANA_DATASOURCE_PROVISIONING`.
- confirmed blocker: two Prometheus datasource provisioning files both declare `uid: dtmo-prometheus` and `isDefault: true`, causing Grafana 13.1.0 provisioning failure and restart loops.
- current Grafana provisioning repair: `PENDING_CI`.
- RC13 overall: `REOPENED / BLOCKED_INTERNAL`; issue #150 remains open.
- Phase 8: `PAUSED_PENDING_RC13_OWNER_RETEST`.
- Phase 9: `NOT COMPLETE`.
- Phase 10: `NOT STARTED`.

DTMO is not production ready.

## Exactly one next priority

**Complete the targeted Grafana datasource provisioning repair, require complete exact-head CI, merge, then resume the accountable project-owner RC13 retest.**
