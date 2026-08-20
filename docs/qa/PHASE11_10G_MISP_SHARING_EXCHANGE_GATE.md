# Phase 11.10g — MISP Sharing & Exchange Gate

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**

## Acceptance objective

Accept the canonical MISP sharing workspace only when the final PR head proves the repository-controlled flow without weakening DTMO's human authority, handling or replay boundaries.

## Required checks

The dedicated `Phase 11 MISP Sharing Exchange Gate` must execute against the exact PR head and verify:

- React/TypeScript workbench typecheck and production build;
- Phase 11.10g repository contract;
- current Phase 11.10 lifecycle/documentation contract;
- accepted Phase 11.5 MISP consolidation contract regression;
- accepted E8 governed MISP export regression;
- deterministic Chromium browser acceptance for the canonical `/workbench/sharing` route.

The full repository workflow matrix registered for that exact head must also be `completed/success` before merge.

## Mandatory authority assertions

- sharing-state reads require `read:intelligence`;
- review remains `review:intelligence`;
- sharing approval remains `approve:share`;
- reviewer and share approver are separate human principals;
- service accounts cannot substitute for either human authority;
- export cannot create its own approval;
- the MISP event is created with `published=false`;
- no Phase 11.10g publish or synchronization action exists.

## Mandatory handling assertions

- authoritative MISP distribution is preserved on re-export;
- authoritative sharing-group restrictions are preserved;
- requested TLP cannot weaken the source TLP;
- MISP-origin intelligence without authoritative restrictions fails closed;
- deterministic current-revision replay is blocked after pending/success/uncertain evidence;
- uncertain external delivery is not automatically retried.

## Browser acceptance

Browser fixtures must prove at least:

1. a reviewed, independently approved item displays attributable governance state and an eligible unpublished export control;
2. the same principal recorded as reviewer cannot operate the share-approval action;
3. canonical sharing-state failure is shown as unavailable and never synthesized into approval or export eligibility;
4. there are no Publish or Synchronize controls;
5. the UI never needs MISP credentials or a direct MISP endpoint.

## Evidence boundary

The uploaded workflow artifact is repository evidence only. It does not establish live MISP health, publication/synchronization, production-equivalent operation, independent assurance or production authorization.

## Merge rule

Do not merge while any workflow registered on the final exact head is queued, in progress, failed, cancelled or skipped. Merge only with expected-head protection after the PR is mergeable and every registered workflow is `completed/success`.

After acceptance, the sole next bounded priority is **Phase 11.10h — TheHive Investigations & Cases**.
