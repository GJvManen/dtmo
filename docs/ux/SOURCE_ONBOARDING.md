# Governed manual source onboarding

## Purpose

DTMO exposes manual intelligence-source onboarding inside the canonical **Sources & Catalog** workspace. The flow reuses the existing source registry, RBAC, audit and safe outbound execution boundaries; it does not create a parallel connector subsystem.

## Disabled-first lifecycle

Every manually registered source is created with `enabled=false`. A create request that attempts to set `enabled=true` is rejected. Activation is a separate operator action after configuration validation and a pre-activation test.

The UI therefore presents the lifecycle as:

1. register disabled;
2. validate configuration;
3. run a bounded pre-activation test where supported;
4. activate separately;
5. use the existing governed source-run path for ingestion.

This sequence is a product safety boundary, not merely a visual convention.

## Explicit onboarding fields

The canonical flow exposes source ID, name, source type, HTTPS endpoint, reliability, schedule/freshness interval, authentication mode, logical secret reference and owner.

`owner` is the authenticated human administrator recorded by the existing source registry as `created_by`. DTMO does not invent a second ownership identity. Authentication mode is reported truthfully from executable configuration:

- `anonymous` when no secret reference is configured;
- `credentialed-secret-reference` when a logical secret reference is configured for a code-reviewed credentialed adapter.

## Credentials

Raw credentials never belong in source registry data. The existing secret-reference validator remains authoritative and accepts only supported logical reference forms such as `env:VARIABLE`, `vault://...` or `secret://...`.

Manual ad-hoc credentialed adapters are not created through this flow. A credential reference is accepted only when the source ID resolves to an existing code-reviewed supported adapter profile that explicitly requires credentials. This prevents an arbitrary manual source from being presented as executable merely because a secret reference was supplied.

## Validation and pre-activation test

`POST /api/v1/admin/sources/{source_id}/validate` validates the stored configuration and reports owner/authentication context.

`POST /api/v1/admin/sources/{source_id}/test` provides a non-ingesting pre-activation test for a manually registered DTMO JSON v1 feed. It uses the same bounded HTTPS/public-address and parsing controls as the governed generic source executor, but it does not require the source to be enabled and does not persist intelligence or connector-run state.

Code-reviewed catalog sources remain on their dedicated adapter execution paths and cannot bypass those adapters through the generic pre-activation test endpoint.

## Activation and normal execution

Activation remains an explicit audited `PATCH` of the source definition. The canonical UI only enables its activation control after a successful configuration validation and successful non-ingesting test in that operator session.

After activation, normal execution continues through the existing source framework. That path retains connector isolation, alerting, raw/canonical persistence and existing operational controls.

## Authorization and audit

Source registry writes, validation, test and execution require the existing `manage:connectors` permission and a human `admin` role. Service accounts cannot use the human-admin source registry mutation flow.

Creation, update, test and execution actions are recorded through the persistent audit chain with the authenticated actor, request ID and source endpoint provenance reference.

## Publication boundary

Registering, validating, testing, activating or executing a source does **not** grant intelligence review authority and does not grant external publication/share authority. Candidate intelligence continues through the independent human-review and separate share-approval boundaries.

## Scope boundary

The pre-activation test intentionally supports manual DTMO JSON v1 feeds only. Broader parser/plugin onboarding is a separate code-review concern and must not be inferred from a successful generic registration.
