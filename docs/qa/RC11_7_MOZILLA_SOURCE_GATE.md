# RC11.7 Mozilla Security Advisories Source Gate

Status: PENDING_CI

## Objective

Connect Mozilla Foundation Security Advisories to the unified source framework through Mozilla's official first-party advisory index and MFSA documents.

## Acceptance criteria

- `mozilla-security-advisories` is `supported` only when `mozilla-mfsa-v1` is registered in `SourceAdapterRegistry`.
- Discovery accepts only first-party `mozilla.org` / `www.mozilla.org` MFSA paths matching `mfsaYYYY-NN`/`mfsaYYYY-NNN`.
- Discovery is bounded to 25 advisories per execution and rejects external origins.
- Detail parsing requires the Mozilla Foundation Security Advisory marker and at least one published CVE identifier.
- Existing bounded HTTPS/DNS/TLS/redirect/response-size transport is reused.
- Advisory ID, canonical URL, discovery title and CVE identifiers remain in raw provenance.
- Exact-head RC4 Quality and all required release workflows must be green before merge.

## Claim boundary

Repository acceptance proves the governed connector contract only. It does not grant publication authority and does not claim Mozilla provider-side staging acceptance.
