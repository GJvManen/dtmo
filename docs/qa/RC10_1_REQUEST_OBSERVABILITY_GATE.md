# RC10.1 Request Observability Gate

## Decision

`CI_VALIDATION_PENDING`

RC10.1 starts Phase 7 with exactly one bounded objective: make HTTP request telemetry correlation-safe, structured and operationally bounded without changing business behavior.

## Scope

- validate or replace inbound `X-Correlation-ID` values before they enter logs;
- bind the accepted correlation ID and HTTP method into the real `structlog` context;
- emit structured `http_request_completed` and `http_request_failed` events with route template, status and duration;
- expose bounded Prometheus request counters and latency histograms keyed by route templates rather than raw URL paths;
- expose an in-flight HTTP request gauge;
- retain exact-head JUnit, pytest log and machine-readable evidence in `request-observability-evidence`.

## Risk addressed

The previous implementation stored correlation IDs in a standalone Python `ContextVar` while the logging pipeline used `structlog.contextvars.merge_contextvars`. That does not by itself bind the standalone value into structlog's context, so correlation could not be relied on as structured-log evidence.

The previous HTTP metrics also labelled requests by raw URL path. Dynamic path values can create unbounded Prometheus label cardinality and weaken operational usefulness.

## Gate

The dedicated `RC10 Request Observability Gate` must pass on the exact pull-request head. Its retained evidence must show:

- safe correlation-ID handling;
- structured log context containing correlation ID and method;
- route-template request counters;
- route-template request latency metrics;
- in-flight request metrics;
- no production data;
- no added business mutation.

Missing, queued, cancelled, failed or unexecuted CI is never `PASS`.

## Claim boundary

RC10.1 does **not** claim:

- distributed tracing is complete;
- connector, queue, storage or search alerting is complete;
- runbooks or on-call handover are complete;
- Phase 7 is complete;
- Phase 6's external VoiceOver/NVDA gate is closed.

## Governance

RBAC, separation of duties, privacy, provenance, persistent audit evidence and separate human share approval remain unchanged. Phase 6 remains `BLOCKED_EXTERNAL` only for genuine assistive-technology execution on supported real hosts.

## Exactly one next priority

Inspect every required workflow on the exact RC10.1 pull-request head and independently inspect retained `request-observability-evidence`; repair only the first deterministic failure, or accept/merge only after complete successful evidence.
