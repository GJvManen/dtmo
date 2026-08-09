# Phase 8 Staging Emulator Gate

## Decision

`CI_VALIDATION_PENDING`

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

## Acceptance rule

PASS requires every registered workflow on the exact final PR head to succeed and the retained `phase8-staging-emulator-evidence` artifact to be exact-head bound and internally consistent. Missing, queued, cancelled, failed or stale-head evidence is not PASS.

## RUN-152 CI-integrity remediation

The first RUN-151 exact head completed 46/47 registered workflows successfully; RC4 failed because this QA document did not contain the canonical phrase `human share approval` required by the governance regression test. The documentation contract was corrected without weakening or suppressing the test. Fresh complete exact-head CI is required.

## Exactly one next priority

Verify every registered workflow on the remediated PR #104 exact head and independently inspect regenerated `phase8-staging-emulator-evidence`. Merge only on complete success.
