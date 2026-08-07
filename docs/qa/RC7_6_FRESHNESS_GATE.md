# RC7.6 Connector Freshness Gate

Status: `CI_VALIDATION_PENDING`

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

## Executed evidence on implementation head

Implementation/documentation head `4718eaf40cac9631ea93242fb4e38f09413b76f8` executed `RC7 Connector Freshness Gate` #1 / run `31175267660` successfully.

Retained `connector-freshness-evidence`:
- artifact ID `8992567326`;
- digest `sha256:63c69677b7e663e5235e51966161db6378d35a481e295c4db1b9a2c187c4b3ab`;
- expired: false at inspection;
- `decision=pass`;
- 7 tests, 0 failures, 0 errors, 0 skipped;
- candidate freshness `fresh`;
- quarantine classifications `stale`, `future_skew`, `invalid`, `missing`;
- quarantine reasons `stale_source_timestamp`, `future_source_timestamp`, `malformed_source_timestamp`, `missing_source_timestamp`;
- `publish_approved=false`.

On the same head, RC7 Live Connector Canary #58, Payload Provenance #20, Connector Contract #29 and Connector Replay #5 had completed successfully at inspection. RC4 Quality #325, RC6 OpenSearch #77, RC6 Multi-store #67 and RC7 Connector State #34 were still queued/in progress and therefore were not counted as PASS.

## Current decision

RC7.6 remains `CI_VALIDATION_PENDING`. The dedicated freshness evidence is successful, but not all required exact-head regression gates were complete when this run closed. This documentation update also moves the PR head, so fresh exact-head execution is required before acceptance or merge.
