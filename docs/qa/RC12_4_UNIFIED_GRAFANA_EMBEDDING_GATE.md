# RC12.4 Unified Grafana Embedding Gate

Status: PENDING_CI

## Objective

Keep DTMO as a single operator-facing application shell while using Grafana as the production dashboard engine.

## Acceptance criteria

- The canonical DTMO unified console remains the operator entry point.
- The analytics view embeds both provisioned dashboards: DTMO Operations and DTMO Intelligence.
- Operators are not redirected to a separate Grafana URL as part of normal dashboard navigation.
- Grafana anonymous access remains disabled.
- Grafana embedding remains explicitly enabled in the self-hosted service.
- Grafana authentication remains independent; this slice does not weaken or bypass Grafana authentication.
- Existing native dashboard-summary visualisations remain present as a governed fallback and accessible table-backed summary surface.
- No new database privileges or datasource privileges are introduced by this slice.

## Evidence

- `backend/dtmo/unified_console.py`
- `backend/tests/test_rc12_4_unified_grafana_embedding.py`
- `docker-compose.yml`
- provisioned dashboards from RC12.2/RC12.3

## Release gate

Do not mark PASS or merge until the complete exact-head GitHub Actions workflow set is green.
