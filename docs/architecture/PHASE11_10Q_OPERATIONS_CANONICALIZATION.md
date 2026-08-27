# Phase 11.10q — Canonical Operations recovery

## Scope

This bounded recovery slice removes `/operations` from the generic shell-foundation path and makes it a real canonical React workspace. The workspace reads the already-authoritative same-origin DTMO runtime contracts instead of sending an operator to the legacy Operations page.

The canonical workspace observes:

- `/health` for API/runtime/environment and scheduler observation;
- `/api/v1/operations/summary` for Prometheus-backed request, latency, alert, queue, trace and connector-run telemetry;
- `/connectors` for connector capability state;
- `/api/v1/operations/runtime-evidence` for persisted connector runtime state and recent durable connector health-event history.

The deep runtime-evidence slice exposes only bounded fields from `connector_runtime_states` and `connector_health_events`: connector identity, health state, last run identifier, success/failure timestamps, failure/isolation state, run status, duration, record count, quarantine count, bounded error code and the persisted `publish_approved=false` authority boundary. Raw quarantined evidence, credentials and connector request payloads are not exposed.

Operator pivots for action stay inside the canonical workbench: Sources & Collection, Administration, Automation and Command Center. Operations itself remains read-only.

## Fail-closed behavior

Unavailable health, telemetry, connector capability or persisted runtime evidence is rendered as unavailable. Missing observations are never turned into zero values, healthy state or absence-of-risk claims. Connector enablement is capability state only and does not prove upstream health or successful collection. Persisted connector runtime state proves only what DTMO durably observed during recorded executions; it is not live upstream availability evidence.

Review, sharing, case mutation, connector execution and configuration remain separate server-authorized actions. This slice does not add credential exposure, publication authority, external sharing authority, connector execution authority or responder authority.

## Evidence boundary

A green gate for this slice is repository-controlled operational observation only. It proves that exact-head canonical Operations can surface durable connector runtime state and recent run evidence through a same-origin read-only contract. It is not live upstream availability evidence, not proof that no incident or vulnerability exists, not owner functional acceptance, not staging evidence, not production-equivalent evidence, and not external-assurance evidence.

The dedicated `Phase 11.10q Operations Functional Recovery Gate` seeds temporary repository-controlled connector state into an exact-head PostgreSQL schema, renders it through the built canonical workbench, verifies the read-only evidence journey in Chromium, and records an artifact with the explicit claim boundary. The test does not execute a live external connector and does not establish production authorization.
