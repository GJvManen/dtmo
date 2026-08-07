# RC7.8 Connector Retry and Backoff Gate

Status: `PASS`

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

## Accepted evidence

Accepted exact PR #35 head: `05daeb35c53a8c44d2d7e51e95a745b2b5ece15a`.

All 11 required workflows completed successfully, including RC7 Connector Retry Gate #1 (`31194427369`), RC4 Quality Gate #340, RC6 OpenSearch Recovery #92 and RC6 Multi-store Recovery #82.

Retained artifact `connector-retry-evidence`:

- artifact ID `9000180534`;
- digest `sha256:2b6475df7b9bf92e53d9c7a2e74719e7918ba18925e8488c330eb90c4105f45a`;
- `decision=pass`;
- 7 tests executed, 0 failures, 0 errors, 0 skipped;
- exponential delays `2/4/8` seconds;
- provider `Retry-After` capped at 120 seconds;
- exhausted and non-retryable failures block further retry;
- independent `nvd` connector remains retryable;
- all retry decisions retain `publish_approved=false`.

PR #35 was merged with expected-head protection as `e4b165df68ae7d9df4e25e51ec9f59e1b1133c92`.

## External-provider context

NVD documents public and API-key request limits and recommends deliberate spacing between requests. Provider-enforced production limits, credentials and terms remain external acceptance gates in issue #1 and are not closed by this internal policy gate.

## Acceptance rule

`PASS` is valid only for the exact accepted head and retained evidence above. Configured, queued, missing or unexecuted workflows are not PASS.
