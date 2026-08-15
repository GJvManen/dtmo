# Phase 8.2.3 — OpenSearch Health and Search Validation

**Status:** `READY_FOR_EXTERNAL_EXECUTION / NOT_YET_ACCEPTED`

## Objective

Validate OpenSearch cluster health, application connectivity and representative search behavior on the owner-approved post-E8 production-equivalent staging deployment. Accepted evidence must bind to the same immutable Phase 8.2 deployment identity used by the other staging checks.

## Preconditions

- Phase 8.2 is active on `main`.
- Step-scoped evidence validation from PR #212 is available.
- The staging environment is owner-approved.
- No result may be accepted until the environment identifier, deployed commit and immutable application image digest are captured for the same deployment.
- 8.2.1 and 8.2.2 may remain open while this check is prepared, but accepted results may not be mixed across deployment identities.

## Validation procedure

1. Observe OpenSearch cluster health from the approved staging environment or approved operational access path.
2. Record the cluster/version identity required to distinguish this runtime from local/emulator infrastructure.
3. Confirm the expected index and alias state for the deployed DTMO release.
4. Execute a representative read/search query using the intended application/staging access path.
5. Confirm the returned record is attributable to canonical staged data rather than a synthetic CI fixture.
6. Confirm the application uses the intended staging OpenSearch configuration/identity and does not reuse production credentials.
7. Exercise or observe the defined degraded/unavailable-search behavior and confirm the application fails safely without fabricating successful search results.
8. Record reviewer, timestamp and a restricted evidence reference. Do not commit credentials, tokens, raw restricted evidence or unnecessary personal data.
9. Populate `checks.opensearch_health_search` in the Phase 8.2 evidence manifest and bind it to the same deployment fingerprint.

## Step validation

After the immutable identity fields and this check record are populated, validate only this evidence class with:

```bash
python3 tools/phase8_platform_validation.py <manifest.json> --check opensearch_health_search
```

A step-scoped `PASS` means the manifest contains a complete, internally consistent OpenSearch evidence record for one immutable deployment identity. It does not independently prove the referenced external evidence is genuine; accountable review of the approved staging environment remains required.

## Acceptance criteria

`PASS` requires all of the following against the approved staging deployment:

- cluster health is observed and acceptable for the staging operating model;
- expected index/alias state is present;
- representative search succeeds against canonical staged data;
- application connectivity uses the intended staging identity/configuration;
- no production credentials are reused;
- degraded/unavailable-search behavior fails safely;
- evidence is timestamped, reviewer-attributed and stored at an approved restricted reference;
- the result is bound to the same immutable Phase 8.2 deployment fingerprint.

Repository CI, OpenSearch recovery gates and staging emulators are supporting evidence only and cannot substitute for deployed-environment acceptance.

## Evidence boundary

This runbook does not mark 8.2.1, 8.2.2, 8.2.3, Phase 8.2 or Phase 8 as `PASS`. Formal acceptance remains fail-closed until external evidence is observed and identity-bound.

Related: #158, #210, #211, #214, PR #212.
