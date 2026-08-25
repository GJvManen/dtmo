# Canonical Administration — Write-only integration credentials

## Purpose

The canonical Administration workspace can set or replace framework integration credentials without requiring the legacy interface. This closes the functional gap where endpoint and enablement were editable but an integration in `credential-required` could not be completed from the canonical control plane.

For MISP, Administration now also exposes the existing governed server-side read/import execution path once the persisted integration state is enabled and ready. This provides an operator-visible end-to-end runtime action rather than stopping at configuration readiness.

## Interaction contract

An authorized principal with `manage:connectors` can configure an integration endpoint, optionally replace its credential and change enablement through the same-origin `/api/v1/admin/integrations/{integration_id}` endpoint.

Credential fields are **write-only**. Existing credential values are never loaded into the browser, never returned by the integration read model and are cleared from the form after a successful save. Leaving the field empty preserves the existing credential.

The read model exposes only `credential_configured: true|false`; it never exposes the credential value.

### Governed MISP runtime action

When the MISP integration is enabled, has a configured API endpoint and has a server-side credential, the canonical Administration card enables **Run MISP import now**. Unsaved configuration disables the action so the runtime call cannot silently use settings that differ from what the operator sees.

The browser calls the existing same-origin `POST /connectors/misp/run` endpoint. DTMO then performs the upstream MISP request server-side through `MispReadConnector`, applies the existing normalization contract and ingests returned records through the canonical persistence/indexing path.

The UI reports the returned runtime result: status, records received, inserted count, indexed count, attempts, alert state and correlation identifier. A failed run remains visibly failed; the UI does not reinterpret it as success.

No MISP credential is sent back to or read by the browser beyond the explicit write-only credential submission flow.

## Server-side persistence boundary

Non-secret runtime settings remain in `/var/lib/dtmo/runtime-integration-settings.json`.

Write-only integration credentials are persisted separately in `/var/lib/dtmo/runtime-integration-secrets.json`. The server creates/replaces this file with mode `0600`. Secret values are never written into the non-secret runtime settings document.

This server-side runtime secret store does not turn the browser into an upstream integration client. Upstream calls continue to use DTMO server-side adapters and server-side credentials.

## Authorization and evidence boundary

Credential mutation and the MISP runtime action require the existing server-authorized `manage:connectors` permission. UI visibility is not authorization.

Saving an endpoint, credential or enablement value does not prove provider connectivity, health, data freshness or successful collection. A completed MISP run is evidence for that specific governed request and its returned ingest counts; it is not a blanket provider-health claim and it does not prove that all relevant MISP content has been collected.

MISP read/import remains separate from governed MISP export. Running an import does not grant intelligence review, case, sharing, publication, remediation, external-assurance or production authority.

## Fail-closed behavior

Unknown integrations are rejected. Empty credential replacement requests are rejected. Production integration endpoints continue to require HTTPS. Persistence failure returns an error rather than reporting success.

The MISP runtime action is unavailable while the card is disabled, not ready or contains unsaved changes. Upstream/runtime failures are returned as failed runtime results and remain observable to the operator.
