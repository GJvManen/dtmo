# RC10.11.2 Source Adapter Gate

## Decision

`PENDING_CI`

## Objective

Promote selected curated catalog sources from visible-only inventory to governed executable feeds inside the unified DTMO console without weakening outbound-network, provenance, review or publication controls.

## This slice

NCSC-NL Security Advisories RSS (`ncsc-nl-advisories-rss`) is promoted to `supported` with the `rss-2.0` execution profile.

The adapter:

- reuses validated HTTPS URLs and DNS re-resolution;
- rejects non-global destinations;
- pins TLS to the validated public address and original SNI hostname;
- rejects redirects;
- bounds responses to 5 MiB;
- accepts only RSS/XML content types;
- parses RSS without executing embedded content;
- normalizes items to `security-advisory` connector records;
- retains raw normalized source fields for provenance;
- fails closed on malformed or empty RSS;
- preserves human review and separate external share approval as independent authorities.

## Claim boundary

This gate does **not** claim support for NCSC-NL CSAF, CERT-EU, MSRC or other catalog entries still marked `planned-parser`. They remain visible in the unified console but non-executable until an adapter-specific gate is implemented and accepted.

## Acceptance evidence

- exact-head RC4 Quality Gate succeeds;
- source-adapter regression tests succeed;
- existing connector contract, payload provenance, replay, retry, timeout and isolation gates remain green;
- browser/console regression gates remain green;
- no catalog source is marked executable without a parser and bounded fetch contract.

## Release rule

Do not mark this gate PASS or merge the implementation until exact-head CI is complete and successful.
