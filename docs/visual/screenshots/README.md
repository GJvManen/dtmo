# DTMO Product Screenshot Catalogue

**Status:** base runtime capture validated; governed image promotion in progress  
**Screenshot type:** actual DTMO runtime UI with sanitized deterministic fixtures unless a record explicitly states otherwise  
**Evidence classification:** documentation illustration only — not staging acceptance, independent assurance or production evidence

## Capture policy

Screenshots in this directory must come from the real DTMO web application rendered in a supported browser. The documentation capture runner may intercept API calls with synthetic fixtures so that images are deterministic, free from production data and safe to publish in repository documentation.

Synthetic API fixtures do **not** turn a screenshot into a mock-up: the HTML/CSS/JavaScript and interaction surface are the actual DTMO application. However, fixture-backed screenshots must always be described as **runtime UI with synthetic fixture data** and must never be presented as proof of live-source connectivity or production-equivalent deployment behavior.

## Standard capture context

- Browser: Chromium through Playwright
- Viewport: 1440 × 1000 unless a specific responsive example says otherwise
- Data: sanitized synthetic fixture data
- Credentials: no production credentials; documentation-only test identity
- External network calls: blocked or intercepted where practical
- Output: PNG
- Base capture command: `python3 tools/capture_documentation_screenshots.py --base-url <running-dtmo-url> --output docs/visual/screenshots/generated`
- Investigation capture command: `python3 tools/capture_documentation_investigation_screenshots.py --base-url <running-dtmo-url> --output docs/visual/screenshots/generated`

The output directory is intentionally separate from the governed catalogue until a capture has been reviewed for secrets, personal data, visual correctness and lifecycle labelling.

## Validated base capture

The base screenshot pipeline was exercised successfully in the **Documentation Screenshot Artifact Gate** for the visual-documentation baseline merged through PR #250. The generated artifact contained the seven currently renderable base product views listed below. The capture proves that these DTMO UI surfaces can be rendered deterministically with the documentation fixtures; it does not establish staging or production behavior.

| ID | Product surface | Target image | Current state | Required label |
|---|---|---|---|---|
| UI-01 | Overview / executive dashboard | `overview-dashboard.png` | capture validated; repository promotion pending | runtime UI with synthetic fixture data |
| UI-02 | Intelligence workspace | `intelligence-workspace.png` | capture validated; repository promotion pending | runtime UI with synthetic fixture data |
| UI-03 | Sources & Catalogue | `sources-catalogue.png` | capture validated; repository promotion pending | runtime UI with synthetic fixture data |
| UI-04 | Vulnerability analytics | `vulnerability-analytics.png` | capture validated; repository promotion pending | runtime UI with synthetic fixture data |
| UI-05 | MISP governed workflow | `misp-governed-workflow.png` | dedicated runtime screenshot pending | runtime UI with synthetic fixture data |
| UI-06 | AIL correlation workspace | `ail-correlation-workspace.png` | capture contract added; exact-head CI validation pending | runtime UI with synthetic fixture data |
| UI-07 | Visual Analytics | `visual-analytics.png` | capture validated; repository promotion pending | runtime UI with synthetic fixture data |
| UI-08 | Governance frameworks | `governance-frameworks.png` | capture validated; repository promotion pending | runtime UI with synthetic fixture data |
| UI-09 | Administration / RBAC | `administration-rbac.png` | capture validated; repository promotion pending | runtime UI with synthetic fixture data |
| UI-10 | Audit / correlation surface | `audit-correlation.png` | dedicated runtime screenshot pending | runtime UI with synthetic fixture data |

## Dedicated MISP, AIL and audit captures

A diagram or API contract must never be promoted as a product screenshot. AIL has a dedicated runtime correlation panel in the Intelligence Workspace; this branch adds a deterministic capture for that actual surface and keeps its status pending until exact-head CI succeeds. MISP and audit/correlation remain pending until the capture implementation identifies the actual rendered governed surface rather than manufacturing a conceptual screen.

The AIL capture follows the same user journey as the dedicated E8 browser test: query an indicator, open the governed intelligence record and render `#ail-correlation-panel`. Its synthetic fixture explicitly records `raw_content_exposed = false` and includes MISP/vulnerability correlations only as analytical context.

## Review record required before publication

For each image promoted from `generated/` into this governed catalogue, record:

- image ID and filename;
- captured commit/release;
- capture date;
- browser and viewport;
- capture mode (`synthetic-fixture`, `local-demo`, `production-equivalent-staging`, or `historical`);
- reviewer;
- confirmation that no raw token, secret, personal data or restricted operational identifier is visible;
- any redaction performed;
- whether the image remains representative of the current navigation and interaction model.

## Review quality criteria

A promoted image should be legible at normal documentation zoom, show the relevant navigation context, avoid accidental empty/error states unless that state is the subject of the image, and contain no secret, token or unnecessary personal data. Full-page captures may be resized or losslessly/visually optimized for repository delivery as long as the UI content is not altered.

## Claim boundary

A screenshot can demonstrate what a rendered DTMO product surface looks like. It does not establish that an external feed was reachable, that a vulnerability applies to a local asset, that an outbound share was authorized, that a deployment passed staging, that a penetration test was accepted or that production deployment is approved.

See also `docs/visual/DOCUMENTATION_VISUAL_STANDARD.md`, `docs/architecture/SYSTEM_WORKFLOWS.md`, `docs/product/PRODUCT_GUIDE.md`, `docs/user/USER_GUIDE.md` and `docs/administration/ADMINISTRATOR_GUIDE.md`.
