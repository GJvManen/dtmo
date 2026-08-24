# Phase 11.10c Command Center Gate

## Purpose

This gate validates the canonical Command Center on the exact PR head. Phase 11.10q recovery extends the original acceptance scope with attributable trends and actionable integration pivots while retaining the fail-closed read-only boundary.

## Required evidence

The exact head must prove:

- the committed frontend dependency graph installs with `npm ci`;
- TypeScript type checking and the Vite production build succeed;
- `/api/v1/command-center` is mounted and requires `READ_INTELLIGENCE`;
- the read model derives operational metrics from canonical DTMO persistence rather than hard-coded dashboard values;
- the read model derives a seven-day intelligence-arrival series from canonical `discovered_at` values;
- the read model derives a canonical severity distribution rather than a synthetic risk score;
- datastore failure returns `null` metrics, empty trend series and `data_state=unavailable` rather than synthetic zeros;
- integration state distinguishes configuration from runtime observation;
- no integration is labelled healthy merely because a feature flag or API base is configured;
- integration readiness exposes actionable pivots to Administration or Collection without granting mutation authority;
- the browser renders canonical KPIs, recent intelligence, the seven-day trend graph, severity distribution, integration readiness and role-aware quick actions;
- the unavailable browser state visibly fails closed for metrics and both trend panels;
- Command Center remains read-only and does not acquire review/share/case/connector/admin authority;
- professional documentation is synchronized to the Phase 11.10q recovery lifecycle.

## Dedicated workflow

`.github/workflows/phase11-command-center.yml`

The workflow checks out the exact PR head, runs the Command Center repository contract, builds the canonical workbench and executes Chromium browser acceptance against that same checked-out code. It uploads non-sensitive repository evidence only.

## Acceptance boundary

A green gate proves repository-controlled behavior for the Command Center read model and browser experience only. It does **not** prove:

- that Taranis, IntelOwl, OpenCTI, MISP, TheHive or Cortex are reachable in a production-equivalent environment;
- that an enabled or previously observed integration is currently healthy;
- that trend counts represent organizational compromise, exposure or incident impact;
- production-equivalent migration, upgrade, rollback, health, saturation or recovery;
- independent external assurance;
- production authorization.

## Phase 11.10q merge rule

Do not merge PR #316 merely because this gate is green. `docs/roadmap/FUNCTIONAL_RECOVERY_ACCEPTANCE.md` remains authoritative and requires owner functional retest of the canonical interface against the accepted same-origin environment. The PR remains draft until all hard blockers are retired and the immutable-candidate lifecycle can restart.
