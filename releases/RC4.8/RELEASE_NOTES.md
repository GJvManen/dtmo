# DTMO RC4.8

RC4.8 integrates the staged RC4 implementation work from RC4.1 through RC4.8.

## Delivered by sprint

### RC4.1 — Platform foundation

- FastAPI service foundation;
- typed configuration and feature flags;
- structured logging and metrics;
- scheduler, Docker Compose and GitHub Actions.

### RC4.2 — Persistence

- SQLAlchemy models for intelligence, provenance and connector runs;
- deduplicating candidate-ingestion repository;
- explicit human share-approval invariant;
- connector run audit records.

### RC4.3 — Intelligence Lake

- immutable raw object landing;
- SHA-256 receipts;
- size and hash verification;
- source/date partitioning suitable for MinIO or S3.

### RC4.4 — Connector operations

- managed connector catalog;
- reliability and minimum-interval validation;
- connector health snapshots;
- failure-state visibility.

### RC4.5 — Knowledge graph

- evidence-backed node and relationship creation;
- confidence validation;
- bounded-depth attack-path queries;
- review status on candidate relationships.

### RC4.6 — SOC workspace

- responsive web workspace;
- executive, intelligence, vulnerability, IOC, graph, hunting and governance views;
- API-driven rendering;
- light/dark mode and mobile navigation.

### RC4.7 — Governance and reporting

- role-based permissions;
- separation of review and share approval;
- evidence-required reporting;
- JSON and CSV exports.

### RC4.8 — Integrated QA

- cross-sprint tests for raw data integrity, graph evidence, RBAC and reporting;
- formal release boundaries;
- external acceptance gates remain tracked in issue #1.

## Current release state

**CI VALIDATION PENDING**

The implementation and automated tests are committed. RC4.8 must not be marked `RC_READY` until the latest GitHub Actions workflow has completed successfully.

## Production boundary

The following remain external blockers:

- independent penetration test;
- representative load and stress test;
- backup and full-restore exercise;
- deployment acceptance;
- live connector credential, licence, rate-limit and terms validation;
- service-owner, CISO/ISO and privacy acceptance.
