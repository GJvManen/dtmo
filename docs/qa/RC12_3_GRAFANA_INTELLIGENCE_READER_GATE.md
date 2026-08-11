# RC12.3 — Grafana Intelligence Reader Gate

Status: **PENDING_CI**

## Objective

Expose bounded DTMO intelligence and connector-health analytics to Grafana without granting Grafana the DTMO application database identity or direct access to public application tables.

## Security boundary

- Grafana uses the dedicated PostgreSQL login `dtmo_grafana_reader`.
- The reader password is supplied only through `GRAFANA_DB_PASSWORD` at runtime.
- The role is provisioned as `NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION`.
- Direct privileges on schema `public` are revoked for the reader.
- The reader receives `USAGE` only on `dtmo_reporting` and `SELECT` only on the two explicit reporting views.
- Reporting views omit titles, summaries, canonical URLs, metadata JSON, tags, provenance passages, raw evidence, audit records, privacy records and quarantine evidence.
- Grafana dashboard SQL must reference only `dtmo_reporting.*`.
- The existing Prometheus datasource remains independent and default.
- Grafana anonymous access remains disabled.

## Reporting views

`dtmo_reporting.intelligence_items_safe` exposes only:

- `discovered_at`
- `source_id`
- `severity`
- `review_status`
- `confidence_score`
- `education_relevance`

`dtmo_reporting.connector_health_safe` exposes only:

- `connector_id`
- `last_success_at`
- `last_failure_at`
- `consecutive_failures`
- `health_status`
- `updated_at`

## Dashboard evidence

The version-controlled `DTMO Intelligence` dashboard provides:

- intelligence count for selected time range;
- average confidence;
- intelligence trend;
- severity distribution;
- top sources;
- review status;
- connector-health distribution.

## Acceptance criteria

1. Alembic upgrade creates the reporting schema and both safe views.
2. Alembic downgrade removes both views and the reporting schema cleanly.
3. Runtime provisioning fails closed when `GRAFANA_DB_PASSWORD` is absent or shorter than 20 characters.
4. Grafana startup depends on successful reader provisioning.
5. The PostgreSQL datasource uses `dtmo_grafana_reader`, is non-default and non-editable, and obtains its password from Grafana environment substitution.
6. No Grafana dashboard query references `public.*`, raw evidence, provenance records or metadata JSON.
7. Existing Prometheus/Grafana operations dashboard behaviour remains unchanged.
8. RC4 Quality Gate and the complete exact-head workflow set are `completed/success`.

## Release decision

Do not mark this gate PASS and do not merge the PR until all acceptance criteria have exact-head evidence. Until then the release decision is **PENDING_CI**.
