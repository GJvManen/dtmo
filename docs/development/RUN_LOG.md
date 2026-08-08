# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260809-080 — Apache-2.0 and open-source governance baseline](runs/RUN-20260809-080.md) — `PASS`: PR #44 exact head `38ba52f700a4324de6039db58422006ad8a17a96` passed all 16 registered required workflows; retained artifact `9028364655` (`sha256:0e63aed861c8e761d626413227f1f2817fe2e36d6a1291fa2a0ebcfac521d83a`) was independently inspected and recorded 5 governance tests, 0 failures/errors/skips; PR #44 merged with expected-head protection as `565c9df9eea133b2e7b1f58fb3d5d772c7753e9b`
- [RUN-20260808-079 — Current-state documentation reconciliation acceptance](runs/RUN-20260808-079.md) — `PASS`: PR #43 exact head `b0260a17200d7a223a9a04403d6dcaaba92b726c` was re-verified with all 15 registered RC4/RC6/RC7/RC8 workflows `completed/success` and merged with expected-head protection as `c79a1c3d4a4664d8972f95bcb444f2cdef660b34`; current-state README, workflow inventory and Mermaid graphs are now on `main`
- [RUN-20260808-077 — Current-state documentation, workflow and graph reconciliation](runs/RUN-20260808-077.md) — `CI_VALIDATION_PENDING`: verified RC8.2 API-read, RC8.3 search-read and RC8.4 ingestion workflows are present on `main`; identified the README as materially stale at RC7.2; added a current-state document with roadmap, runtime/governance and CI/evidence Mermaid graphs; explicitly kept RC8.5 / PR #42 pending and off main until accepted
- [RUN-20260808-075 — RC8.4 exact-head acceptance and merge](runs/RUN-20260808-075.md) — `PASS`: PR #41 exact head `d3ab690ea2b4144e21598f8c2d74ef55c6a066c6` passed all 15 required RC4/RC6/RC7/RC8 workflows; retained artifact `9024869189` (`sha256:bf419775b1ae51df4970e8e1ecceb319ab2841a574559d93d557394a72623b06`) independently verified 500/500 accepted records, 0 data loss, 0 duplicate candidates, 500/500 replay quarantine, 0% errors, 108081.257 records/s, preserved provenance and non-publication state; PR #41 merged with expected-head protection as `781bc043da64fdeb7fc18c69f25521a2f7f22f91`
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

`RUN-20260809-080` is `PASS` for the Apache-2.0/open-source-governance baseline. Licensing, NOTICE, governance policies, third-party rights boundaries, SPDX package metadata and dedicated regression/evidence protection are now on `main`. Mainline implementation remains accepted through RC8.4; RC8.5 remains independently gated in PR #42.

## Exactly one next priority

Return to RC8.5 / PR #42 and validate its exact-head queue-pressure/connector-burst evidence; remediate only the earliest deterministic failure or merge only after complete successful evidence.
