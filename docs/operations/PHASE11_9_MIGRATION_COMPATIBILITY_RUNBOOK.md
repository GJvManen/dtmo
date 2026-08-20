# Phase 11.9 Migration and Compatibility Runbook

## Preconditions

Use one immutable application candidate and record the currently accepted application and database revision. Confirm the migration graph passes the Phase 11 Migration Compatibility Gate before any deployment rehearsal.

## Change sequence

1. Back up governed state according to the Phase 11.8f recovery runbook.
2. Confirm the current Alembic revision and target head.
3. Review each new migration for backward compatibility during the rolling overlap window.
4. Prefer expand/migrate/contract for destructive or shape-changing changes.
5. Apply forward migrations before candidate application cutover.
6. Verify schema revision, application health, data integrity and connector read/write paths.
7. Record exact application digest, schema head and validation evidence.

## Failed candidate

If the candidate application fails, restore the exact prior immutable application digest only when the migrated schema remains compatible. Do not automatically run `alembic downgrade`. If compatibility cannot be established, fail closed, stop the rollout and invoke the governed recovery process with accountable approval.

## Escalation

Escalate missing revision identity, branched/disconnected migration history, destructive migration without an expand/migrate/contract plan, ambiguous data transformation, failed integrity checks, or inability to prove prior-application compatibility.

## Evidence limitation

Repository and ephemeral CI evidence is not production-equivalent evidence. Phase 11.10 must exercise the integrated candidate against representative state and capture fresh compatibility, upgrade, rollback and recovery evidence before Phase 11.11 independent assurance.
