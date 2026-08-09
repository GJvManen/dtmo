# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260809-095 — RC9.1 exact-head CI validation and acceptance](runs/RUN-20260809-095.md) — `PASS`: PR #50 exact head `005512e124ff6c37a5acd3d2b8e4ba8c823d4a01` passed all 20 required workflows; retained artifact `9036392289` (`sha256:111d879e048f5978927472da996020f398448dd0752407f60a3366dbfbbf0fd6`) independently verified Chromium execution, blocked reviewer self-approval, distinct publisher approval, service-account control hiding, backend-derived UI permissions and required human share approval; JUnit 1 test with 0 failures/errors/skips; PR #50 merged with expected-head protection as `ef59eba29d7fa8b2d88b5674e7bb00e98c0dab18`.
- [RUN-20260809-094 — RC9.1 browser fixture persistence remediation](runs/RUN-20260809-094.md) — `CI_VALIDATION_PENDING`: remediated the next known deterministic RC9.1 browser failure by explicitly committing the synthetic candidate before the separately running Uvicorn/browser process consumes it; no prior CI result authorizes the new head.
- [RUN-20260809-093 — RC9.1 first deterministic CI remediation](runs/RUN-20260809-093.md) — `CI_VALIDATION_PENDING`: superseded PR #50 head `5891fdc46b9076707467ca42b26553ecb67ea17e` ran 20 workflows; 18 succeeded while RC4 Quality and RC9 Browser E2E failed. Only the first release-wide deterministic failure was remediated: the browser E2E module now executes only when the dedicated `DTMO_E2E_BASE_URL` environment is present. The separate browser journey failure remains for fresh exact-head evidence. No prior workflow success authorizes merge after head movement.
- [RUN-20260809-092 — RC9.1 governed browser share-approval E2E](runs/RUN-20260809-092.md) — `CI_VALIDATION_PENDING`: added a minimal governed browser decision UI, backend-derived permission visibility, Playwright Chromium E2E for review → blocked self-approval → separate publisher approval, service-account control hiding, persisted separation-of-duties assertions and a dedicated retained-evidence workflow.
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

`RUN-20260809-095` is `PASS`. RC9.1 is accepted on `main` as `ef59eba29d7fa8b2d88b5674e7bb00e98c0dab18`. Phase 6 remains `IN PROGRESS` because additional critical user journeys, responsive/keyboard behavior, WCAG 2.2 AA and operational state coverage are still required. Issue #1 external production gates remain open.

## Exactly one next priority

Phase 6 / RC9.2 — add one bounded critical analyst browser journey, including explicit error/loading/empty-state behavior and backend RBAC consistency, while leaving responsive, keyboard and WCAG-wide acceptance for later Phase-6 objectives.
