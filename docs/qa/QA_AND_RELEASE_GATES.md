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
- Required jobs, workflow contracts, migrations, dependency audit, container smoke and aggregate release gates succeeded for accepted heads.
- Every new branch still requires its own exact-head execution.

## Phase 2 — Application security and identity

Current state after `RUN-20260806-029`:

- route-level RBAC and least-privilege ingestion authority: implemented and validated;
- service-account and human separation: implemented;
- review and share approval remain separate, with different human principals required;
- RC5.3 production trusted-principal validation: `PASS` in Quality Gate #197;
- RC5.4 replaces production shared-secret JWT validation with RS256/JWKS trust;
- production requires a non-empty JWKS and rejects configured token signing secrets;
- token headers must declare `RS256` and a non-empty `kid`;
- a `kid` must resolve to exactly one trusted RSA signing key;
- overlapping active and previous keys are supported for controlled rotation;
- unknown, duplicate, non-RSA, non-signing and algorithm-confusion paths fail closed;
- issuer, audience, expiry, not-before, issued-at, subject, role, principal type and JTI checks remain mandatory;
- focused positive and negative JWKS rotation tests are committed;
- exact-head RC5.4 CI evidence: `PENDING`;
- remote JWKS retrieval/cache policy, token revocation and privileged-operation audit persistence remain future bounded objectives;
- Phase 2 completion: `BLOCKED` until remaining objectives are evidenced.

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

`RUN-20260806-029` is `CI_VALIDATION_PENDING` until the exact PR-head Quality Gate completes successfully.

## Exactly one next priority

Inspect the first completed Quality Gate for RC5.4 and either resolve only its earliest deterministic failure or merge after full success.
