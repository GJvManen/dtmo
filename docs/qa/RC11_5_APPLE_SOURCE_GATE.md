# RC11.5 Apple Security Releases source gate

Status: **PENDING_CI**

## Objective

Connect Apple Security Releases to the unified DTMO source framework without treating a generic web page as an unrestricted scraper target.

## Accepted source contract

- Canonical index: `https://support.apple.com/100100`
- Transport: existing bounded HTTPS fetch with DNS re-resolution, public-address enforcement, TLS validation, redirect denial and response-size limit
- Discovery: first-party Apple Support links only
- Accepted detail-link shape: Apple Support six-digit article identifiers, optionally locale-prefixed
- Index article `100100` is excluded from emitted records
- Links must have security/beveiliging content in the visible title
- Maximum emitted records per execution: 25
- External origins and malformed article paths are ignored
- Empty usable discovery fails closed

Apple currently exposes the Security Releases index and per-release security-content articles on Apple Support. No documented public Apple RSS, CSAF or security-release API is claimed by this gate.

## Normalization and provenance

Each accepted Apple article is normalized as a `security-advisory` record with an `APPLE-<article-id>` external ID, canonical `https://support.apple.com/<article-id>` URL, authoritative source reliability and raw provenance containing the original href, article ID and title.

## Regression evidence

`backend/tests/test_rc11_5_apple_source.py` covers:

- catalog/framework registration;
- first-party article canonicalization;
- external-origin and non-security link rejection;
- fail-closed empty discovery;
- unified framework dispatch through the Apple adapter.

## Claim boundary

Repository acceptance does not grant publication authority and does not claim real-staging provider acceptance. Human review, provenance, RBAC and separate share/publication approval controls remain unchanged.

## Release decision

Do not mark RC11.5 PASS or merge its pull request until the complete exact-head workflow set is green. On any required workflow failure or missing evidence, status remains **PENDING_CI** or **BLOCKED**.
