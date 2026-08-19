# Upgrade and rollback configuration

## Administrative intent
Phase 11.8i exposes rollout-safety settings as reviewed Helm values rather than hidden Deployment defaults. Administrators may tune them only through the governed GitOps path and must preserve the Phase 11.8i safety floor.

## Required values
```yaml
upgrade:
  strategy:
    maxUnavailable: 0
    maxSurge: 1
  revisionHistoryLimit: 5
  progressDeadlineSeconds: 600
  minReadySeconds: 10
  rollback:
    requirePriorImmutableDigest: true
    requirePostRollbackHealthEvidence: true
    forbidAutomaticDatabaseDownMigration: true
```

`maxUnavailable` must remain `0`, `maxSurge` must remain at least `1`, revision history must preserve at least two revisions, the progress deadline must remain finite and at least 60 seconds, and minimum-ready time must remain non-zero.

## Image identity
Set `image.digest` only to a reviewed SHA-256 immutable digest. Record the currently accepted digest before every change. A rollback must restore that exact digest; `latest`, another mutable tag or a rebuild is not an acceptable rollback target.

## Evidence and authority
Post-upgrade and post-rollback health evidence are required. Missing evidence must **fail closed**. Rollout configuration does not alter RBAC, publication/share authority, case-handoff authority, service licensing boundaries or production authorization.

## Database boundary
Application rollback does not authorize automatic database down migration. Confirm backward-compatible schema behavior or use a separately reviewed migration/recovery procedure. If rollback compatibility is unknown, do not claim the application rollback path is safe.

Phase 11.10 remains responsible for exercising these controls in the production-equivalent environment on the same immutable integrated candidate used for later assurance.
