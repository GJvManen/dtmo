# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260808-071 — RC8.2 exact-head acceptance and merge](runs/RUN-20260808-071.md) — `PASS`: PR #39 exact head `e8ab9132bab6da753087d4cc830bac6541eb99ff` passed all 13 required RC4/RC6/RC7/RC8 workflows; retained artifact `9022168980` (`sha256:ca930454d8795be70844ba22befe2ff4420c8c7002289b2c97c979bd9f889d30`) independently verified 500/500 successful API reads at 100.142 req/s, 0% errors, p95 1.878 ms, p99 11.059 ms and preserved governance markers; PR #39 merged with expected-head protection as `13fdadcfa83170b64713f3e72f7261501829e585`
- [RUN-20260808-070 — RC8.2 bounded API-read performance harness](runs/RUN-20260808-070.md) — `CI_VALIDATION_PENDING`: added a workload-profile-driven API-read harness, fail-closed latency/error/governance evaluation, focused regressions and a dedicated retained-evidence workflow against the real DTMO `/health` endpoint; exact-head CI and artifact inspection remain required before PASS
- [RUN-20260808-069 — RC8.1 exact-head acceptance and merge](runs/RUN-20260808-069.md) — `PASS`: PR #38 exact head `9e45a0e1f8991d42c841ebfa4e03b42fe64d4dbb` passed all 12 required RC4/RC6/RC7 workflows and merged with expected-head protection as `67ff969554fbced6b2efbd0e84b7d050bd16c3cc`; workload budgets are accepted targets, not measured performance results
- [RUN-20260808-068 — RC8.1 Phase 5 workload profile](runs/RUN-20260808-068.md) — `CI_VALIDATION_PENDING`: defined a machine-readable synthetic education-sector CTI workload, measurable API/search/ingestion/resource budgets, privacy/governance invariants and regression contract; no performance result is claimed until exact-head CI executes
- [RUN-20260808-067 — RC7.10 exact-head acceptance and merge](runs/RUN-20260808-067.md) — `PASS`: PR #37 exact head `32c62c557e1135dbce4ebf3b8ab03c33a6650cd3` passed all 12 required RC4/RC6/RC7 workflows and merged with expected-head protection as `d84d9edbee10a805ad4c3d904af5e1305bcef623`; Phase 4 accepted
- [RUN-20260808-066 — Phase 4 external connector acceptance](runs/RUN-20260808-066.md) — `CI_VALIDATION_PENDING`: project-owner external/manual attestation dated 2026-08-08 verified the remaining live-connector credentials, provider limits, licences/terms and provider-specific production acceptance; substantive Phase 4 requirements were satisfied pending acceptance-record exact-head CI
- [RUN-20260807-065 — RC7.9 exact-head acceptance and merge](runs/RUN-20260807-065.md) — `PASS`: exact head `0eee765b72d016489af248d2bf29e3b1dbd593db` passed all 12 required RC4/RC6/RC7 workflows; retained artifact `9003952153` independently verified timeout cancellation and governance; PR #36 merged with expected-head protection as `3c5e1ed278d86b5279a285e546d24e12fbaabd3f`

## Current decision

`RUN-20260808-071` is `PASS` for RC8.2. The exact PR head passed all required workflows and the retained API-read artifact was independently inspected before expected-head merge. The bounded internal API-read target is evidenced, but Phase 5 remains `IN PROGRESS`: search, ingestion, queue pressure, connector bursts, degraded dependencies and representative external load/stress acceptance remain unevidenced.

## Exactly one next priority

Implement a bounded synthetic OpenSearch/search-read performance harness driven by the accepted RC8.1 workload profile, with exact-head retained latency/error evidence and fail-closed governance evaluation. Do not broaden that run into ingestion, queue pressure, connector bursts or degraded-dependency testing.
