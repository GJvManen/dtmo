# Phase 11.10c Command Center Gate

## Purpose

This gate accepts the first functional workspace inside the canonical Unified Operations Workbench. It validates the exact PR head only.

## Required evidence

The exact head must prove:

- the committed frontend dependency graph installs with `npm ci`;
- TypeScript type checking and the Vite production build succeed;
- `/api/v1/command-center` is mounted and requires `READ_INTELLIGENCE`;
- the read model derives operational metrics from canonical DTMO persistence rather than hard-coded dashboard values;
- datastore failure returns `null` metrics and `data_state=unavailable` rather than synthetic zeros;
- integration state distinguishes configuration from runtime observation;
- no integration is labelled healthy merely because a feature flag or API base is configured;
- the browser renders canonical KPIs, recent intelligence, integration capability and role-aware quick actions;
- the unavailable browser state visibly fails closed;
- Command Center remains read-only and does not acquire review/share/case/connector/admin authority;
- professional documentation is synchronized to the Phase 11.10c lifecycle.

## Dedicated workflow

`.github/workflows/phase11-command-center.yml`

The workflow records the exact checked-out SHA and uploads non-sensitive repository evidence.

## Acceptance boundary

A green gate proves repository-controlled behavior for the Command Center read model and browser experience only. It does **not** prove:

- that Taranis, IntelOwl, OpenCTI, MISP, TheHive or Cortex are reachable in a production-equivalent environment;
- production-equivalent migration, upgrade, rollback, health, saturation or recovery;
- independent external assurance;
- production authorization.

## Merge rule

Do not merge until every workflow registered for the final exact PR head is `completed/success`, the PR is mergeable, and professional documentation is synchronized. Merge with expected-head protection.

After acceptance, the only next bounded priority is **Phase 11.10d — Unified Intelligence Workspace**.
