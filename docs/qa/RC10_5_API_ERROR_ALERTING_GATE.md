# RC10.5 API Error Alerting Gate

## Decision

`PASS`

## Accepted exact-head evidence

PR #92 exact head `659fa022840e01ed6db4ebeb6a5e703f58a6d259` completed **39/39 registered workflows successfully**. Dedicated run `31327614266` retained artifact `9041987610`, digest `sha256:6a6f2aa5ea2b0b3fb081a0b376f8187a799af726ba950bcbf6fd8618c54e2eca`; independent inspection found exact-head machine-readable PASS evidence and JUnit **6/6**, with 0 failures/errors/skips. PR #92 merged with expected-head protection as `8d6297e17c93150dacb39428ed3580e7c8cc1579`.

## Accepted controls

- request middleware feeds returned statuses and unhandled 500 paths to the observer;
- only bounded route templates are accepted as alert identifiers;
- raw paths/query strings/bodies/headers/identities are outside the observer contract;
- raise after 3 consecutive HTTP 5xx outcomes per route template;
- clear after 2 consecutive non-5xx outcomes while active;
- repeat active failures do not repeat the raise transition;
- bounded Prometheus result/streak/active/transition metrics are present;
- `DTMOApiServerErrors` is actionable and documents raise/clear policy;
- structured evidence contains correlation ID and `publish_approved=false`;
- controlled privacy tests passed.

## Security/advisory boundary

Starlette CVE-2026-48817 and CVE-2026-48818 were recorded during the run. DTMO does not directly pin Starlette; exploitability was not asserted. The exact resolved dependency/security workflows passed on the accepted head.

## Claim boundary

RC10.5 does not claim external notification delivery, search-health alerting, distributed tracing, dashboards, runbooks, on-call handover, Phase 7 completion, Phase 6 VoiceOver/NVDA completion or any issue #1 external production gate.

## Exactly one next priority

RC10.6 bounded search-health alerting.
