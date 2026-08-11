# RC10.10 Graphical Dashboard Gate

## Decision

`PENDING_CI`

## Objective

Provide real-data graphical intelligence and connector-health dashboards without introducing synthetic production values, weakening RBAC or removing accessible non-graphical alternatives.

## Implementation scope

- Read-only dashboard summary endpoint protected by `read:intelligence`.
- Intelligence KPIs: total items, new items in the last 24 hours and average confidence.
- Aggregations by severity, review status and source.
- Connector runtime health aggregation.
- Browser-rendered SVG bar charts driven only by backend API values.
- Accessible HTML table alternative for every graph.
- Live loading/error status and manual refresh.
- Direct navigation to Source Center and Operations.
- No review, publication or share-approval mutation paths in the dashboard.

## Required evidence before PASS

1. Exact-head CI succeeds for every registered required workflow.
2. RC10.10 regression tests pass.
3. Dashboard endpoint returns only bounded aggregate data.
4. Browser/static evidence proves SVG visualizations are driven by `/api/v1/dashboards/summary`.
5. Every graph has a semantic table/text alternative.
6. Read-only governance and publication separation remain intact.
7. Retained CI evidence is bound to the accepted exact head and independently inspected.

## Claim boundary

This gate does not claim production Grafana deployment, historical time-series retention, production staging, external accessibility acceptance, external assurance or production go/no-go.

## Dependency

RC10.10 is stacked on RC10.9 until the feed-operations PR is accepted and merged.

## Next priority after PASS

Reconcile RC10.9/RC10.10 documentation and then resume Phase 8 real staging deployment parity against the operator-complete build.
