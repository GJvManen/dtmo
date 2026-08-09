# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260809-133 — bounded supported object-storage migration](runs/RUN-20260809-133.md) — `CI_VALIDATION_PENDING`: PR #89 prerequisite is verified 37/37 and merged; legacy `minio/minio` is removed from the supported Compose path, AIStor image/license/admin inputs now fail closed through external boundaries, S3 endpoint/persistence/human-approval invariants are preserved, and a dedicated retained-evidence workflow has been added. Acceptance awaits the complete exact-head CI matrix.
- [RUN-20260809-132 — supported object-storage target decision](runs/RUN-20260809-132.md) — `PASS`: PR #89 exact head `79c5684b7e65064efe480e6da7913fd437d52b6d` completed 37/37 workflows and merged as `83e880a289467151c6604e28cd4141118fb538a9`; ADR-0001 selects MinIO AIStor Enterprise Lite or Enterprise with active paid support as the supported successor.
- [RUN-20260809-131 — supported object-storage remediation blocker](runs/RUN-20260809-131.md) — `BLOCKED_EXTERNAL`: confirmed the vulnerable legacy MinIO pin could not truthfully be remediated with another unmaintained community runtime while satisfying the production support gate.
- [RUN-20260809-130 — RC10.4 exact-head acceptance and security-blocker reconciliation](runs/RUN-20260809-130.md) — `PASS`: exact head `036e3a6035794bb115d578919327f0d87fa1c596` passed 37/37 workflows and merged as `4af2f1ceb24ead103690584473118db738f169d3`.
- [RUN-20260809-129 — RC10.4 bounded storage-integrity alerting](runs/RUN-20260809-129.md) — `PASS`: PR #86 exact head `8aa56dacd64583de5e96c0fda188ba954437ffda` passed 37/37 workflows; retained artifact `9041327884`; JUnit 5/5; merged as `4d7494e8b8fcdcddb73349bf87157d8c16763c33`.
- [RUN-20260809-128 — RC10.3 exact-head acceptance and documentation reconciliation](runs/RUN-20260809-128.md) — `PASS`.
- [RUN-20260809-127 — RC10.3 bounded queue-backlog alerting](runs/RUN-20260809-127.md) — `PASS`: PR #84 passed all 36 workflows; retained artifact `9040996591`; JUnit 5/5.
- [RUN-20260809-126 — RC10.2 acceptance and historical documentation reconciliation](runs/RUN-20260809-126.md) — `PASS`.
- [RUN-20260809-125 — RC10.2 controlled connector-failure alerting](runs/RUN-20260809-125.md) — `PASS`: PR #82 passed all 35 workflows; retained artifact `9040485255`; JUnit 4/4.
- [RUN-20260809-124 — RC10.1 exact-head acceptance and documentation reconciliation](runs/RUN-20260809-124.md) — `PASS`.
- [RUN-20260809-123 — RC10.1 request observability baseline](runs/RUN-20260809-123.md) — `PASS`.
- [RUN-20260809-122 — RC9.16 genuine assistive-technology behavior](runs/RUN-20260809-122.md) — `BLOCKED_EXTERNAL`: real VoiceOver/NVDA behavior remains externally required.

## Current decision

Phase 1–5 internal roadmap gates are `PASS`. Phase 6 remains `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA behavior. Phase 7 is `IN PROGRESS`; RC10.1–RC10.4 are accepted for their bounded scopes.

The supported object-storage target decision is accepted. RUN-133 implements the repository migration contract from archived `minio/minio` to AIStor but remains `CI_VALIDATION_PENDING`. No commercial entitlement, production topology, production TLS/SSE, registry-digest attestation, secrets-manager acceptance or other issue #1 external gate is claimed complete.

## Exactly one next priority

Verify the complete exact-head CI matrix and retained migration evidence for RUN-133; merge only after every registered workflow succeeds. After acceptance, perform one bounded post-migration security/recovery/storage-integrity reconciliation before resuming Phase 7 / RC10.5 API-error alerting.
