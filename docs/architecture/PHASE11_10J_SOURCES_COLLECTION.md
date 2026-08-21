# Phase 11.10j — Sources & Collection

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**

## Purpose

Phase 11.10j makes the canonical `/collection` workspace functional without creating a second connector control plane. The browser uses DTMO-owned `/api/v1/admin/sources/...` APIs only. DTMO remains responsible for authorization, audit, source validation, secret-reference resolution, connector isolation, provenance and canonical ingestion.

## Trust path

```mermaid
flowchart LR
    U[Human operator] -->|authenticated DTMO session| W[Collection workspace]
    W -->|DTMO API only| A[/api/v1/admin/sources]
    A --> R[Server-side RBAC + human-admin gate]
    R --> C[Source catalog / registry]
    R --> V[Validate / bounded test]
    R --> X[Explicit collection run]
    X --> I[Governed source adapter]
    I --> N[Canonical normalization + provenance]
    N --> D[DTMO canonical store]
    A --> E[Persistent audit evidence]
    S[Secret manager/reference] -->|server-side resolution only| I
```

## Authority and evidence boundaries

- `manage:connectors` plus a human administrator role is required for registry mutation, bootstrap, validation, test and collection execution.
- Browser code never receives upstream credential values. Registry `secret_ref` values are references, not secrets.
- Supported catalog bootstrap is idempotent and registers sources disabled by default.
- Validation checks governed endpoint policy; it does not prove upstream trust or availability.
- Test execution is bounded and non-ingesting.
- Run is an explicit human-admin action. Connector isolation remains fail closed after repeated failures.
- Successful connectivity, testing or ingestion does not prove source truth, compromise, review completion, publication authority, external-share authority, production readiness or production authorization.
- Collected records continue through canonical DTMO normalization/provenance. Existing review, case and sharing authorities remain separate.

## Acceptance scope

11.10j is repository-complete only when `/collection` is wired to the dedicated workspace, source/catalog state and bounded actions are functional through DTMO APIs, deterministic contract/browser coverage and a dedicated exact-head workflow are present, all authoritative documentation is synchronized, and every registered workflow for the final exact head completes successfully.

Repository CI is non-production evidence. Phase 10 remains **NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED**.
