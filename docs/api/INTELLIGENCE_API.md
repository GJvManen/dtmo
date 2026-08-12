# DTMO Intelligence API

Last updated: **2026-08-12**  
Baseline: **16.0.0rc12 / RC13 accepted + post-RC13 severity read contract**

## Purpose

The DTMO Intelligence API connects the governed ingestion, canonical persistence, investigation and read-side analytics layers.

Canonical intelligence flows through:

1. raw source evidence in S3-compatible object storage;
2. normalized durable application state in PostgreSQL;
3. supporting OpenSearch indexing for analyst search;
4. authenticated read APIs used by the unified DTMO console.

Ingestion creates candidate intelligence only. Read, search, filtering, dashboard aggregation and indexing never grant review or external-share approval.

## Authentication and authorization

Protected intelligence endpoints require an authenticated DTMO principal and the relevant server-side permission. Production identity is based on the configured external bearer-token/identity-provider trust model; development/reference headers are not a substitute for production identity architecture.

Common development/reference headers include:

| Header | Purpose |
|---|---|
| `X-DTMO-Subject` | Auditable subject identifier. |
| `X-DTMO-Roles` | Development/reference role context. |
| `X-DTMO-API-Key` | Development/reference shared API authentication where configured. |
| `X-Correlation-ID` | Optional correlation identifier; DTMO creates one where needed when absent. |

Server-side RBAC remains authoritative. Client-side filters or hidden controls are never authorization boundaries.

## Canonical severity values

The canonical severity taxonomy is:

- `informational`
- `low`
- `medium`
- `high`
- `critical`

`critical` remains distinct from `high`.

The post-RC13 Overview and Intelligence filter UI emits only these canonical values. Severity filtering is analytical/read-side behavior; it does not establish a Normenkader IBP, MITRE ATT&CK or other framework mapping.

## POST `/api/v1/intelligence`

Requires the governed intelligence-ingest/review authority defined by the current RBAC policy.

The route:

1. validates the request;
2. serializes the complete raw payload;
3. stores raw evidence in the Intelligence Lake;
4. creates the evidence checksum/receipt;
5. persists normalized candidate intelligence and provenance;
6. indexes the derived search representation in OpenSearch;
7. reports success only after the canonical database transaction lifecycle completes.

### Example payload

```json
{
  "source_id": "cisa-kev",
  "external_id": "CVE-2026-0001",
  "item_type": "vulnerability",
  "title": "Example vulnerability",
  "summary": "Example normalized summary",
  "canonical_url": "https://example.org/advisory",
  "severity": "high",
  "confidence": 90,
  "education_relevance": 80,
  "tags": ["kev", "education"],
  "provenance": [
    {
      "source_url": "https://example.org/advisory",
      "publisher": "Example publisher",
      "confidence": 90
    }
  ],
  "raw_payload": {"cve": "CVE-2026-0001"}
}
```

### Response properties

- `id` — canonical intelligence UUID;
- `inserted` — whether a new canonical record was inserted;
- `review_status` — governed review state;
- `share_approved` — remains false after ingestion unless separately approved through the governed human process;
- `raw_object_key` — raw evidence object path;
- `raw_sha256` — checksum of the raw evidence object;
- `indexed` — whether the supporting OpenSearch representation was written.

An indexing failure does not erase the raw evidence or canonical PostgreSQL record.

## GET `/api/v1/console/recent-intelligence`

Requires `read:intelligence`.

Purpose: return recent canonical PostgreSQL intelligence independently of the OpenSearch search path.

Query parameters:

- `limit` — 1–100, default 20;
- `severity` — optional typed canonical severity value.

Examples:

```text
/api/v1/console/recent-intelligence?limit=20
/api/v1/console/recent-intelligence?limit=20&severity=high
```

When `severity` is supplied, the canonical PostgreSQL query applies that severity before ordering/limiting. Invalid severity values are rejected by the typed read contract rather than silently broadened.

## GET `/api/v1/dashboards/summary`

Requires `read:intelligence`.

Purpose: return the canonical Overview intelligence aggregation.

Query parameter:

- `severity` — optional typed canonical severity value.

When filtered, the same PostgreSQL severity predicate applies to:

- `total_intelligence`;
- `new_last_24h`;
- `average_confidence`;
- `severity` distribution;
- `review_status` distribution;
- `sources` distribution;
- `intelligence_trend_7d`.

`connector_health` is deliberately **not** severity-filtered because it describes operational connector state rather than intelligence records. The response exposes `connector_health_filter_scope: operational-unfiltered` to make that distinction explicit.

The response also exposes the active `severity_filter` and the canonical `severity_values` list.

## GET `/api/v1/intelligence/search`

Requires `read:intelligence`.

This remains the governed OpenSearch-backed analyst search endpoint. The post-RC13 UI reuses it rather than introducing a parallel search mechanism.

Query parameters:

- `q` — required full-text query;
- `severity` — optional exact severity filter;
- `minimum_relevance` — 0–100;
- `size` — 1–200.

Example:

```text
/api/v1/intelligence/search?q=PaperCut&severity=high&minimum_relevance=60
```

The existing search route accepts the severity string and forwards it as an exact OpenSearch term filter. The shared console UI only emits canonical severity values.

## Shared UI filter behavior

Overview and Intelligence use one session-scoped severity preference.

A filter change composes three existing read paths:

1. dashboard summary;
2. recent canonical intelligence;
3. existing governed search when a query is active.

The default `Alle severities` state sends no severity query parameter and preserves the accepted RC13 refresh/empty-state lifecycle.

Filtered empty results are represented explicitly. No fallback to unrelated severities occurs.

## Framework mapping boundary

Severity is not a framework crosswalk.

The current Governance Mapping Registry remains authoritative. Normenkader IBP and MITRE ATT&CK remain `UNMAPPED`, and CVSS remains `CONTEXT_ONLY`, until first-class provenance-backed mappings/fields are implemented and reviewed.

## Failure behavior

Depending on endpoint and authentication mode, relevant failures include:

- `400` — invalid request semantics where explicitly handled;
- `401` — failed authentication;
- `403` — authenticated principal lacks required permission;
- `422` — typed query/request validation failure, including invalid severity on typed canonical read endpoints;
- `503` — required backend such as search is unavailable.

No error path may silently broaden a requested severity filter or grant publication authority.

## Production requirements

Production deployment requires the accepted Phase 8/9/10 evidence path, including:

- approved production identity and least privilege;
- TLS/network restrictions;
- approved secret-management paths;
- restricted persistence/search/object-store access;
- audit/correlation retention;
- deployment-specific security review;
- independent assurance and formal production go/no-go.
