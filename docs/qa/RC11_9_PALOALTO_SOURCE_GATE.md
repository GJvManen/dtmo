# RC11.9 Palo Alto Networks Security Advisories source gate

Status: `PENDING_CI`

## Objective

Connect the official Palo Alto Networks Security Advisories RSS feed to the unified source framework without introducing a duplicate vendor-specific parser.

## Accepted source contract

- Canonical feed: `https://security.paloaltonetworks.com/rss.xml`
- Provider: Palo Alto Networks Product Security
- Execution profile: `rss-2.0`
- Reliability: `authoritative`
- Runtime path: catalog bootstrap -> enable -> unified source framework -> governed RSS fetch -> normalization -> provenance -> ingestion

## Security boundaries

The existing governed RSS executor remains authoritative for transport and parsing. It requires HTTPS, validates DNS destinations as globally routable, uses pinned TLS transport, rejects redirects, bounds response size, accepts only XML/RSS content types, parses with `defusedxml`, and fails closed for malformed XML or feeds without usable channel items.

No credential is required and no raw secret is stored in the catalog.

## Regression evidence

`backend/tests/test_rc11_9_paloalto_source.py` verifies:

- the catalog uses the official Palo Alto Networks RSS endpoint;
- the source is `supported` through the accepted `rss-2.0` profile;
- the profile exists in the unified `SourceAdapterRegistry`;
- advisory title, URL, publication date and description are normalized;
- raw RSS fields are retained as provenance;
- empty/non-usable feeds fail closed.

## Claim boundary

This gate establishes repository-level execution support for the official Palo Alto Networks RSS distribution channel. It does not claim publication authority, provider SLA acceptance, or production/staging runtime evidence until separately observed.

## Release decision

Do not merge or mark this gate PASS until the complete exact-head GitHub Actions workflow set is `completed/success` for the PR head.
