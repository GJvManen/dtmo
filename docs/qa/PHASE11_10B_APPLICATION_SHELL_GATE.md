# Phase 11.10b — Canonical Application Shell Gate

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**

## Gate objective

Prove the repository-controlled implementation contract for the canonical DTMO Unified Operations Workbench shell without promoting repository/browser evidence to live integration, production-equivalent or production evidence.

## Required exact-head checks

The `Phase 11 Application Shell Gate` must run against the exact PR head and prove:

1. exact direct frontend dependency pins;
2. the committed npm lockfile is present, uses the accepted lockfile schema and is consumed with `npm ci` without manifest mutation;
3. production frontend dependency audit with HIGH/CRITICAL findings failing the gate;
4. strict TypeScript typecheck;
5. Vite production build under `/workbench/`;
6. SHA-256 inventory for generated assets;
7. backend repository contract for canonical routing, CSP, cache and authority boundaries;
8. supported DTMO process serving the built exact-head workbench;
9. browser journey for canonical root redirect, task-oriented navigation, keyboard command palette, context rail and mobile navigation;
10. canonical index CSP and `X-DTMO-Frontend-Mode` response marker;
11. professional current-state, roadmap and evidence synchronization through the central documentation gate;
12. existing supply-chain/container/security/accessibility/integration gates remain green for the same exact final head.

The workflow must never regenerate dependency resolution as part of final acceptance. `frontend/package-lock.json` is an authoritative source input and `npm ci` must leave both dependency manifests unchanged.

## Fail-closed conditions

The slice fails if any of the following is true:

- frontend dependency versions are floating ranges;
- the exact final head has no committed npm lockfile;
- `npm ci` cannot consume the committed lockfile or mutates the dependency manifests;
- production dependency audit reports an unaccepted HIGH/CRITICAL finding;
- typecheck or production build fails;
- browser code directly calls an upstream Taranis/IntelOwl/OpenCTI/MISP/TheHive/Cortex service for a governed product workflow;
- `/workbench/` can traverse outside the built asset root;
- the supported runtime image does not contain the built canonical frontend;
- CSP requires unsafe inline script/style execution;
- shell placeholders are presented as live operational evidence;
- legacy `/ui/console` is treated as a parallel feature target rather than a **compatibility path**;
- authority is inferred from hidden frontend controls rather than **server-side RBAC**;
- command-palette navigation is promoted to a governed high-impact action path in this slice;
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

These tests do not prove Command Center functional data, live upstream connectivity or production-equivalent behavior.

## Evidence artifacts

The final workflow records:

- a copy of the committed npm lockfile used for that exact-head run;
- deterministic frontend asset SHA-256 inventory;
- canonical response headers;
- repository evidence-boundary JSON.

Those artifacts are repository audit evidence only. The source-controlled lockfile remains authoritative; the workflow artifact is not a new dependency graph.

## Security and authority boundary

Normal governed operation remains **browser → DTMO API → governed integration adapter → upstream service**. The browser receives no upstream privileged service credential path. Human publication/share approval, TheHive case-handoff authority, administrative authority and later playbook approval remain distinct server-side decisions.

## Claim boundary

PASS means **Phase 11.10b PASS / REPOSITORY_COMPLETE** only. It **does not prove** live service connectivity, Command Center feature acceptance, production-equivalent operation, independent external assurance or production authorization.

The slice may be accepted only when every registered workflow for the exact final head is `completed/success`, professional documentation is synchronized, the PR remains mergeable and merge uses expected-head protection. Only then may Phase 11.10c begin.
