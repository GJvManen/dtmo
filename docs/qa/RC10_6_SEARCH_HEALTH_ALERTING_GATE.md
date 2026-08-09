# RC10.6 Search Health Alerting Gate

## Decision

`CI_VALIDATION_PENDING`

## Objective

Validate bounded OpenSearch search-health alerting using coarse cluster-health state only, with controlled failure/recovery behavior and no search data or publication authority entering the alert surface.

## Required evidence

Acceptance requires all of the following on one exact PR head:

- only bounded cluster identifier plus `green|yellow|red|unreachable` health state enters the observer;
- two consecutive `red`/`unreachable` observations raise the alert;
- two consecutive `green`/`yellow` observations clear an active alert;
- repeated unhealthy observations do not repeat the raise transition;
- Prometheus metrics and `DTMOSearchHealthFailure` rule are present;
- structured evidence includes safe correlation and actionable guidance;
- query text, document/index identifiers, response bodies, credentials and identities do not enter alert labels/logs;
- `publish_approved=false` and human share approval remain unchanged;
- dedicated `RC10 Search Health Alerting Gate` succeeds and retains JUnit/log/JSON evidence;
- complete registered exact-head workflow matrix succeeds.

## Claim boundary

This gate does not claim external notification delivery, production OpenSearch hardening, distributed tracing, dashboards, runbooks, on-call handover, Phase 7 completion, Phase 6 assistive-technology completion or any issue #1 external production gate.

## Exactly one next priority

Accept only after complete exact-head workflow success and independent retained-artifact inspection. After acceptance, proceed to bounded distributed tracing.
