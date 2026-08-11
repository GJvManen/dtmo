# RC12.2 — Grafana dashboarding release gate

Status: `PENDING_CI`

## Objective

Adopt self-hosted Grafana as the primary production-grade graphical dashboard engine for DTMO operations while preserving the unified-console governance boundary and keeping dashboard configuration version controlled.

## Accepted scope

- self-hosted Grafana 13.1.0 in the Compose topology;
- anonymous access disabled;
- non-default Grafana administrative credentials required outside source control;
- Prometheus provisioned as a read-only/default DTMO datasource;
- DTMO Operations dashboard provisioned from repository JSON;
- dashboard panels use aggregate Prometheus metrics only;
- existing `/api/v1/dashboards/summary` gains a bounded seven-day intelligence trend for the unified-console fallback/summary visualisation;
- existing publication, review and share-approval boundaries remain unchanged.

## Security boundary

This slice does **not** give Grafana access to the DTMO PostgreSQL application account. Grafana's PostgreSQL datasource documentation recommends a dedicated user with only `SELECT` permissions because dashboard users can otherwise issue arbitrary queries. Intelligence-data dashboards therefore require a separate least-privilege reader role and are deferred to RC12.3.

Anonymous/public dashboard access is disabled. No default Grafana password is committed. Grafana provisioning files and dashboard JSON are read-only mounts.

## Evidence required for PASS

1. exact-head RC4 Quality Gate is green;
2. all existing release-critical workflow gates are green;
3. `backend/tests/test_rc12_2_grafana_dashboarding.py` passes;
4. Compose configuration includes Grafana with fail-closed admin credential interpolation;
5. Prometheus datasource UID `dtmo-prometheus` is provisioned and non-editable;
6. dashboard UID `dtmo-operations` is provisioned from Git and non-editable;
7. dashboard queries contain no payload/object-key material;
8. no PostgreSQL datasource is introduced until a dedicated read-only role exists.

## Next slice

RC12.3: dedicated read-only PostgreSQL role + Grafana intelligence dashboards (severity, source, CVE/advisory trends, confidence and review-state analytics), followed by unified-console authenticated embedding/SSO integration.

Do not mark this gate PASS and do not merge the PR until the complete exact-head workflow set succeeds.
