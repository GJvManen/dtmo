# RC11.8 Fortinet PSIRT source gate

Status: PENDING_CI

## Objective

Connect Fortinet PSIRT advisories through the unified source framework without introducing an unbounded or cross-origin scraper.

## Acceptance contract

- catalog source `fortinet-psirt` is `supported` only with execution profile `fortinet-psirt-v1`
- discovery starts at the official `https://www.fortiguard.com/psirt` surface
- followed documents must resolve to first-party `/psirt/FG-IR-YY-NNN[N]` paths
- discovery is capped at 25 advisory documents per execution
- detail parsing requires the expected FG-IR identifier and at least one published CVE
- transport reuses the existing bounded HTTPS/DNS/TLS/redirect/response-size controls
- raw provenance preserves advisory id, canonical URL, discovery title and CVE identifiers
- source-framework/catalog parity tests remain green

## Claim boundary

Fortinet PSIRT pages expose first-party advisories and CVRF/CSAF downloads. This slice proves repository connector behaviour only; it does not claim publication authority or a separately documented public Fortinet advisory-list API.

## Release decision

Do not mark PASS or merge until the complete exact-head workflow set is `completed/success`.
