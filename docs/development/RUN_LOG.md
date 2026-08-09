# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260809-093 — RC9.1 first deterministic CI remediation](runs/RUN-20260809-093.md) — `CI_VALIDATION_PENDING`: inspected superseded PR #50 head `5891fdc46b9076707467ca42b26553ecb67ea17e`; 18/20 workflows succeeded, RC4 Quality and RC9 Browser E2E failed; remediated only the release-wide RC4 test-isolation failure by ensuring the browser E2E module executes only when the dedicated `DTMO_E2E_BASE_URL` is set; fresh exact-head CI is required and the separate browser-journey failure was deliberately not remediated in this run
- [RUN-20260809-092 — RC9.1 governed browser share-approval E2E](runs/RUN-20260809-092.md) — `CI_VALIDATION_PENDING`: added a minimal governed browser decision UI, backend-derived permission visibility, Playwright Chromium E2E for review → blocked self-approval → separate publisher approval, service-account control hiding, persisted separation-of-duties assertions and a dedicated retained-evidence workflow
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

`RUN-20260809-093` is `CI_VALIDATION_PENDING`. The first release-wide deterministic RC9.1 failure was a generic-suite isolation leak and has been remediated. Because the remediation changed PR #50's head, no prior workflow success or browser artifact authorizes merge. Phase 6 remains `IN PROGRESS`.

## Exactly one next priority

Inspect all workflows on the new PR #50 exact head. Repair only the earliest remaining deterministic failure, or—if all required workflows succeed—independently inspect retained `browser-share-approval-evidence` and merge with expected-head protection.
