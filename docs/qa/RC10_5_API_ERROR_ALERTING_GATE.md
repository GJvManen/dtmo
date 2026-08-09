# RC10.5 API Error Alerting Gate

## Decision

`CI_VALIDATION_PENDING`

## Objective

Validate exactly one bounded Phase 7 control: detect repeated API server errors using normalized route-template telemetry, retain safe correlation/action evidence, and clear deterministically after recovery without exposing raw request data or changing publication authority.

## Required exact-head evidence

Acceptance requires all of the following on one final PR head:

- request middleware feeds HTTP outcomes to the API alert observer for both returned responses and unhandled 500 paths;
- only bounded route templates are accepted as alert identifiers;
- raw path parameter values, query strings, bodies, headers and identities are outside the observer input contract;
- alert raises after 3 consecutive HTTP 5xx outcomes for one route template;
- active alert clears only after 2 consecutive non-5xx outcomes;
- repeat 5xx outcomes while active do not repeat the raise transition;
- Prometheus request-result, streak, active-state and transition metrics are present;
- `DTMOApiServerErrors` rule is actionable and documents raise/clear policy;
- structured evidence contains correlation ID and `publish_approved=false`;
- dedicated `RC10 API Error Alerting Gate` succeeds;
- retained JUnit/log/machine-readable evidence is exact-head bound;
- all registered workflows succeed on the exact final head.

## Current implementation

`backend/dtmo/api_alerts.py` implements a route-template-scoped state machine with default thresholds `raise_after=3` and `clear_after=2`. `backend/dtmo/main.py` records both normal response status codes and unhandled 500 outcomes after route normalization. `ops/prometheus/dtmo-alerts.yml` defines `DTMOApiServerErrors` from `dtmo_api_error_alert_active == 1`.

`backend/tests/test_rc10_5_api_error_alerting.py` provides controlled evidence for:

- thresholded raise behavior;
- two-outcome recovery/clear behavior;
- repeat-raise suppression;
- rejection of raw URL/query-like identifiers;
- middleware integration using synthetic path/query material with non-leakage assertions;
- Prometheus alert-rule contract.

## Security/advisory boundary

Fresh review identified Starlette CVE-2026-48817 and CVE-2026-48818 as affecting versions through 1.0.1 and fixed in 1.1.0. DTMO does not directly pin Starlette, so affected-version/exploitability is not asserted. Existing dependency/security CI remains authoritative for the resolved dependency set and may block this gate.

## Claim boundary

RC10.5 does **not** claim:

- external pager/e-mail/chat delivery is configured;
- search-health alerting is complete;
- distributed tracing is complete;
- dashboards or runbooks are complete;
- on-call ownership/handover is complete;
- Phase 7 is complete;
- Phase 6 VoiceOver/NVDA evidence is complete;
- any issue #1 external production gate is complete;
- a 5xx alert proves malicious activity or provides threat attribution.

## Exactly one next priority

Verify the complete exact-head workflow matrix and retained `api-error-alerting-evidence` artifact. Accept and merge only after every registered workflow succeeds and retained evidence is exact-head bound; otherwise record the precise blocker.
