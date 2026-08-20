# Phase 11.9 Migration and Compatibility Architecture

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**

## Objective

Phase 11.9 defines the repository-controlled compatibility boundary between DTMO application revisions and the PostgreSQL schema migration chain before production-equivalent validation begins.

## Compatibility contract

DTMO requires one connected Alembic migration graph with exactly one root and one head. Every revision must declare a single predecessor and explicit `upgrade()` and `downgrade()` functions. The supported deployment direction is forward: schema migration is completed before application cutover.

A rolling application transition may temporarily contain the previous and candidate application revisions only when the schema change is backward-compatible for that bounded overlap. A migration that requires an immediate destructive schema change must use an explicit expand/migrate/contract sequence rather than relying on simultaneous application and schema replacement.

```mermaid
flowchart LR
    A[Accepted app + schema] --> E[Expand schema]
    E --> M[Migrate/verify data]
    M --> C[Candidate app cutover]
    C --> V[Compatibility verification]
    V --> K[Later contract cleanup]
```

## Rollback boundary

Application rollback does **not** authorize automatic database down migration. When a candidate application is rejected, the prior application revision may be restored only if the current schema remains compatible. Otherwise the change must fail closed and use the governed recovery procedure.

## Evidence boundary

The Phase 11.9 CI gate proves the repository migration graph is linear, connected and machine-readable and that migration files expose explicit upgrade/downgrade contracts. Existing database CI separately exercises Alembic migrations. This Phase 11.9 gate does **not** prove a live upgrade, live rollback, production data compatibility, production-equivalent behavior, independent assurance or production authorization. Those claims require Phase 11.10 and 11.11 evidence.
