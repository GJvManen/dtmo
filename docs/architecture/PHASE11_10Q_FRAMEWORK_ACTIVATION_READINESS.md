# Phase 11.10q — Canonical framework activation readiness

## Scope

This recovery slice mounts the existing `FrameworkIntegrationReadiness` control into the canonical `/workbench/administration` route. It closes the UI integration gap where a supported framework service could have an endpoint and server-side credential configured but still appear only as a generic disabled integration with no direct canonical activation path.

## Operator flow

A principal with `manage:connectors` sees framework activation readiness inside canonical Administration. The component reads `/api/v1/admin/integrations` through the same-origin DTMO API and distinguishes enabled integrations, missing endpoints, missing server-side credentials, and configured-but-disabled integrations that require explicit activation. For the last state, the operator may choose **Enable <integration>**. The mutation uses the existing governed PATCH contract with an `X-Request-ID`; no legacy `/ui/*` route is required.

## Safety and authority boundaries

DTMO does not auto-enable external framework services. Endpoint and credential presence make an integration actionable for explicit activation only; they do not prove upstream reachability or runtime health. Component-specific requirements such as analyzer allowlists, organization scope, object scope and other governed runtime settings remain separate prerequisites. Credentials remain server-side and are never returned to or edited by this component.

This control does not grant intelligence review, publication, external-sharing, case-mutation or external-assurance authority. Server-side `manage:connectors` authorization remains authoritative and activation failures remain fail-closed.

## Acceptance impact

The canonical Administration route now exposes the previously isolated activation-readiness control directly in the normal operator path. This is repository-controlled remediation evidence only. `docs/roadmap/FUNCTIONAL_RECOVERY_ACCEPTANCE.md` remains authoritative and **Framework integrations** remains BLOCKED until the owner functional retest confirms that the normal configured deployment is genuinely actionable without legacy fallback.
