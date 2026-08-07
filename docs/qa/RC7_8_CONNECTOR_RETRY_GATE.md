# RC7.8 Connector Retry and Backoff Gate

Status: `CI_VALIDATION_PENDING`

## Control objective

Prove that connector retry behavior is deterministic, bounded and connector-local. A failed upstream request must never produce an unbounded retry loop, cascade delay into unrelated connectors, or imply publication approval.

## Required evidence

- deterministic maximum-attempt budget;
- bounded exponential delay when the provider supplies no retry guidance;
- bounded handling of provider `Retry-After` values;
- invalid provider delay values fail closed;
- non-retryable failures fail closed immediately;
- exhausted attempts fail closed with no further retry timestamp;
- retry decisions are scoped to the connector identifier;
- every retry decision retains `publish_approved=false`;
- dedicated GitHub Actions execution is observable and retains its JUnit and JSON evidence artifact;
- required RC4/RC6/RC7 regression gates succeed on the exact PR head before acceptance.

## External-provider context

NVD documents public and API-key request limits and recommends deliberate spacing between requests. Provider-enforced production limits, credentials and terms remain external acceptance gates in issue #1 and are not closed by this internal policy gate.

## Acceptance rule

`PASS` may be recorded only after the exact PR head executes the dedicated RC7 Connector Retry Gate and all required regressions successfully, with retained evidence independently inspected. Configured, queued, missing or unexecuted workflows are not PASS.
