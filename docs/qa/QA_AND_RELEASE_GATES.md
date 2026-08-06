# DTMO QA and Release Gates

## Purpose

Every DTMO development step must define and evaluate explicit quality gates. A configured or committed test that has not executed is `PENDING`, never `PASS`.

## Baseline blocking gates

| Domain | Blocking evidence |
|---|---|
| Build | Source compiles and required packages resolve |
| Unit and regression tests | New and affected logic executes successfully |
| Security | Authentication, authorization, secrets and input controls are verified |
| Governance | Human review, share approval and separation of duties are preserved |
| Data integrity | Provenance, confidence, constraints and migrations are verified |
| Release | All release-critical jobs and evidence artifacts succeed |

## Phase 1 — CI and workflow integrity

- RC5.1 Quality Gate #177: `PASS`.
- RC5.2 Quality Gate #179: `PASS`.
- RC5.3 Quality Gate #197: `PASS`.
- RC5.4 Quality Gate #203: `PASS`.
- Required jobs, workflow contracts, migrations, dependency audit, container smoke and aggregate release gates succeeded for accepted heads.
- Every new branch still requires its own exact-head execution.

## Phase 2 — Application security and identity

Current state after `RUN-20260806-031`:

- least-privilege RBAC, service-account isolation and human separation of duties: implemented and evidenced;
- trusted-principal token validation and RS256/JWKS overlapping-key rotation: implemented and evidenced through Quality Gate #203;
- RC5.5 adds immutable canonical audit events linked by SHA-256 from a fixed genesis hash;
- the audit verifier detects payload mutation, deletion, reordering, broken links and duplicate event identifiers;
- audit events retain principal, principal type, action, resource, decision, request ID and provenance reference;
- required identity and action fields fail closed;
- focused regression tests are committed;
- persistent append-only storage and integration of live authorization/publication decisions remain separate future objectives;
- exact-head RC5.5 CI evidence: `PENDING`;
- Phase 2 completion: `BLOCKED` until RC5.5 and remaining identity objectives are evidenced.

## Phase 3 — Data integrity and recovery

- canonical RC5 migration and migration-contract tests: `PASS` in accepted quality gates;
- clean-environment restoration, RPO and RTO evidence: not yet implemented;
- Phase 3 completion: `BLOCKED`.

## Security and publication invariants

- ingestion must create candidate intelligence only;
- reviewed and share-approved states remain distinct;
- external publication requires explicit human approval by a principal different from the reviewer;
- service accounts may not review or approve sharing;
- source provenance and confidence may not be silently discarded;
- production secrets may not be committed;
- missing CI or scan evidence may not be reported as successful.

## Current run decision

`RUN-20260806-031` is `CI_VALIDATION_PENDING` until the exact PR-head Quality Gate completes successfully.

## Exactly one next priority

Inspect the first completed Quality Gate for RC5.5 and either resolve only its earliest deterministic failure or merge after full success.
