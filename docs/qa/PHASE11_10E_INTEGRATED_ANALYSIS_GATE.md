# Phase 11.10e — Integrated Analysis Workspace Gate

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**  
Last updated: **2026-08-20**

## Objective

Accept the bounded IntelOwl/Cortex integrated analysis slice only when one exact PR head proves the repository implementation, browser journey, authority boundaries, persistence contract and professional documentation remain mutually consistent.

## Required implementation evidence

The exact head must contain and validate:

- `backend/dtmo/intelowl_execution.py` with the existing IntelOwl routes plus governed analysis capability, Cortex execution and combined-history APIs;
- `backend/dtmo/persistence/cortex.py` with durable immutable Cortex analysis records;
- `database/migrations/versions/0015_cortex_analysis_history.py` chained from revision `0014_thehive_handoff_state`;
- `frontend/src/AnalysisWorkspace.tsx` and `frontend/src/analysis-workspace.css`;
- server-side `read:intelligence` for history/capability reads;
- server-side `review:intelligence` for IntelOwl/Cortex execution;
- DB/runtime invariants that analyzer evidence has no external-share authority and does not prove local compromise;
- Cortex analyzer-only behavior with no responders or automatic analyzer discovery;
- fail-closed rendering for missing history or failed execution.

## Browser acceptance

The browser test must prove that an authorized reviewer can open `/workbench/analysis?item=<uuid>` and see persisted IntelOwl and Cortex evidence in one workspace. It must also prove that a read-only principal is not presented with enabled execution controls.

Fixtures are deterministic repository evidence only. They are not live IntelOwl/Cortex evidence.

## Exact-head workflow

`.github/workflows/phase11-integrated-analysis-workspace.yml` must:

1. check out the exact pull-request head rather than the synthetic merge ref;
2. verify the checked-out SHA;
3. consume the committed frontend dependency graph with `npm ci` and confirm manifests remain unchanged;
4. typecheck/build the React workbench;
5. run the 11.10e repository contracts and preserved Cortex connector contract;
6. execute deterministic Chromium browser acceptance against the built workbench;
7. emit a non-sensitive evidence artifact bound to the run/head while preserving the claim boundary.

## Fail-closed acceptance

The gate fails when any required file, route, permission, migration link, invariant, browser state or documentation marker is missing. A failed/queued/in-progress workflow is not acceptance evidence.

IntelOwl/Cortex configuration does **not prove** runtime health. Analyzer output does **not prove** local compromise and does not grant external-share, publication, case or production authority.

## Merge rule

Do not merge until **every** workflow registered for the final exact head is `completed/success`, the pull request is mergeable and documentation is synchronized. Merge must use expected-head protection.

Passing this repository gate yields only `PASS / REPOSITORY_COMPLETE` for Phase 11.10e. It does not establish production-equivalent behavior, independent assurance or production authorization. DTMO remains **not production authorized**.

After merge the only next bounded priority is **Phase 11.10f — OpenCTI graph/entity workspace**.
