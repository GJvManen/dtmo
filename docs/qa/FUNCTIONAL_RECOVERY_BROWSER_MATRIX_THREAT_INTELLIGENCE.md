# Functional Recovery Browser Matrix — Threat Intelligence

## Status

`SEARCH/FILTER SLICE — EXACT-HEAD CI REQUIRED`

This matrix continues the owner-driven functional retest after PR #338 proved the canonical recent-intelligence, object-detail and downstream pivot journey against real temporary PostgreSQL persistence.

## Accepted repository-controlled journey

The canonical `/workbench/intelligence` recent/detail journey is exercised against the real built workbench and same-origin DTMO APIs without Playwright route interception. A visibly repository-controlled fixture is written to temporary PostgreSQL, rendered in **Recent canonical intelligence**, opened through `/api/v1/intelligence/{id}/workspace`, and removed after the run.

That journey verifies server-derived source, severity, confidence, education relevance, review/sharing state, Analysis & Enrichment and Sharing & Exchange pivots, and the absence of `/ui/*` compatibility links in the exercised path.

## Current bounded priority — real governed search/filter projection

The next acceptance contract exercises the user-visible search form without browser/API mocks. The test creates one unique repository-controlled intelligence object and a matching document in the configured DTMO search projection, then uses the real canonical UI to:

- submit a unique text query;
- apply the **high** severity filter;
- apply a minimum education relevance threshold;
- apply the maximum-result control;
- observe the matching result returned through `/api/v1/intelligence/search`;
- open the selected result through the real canonical object-detail endpoint;
- confirm the canonical object remains attributable to its persisted DTMO source;
- confirm no `/ui/*` compatibility path is required.

The search route is intentionally not replaced with a PostgreSQL-only browser mock. DTMO currently implements governed search through `OpenSearchService`; therefore the functional gate must either provide that repository-controlled dependency or fail with concrete evidence. A missing search dependency must not be misreported as an empty result set.

## Evidence boundary

All records and search documents used by this matrix are repository-controlled acceptance fixtures. They are not live threat intelligence, upstream-source evidence, source-health evidence, owner acceptance, staging evidence, production-equivalent validation, penetration-test evidence, production authorization or independent external assurance.

## Security and authority boundaries

The browser journeys are read-only investigation flows. They do not grant review, share approval, publication, analyzer execution, connector execution, case creation, remediation or external-assurance authority. Server-side RBAC, provenance, fail-closed behavior and credential boundaries remain authoritative. Search failure remains explicit and must not be converted into a false absence conclusion.

## Next after green

After real search/query/filter behavior is green on exact-head CI, continue the page-by-page matrix with IOC Explorer. If exact-head CI fails, fix only the verified search-projection/runtime root cause before adding another workspace.
