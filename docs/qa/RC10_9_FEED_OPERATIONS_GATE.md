# RC10.9 Feed Operations Gate

## Decision

`PENDING_CI`

## Objective

Make code-reviewed executable framework feeds discoverable and operable from the DTMO Source Center without weakening connector isolation, RBAC, audit, provenance or publication controls.

## Implementation scope

- Source Center status reconciles the executable source catalog with registered sources and runtime state.
- Built-in CISA KEV remains on its existing execution path.
- Supported registry feeds use the existing safe registered-source executor.
- Supported catalog feeds can be idempotently bootstrapped from the Source Center.
- Registered feeds can be explicitly enabled/disabled by a human admin.
- Enabled feeds can be manually run from the Source Center with visible result counts and error state.
- Every mutating request supplies a unique `X-Request-ID`.
- Existing `manage:connectors`, human-admin, isolation, audit and provenance controls remain authoritative.
- Ingestion does not grant review or external share approval authority.

## Required evidence before PASS

1. Exact-head CI succeeds for all registered required workflows.
2. RC10.9 regression tests pass.
3. Browser/static evidence proves Source Center exposes bootstrap, enable/disable and manual-run controls.
4. Backend evidence proves the UI only calls existing governed execution routes.
5. Failed/disabled/isolated sources remain fail-closed.
6. Publication authority remains separate and no credentials/raw evidence are exposed in the page.
7. Retained CI artifact is bound to the accepted exact head and independently inspected.

## Claim boundary

This gate does not claim that planned-parser catalog sources are executable. It does not claim production staging, production credentials, external accessibility acceptance, graphical dashboard completion, external assurance or production go/no-go.

## Next priority after PASS

RC10.10 — graphical intelligence and operations dashboards driven by real backend telemetry/intelligence data with accessible table/text alternatives.
