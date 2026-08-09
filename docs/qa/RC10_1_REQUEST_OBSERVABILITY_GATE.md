# RC10.1 Request Observability Gate

## Decision

`PASS`

RC10.1 starts Phase 7 with exactly one bounded objective: make HTTP request telemetry correlation-safe, structured and operationally bounded without changing business behavior.

## Accepted exact-head evidence

PR #80 exact head `01a175e12da7c8af8566178a2d7e6b34a57d58bc` completed all 34 registered workflows successfully.

Retained artifact `9040196394`, digest `sha256:6792020994d94b0484cb84140d202433303eceb82565f8598ffd5937940531d6`, was independently inspected and is identity-bound to the accepted exact head.

Evidence confirms:

- safe inbound correlation-ID handling;
- correlation ID and HTTP method bound into the real `structlog.contextvars` context;
- structured `http_request_completed` and `http_request_failed` events;
- bounded Prometheus request counters and latency histograms keyed by route templates instead of raw URL paths;
- HTTP in-flight request gauge;
- exact-head machine-readable decision `pass`;
- JUnit: 5 tests, 0 failures, 0 errors, 0 skipped;
- no production data used;
- no business mutation added.

PR #80 merged with expected-head protection as `1675d88bb24dcd50e20545f49b26dd7cc2810d97`.

## Risk addressed

The prior implementation stored correlation IDs in a standalone Python `ContextVar` while the logging pipeline consumed structlog context variables, so correlation could not be relied on as structured-log evidence. The prior HTTP metrics also labelled requests by raw URL path, creating a risk of high-cardinality Prometheus series for dynamic paths.

RC10.1 closes those two bounded gaps.

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

Phase 7 / RC10.2 — add one bounded controlled-failure alerting gate for connector failures, including actionable alert signal, correlation evidence, recovery/clear behavior and retained exact-head evidence. Queue backlog, storage integrity, API-error and search-health alerting remain later objectives.
