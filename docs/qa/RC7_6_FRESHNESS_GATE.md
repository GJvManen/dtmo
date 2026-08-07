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

## Current decision

Implementation and dedicated regression/evidence workflow are committed on `rc7-6-connector-freshness`, but no exact-head GitHub Actions execution has yet been inspected. RC7.6 must not be marked PASS until all required exact-head workflows complete successfully and retained evidence is independently inspected.
