# RC11.6 Chrome Security Releases source gate

Status: PENDING_CI

## Objective
Connect the official Google Chrome Releases publication surface to the unified DTMO source framework without widening execution to generic web scraping.

## Accepted execution boundary
- canonical index: `https://chromereleases.googleblog.com/`
- discovery accepts only HTTPS first-party `chromereleases.googleblog.com/YYYY/MM/*.html` posts
- only posts whose discovery title contains both `stable` and `update` are followed
- at most 20 stable posts are followed per run
- each followed document is fetched through the existing bounded HTTPS/DNS/TLS/redirect/size transport
- a record is emitted only when the first-party post contains a Security Fixes section and at least one published `CVE-YYYY-NNNN...` identifier
- raw provenance retains the Chrome post slug, canonical URL, discovery title and published CVE identifiers

## Fail-closed expectations
Malformed/non-UTF-8 index data, no stable-channel discovery, invalid post payloads, external origins, non-post paths and runs containing no published-CVE security posts must not silently produce successful intelligence records.

## Claim boundary
This gate proves repository code and parser-contract acceptance only. It does not claim a separate documented Chrome security API, CSAF feed, publication authority, or real-staging provider acceptance.

## Release decision
Do not mark PASS or merge until the complete exact-head GitHub workflow set is green.
