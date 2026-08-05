# ADR-0001 — Secured intelligence ingestion

- **Status:** Accepted for RC4.8 reference implementation
- **Date:** 2026-08-05

## Context

DTMO previously had separate persistence, raw-object storage and search modules. Without a single controlled orchestration route, integrations could bypass provenance, candidate review state or publication controls.

## Decision

A versioned FastAPI route orchestrates ingestion in this order:

1. authenticate the caller;
2. resolve roles and enforce `review:intelligence`;
3. validate normalized fields and at least one provenance record;
4. land the complete raw object in S3-compatible storage;
5. calculate and persist a SHA-256 receipt;
6. create a normalized PostgreSQL candidate record;
7. attach provenance and raw-object metadata;
8. index the normalized document in OpenSearch;
9. return a result that explicitly reports indexing success or failure.

The normalized record always starts as `candidate` and `share_approved=false`.

## Security boundaries

- API authentication is mandatory in production.
- Caller-provided roles are trusted only behind an authenticated reverse proxy or service mesh.
- Share approval is not exposed through the ingestion route.
- Search indexing failure does not remove source evidence.
- Raw payload storage precedes normalization to preserve lineage.

## Consequences

### Positive

- complete data lineage;
- consistent authorization;
- deterministic deduplication;
- recoverability after index failures;
- explicit separation between collection, review and publication.

### Negative

- the route depends on PostgreSQL and MinIO availability;
- OpenSearch is eventually consistent with persistence when indexing fails;
- a production identity-provider integration remains future work;
- compensating cleanup may be needed when raw landing succeeds but the database transaction fails.

## Follow-up decisions

- adopt OIDC or an identity-aware proxy;
- implement an outbox for reliable asynchronous OpenSearch indexing;
- add audit events for review and share approval;
- define raw-object retention and legal hold policies;
- add idempotency keys and request replay controls.
