# Canonical Collection built-in bootstrap recovery

## Objective

Restore the clean-install path from canonical `Sources & Collection` to useful intelligence without sending operators back to a legacy UI and without auto-enabling external connectivity.

## Verified integration defect

`CISA Known Exploited Vulnerabilities` is already a DTMO `supported-built-in` source. The server-side Source Center reports its runtime health and whether an explicit manual run is permitted. In non-production, a human admin can perform that bounded manual run through the existing `/connectors/cisa-kev/run` route; in production the existing governed live-connector deployment switch remains authoritative.

The canonical `CollectionWorkspace` previously ignored that built-in runtime model. It treated every catalog item absent from the registry as `not registered` and instructed the operator to bootstrap it. Catalog bootstrap intentionally registers registry-based source definitions only, so the built-in CISA KEV path could never become actionable from the canonical interface even though the legacy Source Center already exposed it.

## Recovery

The canonical workspace now:

- reads `/api/v1/source-center/status` through the same-origin DTMO boundary;
- distinguishes `supported-built-in` entries from registry-based sources;
- shows actual built-in manual-run readiness and health instead of `not registered`;
- exposes an explicit `Load CISA KEV now` operator action through the existing governed server-side connector route;
- refreshes runtime status after a run;
- keeps registry bootstrap, manual source registration and activation behavior unchanged.

## Security and authority boundaries

This change does not set `feature_live_connectors` from the browser and does not auto-enable any source. Production continues to require the governed live-connector deployment switch before a built-in manual run is exposed as available. Credentials remain server-side, RBAC remains authoritative and all collection retains the existing provenance, review and separate sharing/publication authority boundaries.

A successful CISA KEV run proves only the recorded attributable collection and resulting persisted state. It does not prove local exploitation, compromise, remediation state, production readiness or publication authorization.

## Acceptance boundary

Repository CI proves the canonical wiring and preservation of the server-side readiness boundary. Live upstream retrieval is intentionally not fabricated or route-mocked in repository browser acceptance. Workflow startup or scheduler state is infrastructure evidence only and must not be interpreted as product acceptance or rejection without an executed job and attributable assertion or runtime result. The next external owner functional retest must prove the real clean-install operator sequence against the supported runtime: open `Sources & Collection`, select CISA KEV, observe manual-load readiness, run the feed, then verify resulting intelligence through the canonical downstream workspaces.
