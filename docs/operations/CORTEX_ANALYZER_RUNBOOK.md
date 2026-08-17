# Cortex Analyzer Operations Runbook

State: **`IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`**

## Preconditions

- approved HTTPS Cortex endpoint;
- dedicated API key identity limited to analyze/read-job capability in the intended organization;
- explicit analyzer allowlist reviewed by security/CTI ownership;
- each analyzer's provider/data-handling and licensing terms reviewed before enablement;
- no production secrets committed to the repository.

## Enablement

Set the Cortex runtime variables and enable `DTMO_FEATURE_CORTEX_ANALYSIS=true` only in an approved environment. The feature remains off by default.

## Failure handling

- authentication/authorization errors: disable the feature and validate service identity/organization scope;
- unknown or unapproved analyzer: fail closed; do not dynamically expand the allowlist;
- malformed or oversized report: reject the result and retain no fabricated success claim;
- job/analyzer identity mismatch: treat as integrity failure;
- timeout or uncertain provider behavior: surface dependency failure; do not infer a security verdict;
- analyzer/provider outage: IntelOwl must not be selected as an automatic hidden fallback; any alternate analysis remains an explicit governed action.

## Security incident response

Rotate the Cortex API key if exposure is suspected. Review Cortex job/audit records and DTMO request/audit correlation. Do not delete Cortex jobs through DTMO because deletion is outside the accepted connector boundary.

## Validation boundary

Repository tests exercise synthetic HTTP behavior only. Live Cortex connectivity, analyzer catalogs, provider entitlements, organization permissions, secrets, network policy and production-equivalent operation belong to later deployment validation.
