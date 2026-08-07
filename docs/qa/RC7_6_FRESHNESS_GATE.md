# RC7.6 Connector Freshness Gate

Status: `PASS`

## Objective

Prove deterministic source freshness/staleness handling at the connector ingestion boundary without weakening provenance, quarantine, RBAC, separation of duties or mandatory human publication approval.

## Required evidence

- source timestamps are parsed deterministically and normalized to UTC;
- every policy-evaluated candidate is classified `fresh` or explicitly `missing_allowed`;
- stale source timestamps fail closed to quarantine as `stale_source_timestamp`;
- timestamps beyond the configured future clock-skew budget fail closed as `future_source_timestamp`;
- malformed timestamps fail closed as `malformed_source_timestamp`;
- missing timestamps fail closed unless the connector contract explicitly permits them;
- source URI, connector/run identity, fetch time, raw evidence, confidence and payload digest remain intact;
- candidate, quarantine and aggregate outcomes remain `publish_approved=false`;
- `RC7 Connector Freshness Gate` executes on the exact PR head and retains `connector-freshness-evidence`;
- existing RC4, RC6 and RC7 regression gates remain successful on the same exact head.

## Public-source review

CISA continues to describe the Known Exploited Vulnerabilities catalog as an authoritative input for vulnerability-management prioritization and publishes machine-readable JSON/CSV plus a schema. The catalog exposes per-record `Date Added` values. This supports retaining provider timestamps as provenance while applying connector-specific freshness policy rather than treating ingestion time as source time.

Source: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
Confidence: high (primary government source).

## Final exact-head acceptance evidence

Final PR #33 head: `cd932c983035537b0cac1af6fc5768a818f238bc`.

All required workflows completed successfully on that exact head:

- RC4 Quality Gate #328;
- RC6 OpenSearch Recovery Gate #80;
- RC6 Multi-store Recovery Gate #70;
- RC7 Connector State Gate #37;
- RC7 Live Connector Canary Gate #61;
- RC7 Connector Contract Gate #32;
- RC7 Payload Provenance Gate #23;
- RC7 Connector Replay Gate #8;
- RC7 Connector Freshness Gate #4 / run `31175416031`.

Retained `connector-freshness-evidence`:

- artifact ID `8992632471`;
- digest `sha256:0fc05c726486a4cf7fd922e6a5af55511f6bff8c5aa0333faf589d4ed77fb606`;
- expired: false at inspection;
- `decision=pass`;
- 7 tests, 0 failures, 0 errors, 0 skipped;
- candidate freshness `fresh`;
- quarantine classifications `stale`, `future_skew`, `invalid`, `missing`;
- quarantine reasons `stale_source_timestamp`, `future_source_timestamp`, `malformed_source_timestamp`, `missing_source_timestamp`;
- `publish_approved=false`.

PR #33 merged with expected-head protection as `ad376612ae13d79d4ba1efd38183d599dcd08ef0`.

## Decision

RC7.6 is `PASS`. The final exact PR head passed the dedicated freshness gate and every required RC4/RC6/RC7 regression gate, and retained evidence independently confirms fail-closed timestamp handling without publication approval. External production connector credentials, provider-enforced limits, licences/terms and provider-specific acceptance remain open in issue #1.
