# Phase 8 Staging Emulator Gate

## Decision

`PASS` for the bounded repository-controlled emulator configuration contract only.

## Objective

Validate a repository-controlled production-equivalent staging emulator contract that exercises production-mode configuration, immutable image identity, network isolation, TLS ingress, external secrets, observability topology and human approval invariants without claiming a real staging deployment.

## Required controls

- DTMO runs in `production` configuration mode so production-only validation remains active.
- Every container image is externally supplied and digest-pinned.
- Backend services are isolated on an internal Docker network.
- Only the TLS gateway is published, and only on loopback by default.
- OpenSearch security is not disabled by configuration.
- Secrets, license material, certificates and credentials are external inputs and never committed.
- Live connectors and AI analyst features default off in the emulator.
- Human publication/share approval remains required and separate from technical access; human share approval is never granted by emulator access, CI success, service identity, or technical responder status.
- CI validates the rendered Compose topology without pulling or executing the declared images.

## Claim boundary

A PASS for this gate does not prove a real staging environment, does not prove container runtime behavior, does not satisfy the ten deployment-parity evidence classes, does not prove production topology parity, and does not complete Phase 8 or production acceptance.

The emulator is a deterministic rehearsal and configuration-control surface. Real staging deployment evidence remains required by `PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`.

## Acceptance evidence

PR #104 final exact head `93d1a659b7b136546ffcf73102890f5d2d00ba84` completed 47/47 registered pull-request workflows successfully, including `RC4 Quality Gate`, `Phase 8 Staging Readiness Gate` and `Phase 8 Staging Emulator Gate`.

Retained artifact `phase8-staging-emulator-evidence`:
- artifact id `9045039742`;
- digest `sha256:959586b389579dfd37bda60eecdfb67e0251eaf4a78daed214986cefe771ce65`;
- exact head `93d1a659b7b136546ffcf73102890f5d2d00ba84`;
- decision `pass`;
- JUnit 4/4 with zero failures, errors or skips;
- all required emulator control flags true;
- all overclaim fields false, including container execution, real staging proof, deployment parity, ten external evidence classes, Phase 8 completion and production acceptance.

PR #104 merged as `3c7a4b7f56e8d8a757541963bbd261fe42a7269c`.

## RUN-152 remediation history

The first RUN-151 exact head completed 46/47 registered workflows successfully; RC4 failed because this QA document did not contain the canonical phrase `human share approval` required by the governance regression test. The documentation contract was corrected without weakening or suppressing the test. The fresh final exact-head matrix then passed completely as recorded above.

## Exactly one next priority

Verify the RUN-153 documentation reconciliation PR on its exact final head and merge only on complete CI success. The real staging deployment-parity gate remains independently `BLOCKED_EXTERNAL`.
