# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260809-100 — RC9.4 bounded auditor read-only browser journey](runs/RUN-20260809-100.md) — `CI_VALIDATION_PENDING`: added one critical auditor browser journey with backend-derived `read:audit`, independent API enforcement, analyst UI denial plus direct backend `403`, real persisted PostgreSQL audit rendering, audit-chain verification and proof that browser reads do not mutate audit row count; exact-head CI and retained browser evidence are required before PASS.
- [RUN-20260809-099 — RC9.3 exact-head acceptance](runs/RUN-20260809-099.md) — `PASS`: PR #55 exact head `e945702adff884f174a40393b3121f3aed99648b` passed all 22 registered workflows; retained artifact `9037014726` (`sha256:69256fdcaa01c5b9832bd711a669ff73ef4db5923cc0bc66beab47034cf2b795`) independently proved Chromium execution, backend-derived `revoke:tokens`, analyst backend denial, CISO revocation, Redis token state and persistent audit-chain validity; merged as `3743203bc1a6d93743af53fcb8d4257af153a710`.
- [RUN-20260809-098 — RC9.3 bounded CISO token-revocation browser journey](runs/RUN-20260809-098.md) — `CI_VALIDATION_PENDING`
- [RUN-20260809-097 — RC9.2 exact-head acceptance](runs/RUN-20260809-097.md) — `PASS`: PR #53 exact head `ebc9a7ca2ebb1c0e9b55c057eaad82d3f04e5afd` passed all 21 registered workflows; retained artifact `9036721912` (`sha256:308f98282c5520b3d96bc04f9b14c382dbdb83c1fc8817809c87ea03ce94a82e`) independently proved Chromium execution, backend-derived `read:intelligence`, loading/empty/success states and real backend 503 behavior; merged as `22bf74bb6c5c367195a3e67b0c8db4ec0489a449`.
- [RUN-20260809-096 — RC9.2 analyst browser operational states](runs/RUN-20260809-096.md) — `CI_VALIDATION_PENDING`
- [RUN-20260809-095 — RC9.1 exact-head acceptance](runs/RUN-20260809-095.md) — `PASS`: PR #50 exact head `005512e124ff6c37a5acd3d2b8e4ba8c823d4a01` passed all 20 required workflows; retained browser artifact `9036392289` (`sha256:111d879e048f5978927472da996020f398448dd0752407f60a3366dbfbbf0fd6`) independently proved Chromium execution, blocked reviewer self-approval, distinct-publisher approval, hidden service-account approval controls and backend-derived permissions; merged as `ef59eba29d7fa8b2d88b5674e7bb00e98c0dab18`.
- [RUN-20260809-094 — RC9.1 browser fixture persistence remediation](runs/RUN-20260809-094.md) — `CI_VALIDATION_PENDING`
- [RUN-20260809-093 — RC9.1 first deterministic CI remediation](runs/RUN-20260809-093.md) — `CI_VALIDATION_PENDING`
- [RUN-20260809-092 — RC9.1 governed browser share-approval E2E](runs/RUN-20260809-092.md) — `CI_VALIDATION_PENDING`
- [RUN-20260809-090 — RC8.8 capacity limits and scaling guidance](runs/RUN-20260809-090.md) — `CI_VALIDATION_PENDING`
- [RUN-20260809-089 — RC8.7 acceptance and merge](runs/RUN-20260809-087.md) — `PASS`
- [RUN-20260809-087 — RC8.7 exact-head evidence acceptance](runs/RUN-20260809-087.md) — `CI_VALIDATION_PENDING`
- [RUN-20260809-086 — RC8.7 bounded concurrency saturation](runs/RUN-20260809-086.md) — `CI_VALIDATION_PENDING`
- [RUN-20260809-085 — RC8.6 exact-head acceptance and merge](runs/RUN-20260809-085.md) — `PASS`
- [RUN-20260809-084 — RC8.6 degraded-dependency performance/correctness](runs/RUN-20260809-084.md) — `CI_VALIDATION_PENDING`
- [RUN-20260809-083 — RC8.5 exact-head acceptance and merge](runs/RUN-20260809-083.md) — `PASS`
- [RUN-20260809-082 — RC8.5 branch reconciliation against current main](runs/RUN-20260809-082.md) — `CI_VALIDATION_PENDING`
- [RUN-20260809-080 — Apache-2.0 and open-source governance baseline](runs/RUN-20260809-080.md) — `PASS`
- [RUN-20260808-079 — Current-state documentation reconciliation acceptance](runs/RUN-20260808-079.md) — `PASS`
- [RUN-20260808-077 — Current-state documentation, workflow and graph reconciliation](runs/RUN-20260808-077.md) — `CI_VALIDATION_PENDING`
- [RUN-20260808-075 — RC8.4 exact-head acceptance and merge](runs/RUN-20260808-075.md) — `PASS`
- [RUN-20260808-074 — RC8.4 bounded ingestion-throughput performance harness](runs/RUN-20260808-074.md) — `CI_VALIDATION_PENDING`
- [RUN-20260808-073 — RC8.3 exact-head acceptance and merge](runs/RUN-20260808-073.md) — `PASS`
- [RUN-20260808-072 — RC8.3 bounded OpenSearch search-read performance harness](runs/RUN-20260808-072.md) — `CI_VALIDATION_PENDING`
- [RUN-20260808-071 — RC8.2 exact-head acceptance and merge](runs/RUN-20260808-071.md) — `PASS`
- [RUN-20260808-070 — RC8.2 bounded API-read performance harness](runs/RUN-20260808-070.md) — `CI_VALIDATION_PENDING`
- [RUN-20260808-069 — RC8.1 exact-head acceptance and merge](runs/RUN-20260808-069.md) — `PASS`
- [RUN-20260808-068 — RC8.1 Phase 5 workload profile](runs/RUN-20260808-068.md) — `CI_VALIDATION_PENDING`
- [RUN-20260808-067 — RC7.10 exact-head acceptance and merge](runs/RUN-20260808-067.md) — `PASS`: Phase 4 accepted
- [RUN-20260808-066 — Phase 4 external connector acceptance](runs/RUN-20260808-066.md) — `CI_VALIDATION_PENDING`
- [RUN-20260807-065 — RC7.9 exact-head acceptance and merge](runs/RUN-20260807-065.md) — `PASS`

## Current decision

`RUN-20260809-100` is `CI_VALIDATION_PENDING`. RC9.1, RC9.2 and RC9.3 are accepted. Phase 6 remains `IN PROGRESS`. RC9.4 adds one critical auditor read-only browser journey but is not accepted until every required workflow succeeds on the exact final PR head and retained `browser-auditor-readonly-evidence` is independently inspected. Issue #1 external production gates remain open.

## Exactly one next priority

Inspect every registered workflow on the final RC9.4 PR head and independently inspect retained `browser-auditor-readonly-evidence`; repair only the first deterministic failure, or accept/merge only after complete successful exact-head evidence.
