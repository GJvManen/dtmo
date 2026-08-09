# Search Health Degradation Runbook

## Trigger

Use this runbook when `dtmo_search_health_alert_active` is active or OpenSearch health is repeatedly `red`/`unreachable`.

## Immediate checks

1. Assign Incident Commander and severity.
2. Record UTC start time, bounded cluster identifier, correlation ID, health state and recent infrastructure/deployment changes.
3. Determine whether the condition is node loss, shard allocation, storage pressure, networking/TLS/authentication, resource exhaustion or broader host/platform failure.
4. Treat search results as potentially incomplete while health is red/unreachable; do not present partial results as authoritative.
5. Correlate with API errors, latency, queue pressure and storage alerts.

## Containment

- Avoid destructive shard/index operations until evidence and recovery path are understood.
- Reduce nonessential indexing/ingestion if it worsens pressure.
- Preserve cluster diagnostics needed for incident analysis, while excluding query contents, document bodies, identities and credentials from general incident channels.
- Do not disable security controls or expose an unauthenticated production cluster to restore service.

## Recovery

1. Restore node/connectivity/resource health through approved infrastructure change.
2. Validate cluster health through the bounded health probe.
3. Confirm `dtmo_search_health_alert_active` clears only after the configured healthy streak.
4. Execute representative read-only search checks and compare expected result completeness against known-good references.
5. Verify ingestion/indexing resumes without provenance loss or duplicate amplification.
6. Maintain an observation period to detect recurrence.

## Security / privacy branch

Escalate to SEV-1 for unexpected administrative changes, evidence of unauthorized index access/deletion, credential compromise, suspicious outbound traffic, or integrity anomalies. Preserve logs and snapshots/receipts where available before destructive recovery.

## Communication

Clearly state that search may be incomplete or unavailable. Never expose query text, indexed sensitive data, credentials or internal diagnostic bodies in broad updates. External/broad communication requires human communications/privacy approval.

## Closure criteria

- stable green/yellow state appropriate to the accepted topology;
- search completeness validated;
- no unresolved security/integrity concern;
- queue/indexing catch-up controlled;
- evidence and follow-up ownership recorded.
