# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Current runs

- [RUN-20260812-206 — RC13 owner retest: supported-source normalization blockers](runs/RUN-20260812-206.md) — newest accountable owner evidence after PR #167: runtime and OpenSearch writes progress, while NVD FTP canonical URLs and `security-advisory` enum mismatch block complete canonical source-to-interface acceptance; bounded normalization repair is `PENDING_CI`.
- [RUN-20260812-204 — RC13 owner retest: source load not visible in canonical interface](runs/RUN-20260812-204.md) — historical owner evidence that led to PR #167.
- [RUN-20260812-202 — RC13 owner retest: catalog repaired, local object-store credential contract blocked](runs/RUN-20260812-202.md) — historical evidence that led to PR #165.
- [RUN-20260812-200 — RC13 source catalog bootstrap secret-reference blocker](runs/RUN-20260812-200.md) — historical record repaired by PR #163.
- [RUN-20260812-199 — RC13 post-#161 status reconciliation](runs/RUN-20260812-199.md) — historical point-in-time record.
- [RUN-20260812-198 — RC13 Grafana datasource provisioning runtime failure](runs/RUN-20260812-198.md) — historical duplicate-default datasource failure repaired by PR #161.
- [RUN-20260812-197 — RC13 local Compose startup packaging blocker](runs/RUN-20260812-197.md) — historical missing runtime provisioner defect repaired by PR #160.
- [RUN-20260812-196 — RC13 reopened owner-retest usability repair](runs/RUN-20260812-196.md) — historical console defects repaired by PR #159.

RUN-201, RUN-203 and RUN-205 existed only on unmerged/superseded documentation branches and never became authoritative on `main`. Historical run records that did reach `main` remain immutable.

## Historical evidence rule

Historical run records remain immutable point-in-time evidence. Newer evidence may change the current decision without rewriting earlier records.

## Current decision

- Phases 1–7: `PASS`.
- PR #159 console usability: repository-controlled `PASS`.
- PR #160 Compose runtime packaging: repository-controlled `PASS`.
- PR #161 Grafana datasource provisioning: repository-controlled `PASS`.
- PR #163 source catalog bootstrap: repository-controlled `PASS`; later owner-observed bootstrap 200.
- PR #165 local object-store credential contract: repository-controlled `PASS`; merged `65440afea6cfa3c3300b25d577d746432cc95700`.
- PR #167 canonical connector commit visibility: repository-controlled `PASS`; exact head `bf18ef2c499edcf8399d1f91b80190937538fdce`; merged `e9a0926f9e13b603be759a7d7036058685ebc3cc`.
- newest owner retest: runtime healthy and multiple OpenSearch documents created, but NVD FTP URL validation and advisory enum normalization failures remain.
- supported-source normalization repair: `PENDING_CI`.
- RC13 overall: `REOPENED / BLOCKED_INTERNAL`; issue #150 remains open.
- Phase 8: `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`.
- Phase 9: `NOT COMPLETE`.
- Phase 10: `NOT STARTED`.

Repository CI and local runtime evidence do not manufacture accountable owner acceptance. DTMO is not production ready.

## Exactly one next priority

**Complete the supported-source normalization repair, require complete exact-head CI, merge, then resume accountable project-owner RC13 retesting.**
