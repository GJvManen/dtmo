# Administration bundled Grafana readiness recovery

## Objective

Make bundled Grafana discoverable and diagnosable from canonical Administration without weakening authentication or introducing a separate browser credential path.

## Scope

- mount a bundled platform-readiness surface in `/workbench/administration`;
- expose Grafana as part of the supported bundled Compose topology without issuing an unsolicited health request when Administration loads;
- let an authorized operator explicitly run `Check Grafana` through the supported same-origin `/grafana/api/health` gateway path;
- distinguish reachable, authentication-required and unavailable states after that explicit observation;
- expose direct same-origin pivots to the provisioned `DTMO Operations` and `DTMO Intelligence` dashboards;
- preserve Grafana anonymous-access disablement and separate authenticated-session requirements.

The default `not-checked` state is intentional. A DTMO process running without the bundled gateway/Grafana topology must still render Administration cleanly instead of manufacturing browser 404 errors or claiming that Grafana was observed. An explicit operator check is the boundary that converts configured topology into a runtime reachability observation.

## Evidence boundary

This slice proves repository product wiring and exact-head contracts only. A successful explicit health response is component reachability evidence, not proof that telemetry is complete, dashboards contain current operational data, production-equivalent behavior is validated, or production is authorized. A `not-checked` or unavailable state is never promoted to health evidence.

## Security boundary

No anonymous Grafana access, static browser credential, auth-proxy bypass or privilege broadening is introduced. Existing server-side DTMO RBAC and separate Grafana authentication remain authoritative.
