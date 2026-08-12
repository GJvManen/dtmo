# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Current runs

- [RUN-20260812-200 — RC13 source catalog bootstrap secret-reference blocker](runs/RUN-20260812-200.md) — the post-#161 owner retest confirmed the prior Compose/Grafana startup blockers are cleared, then exposed a repository contract mismatch that makes supported source-catalog bootstrap return HTTP 500; targeted repair is `PENDING_CI`.
- [RUN-20260812-199 — RC13 post-#161 status reconciliation](runs/RUN-20260812-199.md) — historical point-in-time record after PR #161 merged and before the next owner retest exposed the catalog-bootstrap blocker.
- [RUN-20260812-198 — RC13 Grafana datasource provisioning runtime failure](runs/RUN-20260812-198.md) — historical point-in-time record of the duplicate-default Grafana datasource failure repaired by PR #161.
- [RUN-20260812-197 — RC13 local Compose startup packaging blocker](runs/RUN-20260812-197.md) — historical point-in-time record of the missing runtime provisioner defect repaired by PR #160.
- [RUN-20260812-196 — RC13 reopened owner-retest usability repair](runs/RUN-20260812-196.md) — historical point-in-time record of the owner-observed console defects repaired by PR #159.
- [RUN-20260812-195 — RC13 owner acceptance and Phase 8.1 external deployment identity](runs/RUN-20260812-195.md) — historical point-in-time record: earlier owner acceptance closed RC13 and opened Phase 8 before subsequent retesting found new blockers.
- [RUN-20260811-194 — RC13.5 exact-head acceptance and owner-retest transition](runs/RUN-20260811-194.md) — historical RC13 owner-retest transition record.
- [RUN-20260811-193 — RC13.4 acceptance and RC13.5 full browser acceptance](runs/RUN-20260811-193.md) — historical RC13.5 implementation record.
- [RUN-20260811-190 — Functional console acceptance reopened](runs/RUN-20260811-190.md) — first owner-observed functional blockers inserted RC13 and paused Phase 8.

## Historical evidence rule

Historical run records remain immutable point-in-time evidence. Newer evidence may change the current decision without rewriting earlier records.

## Current decision

- Phases 1–7: `PASS`.
- PR #159 console usability repair: repository-controlled `PASS`; merged as `b4fffecc47f87b1edab8258514eaa130d949c195`.
- PR #160 Compose runtime packaging repair: repository-controlled `PASS`; merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`; the latest owner retest progressed past its former missing-file failure.
- PR #161 Grafana datasource provisioning repair: repository-controlled `PASS`; final exact head `e471d6368639a45cee6dccadd353a9068e5205e9`; merged as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`; the latest owner retest showed Grafana starting without the former duplicate-default restart loop.
- new confirmed repository blocker: supported source-catalog bootstrap fails because Cisco uses executable `env:CISCO_OPENVULN_TOKEN` while the registry rejected that syntax.
- targeted source-catalog secret-reference repair: `PENDING_CI`.
- RC13 overall: `REOPENED / BLOCKED_INTERNAL`; issue #150 remains open.
- Phase 8: `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`.
- Phase 9: `NOT COMPLETE`.
- Phase 10: `NOT STARTED`.

The MinIO `InvalidAccessKeyId` observed in the same owner log is not classified here as a repository defect because the owner explicitly identified the local `.env` as incorrect and asked to skip that configuration point. No successful source-ingestion claim is made from that attempt.

Repository CI and local runtime evidence do not manufacture accountable owner acceptance. DTMO is not production ready.

## Exactly one next priority

**Complete the source catalog secret-reference contract repair, require complete exact-head CI, merge, then resume accountable project-owner RC13 retesting.**
