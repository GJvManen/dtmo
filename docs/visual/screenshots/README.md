# DTMO Product Screenshot Catalogue

**Status:** capture pipeline in preparation  
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
- Capture command: `python3 tools/capture_documentation_screenshots.py --base-url <running-dtmo-url> --output docs/visual/screenshots/generated`

The output directory is intentionally separate from the governed catalogue until a capture has been reviewed for secrets, personal data, visual correctness and lifecycle labelling.

## Catalogue

| ID | Product surface | Target image | Current state | Required label |
|---|---|---|---|---|
| UI-01 | Overview / executive dashboard | `overview-dashboard.png` | capture pending | runtime UI with synthetic fixture data |
| UI-02 | Intelligence workspace | `intelligence-workspace.png` | capture pending | runtime UI with synthetic fixture data |
| UI-03 | Sources & Catalogue | `sources-catalogue.png` | capture pending | runtime UI with synthetic fixture data |
| UI-04 | Vulnerability analytics | `vulnerability-analytics.png` | capture pending | runtime UI with synthetic fixture data |
| UI-05 | MISP governed workflow | `misp-governed-workflow.png` | capture pending | runtime UI with synthetic fixture data |
| UI-06 | AIL correlation workspace | `ail-correlation-workspace.png` | capture pending | runtime UI with synthetic fixture data |
| UI-07 | Visual Analytics | `visual-analytics.png` | capture pending | runtime UI with synthetic fixture data |
| UI-08 | Governance frameworks | `governance-frameworks.png` | capture pending | runtime UI with synthetic fixture data |
| UI-09 | Administration / RBAC | `administration-rbac.png` | capture pending | runtime UI with synthetic fixture data |
| UI-10 | Audit / correlation surface | `audit-correlation.png` | capture pending | runtime UI with synthetic fixture data |

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

## Claim boundary

A screenshot can demonstrate what a rendered DTMO product surface looks like. It does not establish that an external feed was reachable, that a vulnerability applies to a local asset, that an outbound share was authorized, that a deployment passed staging, that a penetration test was accepted or that production deployment is approved.

See also `docs/visual/DOCUMENTATION_VISUAL_STANDARD.md` and `docs/architecture/SYSTEM_WORKFLOWS.md`.
