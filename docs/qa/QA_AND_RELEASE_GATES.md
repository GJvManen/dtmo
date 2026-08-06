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
| Privacy | Direct identifiers, purpose limitation, retention and legal holds are verified |
| Release | All release-critical jobs and evidence artifacts succeed |

## Evidenced quality gates

RC5.1 #177, RC5.2 #179, RC5.3 #197, RC5.4 #203, RC5.5 #205, RC5.6 #207, RC5.7 #209, RC5.8 #215, RC5.9 #217, RC5.10 #219 and RC5.11 #221 are `PASS`.

## Phase 2 — Application security, identity and privacy

Current state after `RUN-20260806-039`:

- privacy-minimized projections use purpose-bound references and exclude direct identity, resource and request identifiers;
- RC5.12 adds a dedicated storage table for derived projections, separate from immutable source audit records;
- projection writes are idempotent and reject event-ID/source-hash conflicts;
- retention expiry is materialized at write time;
- purge deletes only expired records without legal hold;
- legal hold can be escalated and is never silently cleared by ordinary persistence;
- migration `0004_minimized_projection` is reversible;
- exact-head RC5.12 CI evidence remains `PENDING`.

## Phase 3 — Data integrity and recovery

- canonical and persistent-audit migrations are evidenced;
- volatile revocation state is recoverable from integrity-verified durable evidence;
- projection retention storage is reversible and independently purgeable;
- clean-environment database/object restoration, RPO and RTO evidence remain outstanding.

## Security, privacy and publication invariants

- immutable source audit records are never included in projection purge;
- legal-hold records must survive ordinary retention purge;
- direct identifiers may not enter minimized projection storage;
- production token-state and authorization-denial failures remain fail closed;
- human publication approval and separation of duties remain mandatory;
- missing CI evidence may not be reported as successful.

## Current run decision

`RUN-20260806-039` is `CI_VALIDATION_PENDING` until the exact PR-head Quality Gate completes successfully.

## Exactly one next priority

Inspect the exact-head RC5.12 Quality Gate and either resolve only its earliest deterministic failure or merge after full success.
