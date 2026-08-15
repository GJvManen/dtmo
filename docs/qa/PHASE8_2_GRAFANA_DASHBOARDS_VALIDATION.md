# Phase 8.2.12 — Grafana dashboards validation

## Objective
Validate Grafana dashboard availability, staging data-source integration, authorization and restart-stable provisioning against the owner-approved post-E8 production-equivalent staging deployment.

## Evidence boundary
Repository CI, compose fixtures and synthetic browser checks are supporting evidence only. `PASS` requires real evidence from the approved staging deployment and must be attributable to the same immutable Phase 8.2 deployment fingerprint.

## Preconditions
- Phase 8.2 is active.
- Owner-approved production-equivalent staging exists.
- Exact deployed commit and immutable application image identity are captured before final acceptance.
- Prometheus metrics validation is accepted or explicitly tracked against the same deployment identity.

## Validation procedure
1. Confirm the approved staging Grafana endpoint and intended access path.
2. Authenticate with an approved staging identity and verify unauthorized access is denied as designed.
3. Confirm the expected DTMO dashboards are provisioned and load without authentication loops or missing-dashboard errors.
4. Verify Grafana uses the intended staging Prometheus data source and not a production endpoint.
5. Confirm representative panels execute successfully and show current staging data.
6. Generate a representative DTMO request/activity and verify the corresponding dashboard signal changes where applicable.
7. Verify dashboard visibility follows the intended role boundary and that embedded/linked views do not bypass DTMO authorization.
8. Restart or reload the approved staging Grafana/provisioning component using the approved operational procedure and verify the expected dashboards and data-source configuration return without manual drift.
9. Confirm no production Grafana/Prometheus credentials or endpoints are reused.
10. Record timestamp, reviewer, restricted evidence reference and the Phase 8.2 deployment fingerprint.

## PASS criteria
- Grafana endpoint access behaves as designed.
- Expected DTMO dashboards load successfully.
- Staging Prometheus is the active data source.
- Representative panels render fresh staging data without broken queries.
- Representative DTMO activity produces an observable dashboard change where applicable.
- Dashboard authorization is correct and cannot be bypassed through embedding/linking.
- Provisioning survives the approved restart/reload procedure without manual configuration drift.
- No production monitoring credentials/endpoints are reused.
- Evidence is bound to the same immutable Phase 8.2 deployment identity.

## Fail-closed conditions
Any authentication loop, broken critical dashboard query, unexpected production endpoint/credential reuse, authorization bypass, provisioning drift after restart, stale/unattributable evidence, or missing deployment identity binding keeps this check from `PASS`.

## Evidence manifest
Manifest field: `checks.grafana_dashboards`

Validate only this step with:

```bash
python3 tools/phase8_platform_validation.py <manifest.json> --check grafana_dashboards
```

The step validator does not make the full Phase 8.2 or Phase 8 acceptance claim.

Related: issue #237, #235, #232, #230, #227, #225, #221, #219, #217, #214, #211, #210, #158; PR #212, #216, #218, #220, #224, #226, #229, #231, #234, #236.
