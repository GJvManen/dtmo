# Phase 8 Staging Emulator Runtime Gate

## Decision

`PASS` for the bounded repository-controlled DTMO application-container runtime smoke only.

## Objective

Prove that the repository-built DTMO container can start in `production` configuration mode under bounded container hardening and pass a runtime smoke probe without weakening RBAC, privacy, provenance, auditability, separation of duties or human share approval.

## Required controls

- Build the DTMO image from the exact pull-request head.
- Start the container with `DTMO_ENVIRONMENT=production` and production-only configuration validation active.
- Bind the runtime only to `127.0.0.1` in CI.
- Restrict the probe helper to loopback HTTP targets and reject non-loopback or non-HTTP URLs before any request is created.
- Use a read-only root filesystem, `/tmp` tmpfs, `no-new-privileges` and dropped Linux capabilities.
- Keep live connectors and AI analyst features disabled.
- Keep human publication approval and human share approval separate from technical runtime access.
- Exercise `/health`, `/ready`, `/connectors`, the disabled connector execution path, security response headers and `/metrics` against the running container.
- Retain the exact-head local image identity, runtime probe JSON/JUnit, contract-test JUnit/log and privacy-safe container log.
- Fail if synthetic sensitive markers are present in retained runtime logs.

## Acceptance evidence

PR #107 final exact head `52d7a37660c9bb1c9f8468f11010f36d17bd1fba` completed 48/48 registered workflows successfully, including `RC4 Quality Gate`, `Phase 8 Staging Readiness Gate`, `Phase 8 Staging Emulator Gate` and `Phase 8 Staging Emulator Runtime Gate`. PR #107 merged with expected-head protection as `23d629964f55709845683e808f707998cc8d4aa2`.

Retained artifact `phase8-staging-emulator-runtime-evidence`:
- artifact id `9057259246`;
- digest `sha256:d577415a5b40952a305577c5a1fbeae1e3e154fcbf95a42030cdd19632d77aa5`;
- exact head `52d7a37660c9bb1c9f8468f11010f36d17bd1fba`;
- machine-readable decision `pass`;
- local image identity `sha256:aeaf09fff7b58e3eed225138bfec306c1c0aaeb8dadf4c8611d59eda3aa04223`;
- contract JUnit 4/4 with zero failures/errors/skips;
- runtime JUnit 12/12 with zero failures/errors/skips;
- all runtime checks true, including production mode, health/readiness, human publication gate, authentication contract, security headers, correlation header, connectors disabled/fail-closed and metrics availability;
- all real-staging/deployment-parity/Phase-8/production claim-boundary fields false;
- retained container log contains no configured synthetic sensitive-marker leakage.

## Claim boundary

This PASS proves only the bounded DTMO application-container runtime smoke described above. It does not prove that the complete emulator dependency topology was executed; it does not execute the external TLS gateway, PostgreSQL, Redis, OpenSearch or object-storage services; it does not prove a real staging environment; it does not satisfy the ten deployment-parity evidence classes; and it does not complete Phase 8 or production acceptance.

## RUN-155 remediation history

The original PR #105 runtime gate proved independently observable execution, but RC4 failed at Ruff S310 because the probe helper's URL construction was not explicitly constrained at the flagged request-creation line. RUN-155 ported the runtime gate onto current `main`, added explicit loopback-HTTP validation, preserved the narrow warning suppression only after validation, and then completed a fresh full exact-head matrix successfully on PR #107.

## RUN-157 lifecycle-regression remediation

PR #108 previous exact head `c4c28938a49b2a3dcba90ab01e6bd1cb430a3439` completed 47/48 registered workflows. RC4 failed because `backend/tests/test_phase8_staging_emulator_runtime.py` still required the obsolete lifecycle token `CI_VALIDATION_PENDING` even though this QA gate had already advanced to bounded `PASS` from accepted PR #107 evidence.

The regression was corrected to require this exact bounded PASS decision and to continue requiring human share approval plus the unchanged real-staging, deployment-parity, Phase-8 and production non-overclaim statements. PR #108 exact head `25ac24bfa40f2f9ccebb5d1307615c6fbd14cf05` then completed 48/48 workflows successfully, including RC4 and all three Phase 8 repository gates. RC4 pytest completed 292 passed / 16 skipped with 84.96% coverage. Retained runtime artifact `9057841831`, digest `sha256:0e68feb37e9937b574a6ef80affeff13aeda162eb83c8805a8f220cb082999b1`, is exact-head bound.

RUN-157 is therefore accepted as `PASS` for its bounded lifecycle-regression scope. This does not alter the real-staging blocker or broaden this QA gate's claim.

## Exactly one next priority

Verify all 48 workflows on PR #108's documentation-finalization exact head and merge only on complete success. After merge, provide or provision one approved real staging deployment and retain all ten deployment-parity evidence classes against the same immutable deployment identity. Repository runtime evidence is not a substitute for that gate.
