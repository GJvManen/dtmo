# Administration bundled Grafana readiness recovery

## Objective

Make bundled Grafana discoverable and diagnosable from canonical Administration without weakening authentication or introducing a separate browser credential path.

## Scope

- mount a bundled platform-readiness surface in `/workbench/administration`;
- check Grafana through the supported same-origin `/grafana/api/health` gateway path;
- distinguish reachable, authentication-required and unavailable states;
- expose direct same-origin pivots to the provisioned `DTMO Operations` and `DTMO Intelligence` dashboards;
- preserve Grafana anonymous-access disablement and separate authenticated-session requirements.

## Evidence boundary

This slice proves repository product wiring and exact-head contracts only. A successful health response is component reachability evidence, not proof that telemetry is complete, dashboards contain current operational data, production-equivalent behavior is validated, or production is authorized.

## Security boundary

No anonymous Grafana access, static browser credential, auth-proxy bypass or privilege broadening is introduced. Existing server-side DTMO RBAC and separate Grafana authentication remain authoritative.
