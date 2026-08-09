# RC10.8 Operational Dashboard Gate

## Decision

`CI_VALIDATION_PENDING`

## Objective

Validate a bounded, read-only operational dashboard over existing DTMO Prometheus telemetry without exposing sensitive request data, introducing production credentials or granting publication authority.

## Required exact-head evidence

Acceptance requires all of the following on one final PR head:

- non-editable provisioned Prometheus datasource and dashboard provider;
- dashboard covers HTTP rate/latency/in-flight, API alert, connector alert/outcome, queue utilization, storage-integrity alert, search-health alert and bounded trace-context signals;
- raw request/response bodies, raw URLs/query strings, credentials, identities, object keys and checksums are excluded from dashboard queries/configuration;
- anonymous access, self-signup and org creation are disabled in the local overlay;
- local Grafana port is loopback-only;
- Grafana runtime image fails closed to an externally supplied supported security-patched tag plus sha256 digest;
- administrative credentials are externally supplied and not stored in source;
- no-new-privileges is enabled;
- RBAC, separation of duties, provenance and human share approval are unchanged;
- dedicated `RC10 Operational Dashboard Gate` succeeds and retains exact-head JUnit/log/JSON evidence;
- every registered workflow succeeds on the exact final head.

## Security/vendor boundary

First-party Grafana advisories reviewed for this run include CVE-2026-27876, CVE-2026-28383 and CVE-2026-21721. The repository therefore does not claim any fixed Grafana tag is currently safe; deployment must select a supported security-patched release, verify the image digest and repeat advisory review at deployment time.

## Claim boundary

This gate does not claim production Grafana deployment, production TLS/network controls, SSO/RBAC integration, runbook completion, on-call handover, Phase 7 completion, Phase 6 assistive-technology completion or any issue #1 external production gate.

## Exactly one next priority

Accept only after complete exact-head workflow success and independent retained-artifact inspection.
