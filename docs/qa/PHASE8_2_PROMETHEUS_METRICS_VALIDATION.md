# Phase 8.2.11 — Prometheus metrics validation

## Purpose

Validate real Prometheus metrics exposure and scrape behavior on the owner-approved post-E8 production-equivalent staging deployment. Accepted evidence must remain bound to the same immutable Phase 8.2 deployment identity used by the other staging validation steps.

## Entry conditions

- Phase 8.2 is active on `main`.
- The staging environment is owner-approved.
- Repository-side step validation is available via `tools/phase8_platform_validation.py --check prometheus_metrics`.
- External evidence must identify the immutable environment/deployed commit/application image fingerprint before this step can be accepted as PASS.

## Validation procedure

1. Record the staging deployment fingerprint and reviewer/timestamp.
2. Verify the approved metrics endpoint or scrape target is reachable only through the intended staging access path.
3. Confirm Prometheus reports the DTMO target as healthy/up.
4. Execute a representative application request and verify expected counters/rates/latency samples change coherently.
5. Verify connector, queue, search and storage operational signals are present where the deployment implements them.
6. Inspect representative labels and metric values for secret hygiene: no bearer tokens, passwords, raw credentials or uncontrolled sensitive high-cardinality values.
7. Verify metrics access control matches the intended staging design and broader unauthorized users cannot obtain monitoring data.
8. Exercise or inspect one unavailable/scrape-failure condition and confirm it is observable rather than silently represented as healthy.
9. Verify sample timestamps/freshness align with the validation window.
10. Confirm no production monitoring credentials or endpoints are reused.

## Required evidence

- immutable Phase 8.2 deployment fingerprint;
- Prometheus target/scrape evidence;
- representative metric names and safe sample output;
- before/after observation for a representative request;
- evidence of access-control behavior;
- failure/unavailable-state observation where safe;
- reviewer and timestamp;
- restricted evidence reference without secrets.

## Acceptance

`PASS` requires real Prometheus scrape and representative metric behavior on the approved staging deployment. Repository CI, compose/emulator behavior and synthetic fixtures are supporting evidence only and cannot replace external staging evidence.

The accepted result must be attributable to the same immutable Phase 8.2 deployment fingerprint used by the other Phase 8.2 checks.
