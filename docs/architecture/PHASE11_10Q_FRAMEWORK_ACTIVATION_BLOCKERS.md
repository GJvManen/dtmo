# Phase 11.10q — Framework activation blocker recovery

## Scope

This bounded recovery slice makes framework activation readiness server-derived instead of inferred in the browser from endpoint and credential presence alone. The canonical Administration route continues to use the existing governed integration API and does not auto-enable any external service.

## Server-derived activation contract

`/api/v1/admin/integrations` now returns `can_activate` and `activation_blockers` for each supported framework integration. The blocker list contains configuration categories only and never secret values. Endpoint and server-side credential presence remain required. Additional component-specific requirements are evaluated where applicable: AIL object scope, IntelOwl and Cortex analyzer allowlists, TheHive organization scope, OpenCTI entity-type/checkpoint configuration and Taranis checkpoint configuration.

A PATCH that would leave an integration enabled while an activation blocker remains fails closed with HTTP 422. The mutation is not persisted and the feature flag is not enabled. Disabling an integration remains possible. Runtime configuration persistence continues to contain only non-secret enablement and endpoint values; credentials stay deployment/server-side.

## Canonical Administration behavior

`FrameworkIntegrationReadiness` consumes the server-derived readiness contract. It no longer decides that endpoint plus credential is sufficient. An Enable action is rendered only when `can_activate` is true. Otherwise the operator sees the concrete missing configuration categories. Successful enablement still proves configuration state only; upstream reachability and runtime health require separate observation.

## Authority and evidence boundaries

This change does not grant review, publication, sharing or external-assurance authority. It does not expose credentials, synthesize health, auto-enable services, or convert repository-controlled CI into live/staging/production-equivalent evidence. `docs/roadmap/FUNCTIONAL_RECOVERY_ACCEPTANCE.md` remains authoritative and owner functional acceptance is still required before PR #316 can merge.
