# Phase 11.8i — Upgrade and rollback gate

## Decision objective
The gate accepts only a bounded repository exercise proving that DTMO can describe and evidence an immutable application upgrade followed by restoration of the exact prior immutable digest under explicit rollout-safety constraints.

## Required checks
- Helm values define `maxUnavailable: 0`, `maxSurge: 1`, revision history, a finite progress deadline and a non-zero minimum-ready period.
- Helm rendering fails when the rollout-safety minima are weakened.
- Baseline and candidate identities must both be valid, different SHA-256 **immutable digest** values.
- Machine-readable evidence records baseline → candidate → exact baseline.
- Post-upgrade and post-rollback **health evidence** are mandatory acceptance conditions.
- Automatic **database down migration** remains forbidden.
- Missing required evidence must **fail closed**.
- The exercise preserves human change authority and explicitly disclaims live-cluster rollback, production-equivalent behavior and **production authorization**.

## Machine-readable evidence
CI writes `artifacts/phase11-8i-upgrade-rollback-evidence.json`. The exact-head field must equal the pull-request head SHA, the rollback digest must equal the original baseline digest, and all no-claim boundaries must remain false.

## Acceptance boundary
Repository acceptance is not live-cluster rollback evidence. Phase 11.10 must exercise the same control against one immutable integrated production-equivalent candidate. Phase 11.11 provides independent assurance; Phase 12 remains the production GO/NO-GO decision.
