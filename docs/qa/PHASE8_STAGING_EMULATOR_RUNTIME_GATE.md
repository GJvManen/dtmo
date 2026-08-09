# Phase 8 Staging Emulator Runtime Gate

## Decision

`CI_VALIDATION_PENDING`

## Objective

Prove that the repository-built DTMO container can start in `production` configuration mode under bounded container hardening and pass a runtime smoke probe without weakening RBAC, privacy, provenance, auditability, separation of duties or human share approval.

## Required controls

- Build the DTMO image from the exact pull-request head.
- Start the container with `DTMO_ENVIRONMENT=production` and production-only configuration validation active.
- Bind the runtime only to `127.0.0.1` in CI.
- Use a read-only root filesystem, `/tmp` tmpfs, `no-new-privileges` and dropped Linux capabilities.
- Keep live connectors and AI analyst features disabled.
- Keep human publication approval and human share approval separate from technical runtime access.
- Exercise `/health`, `/ready`, `/connectors`, the disabled connector execution path, security response headers and `/metrics` against the running container.
- Retain the exact-head local image identity, runtime probe JSON/JUnit, contract-test JUnit/log and privacy-safe container log.
- Fail if synthetic sensitive markers are present in retained runtime logs.

## Claim boundary

A PASS proves only the bounded DTMO application-container runtime smoke described above. It does not prove that the complete emulator dependency topology was executed; it does not execute the external TLS gateway, PostgreSQL, Redis, OpenSearch or object-storage services; it does not prove a real staging environment; it does not satisfy the ten deployment-parity evidence classes; and it does not complete Phase 8 or production acceptance.

## Acceptance rule

PASS requires every registered workflow on the exact final PR head to succeed and retained `phase8-staging-emulator-runtime-evidence` to be exact-head bound, machine-readable PASS, internally consistent, privacy-safe, and accompanied by zero-failure/zero-error/zero-skip runtime evidence. Missing, stale, queued, cancelled or failed evidence is not PASS.

## Exactly one next priority

After this runtime-smoke gate is accepted, use the accepted emulator contract to provision and evidence the complete dependency topology or the approved real staging environment. The ten external deployment-parity evidence classes remain mandatory before any real staging acceptance suite is credited.
