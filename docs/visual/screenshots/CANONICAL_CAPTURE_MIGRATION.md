# Canonical Workbench Screenshot Migration

## Status

`IN PROGRESS — generated / review required before promotion`

The governed UI-01–UI-10 catalogue contains historically reviewed documentation images, but the current product architecture uses the canonical `/workbench/*` application. Historical published images are not silently relabelled as current canonical UI.

## Canonical Command Center replacement candidate

The UI-01 migration introduced an artifact candidate named `command-center-workbench.png` captured from the exact canonical route `/workbench/command-center` in Chromium/Playwright.

The candidate uses the real current DTMO frontend with sanitized deterministic API fixture data. Its capture metadata records:

- `canonical_route = /workbench/command-center`;
- `capture_mode = actual-runtime-ui-with-synthetic-fixture-data`;
- `evidence_classification = documentation-illustration-only`;
- `live_connectivity_proven = false`;
- `owner_acceptance_proven = false`;
- `production_equivalent_proven = false`.

The candidate **must not replace `overview-dashboard.png` until** its exact-head screenshot artifact has completed the governed visual-review and promotion path. The reviewed source artifact is governed by the separate screenshot-promotion mechanism introduced after capture. Promotion remains exact-run, exact-head, artifact-digest and image-digest bound and cannot auto-merge.

## Canonical Threat Intelligence replacement candidate

This slice adds the independent UI-02 candidate `threat-intelligence-workbench.png` from the actual canonical route `/workbench/intelligence`.

The capture deliberately exercises a useful read-only operator journey rather than a heading-only state:

`recent canonical intelligence -> object detail -> provenance chain`

It uses sanitized deterministic canonical intelligence and provenance fixtures. The fixture contains no production credentials, personal data or live-source assertions. The metadata preserves these boundaries:

- `canonical_route = /workbench/intelligence`;
- `capture_mode = actual-runtime-ui-with-synthetic-fixture-data`;
- `evidence_classification = documentation-illustration-only`;
- `live_connectivity_proven = false`;
- `owner_acceptance_proven = false`;
- `production_equivalent_proven = false`;
- `review_authority_proven = false`;
- `share_authority_proven = false`.

The candidate **must not replace `intelligence-workspace.png` until** its exact-head screenshot artifact has been visually reviewed for current navigation, complete detail/provenance rendering, absence of transient/error state, safe disclosure and representative operator context. Review and promotion are separate bounded changes.

## Migration rule

Each remaining published screenshot is migrated independently to an attributable `/workbench/*` route. Legacy console navigation is not accepted as proof that a screenshot represents the current canonical product. Existing historical review records remain intact until their images are explicitly superseded.

Repository screenshot CI and fixture-backed Chromium rendering are engineering/documentation evidence only. They do not establish live external connectivity, clean-install owner acceptance, staging acceptance, production-equivalent behavior, penetration-test evidence, independent assurance or production authorization.
