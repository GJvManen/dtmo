# Phase 11.10 Production-Equivalent Validation Runbook

## Purpose

This runbook governs the fresh production-equivalent validation required for the materially changed integrated DTMO candidate after Phase 11.9. It converts the Phase 11.10 repository evidence contract into an accountable external execution procedure.

**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`

This document is an execution contract. It is **not** evidence that the production-equivalent environment has already been exercised and it does not authorize production.

## Acceptance principle

Phase 11.10 may be accepted only when all mandatory evidence classes are observed against **one immutable integrated deployment identity** in an approved production-equivalent environment:

1. immutable candidate identity;
2. migration/compatibility;
3. upgrade;
4. rollback;
5. health/readiness;
6. representative saturation/capacity behavior;
7. recovery/continuity.

Historical Phase 8 or Phase 9 evidence is retained as immutable audit history and must not be reused as Phase 11.10 acceptance evidence.

## Roles and separation of duties

| Role | Responsibility |
|---|---|
| Deployment operator | Deploys the approved candidate and records immutable identities. |
| Validation operator | Executes the prescribed validation steps and captures restricted evidence references. |
| Security/release reviewer | Reviews candidate binding, completeness, security boundaries and deviations. |
| Accountable owner | Makes the explicit Phase 11.10 acceptance decision. |

The same person may perform multiple roles only where organizational controls allow it. Evidence must still identify the actor and review role separately.

## Pre-flight gate

Do not start evidence collection until all of the following are true:

- the environment is explicitly designated production-equivalent;
- the deployed application commit is recorded as an exact 40-character Git SHA;
- every application/supporting image is recorded by immutable `sha256:` digest;
- the expected Alembic migration head is recorded;
- the GitOps/Helm deployment revision is recorded where applicable;
- an approved prior immutable application digest exists for rollback;
- production credentials and unsanitized production data are not used unless separately and explicitly authorized;
- timestamps are synchronized sufficiently to reconstruct the exercise;
- monitoring, logs and audit/correlation evidence are available to authorized reviewers.

If candidate identity is missing or ambiguous, **stop**. Do not begin the exercise.

## Candidate fingerprint

The evidence package uses one candidate fingerprint derived from stable identity fields. The repository validator verifies that every evidence class uses the same fingerprint.

Required identity fields:

- `environment_id`;
- `deployed_commit`;
- `application_image_digest`;
- `migration_head`;
- `deployment_revision`.

Supporting image digests may also be recorded. They must be immutable digests, never mutable tags alone.

## Execution sequence

### 1. Identity capture

Record the approved environment, exact commit, immutable application image digest, supporting image digests, migration head and deployment revision. Generate and retain the candidate fingerprint before other evidence is accepted.

### 2. Migration and compatibility

Validate the accepted Phase 11.9 forward-first migration contract against the deployed candidate:

- migration reaches the expected head without an ambiguous or divergent graph;
- application/schema overlap remains backward compatible for the exercised rollout path;
- no automatic database down migration is performed during application rollback;
- destructive changes, if any, follow expand/migrate/contract;
- representative read/write behavior remains valid through the supported transition.

### 3. Upgrade

Exercise candidate rollout from the approved prior immutable digest to the new immutable digest:

- observe rollout progression and readiness;
- confirm `maxUnavailable: 0` / governed rolling behavior where applicable;
- confirm no unintended identity or secret fallback;
- confirm service boundaries and authorization remain intact;
- capture before/after immutable digests and timestamps.

### 4. Health and readiness

Validate health/readiness after upgrade:

- application health is successful;
- readiness represents required dependencies rather than process liveness only;
- representative API/UI path is usable;
- audit/correlation and operational telemetry are present;
- no synthetic/emulator result is substituted for live environment evidence.

### 5. Saturation and capacity

Apply a representative approved workload sufficient to exercise the Phase 11.8h resource/capacity assumptions:

- record workload profile and duration;
- record latency/error/queue/resource observations;
- identify the first constrained resource or confirm the planned headroom;
- verify degraded behavior is visible and does not fabricate intelligence;
- record any deviation from the approved capacity envelope.

This is a production-equivalent validation exercise, not an uncontrolled denial-of-service test.

### 6. Recovery

Exercise approved recovery behavior relevant to the integrated candidate. At minimum, demonstrate the selected recovery path for application and required stateful dependencies and capture:

- trigger/failure condition;
- recovery procedure;
- data-integrity observation;
- observed RPO/RTO where applicable;
- post-recovery health/readiness;
- audit/monitoring continuity;
- deviations and residual risk.

### 7. Exact prior-digest rollback

Rollback the application to the exact approved prior immutable digest without automatically down-migrating the database. Confirm:

- the prior application identity is restored;
- the retained schema is compatible with the prior application under the accepted Phase 11.9 contract;
- health/readiness succeeds after rollback;
- representative read/write behavior succeeds;
- rollback evidence records both candidate and prior immutable digests.

### 8. Evidence consolidation and review

Populate `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json` outside the repository with real evidence references or in an approved restricted evidence location. Do not commit secrets, bearer tokens, raw credentials, private keys or unsanitized sensitive evidence.

Validate the manifest with:

```bash
python3 tools/phase11_production_equivalent_validation.py --manifest /path/to/phase11-10-evidence.json
```

A valid manifest proves only that the supplied evidence metadata satisfies the repository contract. The reviewer must still inspect the referenced evidence and make the accountable acceptance decision.

## Fail-closed conditions

The validator and reviewer must reject the package when any of the following is true:

- required identity field is missing or placeholder text;
- mutable image tags are supplied without immutable digest identity;
- required evidence class is missing;
- an evidence result is not `PASS`;
- evidence references are blank, placeholders or point only to repository CI/synthetic fixtures;
- evidence classes reference a different candidate fingerprint or environment;
- historical Phase 8/9 evidence is presented as current Phase 11.10 proof;
- rollback does not target the exact prior immutable application digest;
- post-rollback health evidence is missing;
- reviewer/observer/timestamp attribution is missing;
- release-blocking deviation is unresolved or lacks an accountable disposition.

## Acceptance record

Phase 11.10 is complete only after the accountable owner records an explicit `PASS / OWNER_ACCEPTED` decision for the full evidence package. Repository CI, the manifest validator, this runbook, local Compose, staging emulators and synthetic browser tests cannot make that decision.

After acceptance, Phase 11.11 independent external assurance may begin **against the same immutable integrated candidate**. Any material candidate change requires a new Phase 11.10 evidence binding before assurance proceeds.
