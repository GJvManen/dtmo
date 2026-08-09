# RC10.6 Search Health Alerting Gate

## Decision

`PASS`

## Objective

Validate bounded OpenSearch search-health alerting using coarse cluster-health state only, with controlled failure/recovery behavior and no search data or publication authority entering the alert surface.

## Accepted evidence

PR #93 exact head `14990a8b5d40f975951cdcbba9296a2116fb254c` completed **40/40 registered workflows successfully**. Dedicated `RC10 Search Health Alerting Gate` run `31328060183` retained artifact `9042097760`, digest `sha256:9e317e6b7ad4ce75b50090fafbcb3297b19bcc5cea458761a6ad908ae827e847`, exact-head bound. Independent inspection recorded machine-readable PASS evidence and JUnit **6/6**, zero failures/errors/skips. PR #93 merged as `bb1bb3f2feaf79f4a5a73ffedb78f64294097602`.

Accepted controls:

- only bounded cluster identifier plus `green|yellow|red|unreachable` enters the observer;
- two consecutive unhealthy observations raise;
- two consecutive healthy observations clear;
- repeated unhealthy observations do not repeat raise transitions;
- Prometheus metrics and `DTMOSearchHealthFailure` are present;
- correlation/action evidence is structured and privacy bounded;
- query text, index/document identifiers, response bodies, credentials and identities do not enter the alert contract;
- `publish_approved=false` and human share approval remain unchanged.

## Claim boundary

This PASS does not claim external notification delivery, production OpenSearch hardening, distributed tracing, dashboards, runbooks, on-call handover, Phase 7 completion, Phase 6 assistive-technology completion or any issue #1 external production gate.

## Exactly one next priority

RC10.7 bounded distributed trace-context baseline.
