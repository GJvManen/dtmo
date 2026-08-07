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

## Current evidence

Implementation, migration, focused tests and a fail-closed GitHub Actions workflow are committed on `rc7-5-replay-protection`. They are not accepted as PASS until actual exact-head workflow execution and retained artifacts are independently observable.

## Decision

`CI_VALIDATION_PENDING`. No absent or unexecuted test is interpreted as success.
