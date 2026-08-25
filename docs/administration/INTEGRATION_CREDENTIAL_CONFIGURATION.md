# Canonical Administration — Write-only integration credentials

## Purpose

The canonical Administration workspace can set or replace framework integration credentials without requiring the legacy interface. This closes the functional gap where endpoint and enablement were editable but an integration in `credential-required` could not be completed from the canonical control plane.

## Interaction contract

An authorized principal with `manage:connectors` can configure an integration endpoint, optionally replace its credential and change enablement through the same-origin `/api/v1/admin/integrations/{integration_id}` endpoint.

Credential fields are **write-only**. Existing credential values are never loaded into the browser, never returned by the integration read model and are cleared from the form after a successful save. Leaving the field empty preserves the existing credential.

The read model exposes only `credential_configured: true|false`; it never exposes the credential value.

## Server-side persistence boundary

Non-secret runtime settings remain in `/var/lib/dtmo/runtime-integration-settings.json`.

Write-only integration credentials are persisted separately in `/var/lib/dtmo/runtime-integration-secrets.json`. The server creates/replaces this file with mode `0600`. Secret values are never written into the non-secret runtime settings document.

This server-side runtime secret store does not turn the browser into an upstream integration client. Upstream calls continue to use DTMO server-side adapters and server-side credentials.

## Authorization and evidence boundary

Credential mutation requires the existing server-authorized `manage:connectors` permission. UI visibility is not authorization.

Saving an endpoint, credential or enablement value does not prove provider connectivity, health, data freshness or successful collection. Runtime observations and collection results remain separate evidence.

Administration does not grant intelligence review, case, sharing, publication, remediation, external-assurance or production authority.

## Fail-closed behavior

Unknown integrations are rejected. Empty credential replacement requests are rejected. Production integration endpoints continue to require HTTPS. Persistence failure returns an error rather than reporting success.
