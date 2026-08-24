# Phase 11.10q — Canonical Operations recovery

## Scope

This bounded recovery slice removes `/operations` from the generic shell-foundation path and makes it a real canonical React workspace. The workspace reads the already-authoritative same-origin DTMO runtime contracts instead of sending an operator to the legacy Operations page.

The canonical workspace observes:

- `/health` for API/runtime/environment and scheduler observation;
- `/api/v1/operations/summary` for Prometheus-backed request, latency, alert, queue, trace and connector-run telemetry;
- `/connectors` for connector capability state.

Operator pivots for action stay inside the canonical workbench: Sources & Collection, Administration, Automation and Command Center. Operations itself remains read-only.

## Fail-closed behavior

Unavailable health, telemetry or connector APIs are rendered as unavailable. Missing observations are never turned into zero values, healthy state or absence-of-risk claims. Connector enablement is capability state only and does not prove upstream health or successful collection.

Review, sharing, case mutation, connector execution and configuration remain separate server-authorized actions. This slice does not add credential exposure, publication authority, external sharing authority or responder authority.

## Evidence boundary

A green gate for this slice is repository-controlled operational observation only. It is not owner functional acceptance, not staging evidence, not production-equivalent evidence, and not external-assurance evidence. `docs/roadmap/FUNCTIONAL_RECOVERY_ACCEPTANCE.md` remains authoritative and PR #316 remains blocked until the owner completes and accepts the canonical functional retest.
