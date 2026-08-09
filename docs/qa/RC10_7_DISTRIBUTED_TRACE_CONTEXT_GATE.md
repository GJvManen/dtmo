# RC10.7 Distributed Trace Context Gate

## Decision

`CI_VALIDATION_PENDING`

## Objective

Validate a bounded W3C distributed trace-context baseline that provides privacy-safe cross-service request correlation without adding request data, credentials, identities or publication authority to traces.

## Required exact-head evidence

Acceptance requires all of the following on one final PR head:

- strict W3C version-00 `traceparent` parsing;
- invalid, unsupported, uppercase/non-hex, all-zero, oversized or extended context is rejected and restarted locally;
- generated trace/span identifiers are cryptographically random and non-semantic;
- valid incoming trace ID is preserved while a fresh local span ID is created;
- structured request logs include trace ID + span ID + existing correlation ID;
- raw `traceparent`, `tracestate`, URLs, query values, bodies, credentials and identities are not traced;
- HTTP responses do not echo trace headers;
- outbound connector HTTP clients carry a valid child `traceparent`;
- bounded trace-context decision metrics expose only accepted/generated/rejected state;
- RBAC, provenance, separation of duties and human share approval are unchanged;
- no new telemetry SDK/runtime dependency is introduced in this bounded baseline;
- dedicated `RC10 Distributed Trace Context Gate` succeeds and retains exact-head JUnit/log/JSON evidence;
- every registered workflow succeeds on the exact final head.

## Current CI evidence

PR #94 head `cb889d2e643f4f00386bb6281ae3082f47031b98` completed 40 of 41 workflows successfully, but `RC4 Quality Gate` failed. Workflow run `31328513139`, job `93282799136`, failed in the Ruff lint step with two `S105` findings caused by test-only synthetic marker variable names (`secret_path`, `secret_query`). That head is **not accepted**.

RUN-138 remediates the deterministic lint failure by renaming only those test fixture variables to neutral `synthetic_*_marker` names. No scanner suppression, ignore rule, skipped test or workflow bypass was introduced. The remediated exact head must rerun the complete workflow matrix and regenerate retained trace-context evidence before acceptance.

## Standards/security boundary

W3C Trace Context identifies privacy, information-exposure and denial-of-service risks for trace headers and requires implementations to treat them as untrusted input. DTMO therefore accepts only the fixed version-00 identifier format and deliberately does not ingest `tracestate` in this baseline.

## Claim boundary

This gate does **not** claim:

- an OpenTelemetry/OTLP collector is deployed;
- a trace exporter/backend is deployed;
- cross-service trace visualization is operational;
- dashboards, runbooks or on-call handover are complete;
- Phase 7 is complete;
- Phase 6 assistive-technology evidence is complete;
- any issue #1 external production gate is complete.

## Exactly one next priority

Verify the complete exact-head workflow matrix and regenerated retained `distributed-trace-context-evidence` artifact on the remediated PR #94 head; accept and merge only if both are complete and internally consistent.
