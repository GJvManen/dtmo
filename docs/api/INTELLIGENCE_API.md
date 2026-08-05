# DTMO Intelligence API

## Purpose

The RC4.8 API connects three previously separate platform components:

1. PostgreSQL persistence for normalized intelligence and provenance;
2. MinIO/S3-compatible raw-object storage for immutable source payloads;
3. OpenSearch for analyst search and prioritisation.

All intelligence remains a `candidate` after ingestion. Ingestion does not grant review or external sharing approval.

## Authentication headers

| Header | Purpose |
|---|---|
| `X-DTMO-API-Key` | Shared service authentication key. Required when `DTMO_API_KEY` is configured and always required in production. |
| `X-DTMO-Subject` | Auditable subject identifier, for example an account or service name. |
| `X-DTMO-Roles` | Comma-separated DTMO roles, for example `soc,cert`. |
| `X-Correlation-ID` | Optional request identifier. DTMO generates one when omitted. |

The initial RC4.8 authentication mechanism is intended for a trusted reverse proxy or internal service mesh. It is not a replacement for an enterprise identity provider. Production deployment should terminate TLS before the API and inject authenticated subject and role headers only after identity validation.

## Roles and permissions

- `executive`: read intelligence and export reports;
- `ciso`: read, review and export;
- `soc`: read and review;
- `cert`: read, review and export;
- `privacy`: read, review and export;
- `auditor`: read intelligence and audit evidence;
- `admin`: all permissions, including separate share approval.

Review and share approval remain separate permissions.

## POST `/api/v1/intelligence`

Requires `review:intelligence`.

The route:

1. validates the request;
2. serializes the complete raw payload;
3. stores it in the Intelligence Lake;
4. creates a SHA-256 receipt;
5. persists normalized candidate intelligence and provenance;
6. attempts OpenSearch indexing;
7. returns indexing state without bypassing the database transaction or publication gate.

### Example

```bash
curl -X POST http://localhost:8000/api/v1/intelligence \
  -H 'Content-Type: application/json' \
  -H 'X-DTMO-API-Key: development-key' \
  -H 'X-DTMO-Subject: analyst@example.org' \
  -H 'X-DTMO-Roles: soc' \
  -d '{
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
    "provenance": [{
      "source_url": "https://example.org/advisory",
      "publisher": "Example publisher",
      "confidence": 90
    }],
    "raw_payload": {"cve": "CVE-2026-0001"}
  }'
```

### Response properties

- `id`: normalized intelligence UUID;
- `inserted`: false when source and external ID already exist;
- `review_status`: always starts as `candidate`;
- `share_approved`: always false after ingestion;
- `raw_object_key`: immutable lake object path;
- `raw_sha256`: checksum of the raw source object;
- `indexed`: whether OpenSearch indexing completed.

An OpenSearch failure is recorded in item metadata. It does not erase the raw object or normalized database record.

## GET `/api/v1/intelligence/search`

Requires `read:intelligence`.

Query parameters:

- `q`: required full-text query;
- `severity`: optional exact severity filter;
- `minimum_relevance`: 0–100;
- `size`: 1–200.

Example:

```bash
curl 'http://localhost:8000/api/v1/intelligence/search?q=PaperCut&minimum_relevance=60' \
  -H 'X-DTMO-API-Key: development-key' \
  -H 'X-DTMO-Subject: ciso@example.org' \
  -H 'X-DTMO-Roles: ciso'
```

## Failure behaviour

- `400`: invalid role or request field;
- `401`: invalid API key;
- `403`: authenticated principal lacks the required permission;
- `503`: authentication configuration or search backend unavailable.

## Production requirements

- API key of at least 32 characters;
- TLS at the ingress/reverse proxy;
- trusted identity and role injection;
- secret manager rather than plaintext environment files;
- restricted access to PostgreSQL, OpenSearch and MinIO;
- audit retention and correlation-ID logging;
- independent security and deployment acceptance.
