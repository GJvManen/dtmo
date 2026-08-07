# RC7.9 Connector Timeout and Cancellation Gate

Status: `PASS`

## Control objective

Prove that a slow or hung upstream connector invocation is bounded by an explicit timeout budget, that timeout/cancellation is scoped to the affected connector, that operational provenance remains attached to the decision, and that no timeout or successful fetch state can imply publication approval.

## Accepted evidence

Exact PR head: `0eee765b72d016489af248d2bf29e3b1dbd593db`.

All required exact-head workflows completed successfully: RC4 Quality #345, RC6 OpenSearch Recovery #97, RC6 Multi-store Recovery #87, RC7 Connector State #42, Live Connector Canary #78, Connector Contract #49, Payload Provenance #40, Connector Replay #13, Connector Freshness #9, Connector Failure Isolation #5, Connector Retry #2 and Connector Timeout #1.

Retained artifact:

- name: `connector-timeout-evidence`;
- artifact ID: `9003952153`;
- digest: `sha256:b448608ae258086bacf0f4cb69c2c18f566b58851f7e55ace322fb30b5dc353f`;
- source workflow run: `31203965560` (RC7 Connector Timeout Gate #1).

Independent artifact inspection confirmed:

- JSON `decision=pass`;
- 8 executed tests, 0 failures, 0 errors, 0 skips;
- `cisa-kev` exceeded the 0.02 second evidence budget and failed closed as `timeout_budget_exhausted`;
- the timed-out operation was actually cancelled;
- independent `nvd` execution completed as `nvd-ok`;
- connector/run/source provenance was retained;
- both timeout and successful execution decisions retained `publish_approved=false`;
- scheduler cancellation and invalid/missing provenance were covered by the executed regression suite.

PR #36 was merged with expected-head protection as `3c5e1ed278d86b5279a285e546d24e12fbaabd3f`.

## Provider and threat-intelligence context

The NVD states that its API is provided on an `as-available` basis and does not warrant uninterrupted access. Its developer guidance also enforces request-rate limits and recommends deliberate spacing between requests. These conditions support bounded client-side execution but do not close the external credential, provider-limit, licence or terms gates in issue #1.

No objective-specific CVE changed the timeout control design during this acceptance run. Vulnerability content remains governed by the existing provenance, freshness, replay, quarantine and human-approval controls.

## Acceptance rule

`PASS` applies only to exact head `0eee765b72d016489af248d2bf29e3b1dbd593db` with the workflow and retained-artifact evidence above. Queued, configured, missing or unexecuted workflows are never treated as PASS.

## Remaining Phase 4 blocker

Issue #1 still requires external validation of live-connector credentials, provider-enforced limits, licences/terms and provider-specific production acceptance. RC7.9 does not satisfy or waive those external gates.