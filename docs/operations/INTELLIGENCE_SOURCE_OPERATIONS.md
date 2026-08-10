# Intelligence Source Operations

## Current supported live source

DTMO 16.0.0rc7 supports the existing `cisa-kev` connector as the first end-to-end live source. It fetches the CISA-maintained KEV JSON mirror, preserves the raw record and provenance, persists a canonical candidate record, and indexes it for governed search.

The connector does not review intelligence and does not approve external sharing.

## Automatic polling

Automatic polling is disabled by default. To enable the registered live connector in a non-production test deployment, set:

```env
DTMO_FEATURE_LIVE_CONNECTORS=true
```

and recreate/restart the application container. The poll interval is controlled by `DTMO_CONNECTOR_POLL_SECONDS`.

Production configuration remains subject to the existing production security and external acceptance gates.

## Manual governed execution

The existing manual endpoint is:

```text
POST /connectors/cisa-kev/run
```

It requires the server-side permission:

```text
manage:connectors
```

In local/development test mode an ADMIN principal can be supplied using the existing development identity headers, for example through an API client:

```text
X-DTMO-Subject: local-admin
X-DTMO-Roles: admin
X-Request-ID: <unique-request-id>
```

If `DTMO_API_KEY` is configured, the matching `X-DTMO-API-KEY` is also required by the development authentication path. Do not copy credentials into documentation, issues, logs, screenshots, or source control.

A successful response reports the number of fetched `records`, newly `inserted` canonical records, and successfully `indexed` search documents. Replaying the connector is permitted and is intentionally idempotent for canonical records while repairing derived OpenSearch documents where possible.

## Search behavior

Search endpoint:

```text
GET /api/v1/intelligence/search?q=<query>
```

An empty/fresh deployment now creates the intelligence index on demand and returns zero results rather than treating a missing index as a backend outage.

## Source-management boundary

16.0.0rc7 intentionally does **not** permit arbitrary source URLs to be registered. New-source administration requires a separate governed source registry with supported connector types, network/URL validation, SSRF controls, secret references, ownership, provenance, scheduling, audit history and explicit lifecycle state.

Until that registry is implemented, source additions must be made through reviewed connector code rather than unvalidated runtime URLs.
