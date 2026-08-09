# API Outage / Elevated 5xx Runbook

## Trigger

Use this runbook when `dtmo_api_error_alert_active` is active, HTTP 5xx rates rise materially, request latency/in-flight requests indicate saturation, or users report API unavailability.

## Immediate checks

1. Assign Incident Commander and severity.
2. Capture UTC start time, affected route template(s), correlation IDs, trace IDs, deployment/change identifier and current dashboard state.
3. Confirm whether the symptom is API-local or correlated with PostgreSQL, Redis, OpenSearch, object storage or connector degradation.
4. Check recent deploy/configuration changes before restarting anything.
5. If compromise is suspected, preserve logs/evidence and involve the Security Lead before destructive remediation.

## Containment

- Pause or reduce nonessential producers/automations if they are amplifying load.
- Prefer rollback to a known-good deployment over ad-hoc production edits.
- Revoke exposed sessions/credentials if authentication compromise is suspected.
- Do not disable RBAC, audit logging, human share approval, security scanning or integrity checks to restore availability.

## Recovery

1. Restore the failed dependency or known-good application version.
2. Verify health endpoints and dependency connectivity.
3. Verify `dtmo_api_error_alert_active` returns to clear and 5xx rate falls.
4. Confirm latency and in-flight requests stabilize within accepted internal baselines.
5. Execute at least one read-only critical journey and, where relevant, one authorization-negative check.
6. Keep observation active long enough to exclude immediate recurrence; alert clearance alone is not sufficient.

## Security / privacy branch

Escalate to SEV-1 when unexplained 5xx errors coincide with suspicious authentication events, unexpected privilege use, data-integrity anomalies, exfiltration indicators or evidence loss. Preserve relevant logs and immutable receipts before restart/rollback where feasible.

## Communication

State confirmed impact, affected service/route template, start time, current containment, confidence and unknowns. Never include credentials, raw request bodies, student/person data or full query strings. External or broad internal communication requires the applicable human communications/privacy approval.

## Closure criteria

- stable non-5xx behavior demonstrated;
- dependency health validated;
- no unresolved integrity/security concern hidden by the recovery;
- evidence/timeline stored with bounded identifiers;
- follow-up defects/changes assigned;
- IC and service/data owner agree to closure or handoff.
