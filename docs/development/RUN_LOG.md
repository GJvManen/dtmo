# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260809-090 — RC8.8 capacity limits and scaling guidance](runs/RUN-20260809-090.md) — `CI_VALIDATION_PENDING`: documented conservative internal capacity ceilings, scaling/headroom rules and revalidation triggers from accepted RC8.1–RC8.7 evidence; explicitly preserves issue #1's external representative load/stress gate and fail-closed governance; exact-head GitHub Actions must succeed before PASS/merge
- [RUN-20260809-089 — RC8.7 acceptance and merge](runs/RUN-20260809-087.md) — `PASS`: PR #46 final exact head `ba99df99ccfa2afba940a410b301bda0b493d0b2` passed all 19 registered workflows; retained artifact `9032891744` (`sha256:01b07d36a4c9ae86f9e5361c6f2b7735cfaa29693adbf44aa62b12544132b1aa`) independently verified concurrency 20/20, 40 reads, 40 unique ingests, read p95 5.876 ms, 0.0% errors, zero data loss and preserved non-publication; PR #46 merged with expected-head protection as `7ecd1bf88d0577074390a173847186c8a92e48b6`
- [RUN-20260809-087 — RC8.7 exact-head evidence acceptance](runs/RUN-20260809-087.md) — `CI_VALIDATION_PENDING`: PR #46 implementation head `adf18135e91c0e28c151f8255563aba69b8df008` passed all 19 registered workflows; retained artifact `9032235183` (`sha256:66099a09e34099c3befc63918bdea0a8d0baf2302368138303eb6c96ccc1852d`) independently verified concurrency 20, 40 reads, 40 ingests, 5.734 ms read p95, 0.0% errors, zero data loss, preserved non-publication, and JUnit 6 tests with 0 failures/errors/skips; because this audit record changed the PR head, fresh exact-head CI was required before final acceptance
- [RUN-20260809-086 — RC8.7 bounded concurrency saturation](runs/RUN-20260809-086.md) — `CI_VALIDATION_PENDING`: added a synthetic sustained concurrent read/ingest harness, focused regressions, dedicated retained-evidence workflow and fail-closed QA gate
- [RUN-20260809-085 — RC8.6 exact-head acceptance and merge](runs/RUN-20260809-085.md) — `PASS`: PR #45 exact head `e3c157505f4619ef2accbd1e2990fdc673c1cf86` passed all 18 registered required workflows; retained artifact `9030972060` (`sha256:f8ca3ccaac5b3bfb5ad9fbc30004d02f45b57ea6c84f4a7f33899178f160abbf`) independently verified 100/100 delivery, 20 buffered records during a 0.25 s dependency outage, 300 dependency-failure events, zero data loss, zero duplicate candidate deliveries, 1.013 s recovery, preserved provenance/non-publication, and JUnit 6 tests with 0 failures/errors/skips; PR #45 merged with expected-head protection as `fc42e76e60783bdf1670fe2e208ef9eff70e68bc`
- [RUN-20260809-084 — RC8.6 degraded-dependency performance/correctness](runs/RUN-20260809-084.md) — `CI_VALIDATION_PENDING`
- [RUN-20260809-083 — RC8.5 exact-head acceptance and merge](runs/RUN-20260809-083.md) — `PASS`: PR #42 exact head `65c7949624c3770ce91d00c34a957b6b2cb9946a` passed all 17 registered required workflows; retained artifact `9029584698` (`sha256:a934d6179f347e3bf9a198fcb155e7996c42fc670959c2cfd50453969969b974`) independently verified 250/250 accepted records, 170 backpressure events, queue depth 40/40, zero data loss, zero duplicate candidates, 0.602 s recovery and preserved provenance/non-publication; JUnit 6 tests, 0 failures/errors/skips; PR #42 merged with expected-head protection as `37a897aa39e33353c63f7b96192f06e61e200cdb`
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

`RUN-20260809-090` is `CI_VALIDATION_PENDING`. RC8.7 is accepted on `main` as `7ecd1bf88d0577074390a173847186c8a92e48b6`. RC8.8 now documents conservative capacity limits and scaling guidance from accepted internal evidence, but no PASS or Phase-5 completion is authorized until every registered workflow succeeds on the final RC8.8 PR head and the documentation is merged. Issue #1's independent representative load/stress and production OpenSearch hardening gates remain open.

## Exactly one next priority

Validate every registered workflow on the final RC8.8 PR head; if all are successful, merge with expected-head protection and mark internal Phase 5 `PASS`. If any workflow fails, repair only the first deterministic failure.
