# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260806-044 — RC7.1 governed live connector canary](runs/RUN-20260806-044.md) — `CI_VALIDATION_PENDING`: controlled CISA KEV canary, provenance, licensing, timeout, bounded retry/backoff, deduplication, quarantine and fail-closed publication evidence committed
- [RUN-20260806-043 — RC6.4 combined multi-store recovery acceptance](runs/RUN-20260806-043.md) — `PASS`: Multi-store Recovery Gate #4, RC4 Quality Gate #262 and OpenSearch Recovery Gate #14 succeeded on exact head `ba3389613341c84aa21b591b706b7819981b7a4b`; combined cross-store evidence retained; PR #26 merged
- [RUN-20260806-042 — RC6.3 clean OpenSearch reconstruction](runs/RUN-20260806-042.md) — `PASS`: OpenSearch Recovery Gate #5 and RC4 Quality Gate #253 succeeded on exact head `fbe3924d202d81ab59ebbcd10889a9a75b146941`; deterministic reconstruction evidence retained; PR #25 merged
- [RUN-20260806-041 — RC6.2 clean MinIO backup and restore evidence](runs/RUN-20260806-041.md) — `PASS`: Quality Gate #243 succeeded on exact head `bd2fa4f16d09e924ae3aa0cfb40946aba1fc9084`; isolated MinIO restore, object digest and provenance evidence retained; PR #24 merged
- [RUN-20260806-040 — RC6.1 clean PostgreSQL backup and restore evidence](runs/RUN-20260806-040.md) — `PASS`: Quality Gate #229 succeeded on exact head `d1d0e809ffcee6458cb8a8f31ad2d10d481fefb0`; clean-target restore and integrity evidence retained; PR #22 merged
- [RUN-20260806-039 — RC5.12 storage-layer retention enforcement](runs/RUN-20260806-039.md) — `PASS`: Quality Gate #224 succeeded and PR #21 merged
- [RUN-20260806-038 — RC5.11 privacy minimization and retention controls](runs/RUN-20260806-038.md) — `PASS`: Quality Gate #221 succeeded and PR #19 merged
- [RUN-20260806-037 — RC5.10 revocation reconciliation and recovery](runs/RUN-20260806-037.md) — `PASS`: Quality Gate #219 succeeded and PR #18 merged
- [RUN-20260806-036 — Operational revocation and authorization-denial audit](runs/RUN-20260806-036.md) — `PASS`: Quality Gate #217 succeeded and PR #17 merged
- [RUN-20260806-035 — Isolate production JWKS regression from external Redis](runs/RUN-20260806-035.md) — `PASS`: Quality Gate #215 succeeded and PR #16 merged
- [RUN-20260806-034 — RC5.8 token revocation and replay-state enforcement](runs/RUN-20260806-034.md) — `PASS`: Quality Gate #215 succeeded and PR #16 merged
- [RUN-20260806-033 — Governed decision audit integration](runs/RUN-20260806-033.md) — `PASS`: Quality Gate #209 succeeded and PR #15 merged
- [RUN-20260806-032 — Persistent append-only audit storage](runs/RUN-20260806-032.md) — `PASS`: Quality Gate #207 succeeded and PR #14 merged
- [RUN-20260806-031 — RC5.5 tamper-evident audit chain](runs/RUN-20260806-031.md) — `PASS`: Quality Gate #205 succeeded and PR #13 merged
- [RUN-20260806-030 — RC5.4 PyJWK type-contract remediation](runs/RUN-20260806-030.md) — `PASS`: Quality Gate #203 succeeded and PR #12 merged
- [RUN-20260806-029 — RC5.4 asymmetric JWKS key rotation](runs/RUN-20260806-029.md) — `PASS`: exact-head Quality Gate #203 succeeded and PR #12 merged
- [RUN-20260806-028 — Align secure production configuration regression test](runs/RUN-20260806-028.md) — `PASS`: Quality Gate #197 succeeded and RC5.3 merged through PR #11
- [RUN-20260806-027 — Restore direct-call-safe principal resolution](runs/RUN-20260806-027.md) — superseded by successful Quality Gate #197
- [RUN-20260806-026 — RC5.3 PyJWT type-contract remediation](runs/RUN-20260806-026.md) — superseded by successful Quality Gate #197
- [RUN-20260806-025 — RC5.3 trusted principal token validation](runs/RUN-20260806-025.md) — `PASS`: exact-head Quality Gate #197 succeeded and PR #11 merged
- [RUN-20260806-024 — RC5.2 least-privilege RBAC and separation of duties](runs/RUN-20260806-024.md) — `PASS`: Quality Gate #179 succeeded and PR #10 merged
- [RUN-20260806-023 — Restore clean RC5.1 delivery path](runs/RUN-20260806-023.md) — `PASS`: Quality Gate #177 succeeded and PR #9 merged
- [RUN-20260806-022 — Reversible canonical intelligence migration](runs/RUN-20260806-022.md) — `PASS`
- [RUN-20260806-020 — Remediate pytest dependency advisory](runs/RUN-20260806-020.md) — `PASS`
- [RUN-20260806-019 — RC5.1 canonical intelligence model](runs/RUN-20260806-019.md) — `PASS`
- [RUN-20260806-013 — Restore observable GitHub Actions execution](runs/RUN-20260806-013.md) — `PASS`

## Current decision

`RUN-20260806-044` is `CI_VALIDATION_PENDING`. The live canary implementation and documentation are committed, but exact-head Quality Gate execution and retained connector evidence have not yet completed successfully.

## Exactly one next priority

Inspect the exact-head RC7 Live Connector Canary Gate and remediate only its earliest deterministic failure, or merge after all exact-head gates and retained evidence succeed.
