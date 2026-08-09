# RC10.2 Connector Failure Alerting Gate

## Decision

`CI_VALIDATION_PENDING`

RC10.2 implements exactly one bounded Phase 7 objective: controlled connector-failure alerting after the connector's existing bounded retry policy reaches a terminal result.

## Scope

- terminal connector failure sets `dtmo_connector_alert_active{connector=...}` to `1`;
- a Prometheus alert rule raises `DTMOConnectorFailure` from that bounded signal;
- structured alert events retain a safe correlation ID and actionable operator guidance;
- raw connector error text is not copied into alert logs;
- repeated failures while an alert is active do not generate another raise transition;
- a subsequent successful connector run clears the metric to `0` and emits `connector_alert_cleared`;
- connector run and alert-transition counters remain bounded by connector/status/transition labels;
- publication approval remains unchanged and false in the alert signal;
- exact-head JUnit, pytest log and machine-readable evidence are retained as `connector-alerting-evidence`.

## Existing controls preserved

RC7 connector retry/backoff and source-health/failure-isolation controls remain authoritative. RC10.2 observes the terminal result; it does not create a second retry policy, change circuit-breaker behavior or automatically publish intelligence.

## Gate

`PASS` requires every registered workflow on the exact final PR head to succeed and retained `connector-alerting-evidence` to be independently inspected. Missing, queued, cancelled, failed or unexecuted CI is never `PASS`.

## Claim boundary

RC10.2 does **not** claim:

- pager/email/chat notification delivery is configured or accepted;
- queue-backlog alerting is complete;
- storage-integrity alerting is complete;
- API-error alerting is complete;
- search-health alerting is complete;
- operational runbooks/on-call handover are complete;
- Phase 7 is complete;
- Phase 6's genuine VoiceOver/NVDA external gate is closed.

## Governance

No production credentials or production data are required. RBAC, separation of duties, privacy, provenance, persistent auditability and separate human share approval remain unchanged.

## Exactly one next priority

Inspect every required workflow on the final RC10.2 pull-request head and independently inspect retained `connector-alerting-evidence`; repair only the first deterministic failure, or accept/merge only after complete successful evidence.
