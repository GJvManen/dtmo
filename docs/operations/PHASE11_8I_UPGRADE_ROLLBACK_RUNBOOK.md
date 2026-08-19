# Phase 11.8i — Upgrade and rollback runbook

## Purpose
This runbook defines the accountable application upgrade and rollback sequence for the Phase 11 Kubernetes runtime. It is a repository control and rehearsal procedure; it is not evidence that a live production rollback has succeeded.

## Preconditions
1. Record the currently accepted application **immutable digest** and exact Git revision.
2. Record the candidate immutable digest and verify it is different from the baseline.
3. Confirm required supply-chain evidence for the candidate is present and accepted.
4. Confirm readiness/liveness health checks, observability and capacity evidence channels are available for the target environment.
5. Confirm the schema change is rollback-compatible. If rollback would require an automatic **database down migration**, stop: that migration path is not authorized by this runbook.
6. Identify the accountable human change authority and rollback decision owner.

Missing required identity, health evidence, rollback compatibility or accountable authority must **fail closed**.

## Upgrade exercise
1. Preserve the exact baseline digest as the rollback target.
2. Apply the reviewed GitOps change that replaces only the application image digest with the candidate digest and any separately reviewed compatible configuration.
3. Observe rollout progress within the configured progress deadline.
4. Require all replacement pods to satisfy the minimum-ready period and health checks.
5. Record post-upgrade health evidence, workload identity, candidate digest, exact Git revision and decision.
6. Do not infer production authorization from a successful rollout.

## Rollback exercise
Trigger rollback when the candidate fails bounded health, correctness, capacity or operator acceptance criteria.

1. Restore the exact prior accepted immutable digest through the reviewed GitOps source of truth.
2. Do not use `latest`, another mutable tag, or a rebuilt image as a substitute for the prior digest.
3. Do not automatically reverse database migrations.
4. Wait for the configured RollingUpdate to complete and require post-rollback **health evidence**.
5. Verify the resulting application digest equals the recorded baseline digest.
6. Record the rollback decision, initiating evidence, restored digest, health result and accountable operator.
7. If health cannot be proven after rollback, fail closed and invoke the Phase 11.8f recovery procedure rather than declaring rollback successful.

## CI rehearsal
The repository gate runs `tools/phase11_upgrade_rollback_exercise.py` with two synthetic SHA-256 image identities. The generated evidence must show baseline → candidate → exact baseline and must explicitly state that live-cluster rollback, production-equivalent behavior and production authorization are not claimed.

## Later validation
Phase 11.10 must repeat the exercised upgrade/rollback path on the immutable integrated production-equivalent candidate, including health, saturation and recovery evidence. Phase 11.11 then performs independent assurance against that same candidate before any Phase 12 GO/NO-GO decision.
