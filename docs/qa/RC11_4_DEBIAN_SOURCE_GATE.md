# RC11.4 Debian Security Source Gate

Status: `PENDING_CI`

## Objective

Connect Debian Security Advisories to the unified source framework using Debian's official Recent Advisories RSS distribution while reusing the accepted governed `rss-2.0` adapter.

## Acceptance criteria

- `debian-security` is `supported` in the source catalog.
- Canonical endpoint is `https://www.debian.org/security/dsa`.
- Execution profile is the existing `rss-2.0` profile; no duplicate Debian-specific parser is introduced.
- Existing bounded HTTPS transport, DNS re-resolution, global-address validation, TLS/SNI pinning, redirect denial, response-size limits and `defusedxml` parsing remain unchanged.
- Representative DSA RSS data normalizes to `security-advisory` records with authoritative reliability and raw provenance retained.
- Unified source framework/catalog contract remains green.
- Full exact-head CI and all release-critical gates complete successfully.

## Claim boundary

This gate proves repository implementation and regression acceptance only. It does not grant publication authority and does not claim real-staging provider acceptance. Ingested intelligence remains subject to existing provenance, review, RBAC and publication/share approval controls.

## Evidence

Evidence is the exact-head GitHub Actions workflow set for the PR carrying this document. Keep status `PENDING_CI` until that set is complete and green.
