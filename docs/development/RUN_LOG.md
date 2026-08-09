# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260809-135 — bounded API-error alerting](runs/RUN-20260809-135.md) — `CI_VALIDATION_PENDING`: PR #91 exact head `d81caaa372b0cf3e079023eb255a57fd4892d6e0` passed 38/38 workflows and merged as `23af430c041e3f0e203b7a7f7a6c69f3eea79055`; RC10.5 now implements route-template-only API 5xx alerting with 3-error raise / 2-non-5xx clear behavior, correlation/action evidence, repeat-raise suppression, Prometheus rule/metrics and a dedicated retained-evidence workflow. Acceptance awaits exact-head CI and artifact inspection.
- [RUN-20260809-134 — post-migration security/recovery/storage-integrity reconciliation](runs/RUN-20260809-134.md) — `PASS`: PR #91 exact head `d81caaa372b0cf3e079023eb255a57fd4892d6e0` passed 38/38 workflows and merged as `23af430c041e3f0e203b7a7f7a6c69f3eea79055`; RUN-133 migration evidence remains accepted and deployment-time AIStor security/advisory gates remain external.
- [RUN-20260809-133 — bounded supported object-storage migration](runs/RUN-20260809-133.md) — `PASS`: PR #90 exact head `0fe5c5f0003211fe9df8535954d9276a2090af35` passed 38/38 workflows; dedicated artifact `9041774769` (`sha256:24e7241138dc0b293957f5e2cd06a4d3a6606b7ba68d688097795047f114ccf8`) independently showed JUnit 4/4; merged as `383702bec6ba07cba065524efa451fd89cbd3b50`.
- [RUN-20260809-132 — supported object-storage target decision](runs/RUN-20260809-132.md) — `PASS`: PR #89 exact head `79c5684b7e65064efe480e6da7913fd437d52b6d` completed 37/37 workflows and merged as `83e880a289467151c6604e28cd4141118fb538a9`; ADR-0001 selects MinIO AIStor Enterprise Lite or Enterprise with active paid support as the supported successor.
- [RUN-20260809-131 — supported object-storage remediation blocker](runs/RUN-20260809-131.md) — `BLOCKED_EXTERNAL`: confirmed the vulnerable legacy MinIO pin could not truthfully be remediated with another unmaintained community runtime while satisfying the production support gate.
- [RUN-20260809-130 — RC10.4 exact-head acceptance and security-blocker reconciliation](runs/RUN-20260809-130.md) — `PASS`.
- [RUN-20260809-129 — RC10.4 bounded storage-integrity alerting](runs/RUN-20260809-129.md) — `PASS`.
- [RUN-20260809-128 — RC10.3 exact-head acceptance and documentation reconciliation](runs/RUN-20260809-128.md) — `PASS`.
- [RUN-20260809-127 — RC10.3 bounded queue-backlog alerting](runs/RUN-20260809-127.md) — `PASS`.
- [RUN-20260809-126 — RC10.2 acceptance and historical documentation reconciliation](runs/RUN-20260809-126.md) — `PASS`.
- [RUN-20260809-125 — RC10.2 controlled connector-failure alerting](runs/RUN-20260809-125.md) — `PASS`.
- [RUN-20260809-124 — RC10.1 exact-head acceptance and documentation reconciliation](runs/RUN-20260809-124.md) — `PASS`.
- [RUN-20260809-123 — RC10.1 request observability baseline](runs/RUN-20260809-123.md) — `PASS`.
- [RUN-20260809-122 — RC9.16 genuine assistive-technology behavior](runs/RUN-20260809-122.md) — `BLOCKED_EXTERNAL`.

## Current decision

Phase 1–5 internal roadmap gates are `PASS`. Phase 6 remains `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA behavior. Phase 7 is `IN PROGRESS`; RC10.1–RC10.4 are accepted, the bounded object-storage migration/reconciliation is accepted, and RC10.5 implementation is now exact-head CI gated.

Fresh RC10.5 advisory review recorded Starlette CVE-2026-48817 and CVE-2026-48818 as affecting versions through 1.0.1 and fixed in 1.1.0. DTMO exploitability is not asserted because Starlette is transitive and the resolved version remains subject to dependency/security CI.

Commercial entitlement/support, production topology, registry-digest verification for the selected AIStor release, TLS/network encryption, server-side encryption/KMS, secrets-manager acceptance, staging/production deployment acceptance and other issue #1 external gates remain open.

## Exactly one next priority

Verify the complete exact-head workflow matrix and retained `api-error-alerting-evidence` artifact for RUN-135; merge only after every registered workflow succeeds and the retained evidence is exact-head bound and internally consistent.
