# Phase 11.8f — Backup, restore and recovery runbook

## Preconditions

Confirm the immutable integrated candidate identity, stateful-service owners, backup destinations, encryption/key ownership, retention policy, RPO/RTO targets and authorized recovery operators. Do not store backup credentials or secret material in Git.

## Required recovery domains

PostgreSQL, Redis, OpenSearch and object storage must each have a deployment-owned backup and restore procedure. A successful backup job alone is insufficient; restore verification is mandatory.

## Recovery exercise

1. Select an approved recovery point and record its provenance.
2. Restore into an isolated recovery target where possible.
3. Verify integrity, application compatibility and expected data boundaries.
4. Measure elapsed recovery time and recovered data age against the declared RTO/RPO targets.
5. Record only non-sensitive evidence references, timestamps, immutable candidate identity and accountable operator approval.
6. Destroy temporary recovery targets and revoke temporary access when the exercise completes.

## Failure handling

If a backup is missing, corrupt, unverifiable, outside retention, or the restore exceeds approved RPO/RTO, mark the recovery control failed. Do not substitute historical Phase 8/9 evidence or CI success for the failed deployment-bound recovery evidence.

## Rollback

Recovery rollback returns the environment to the last accepted stateful snapshot/revision under accountable operator control. Application GitOps rollback and stateful-data rollback must be coordinated; never overwrite a newer data state solely because an application revision was rolled back.

## Evidence boundary

This runbook defines the required procedure only. Repository acceptance does not prove live backup execution, provider durability, successful restore, measured RPO/RTO, disaster recovery, production readiness or independent assurance.
