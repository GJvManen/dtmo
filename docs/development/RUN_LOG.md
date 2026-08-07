# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260807-050 — RC7.3 quality-gate lint remediation](runs/RUN-20260807-050.md) — `CI_VALIDATION_PENDING`: RC4 Quality Gate #297 failed deterministically on Ruff `S105` for a synthetic redaction-test fixture; fixture was made explicitly non-sensitive with a narrow line-level suppression; no product control changed
- [RUN-20260807-049 — RC7.3 governed connector contract validation](runs/RUN-20260807-049.md) — `CI_VALIDATION_PENDING`: connector-contract, canary, state and recovery gates passed on head `b333d013d2b183d2678a7aaec04010bc6b1549d1`, but RC4 Quality Gate #297 failed at lint and blocked acceptance
- [RUN-20260807-048 — RC7.2 exact-head acceptance and merge](runs/RUN-20260807-048.md) — `PASS`: Connector State Gate #17, Quality Gate #292, Canary Gate #25, OpenSearch Recovery Gate #44 and Multi-store Recovery Gate #34 succeeded on exact head `af4625b0f285da6e2b0d5135a623c418a9f3b9d4`; retained connector-state artifact `8976473782`; PR #29 merged as `ac31b9d4409b97d6db734791365a3dd814255c9d`
- [RUN-20260807-047 — RC7.2 parent-before-child persistence ordering](runs/RUN-20260807-047.md) — `PASS`: remediation validated by exact-head Connector State Gate #17 and retained evidence; superseded by RUN-20260807-048 acceptance
- [RUN-20260807-046 — Exact-head CI execution blocker](runs/RUN-20260807-046.md) — superseded by successful exact-head execution and RUN-20260807-048 acceptance
- [RUN-20260806-045 — RC7.2 persistent connector state and failure isolation](runs/RUN-20260806-045.md) — `PASS`: PostgreSQL-backed run state, source-health history, connector-scoped isolation and human-reviewed quarantine recovery accepted through RUN-20260807-048
- [RUN-20260806-044 — RC7.1 governed live connector canary](runs/RUN-20260806-044.md) — `PASS`: RC7 Live Connector Canary Gate #3, RC4 Quality Gate #270, OpenSearch Recovery Gate #22 and Multi-store Recovery Gate #12 succeeded on exact head `c82e20c110354c1163b58ac8b9820756f829a4ae`; retained canary evidence artifact `8973407243`; PR #28 merged as `aeeb0709a26ecb1f20620d7ac21f823fec35e98f`
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

`RUN-20260807-050` is `CI_VALIDATION_PENDING`. The first deterministic RC4 failure was remediated without changing product controls; exact-head GitHub Actions must execute again before RC7.3 can be accepted.

## Exactly one next priority

Inspect the first RC4 Quality Gate registered for the current exact head; remediate only its earliest deterministic failure, or accept and merge PR #30 only after every required exact-head gate and retained evidence artifact succeeds.