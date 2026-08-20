# DTMO Unified Operations Workbench frontend

Status: **Phase 11.10b — canonical application shell implementation**.

This directory contains the separately built React/TypeScript/Vite browser application defined by the accepted Phase 11.10a frontend architecture contract.

## Supported commands

```bash
npm ci
npm run typecheck
npm run build
```

The supported deployment build produces `frontend/dist`. DTMO serves that immutable build through the same application origin under `/workbench/`; the browser does not become a privileged integration client.

During Phase 11.10b migration, `/ui/console` remains a compatibility path. New feature development targets the canonical workbench only.

## Security and authority boundary

Normal product operations remain:

**browser → DTMO API → server-side authorization/audit → canonical service → governed integration adapter → upstream service**.

Frontend visibility is not authorization. Human intelligence review, case authority, external share/publication approval and administrative authority remain distinct server-side decisions.

## Evidence boundary

A successful frontend build and repository browser gate prove only the repository-controlled shell, routing, accessibility/responsive baseline and same-origin serving contract. They do not prove live upstream behavior, production-equivalent operation, independent assurance or production authorization.
