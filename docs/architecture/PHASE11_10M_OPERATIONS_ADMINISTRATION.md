# Phase 11.10m — Operations & Administration

Status: **IN PROGRESS / REPOSITORY-CONTROLLED IMPLEMENTATION**

## Objective

Phase 11.10m makes the canonical `/operations` and `/administration` workspaces functional through DTMO-owned APIs while preserving the accepted runtime, RBAC, provenance, separation-of-duties and fail-closed boundaries established through Phase 11.10l.

This slice does **not** authorize production, does not convert repository CI into production-equivalent evidence, and does not reuse historical Phase 8/9 evidence as proof for the materially changed Phase 11.10 candidate. Phase 10 remains **NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED**.

## Canonical trust paths

Operations visibility follows:

`browser -> DTMO same-origin API -> canonical runtime/observability data -> attributable presentation`

Administration follows:

`browser -> DTMO same-origin administration API -> server-side RBAC/policy enforcement -> auditable governed mutation`

Browser code never receives service-to-service credentials. Credentials, connector secrets and production bearer material remain server-side references or deployment-managed secrets.

## Operations workspace

The `/operations` workspace may expose only attributable repository/runtime observations already available through DTMO-owned endpoints, including platform health, environment identity, operational dashboard summaries, integration/runtime observation state and links to governed runbooks.

Missing or inaccessible observations must render as unavailable/unknown. DTMO must not infer healthy service state, zero incidents, successful recovery, production readiness or production-equivalent operation from configuration, workflow success, connector enablement or absent telemetry.

Operational actions that mutate connectors, cases, sharing state, identities, infrastructure or production remain outside this read-oriented surface unless an existing server-authorized action explicitly governs them.

## Administration workspace

The `/administration` workspace reuses the accepted server-side RBAC administration contract. It may list the immutable role catalogue and managed principals and may expose principal create/update actions only where the server authorizes the caller.

Required boundaries:

- role definitions remain server-controlled; the browser cannot mint arbitrary roles or permissions;
- service accounts cannot acquire human review/share/publication authority outside policy;
- self-management protections remain server-side;
- mutating requests carry unique request identifiers and remain auditable;
- role changes do not silently prove production identity-provider/token reconciliation;
- browser visibility does not grant administration authority.

## Evidence and acceptance

Repository acceptance requires deterministic contract tests, Chromium browser acceptance, a dedicated exact-head workflow, synchronized professional documentation and a final unchanged head for which every registered workflow is `completed/success`.

Repository CI is engineering evidence only. It does not prove production-equivalent deployment, independent assurance, owner acceptance or production authorization.

## Next boundary

After accepted Phase 11.10m, exactly the next bounded priority is **Phase 11.10n role-aware UX/accessibility**. Phase 11.10o consolidation/full functional acceptance follows; Phase 11.10p production-equivalent validation is prohibited until 11.10a–11.10o are complete and one immutable candidate is frozen.
