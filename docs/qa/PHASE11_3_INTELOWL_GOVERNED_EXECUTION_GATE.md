# Phase 11.3 IntelOwl Governed Execution/Persistence Gate

State: **`PENDING EXACT-HEAD CI`**  
Last reviewed: **2026-08-16**

## Acceptance objective

Prove the repository-controlled implementation of governed IntelOwl execution and durable enrichment history without overstating live deployment or production evidence.

## Required gate evidence

The exact PR head must pass the repository quality matrix, including lint, typing, unit tests, migration upgrade/downgrade, container build, dependency review and documentation contracts. The bounded Phase 11.3 tests must demonstrate:

- immutable persistence schema linked to canonical intelligence;
- uniqueness of `(item_id, job_id)`;
- database-enforced `external_share_authorized=false` and `local_compromise_proven=false`;
- governed POST execution requiring `REVIEW_INTELLIGENCE`;
- read-only history requiring `READ_INTELLIGENCE`;
- feature-flag disablement;
- fail-closed handling/analyzer policy before disclosure;
- immutable job-id and analyzer validation inherited from the accepted adapter;
- no IntelOwl external Connector side effects (`connectors_requested=[]`);
- bounded upstream failure semantics and no fabricated enrichment evidence;
- synchronized integration/current-state/user/operations documentation.

## Non-evidence

A green repository gate does not prove live IntelOwl connectivity, deployed service-account permissions, provider credentials, analyzer quality, privacy/data-processing approval, production-equivalent persistence/recovery, independent external assurance or production authorization.

Historical Phase 8/9 evidence is not reused for this materially changed candidate. Phase 11.10 and 11.11 remain mandatory before Phase 12.

## Merge rule

Merge only when every required check is green on one immutable exact-head SHA. Use expected-head protection. If any required documentation or contract test is stale, the PR remains blocked even if code-only checks are green.

## Next step

Only after this slice is merged and Phase 11.3 is reconciled as `PASS / REPOSITORY_COMPLETE` may Phase 11.4 OpenCTI begin.
