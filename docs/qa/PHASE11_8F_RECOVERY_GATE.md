# Phase 11.8f — Backup, restore and recovery gate

## Acceptance criteria

- PostgreSQL, Redis, OpenSearch and object storage are explicit recovery domains;
- each domain requires an accountable owner, backup method, retention, restore procedure and exercise cadence;
- RPO/RTO are explicit deployment-owned targets, not inferred repository claims;
- restore verification is mandatory and backup-job success alone is insufficient;
- recovery evidence preserves provenance and excludes secrets/restricted payloads;
- missing recovery evidence fails closed for later production-equivalent validation;
- documentation includes architecture, operations, rollback and non-claims.

## Repository evidence

The exact-head gate validates this contract and professional documentation. Shared regressions must remain green.

## Non-claims

Repository CI does not prove successful live backups, point-in-time recovery, achieved RPO/RTO, provider durability, disaster failover, production-equivalent behavior, independent assurance or production authorization.
