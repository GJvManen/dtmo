# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260808-076 — RC8.5 queue pressure and connector burst](runs/RUN-20260808-076.md) — `CI_VALIDATION_PENDING`: added a bounded asyncio queue-pressure harness driven by the accepted 250 records/s burst, connector parallelism 20 and <=900 s recovery budget; scaled CI fixture requires observable backpressure, zero data loss, zero duplicate candidates, preserved provenance and `publish_approved=false`; exact-head workflows and retained evidence remain required before PASS
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

`RUN-20260808-076` is `CI_VALIDATION_PENDING` for RC8.5. The queue-pressure/connector-burst implementation is committed and fail-closed by contract, but no exact-head workflow or retained runtime evidence is accepted until it actually executes successfully. Phase 5 remains `IN PROGRESS`; issue #1's independent representative load/stress gate remains open.

## Exactly one next priority

Inspect every required exact-head workflow for the RC8.5 pull request. Remediate only the earliest deterministic failure, or independently inspect retained queue-burst evidence and merge only if all required gates succeed. Degraded-dependency testing remains outside that acceptance run.
