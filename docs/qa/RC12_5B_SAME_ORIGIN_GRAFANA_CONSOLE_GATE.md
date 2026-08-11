# RC12.5b — Same-origin Grafana console gate

## Objective

Complete the same-origin browser integration by switching the unified DTMO console from the compatibility Grafana port to the managed `/grafana/` subpath introduced by RC12.5a.

## Scope

- use relative `/grafana/...` dashboard URLs in the unified console
- remove browser-facing `:3000` references from the console
- retain Grafana authentication and anonymous-access restrictions
- retain native DTMO fallback charts and table equivalents

## Acceptance criteria

1. The unified console contains no browser-facing `:3000` Grafana target.
2. Operations and Intelligence dashboards resolve through `/grafana/`.
3. Native severity, source and connector fallback visualisations and tables remain present.
4. RC4 Quality and all release-critical exact-head workflows pass.

## Release status

`PENDING_CI`
