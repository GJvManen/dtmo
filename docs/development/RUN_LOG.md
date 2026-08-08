# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260809-080 — Apache-2.0 and open-source governance baseline](runs/RUN-20260809-080.md) — `CI_VALIDATION_PENDING`: added the complete Apache-2.0 licence/NOTICE package, security/contribution/conduct/support policies, third-party licensing boundaries, SPDX package metadata, focused regressions and a dedicated retained-evidence Open Source Governance Gate; exact-head CI is required before acceptance
- [RUN-20260808-079 — Current-state documentation reconciliation acceptance](runs/RUN-20260808-079.md) — `PASS`: PR #43 exact head `b0260a17200d7a223a9a04403d6dcaaba92b726c` was re-verified with all 15 registered RC4/RC6/RC7/RC8 workflows `completed/success` and merged with expected-head protection as `c79a1c3d4a4664d8972f95bcb444f2cdef660b34`; current-state README, workflow inventory and Mermaid graphs are now on `main`
- [RUN-20260808-077 — Current-state documentation, workflow and graph reconciliation](runs/RUN-20260808-077.md) — `CI_VALIDATION_PENDING`: verified RC8.2 API-read, RC8.3 search-read and RC8.4 ingestion workflows are present on `main`; identified the README as materially stale at RC7.2; added a current-state document with roadmap, runtime/governance and CI/evidence Mermaid graphs; explicitly kept RC8.5 / PR #42 pending and off main until accepted
- [RUN-20260808-075 — RC8.4 exact-head acceptance and merge](runs/RUN-20260808-075.md) — `PASS`: PR #41 exact head `d3ab690ea2b4144e21598f8c2d74ef55c6a066c6` passed all 15 required RC4/RC6/RC7/RC8 workflows; retained artifact `9024869189` (`sha256:bf419775b1ae51df4970e8e1ecceb319ab2841a574559d93d557394a72623b06`) independently verified 500/500 accepted records, 0 data loss, 0 duplicate candidates, 500/500 replay quarantine, 0% errors, 108081.257 records/s, preserved provenance and non-publication state; PR #41 merged with expected-head protection as `781bc043da64fdeb7fc18c69f25521a2f7f22f91`
- [RUN-20260808-074 — RC8.4 bounded ingestion-throughput performance harness](runs/RUN-20260808-074.md) — `CI_VALIDATION_PENDING`: added a workload-profile-driven governed ingestion normalization/replay harness, 500-record scaled synthetic CI fixture, zero-data-loss and zero-duplicate-candidate acceptance checks, focused regressions and a dedicated retained-evidence workflow; exact-head CI and artifact inspection were required before PASS
- [RUN-20260808-073 — RC8.3 exact-head acceptance and merge](runs/RUN-20260808-073.md) — `PASS`: PR #40 exact head `78da9e8bc6ca6799bc6cf48d21ac79054bc9e8ae` passed all 14 required RC4/RC6/RC7/RC8 workflows; retained artifact `9023474648` verified bounded search performance and governance; PR #40 merged with expected-head protection as `635a9736f9cb3b5091f00b99fc89eb47574858ae`
- [RUN-20260808-072 — RC8.3 bounded OpenSearch search-read performance harness](runs/RUN-20260808-072.md) — `CI_VALIDATION_PENDING`
- [RUN-20260808-071 — RC8.2 exact-head acceptance and merge](runs/RUN-20260808-071.md) — `PASS`: PR #39 exact head `e8ab9132bab6da753087d4cc830bac6541eb99ff` passed all 13 required workflows; retained artifact `9022168980` verified bounded API-read performance and governance; PR #39 merged as `13fdadcfa83170b64713f3e72f7261501829e585`
- [RUN-20260808-070 — RC8.2 bounded API-read performance harness](runs/RUN-20260808-070.md) — `CI_VALIDATION_PENDING`
- [RUN-20260808-069 — RC8.1 exact-head acceptance and merge](runs/RUN-20260808-069.md) — `PASS`
- [RUN-20260808-068 — RC8.1 Phase 5 workload profile](runs/RUN-20260808-068.md) — `CI_VALIDATION_PENDING`
- [RUN-20260808-067 — RC7.10 exact-head acceptance and merge](runs/RUN-20260808-067.md) — `PASS`: Phase 4 accepted
- [RUN-20260808-066 — Phase 4 external connector acceptance](runs/RUN-20260808-066.md) — `CI_VALIDATION_PENDING`
- [RUN-20260807-065 — RC7.9 exact-head acceptance and merge](runs/RUN-20260807-065.md) — `PASS`

## Current decision

`RUN-20260809-080` is `CI_VALIDATION_PENDING` for the Apache-2.0/open-source-governance baseline. The branch now has an explicit project licence, NOTICE, governance policies, third-party rights boundary, SPDX Python metadata and dedicated regression/evidence protection. No PASS is claimed until exact-head workflows actually execute successfully and retained governance evidence is inspected. Mainline implementation remains accepted through RC8.4; RC8.5 remains separately gated in PR #42.

## Exactly one next priority

Validate RUN-20260809-080 on exact-head CI and independently inspect retained open-source-governance evidence; merge only after every required gate succeeds. After that acceptance, return to RC8.5 / PR #42 as the sole Phase-5 product priority.
