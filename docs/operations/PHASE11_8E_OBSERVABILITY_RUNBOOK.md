# Phase 11.8e — Observability operations runbook

## Preconditions

Confirm the accepted runtime revision, monitoring ownership, required CRDs/collectors, retention policy and access-control ownership before enabling any telemetry integration. Never place monitoring credentials in Helm values or Git.

## Enablement

1. Keep metrics, ServiceMonitor and tracing disabled until the deployment environment has approved collectors.
2. Enable metrics and then ServiceMonitor only when the Prometheus Operator CRD is present and the selected collector is authorized to scrape the namespace.
3. Configure OTLP only through deployment-owned configuration and secret delivery where authentication is required.
4. Confirm logs remain structured JSON and do not expose secrets, tokens or sensitive payload content.
5. Validate metric scrape health, log arrival and trace continuity in the deployment environment; store only non-sensitive evidence references.

## Failure handling

If a collector, CRD or telemetry endpoint is unavailable, keep or return the affected export path to disabled. Do not interpret missing telemetry as application health. Escalate gaps through the operational owner and preserve the distinction between application availability and observability availability.

## Rollback

Revert to the last accepted GitOps revision, disable ServiceMonitor and trace export, and verify application traffic remains independent of telemetry backends. Remove obsolete collector permissions or endpoint configuration. Do not use ad-hoc live edits as the authoritative rollback mechanism.

## Evidence boundary

Repository acceptance does not prove live ingestion, retention, alert delivery, SLO performance or production readiness. Those claims require later production-equivalent validation against the immutable integrated candidate.
