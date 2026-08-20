# Phase 11.10 Production-Equivalent Validation Gate

## Objective

Phase 11.10 validates the materially changed integrated Phase 11 candidate in a production-equivalent environment. Acceptance is candidate-bound and requires one immutable integrated deployment identity across all evidence classes.

## Required evidence

The acceptance package must contain fresh evidence for: immutable candidate identity, migration compatibility, upgrade, rollback, health, saturation and recovery. Each evidence item must identify the same candidate and environment. Missing, ambiguous, mixed-candidate or historical-only evidence fails closed.

Historical Phase 8 staging evidence is retained for audit history but is not reusable as Phase 11.10 acceptance evidence. Repository CI may validate the evidence contract and exact-head metadata, but it does not prove that a production-equivalent environment was deployed or exercised.

## Acceptance boundary

Phase 11.10 remains `IN PROGRESS` until accountable environment execution supplies and reviews the complete fresh evidence set. Repository-green status alone does not authorize production. Phase 11.11 independent external assurance must use the same immutable integrated candidate accepted here.

## Required operator sequence

1. Record the immutable candidate image digest and deployment/configuration identity.
2. Perform forward migration and verify application/schema compatibility.
3. Exercise upgrade and exact prior-digest rollback without automatic database down migration.
4. Capture post-upgrade and post-rollback health evidence.
5. Exercise declared saturation boundaries and verify controlled degradation/recovery.
6. Exercise backup/restore/recovery with integrity checks.
7. Reconcile every artifact to the same candidate and environment identity.
8. Fail closed if any evidence class is missing, ambiguous or belongs to another candidate.
