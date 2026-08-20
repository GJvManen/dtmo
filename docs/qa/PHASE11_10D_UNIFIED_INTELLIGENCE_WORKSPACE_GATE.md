# Phase 11.10d — Unified Intelligence Workspace Gate

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**

## Purpose

This gate accepts only the bounded repository implementation of the Unified Intelligence Workspace. It must **fail closed** when required code, contracts, browser behavior, documentation or exact-head evidence is missing.

## Required checks

1. checkout equals the exact pull-request head SHA;
2. committed frontend dependency graph installs with `npm ci` and does not mutate manifests;
3. TypeScript typecheck and Vite production build succeed;
4. existing `read:intelligence` search and canonical-detail API boundaries remain mounted;
5. `/workbench/intelligence` renders governed discovery without synthetic default records;
6. `/workbench/intelligence/iocs` uses the same governed DTMO intelligence contracts;
7. a deterministic browser journey proves search → result selection → canonical detail → provenance rendering;
8. a deterministic dependency-failure journey proves search failure is unavailable rather than a synthetic empty result;
9. current lifecycle documentation is reconciled in the same pull request;
10. exact-head non-sensitive evidence is uploaded.

## Authority checks

The workspace must not add browser-side privileged upstream calls or mutation authority. Search and detail use DTMO server endpoints protected by `read:intelligence`. Review, publication/share approval, connector execution, analyzer execution, case mutation and administration remain separately server-authorized.

## Evidence boundary

Passing this gate establishes repository-controlled evidence for the exact-head frontend build and deterministic browser behavior. It **does not prove**:

- completeness across every live upstream source;
- live Taranis, IntelOwl, OpenCTI, MISP, TheHive or Cortex health;
- production-equivalent deployment, continuity or recovery;
- independent external assurance;
- production authorization.

Phase 11.10 remains **IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED**. Fresh production-equivalent execution remains deferred to 11.10p after the integrated candidate is complete and frozen. Phase 11.11 remains **NOT STARTED** and Phase 12 remains **NOT STARTED**.
