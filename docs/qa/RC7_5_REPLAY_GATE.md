# RC7.5 Connector Replay Gate

Status: `PASS`

## Required evidence

- migration `0006_connector_replay` upgrades cleanly on PostgreSQL;
- the first occurrence of a connector/external-ID/canonical-payload tuple creates exactly one durable replay claim;
- the identical tuple in a later run creates no candidate and is quarantined as `replayed_record`;
- a materially changed payload for the same external ID is not incorrectly suppressed;
- candidate, quarantine and replay-claim records remain `publish_approved=false`;
- `RC7 Connector Replay Gate` executes on the exact PR head and retains `connector-replay-evidence`;
- existing RC4, RC6 and RC7 regression gates remain successful on the same head.

## Final exact-head evidence

Exact PR head `677b90b8690a60b2a9de130bc50e3b273b351e6d` executed successfully in GitHub Actions:
- RC7 Connector Replay Gate #4 / run `31167140732` — success;
- RC7 Connector State Gate #33 / run `31167140723` — success;
- RC4 Quality Gate #320 / run `31167140710` — success;
- RC6 OpenSearch Recovery Gate #72 / run `31167140753` — success;
- RC6 Multi-store Recovery Gate #62 / run `31167140709` — success;
- RC7 Connector Contract Gate #24 / run `31167140712` — success;
- RC7 Live Connector Canary Gate #53 / run `31167140734` — success;
- RC7 Payload Provenance Gate #15 / run `31167140727` — success.

Retained `connector-replay-evidence`:
- artifact ID `8989448410`;
- digest `sha256:cc80113746341b4c0a3ce43c46d307b5869941d74eb0c5aab4adcf025a842d9e`;
- expired: false at inspection;
- `decision=pass`;
- `claim_count=1`;
- first candidate count `1`;
- replay candidate count `0`;
- replay quarantine reason `replayed_record`;
- `publish_approved=false`;
- JUnit: 2 tests, 0 failures, 0 errors, 0 skipped, including changed-payload non-suppression.

## Decision

RC7.5 is `PASS`. PR #32 was merged with expected-head protection as `41113d3f53028a174a823b06ce01545ede1cd232`. No absent or unexecuted test was interpreted as success. External production connector credentials, provider limits, licences/terms and provider acceptance remain separate open gates in issue #1 and are not implied by this acceptance.
