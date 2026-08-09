# Connector Failure / Upstream Source Degradation Runbook

## Trigger

Use this runbook when `dtmo_connector_alert_active` is active, repeated connector attempts terminate as failed, freshness degrades, or a source becomes unavailable/untrustworthy.

## Immediate checks

1. Assign Incident Commander and severity.
2. Record connector identifier, UTC time, correlation ID, terminal attempt count and source/freshness impact.
3. Determine whether failure is upstream availability, authentication/authorization, rate limiting, schema/format drift, network/TLS, licence/terms restriction or an internal parser/storage dependency.
4. Check whether multiple connectors fail simultaneously; correlated failures can indicate shared infrastructure or credential compromise.
5. Preserve failed payload provenance/quarantine evidence without copying raw sensitive payloads into incident chat.

## Containment

- Keep the failed connector isolated from publication; connectors never gain share approval.
- Do not bypass validation, provenance, confidence, deduplication or quarantine controls to restore ingestion.
- If upstream responses are malformed or suspicious, stop automated retries when continued calls could amplify harm or violate rate/terms limits.
- Rotate/revoke credentials through approved secret-management processes if exposure is suspected; never place replacement secrets in tickets or source control.

## Recovery

1. Validate upstream status, credentials, rate limits and terms/licence boundary.
2. Run a controlled connector canary using non-production-safe inputs/approved endpoint conditions.
3. Confirm terminal run status becomes `completed` and `dtmo_connector_alert_active` clears.
4. Verify freshness, provenance fields, timestamps, confidence and raw-evidence receipts remain intact.
5. Replay only from approved/quarantined evidence and verify deduplication before returning normal scheduling.
6. Require human review/share approval for anything that may later be published.

## Security / privacy branch

Escalate to SEV-1 when failure coincides with credential theft, unexpected source redirection, TLS/certificate anomaly, malicious payload indicators, provenance loss or unauthorized publication attempts. Preserve source metadata and relevant logs before credential/session changes where practicable.

## Communication

Communicate source impact and freshness limitations explicitly. Do not imply data is current when the connector is degraded. External/broad sharing requires human communications/privacy approval and must distinguish confirmed facts, confidence and unknowns.

## Closure criteria

- connector succeeds under normal control path;
- freshness/provenance/integrity are validated;
- no bypass remains enabled;
- backlog/replay risk is understood and controlled;
- evidence and follow-up ownership are recorded.
