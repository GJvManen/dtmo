# Canonical Administration — Governed framework runtime

## Purpose

The canonical Administration workspace configures framework integrations without requiring the legacy interface. Endpoint, enablement and write-only credentials remain governed by the DTMO server-side control plane.

MISP exposes its governed read/import execution path from Administration. AIL now also exposes the explicit object scope required by the existing read-only connector and can execute that scoped connector from the same canonical card.

## Shared interaction contract

An authorized principal with `manage:connectors` can configure an integration through the same-origin `/api/v1/admin/integrations/{integration_id}` endpoint. Credential fields are write-only. Existing credential values are never loaded into the browser or returned by the read model; the API exposes only `credential_configured`.

A runtime action is enabled only for persisted, enabled and server-derived `ready` configuration with no unsaved browser changes. Runtime execution uses existing DTMO server-side adapters and never turns the browser into an upstream client.

## MISP runtime

**Run MISP import now** calls the existing same-origin `POST /connectors/misp/run` route. Returned records continue through canonical normalization, persistence and indexing. The UI reports request-specific status, record/insert/index counts, attempts, alert state and correlation ID.

## AIL scoped runtime

AIL is intentionally narrower than a crawler integration. `AilReadConnector` only reads explicitly scoped object global IDs and refuses to run without `ail_object_global_ids`. The canonical AIL card exposes **AIL object scope** as non-secret runtime configuration and persists it server-side before AIL can become ready.

Once endpoint, write-only credential, explicit object scope and enablement are persisted, **Run AIL import now** uses the existing same-origin `POST /connectors/ail/run` route. DTMO performs all AIL API requests server-side, imports only the configured explicit objects, applies the existing data-minimized normalization and canonical ingest path, and reports the request-specific runtime result.

For AIL, the Administration read model consumes the server-derived governed integration-readiness contract. Endpoint plus credential alone therefore never labels AIL ready when its explicit object scope is absent. `activation_blockers` explains incomplete AIL runtime configuration.

## Persistence and secret boundary

Non-secret runtime settings remain in `/var/lib/dtmo/runtime-integration-settings.json`. AIL object scope is non-secret configuration and is persisted there. Integration credentials remain separately persisted in `/var/lib/dtmo/runtime-integration-secrets.json` with mode `0600`; secret values are never written into the non-secret document or returned to the browser.

## Authorization and evidence boundary

Configuration and runtime execution require server-authorized `manage:connectors`; UI visibility is not authorization. A completed MISP or AIL run is evidence only for that specific request and returned ingest result. It is not a blanket provider-health, completeness or source-truth claim.

AIL execution never creates or starts crawlers. Imported AIL objects remain read-only, data-minimized and without external-share authority. Neither MISP nor AIL import grants intelligence review, case, sharing, publication, remediation, external-assurance or production authority.

## Fail-closed behavior

Unknown integrations, empty credential replacements and invalid production endpoints are rejected. AIL without explicit object scope remains `configuration-required` and cannot execute from canonical Administration. AIL scope submitted against a non-AIL integration is rejected. Unsaved configuration disables runtime actions, and upstream/runtime failures remain visibly failed rather than being promoted to healthy state.
