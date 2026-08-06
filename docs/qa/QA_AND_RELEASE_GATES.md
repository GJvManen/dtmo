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
- Required jobs, workflow contracts, migrations, dependency audit, container smoke and aggregate release gates succeeded for both accepted heads.
- Every new branch still requires its own exact-head execution.

## Phase 2 — Application security and identity

Current state after `RUN-20260806-027`:

- route-level RBAC and least-privilege ingestion authority: implemented and validated in Quality Gate #179;
- service-account and human separation: implemented;
- review and share approval remain separate, with different human principals required;
- production no longer accepts caller-supplied subject or role headers as identity;
- production principal resolution requires a signed bearer token;
- token signature algorithm is restricted to `HS256` for this bounded implementation;
- issuer, audience, expiry, not-before, issued-at, subject, role, principal type and JTI claims are required;
- machine identities may use only the `service_account` role;
- human identities may not claim the `service_account` role;
- signing secret, HTTPS issuer and audience are mandatory production settings;
- Quality Gate #181 failed at Ruff; semantic renaming corrected the false positives without suppressions;
- Quality Gate #185 passed Ruff and failed strict MyPy; PyJWT options now use `jwt.types.Options`;
- Quality Gate #189 reached pytest and failed because direct invocation received a FastAPI `Header` descriptor as the omitted authorization argument;
- header dependencies now use `Annotated[str, Header()]` metadata with real string defaults, preserving HTTP injection and direct unit-test behaviour;
- the full replacement test and coverage gate has not yet executed successfully and remains `PENDING`;
- distributed key rotation/JWKS, token revocation and privileged-operation audit persistence remain future bounded objectives;
- Phase 2 completion: `BLOCKED` until these remaining objectives are evidenced.

## Phase 3 — Data integrity and recovery

- canonical RC5 migration and migration-contract tests: `PASS` in Quality Gate #177 and #179;
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

`RUN-20260806-027` is `BLOCKED` until the replacement exact PR-head Quality Gate completes successfully.

## Exactly one next priority

Inspect the replacement Quality Gate for the updated PR #11 head and either accept full success or resolve only its earliest deterministic failure.
