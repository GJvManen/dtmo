# Canonical Workbench Screenshot Migration

## Status

`IN PROGRESS — generated / review required before promotion`

The governed UI-01–UI-10 catalogue contains historically reviewed documentation images, but the current product architecture uses the canonical `/workbench/*` application. Historical published images are not silently relabelled as current canonical UI.

## Canonical Command Center replacement candidate

This slice introduces an unreviewed artifact candidate named `command-center-workbench.png` captured from the exact canonical route `/workbench/command-center` in Chromium/Playwright.

The candidate uses the real current DTMO frontend with sanitized deterministic API fixture data. Its capture metadata must explicitly record:

- `canonical_route = /workbench/command-center`;
- `capture_mode = actual-runtime-ui-with-synthetic-fixture-data`;
- `evidence_classification = documentation-illustration-only`;
- `live_connectivity_proven = false`;
- `owner_acceptance_proven = false`;
- `production_equivalent_proven = false`.

The candidate **must not replace `overview-dashboard.png` until** the exact-head screenshot artifact has been visually reviewed for current navigation, complete rendering, absence of transient/error states, secret/personal-data exposure and representative interaction state. Promotion of a reviewed PNG is a separate bounded repository change with its source workflow run, artifact digest and image SHA-256 recorded in the governed catalogue.

## Migration rule

Each remaining published screenshot is migrated independently to an attributable `/workbench/*` route. Legacy console navigation is not accepted as proof that a screenshot represents the current canonical product. Existing historical review records remain intact until their images are explicitly superseded.

Repository screenshot CI and fixture-backed Chromium rendering are engineering/documentation evidence only. They do not establish live external connectivity, clean-install owner acceptance, staging acceptance, production-equivalent behavior, penetration-test evidence, independent assurance or production authorization.
