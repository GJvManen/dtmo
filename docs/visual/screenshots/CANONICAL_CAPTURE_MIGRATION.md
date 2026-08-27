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

The UI-02 migration adds the independent candidate `threat-intelligence-workbench.png` from the actual canonical route `/workbench/intelligence`.

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

## Canonical Sources & Collection replacement candidate

The UI-03 migration adds the independent candidate `sources-collection-workbench.png` from the actual canonical route `/workbench/collection`.

The capture exercises a bounded inspection journey without triggering connector execution or source activation:

`source catalog -> built-in readiness -> provenance boundary`

It uses the real Collection workspace with sanitized deterministic catalog, source-registry and source-center fixtures. A public source identity may be displayed as provenance context, but no upstream call is made and no credential value is exposed. The metadata preserves these boundaries:

- `canonical_route = /workbench/collection`;
- `capture_mode = actual-runtime-ui-with-synthetic-fixture-data`;
- `evidence_classification = documentation-illustration-only`;
- `live_connectivity_proven = false`;
- `owner_acceptance_proven = false`;
- `production_equivalent_proven = false`;
- `connector_execution_proven = false`;
- `source_activation_authority_proven = false`;
- `publication_authority_proven = false`;
- `credential_value_exposed = false`.

The candidate **must not replace `sources-catalogue.png` until** its exact-head screenshot artifact has been visually reviewed for canonical navigation, source/readiness rendering, provenance context, absence of transient/error state, safe disclosure and representative operator context. Review and promotion are separate bounded changes.

## Canonical Vulnerability & Exposure replacement candidate

The UI-04 migration adds the independent candidate `vulnerability-exposure-workbench.png` from the actual canonical route `/workbench/exposure`.

The capture exercises a bounded read-only prioritization journey:

`vulnerability evidence -> prioritization attributes -> provenance boundary`

It uses the real Vulnerability & Exposure Center with sanitized deterministic CVSS, EPSS, KEV, vendor, product, CWE and provenance fixtures. These attributes are prioritization evidence only. They do not establish local exposure and do not establish that a local asset is affected, reachable, exploitable, compromised or remediated. The capture grants no scanner, publication or sharing authority. The metadata preserves these boundaries:

- `canonical_route = /workbench/exposure`;
- `capture_mode = actual-runtime-ui-with-synthetic-fixture-data`;
- `evidence_classification = documentation-illustration-only`;
- `live_connectivity_proven = false`;
- `owner_acceptance_proven = false`;
- `production_equivalent_proven = false`;
- `local_exposure_proven = false`;
- `exploitability_proven = false`;
- `compromise_proven = false`;
- `remediation_proven = false`;
- `scanner_authority_proven = false`;
- `publication_authority_proven = false`;
- `share_authority_proven = false`.

The candidate **must not replace `vulnerability-analytics.png` until** its exact-head screenshot artifact has been visually reviewed for canonical navigation, complete CVSS/EPSS/KEV and provenance rendering, absence of transient/error state, safe disclosure and representative operator context. Review and promotion are separate bounded changes.

## Canonical Sharing & Exchange replacement candidate

The UI-05 migration adds the independent candidate `sharing-exchange-workbench.png` from the actual canonical route `/workbench/sharing`.

The capture renders the governed decision and evidence chain without performing a mutation:

`independent review -> separate share approval -> unpublished MISP export evidence -> authority boundary`

It uses the real Sharing & Exchange workspace with sanitized deterministic canonical-intelligence, restriction and persisted export-history fixtures. The fixture shows that independent review and separate share approval are distinct human authority steps and that any MISP export evidence remains unpublished. No review, approval or export action is executed by the capture itself. **publication authority** and synchronization authority remain absent. The metadata preserves these boundaries:

- `canonical_route = /workbench/sharing`;
- `capture_mode = actual-runtime-ui-with-synthetic-fixture-data`;
- `evidence_classification = documentation-illustration-only`;
- `live_connectivity_proven = false`;
- `owner_acceptance_proven = false`;
- `production_equivalent_proven = false`;
- `human_review_executed = false`;
- `share_approval_executed = false`;
- `misp_export_executed = false`;
- `publication_authority_proven = false`;
- `synchronization_authority_proven = false`;
- `credential_value_exposed = false`.

The candidate **must not replace `misp-governed-workflow.png` until** its exact-head screenshot artifact has been visually reviewed for canonical navigation, independent review/separate approval rendering, unpublished export evidence, handling restrictions, replay evidence, authority boundaries, absence of transient/error state and safe disclosure. Review and promotion are separate bounded changes.

## Migration rule

Each remaining published screenshot is migrated independently to an attributable `/workbench/*` route. Legacy console navigation is not accepted as proof that a screenshot represents the current canonical product. Existing historical review records remain intact until their images are explicitly superseded.

Repository screenshot CI and fixture-backed Chromium rendering are engineering/documentation evidence only. They do not establish live external connectivity, clean-install owner acceptance, staging acceptance, production-equivalent behavior, penetration-test evidence, independent assurance or production authorization.
