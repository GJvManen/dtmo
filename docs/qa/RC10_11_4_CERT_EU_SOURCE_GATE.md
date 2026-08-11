# RC10.11.4 CERT-EU source gate

Status: `PENDING_CI`

## Objective

Make the curated CERT-EU security-advisory source executable from the unified DTMO console while preserving the existing egress, provenance, audit and publication-governance boundaries.

## Acceptance contract

- `cert-eu-advisories` is promoted to `supported` only with an explicit `cert-eu-advisories-v1` executor.
- Discovery is bounded to the official CERT-EU advisory year page and only accepts same-site relative paths matching `/publications/security-advisories/YYYY-NNN/`.
- At most 25 advisory documents are fetched per run.
- Advisory content is fetched only from the official per-advisory `/json` endpoint.
- Every request uses the existing HTTPS-only, DNS re-resolution, global-address, redirect-denial and 5 MiB response-size controls.
- JSON advisory identity must match the requested advisory path.
- Full advisory JSON is retained as raw provenance.
- Ingestion does not grant review, publication or share-approval authority.
- Every catalog entry marked `supported` must have an executor profile present in `SUPPORTED_REGISTRY_EXECUTION_PROFILES`.

## Required evidence

- targeted CERT-EU parser/discovery regression tests
- full RC4 quality gate
- connector/state/provenance regression gates
- container and staging-emulator runtime gates
- accessibility/browser regressions for the unified console
- source connection matrix updated

Do not mark PASS or merge until the exact PR head has completed the required workflow set successfully.
