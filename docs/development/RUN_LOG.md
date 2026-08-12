# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Current runs

- [RUN-20260812-202 — RC13 owner retest: catalog repaired, local object-store credential contract blocked](runs/RUN-20260812-202.md) — owner evidence confirms PR #163 catalog bootstrap `200 OK`, then exposes a fresh-clone source-to-intelligence failure at the local AIStor credential boundary; bounded repair is `PENDING_CI`.
- [RUN-20260812-200 — RC13 source catalog bootstrap secret-reference blocker](runs/RUN-20260812-200.md) — historical point-in-time record of the catalog bootstrap HTTP 500 repaired by PR #163 and subsequently owner-observed as resolved.
- [RUN-20260812-199 — RC13 post-#161 status reconciliation](runs/RUN-20260812-199.md) — historical point-in-time record after PR #161 merged and before later owner retesting exposed further blockers.
- [RUN-20260812-198 — RC13 Grafana datasource provisioning runtime failure](runs/RUN-20260812-198.md) — historical point-in-time record of the duplicate-default Grafana datasource failure repaired by PR #161.
- [RUN-20260812-197 — RC13 local Compose startup packaging blocker](runs/RUN-20260812-197.md) — historical point-in-time record of the missing runtime provisioner defect repaired by PR #160.
- [RUN-20260812-196 — RC13 reopened owner-retest usability repair](runs/RUN-20260812-196.md) — historical point-in-time record of the owner-observed console defects repaired by PR #159.
- [RUN-20260812-195 — RC13 owner acceptance and Phase 8.1 external deployment identity](runs/RUN-20260812-195.md) — historical point-in-time record: earlier owner acceptance closed RC13 and opened Phase 8 before subsequent retesting found new blockers.
- [RUN-20260811-194 — RC13.5 exact-head acceptance and owner-retest transition](runs/RUN-20260811-194.md) — historical RC13 owner-retest transition record.
- [RUN-20260811-193 — RC13.4 acceptance and RC13.5 full browser acceptance](runs/RUN-20260811-193.md) — historical RC13.5 implementation record.
- [RUN-20260811-190 — Functional console acceptance reopened](runs/RUN-20260811-190.md) — first owner-observed functional blockers inserted RC13 and paused Phase 8.

RUN-201 existed only on the unmerged/superseded PR #164 branch. It never became authoritative on `main`; historical records that did reach `main` remain immutable.

## Historical evidence rule

Historical run records remain immutable point-in-time evidence. Newer evidence may change the current decision without rewriting earlier records.

## Current decision

- Phases 1–7: `PASS`.
- PR #159 console usability repair: repository-controlled `PASS`; merged as `b4fffecc47f87b1edab8258514eaa130d949c195`.
- PR #160 Compose runtime packaging repair: repository-controlled `PASS`; merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`; later owner evidence progressed beyond its former missing-file failure.
- PR #161 Grafana datasource provisioning repair: repository-controlled `PASS`; merged as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`; later owner evidence progressed beyond its former restart loop.
- PR #163 source catalog secret-reference/bootstrap repair: repository-controlled `PASS`; exact head `4198f06e360929d3937065b8528237741cbe189a`; merged as `adc027143f1274c604a16446fe1ad2bdc7bc835f`; latest owner run confirms catalog bootstrap `200 OK`.
- new confirmed repository blocker: local Compose API object-store credentials and local AIStor credentials are inconsistent in the shipped fresh-clone configuration contract, causing CISA source persistence to fail with `InvalidAccessKeyId`.
- targeted local object-store credential-contract repair: `PENDING_CI`.
- RC13 overall: `REOPENED / BLOCKED_INTERNAL`; issue #150 remains open.
- Phase 8: `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`.
- Phase 9: `NOT COMPLETE`.
- Phase 10: `NOT STARTED`.

## Tooling incident

An assistant tool call briefly created an empty `dummy` file directly on `main` and immediately removed it. The cleanup head is `0c3a4eb9f98cec875e3a80b92a61a1fe88b5ee92`. GitHub comparison from the #163 merge commit to the cleanup head reports no changed files, so repository content is unchanged. RUN-20260812-202 records this explicitly.

Repository CI and local runtime evidence do not manufacture accountable owner acceptance. DTMO is not production ready.

## Exactly one next priority

**Complete the local object-store credential contract repair, require complete exact-head CI, merge, then resume accountable project-owner RC13 retesting.**
