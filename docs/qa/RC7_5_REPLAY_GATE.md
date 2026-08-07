# RC7.5 Connector Replay Gate

Status: `CI_VALIDATION_PENDING`

## Required evidence

- migration `0006_connector_replay` upgrades cleanly on PostgreSQL;
- the first occurrence of a connector/external-ID/canonical-payload tuple creates exactly one durable replay claim;
- the identical tuple in a later run creates no candidate and is quarantined as `replayed_record`;
- a materially changed payload for the same external ID is not incorrectly suppressed;
- candidate, quarantine and replay-claim records remain `publish_approved=false`;
- `RC7 Connector Replay Gate` executes on the exact PR head and retains `connector-replay-evidence`;
- existing RC4, RC6 and RC7 regression gates remain successful on the same head.

## Executed implementation-head evidence

Implementation head `b1cdcfbdead00b8b687691a2b749407842fa0a14` executed successfully in GitHub Actions:
- RC7 Connector Replay Gate #1 / run `31163250434` — success;
- RC7 Connector State Gate #30 — success;
- RC4 Quality Gate #317 — success;
- RC6 OpenSearch Recovery Gate #69 — success;
- RC6 Multi-store Recovery Gate #59 — success;
- RC7 Connector Contract Gate #21 — success;
- RC7 Live Connector Canary Gate #50 — success;
- RC7 Payload Provenance Gate #12 — success.

Retained `connector-replay-evidence`:
- artifact ID `8987942539`;
- digest `sha256:724333380a09072c25d933f4ab6d73063ce83391634ab079d9eb2a269015dcdd`;
- expired: false at inspection;
- `decision=pass`;
- `claim_count=1`;
- first candidate count `1`;
- replay candidate count `0`;
- replay quarantine reason `replayed_record`;
- `publish_approved=false`;
- JUnit: 2 tests, 0 failures, 0 errors, 0 skipped, including changed-payload non-suppression.

## Current decision

The implementation-head evidence satisfies the RC7.5 behavioral requirements. However, RUN-20260807-056 documentation changes the PR head, so the gate remains `CI_VALIDATION_PENDING` until the new exact head also completes all required workflows successfully. No absent or unexecuted test is interpreted as success. External production connector credentials, provider limits, licences/terms and provider acceptance remain separate open gates in issue #1.
