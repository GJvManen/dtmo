# RC12.5a — Same-origin Grafana gateway gate

## Objective

Prepare Grafana to run below the managed DTMO browser origin instead of requiring a separate browser origin on port 3000.

## Scope

- add a hardened Nginx gateway
- route `/` to the DTMO API/console
- route `/grafana/` to Grafana
- configure Grafana `root_url` for `/grafana/`
- enable `serve_from_sub_path`
- keep anonymous Grafana access disabled
- keep the current console iframe target unchanged until RC12.5b

## Security boundary

The gateway runs read-only with `no-new-privileges`. Grafana authentication remains enabled and independent. This gate does not introduce anonymous/public dashboards or relax the dedicated read-only PostgreSQL reporting boundary.

## Acceptance criteria

1. Compose validates with the gateway service present.
2. `/grafana/` is proxied only to the internal Grafana service.
3. `/` is proxied to the DTMO application service.
4. Grafana is configured for `/grafana/` subpath serving.
5. Anonymous Grafana access remains disabled.
6. RC4 Quality and all release-critical exact-head workflows pass.

## Follow-up

RC12.5b switches the unified console iframe URLs from the compatibility `:3000` target to relative `/grafana/...` URLs only after this infrastructure slice passes CI.

## Release status

`PENDING_CI`
