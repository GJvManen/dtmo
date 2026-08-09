# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260809-084 — RC8.6 degraded-dependency performance/correctness](runs/RUN-20260809-084.md) — `CI_VALIDATION_PENDING`: added a bounded synthetic temporary-outage harness for the representative `opensearch-index-sink`, focused zero-loss/zero-duplicate/fail-closed regressions, retained JSON/JUnit evidence and a dedicated aggregate workflow; exact-head CI and independent artifact inspection are required before PASS
- [RUN-20260809-083 — RC8.5 exact-head acceptance and merge](runs/RUN-20260809-083.md) — `PASS`: PR #42 exact head `65c7949624c3770ce91d00c34a957b6b2cb9946a` passed all 17 registered required workflows; retained artifact `9029584698` (`sha256:a934d6179f347e3bf9a198fcb155e7996c42fc670959c2cfd50453969969b974`) independently verified 250/250 accepted records, 170 backpressure events, queue depth 40/40, zero data loss, zero duplicate candidates, 0.602 s recovery and preserved provenance/non-publication; JUnit 6 tests, 0 failures/errors/skips; PR #42 merged with expected-head protection as `37a897aa39e33353c63f7b96192f06e61e200cdb`
- [RUN-20260809-082 — RC8.5 branch reconciliation against current main](runs/RUN-20260809-082.md) — `CI_VALIDATION_PENDING`: PR #42 was 30 commits behind `main`, non-mergeable and had no workflows for head `d96db2694afb720dba37f3236c2cfcff82c39b92`; the branch was reconciled to current main and only the bounded RC8.5 harness, focused regressions, retained-evidence workflow and audit documentation were restored; exact-head CI must execute again before acceptance
- [RUN-20260809-080 — Apache-2.0 and open-source governance baseline](runs/RUN-20260809-080.md) — `PASS`: PR #44 exact head `38ba52f700a4324de6039db58422006ad8a17a96` passed all 16 registered required workflows; retained artifact `9028364655` (`sha256:0e63aed861c8e761d626413227f1f2817fe2e36d6a1291fa2a0ebcfac521d83a`) was independently inspected and recorded 5 governance tests, 0 failures/errors/skips; PR #44 merged with expected-head protection as `565c9df9eea133b2e7b1f58fb3d5d772c7753e9b`
- [RUN-20260808-079 — Current-state documentation reconciliation acceptance](runs/RUN-20260808-079.md) — `PASS`: PR #43 exact head `b0260a17200d7a223a9a04403d6dcaaba92b726c` was re-verified with all 15 registered RC4/RC6/RC7/RC8 workflows `completed/success` and merged with expected-head protection as `c79a1c3d4a4664d8972f95bcb444f2cdef660b34`; current-state README, workflow inventory and Mermaid graphs are now on `main`
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

`RUN-20260809-084` is `CI_VALIDATION_PENDING` for RC8.6. The branch contains a bounded degraded-dependency correctness harness and dedicated retained-evidence gate, but no PASS may be claimed until the exact PR head executes every required workflow successfully and the retained evidence is independently inspected. Phase 5 remains `IN PROGRESS`; issue #1 external representative load/stress and production OpenSearch hardening remain open.

## Exactly one next priority

Inspect all required workflows on the exact RC8.6 PR head and independently inspect the retained degraded-dependency artifact; remediate only the earliest deterministic failure, or accept/merge only after complete successful evidence.
