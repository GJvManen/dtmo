# Phase 11.10b — Canonical Application Shell Gate

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**

## Gate objective

Prove the repository-controlled implementation contract for the canonical DTMO Unified Operations Workbench shell without promoting repository/browser evidence to live integration, production-equivalent or production evidence.

## Required exact-head checks

The `Phase 11 Application Shell Gate` must run against the exact PR head and prove:

1. exact direct frontend dependency pins;
2. deterministic npm lock resolution and, before acceptance, a committed lockfile consumed with `npm ci`;
3. production frontend dependency audit with HIGH/CRITICAL findings failing the gate;
4. strict TypeScript typecheck;
5. Vite production build under `/workbench/`;
6. SHA-256 inventory for generated assets;
7. backend repository contract for canonical routing, CSP, cache and authority boundaries;
8. supported DTMO process serving the built exact-head workbench;
9. browser journey for canonical root redirect, task-oriented navigation, keyboard command palette, context rail and mobile navigation;
10. canonical index CSP and `X-DTMO-Frontend-Mode` response marker;
11. professional current-state, roadmap and evidence synchronization through the central documentation gate;
12. existing supply-chain/container gates remain green when the Dockerfile changes.

## Fail-closed conditions

The slice fails if any of the following is true:

- frontend dependency versions are floating ranges;
- the accepted final head has no committed npm lockfile;
- typecheck or production build fails;
- browser code directly calls an upstream Taranis/IntelOwl/OpenCTI/MISP/TheHive/Cortex service for a governed product workflow;
- `/workbench/` can traverse outside the built asset root;
- the supported runtime image does not contain the built canonical frontend;
- CSP requires unsafe inline script/style execution;
- shell placeholders are presented as live operational evidence;
- legacy `/ui/console` is treated as a parallel feature target;
- authority is inferred from hidden frontend controls rather than server-side RBAC;
- exact-head identity is ambiguous;
- any registered exact-head workflow is incomplete or failed.

## Browser acceptance

Repository browser acceptance verifies only shell mechanics:

- `/` transitions to `/workbench/command-center` when built assets exist;
- Command Center route is present as a shell foundation, not synthetic content;
- primary workspace navigation is visible and functional;
- Ctrl/Cmd+K opens a navigation-only command palette;
- context rail explicitly reports no selected object;
- compatibility console link remains visible during migration;
- mobile navigation is operable;
- skip-to-content remains present.

## Evidence artifacts

The workflow records:

- generated dependency lockfile during bootstrap runs;
- deterministic frontend asset SHA-256 inventory;
- canonical response headers;
- repository evidence-boundary JSON.

Before Phase 11.10b acceptance, the generated lockfile must be reconciled back into source control and the final exact-head workflow must use the committed lockfile with `npm ci` rather than generating a new dependency graph.

## Claim boundary

PASS means **Phase 11.10b PASS / REPOSITORY_COMPLETE** only. It does not prove live service connectivity, Command Center feature acceptance, production-equivalent operation, independent external assurance or production authorization.
