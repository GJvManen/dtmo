# DTMO Canonical Frontend Architecture

Status: **Phase 11.10a–11.10e — PASS / REPOSITORY_COMPLETE; Phase 11.10f — IN PROGRESS / OPENCTI GRAPH ENTITY WORKSPACE**  
Last updated: **2026-08-20**

## 1. Purpose

This document is the accepted architecture baseline for the DTMO Unified Operations Workbench. Phase 11.10a established the frontend, information-architecture, design-system and browser/API contracts. **Phase 11.10b implemented the canonical shell**, Phase 11.10c delivered the Command Center, Phase 11.10d delivered governed intelligence discovery/investigation, Phase 11.10e delivered governed IntelOwl/Cortex analysis, and Phase 11.10f is the active migration of persisted OpenCTI graph/entity context.

The objective remains one maintainable canonical browser application while preserving security, authority, provenance and evidence boundaries already accepted elsewhere in DTMO.

## 2. Architectural decision

The canonical browser application uses:

- **React** for composable application views;
- **TypeScript** for typed frontend contracts;
- **Vite** for deterministic frontend development/build tooling;
- **React Router** for canonical client-side navigation;
- **TanStack Query** for governed server-state retrieval, cache invalidation and request state;
- a DTMO-owned component/design-system layer using CSS design tokens;
- bounded graph and analytical visualization adapters only when their feature slices are accepted.

The direct frontend dependency set remains exact-pinned and the npm lockfile committed. Third-party packages remain subject to DTMO licensing, dependency and supply-chain controls; browser inclusion does not collapse upstream service or licensing boundaries.

## 3. Canonical trust path

The browser is never a privileged integration broker. The canonical path is:

```mermaid
flowchart LR
    U[User browser] --> FE[DTMO frontend]
    FE --> API[DTMO FastAPI API]
    API --> AUTH[DTMO authorization + audit]
    AUTH --> CORE[Canonical DTMO services]
    CORE --> PG[(PostgreSQL)]
    CORE --> OS[(OpenSearch)]
    CORE --> OBJ[(Object storage)]
    CORE --> EXT[Governed integration adapters]
    EXT --> TAR[Taranis AI]
    EXT --> OWL[IntelOwl]
    EXT --> OCTI[OpenCTI]
    EXT --> MISP[MISP]
    EXT --> HIVE[TheHive]
    EXT --> CTX[Cortex]
```

### Invariant

**Browser → DTMO API → governed integration adapter → upstream service** is mandatory for normal product operations.

The browser must not directly invoke Taranis AI, IntelOwl, OpenCTI, MISP, TheHive or Cortex for governed product workflows. Advanced upstream administration can remain an explicitly separate operational escape hatch where required, but it is not the canonical DTMO product path and cannot bypass DTMO authorization, provenance or evidence controls.

## 4. Application shell

The canonical shell contains four persistent regions:

1. **Primary navigation** — stable navigation grouped by operator intent rather than service ownership.
2. **Global command/status bar** — navigation/command palette, environment health and principal context.
3. **Main workspace** — task-specific content delivered incrementally in 11.10c–11.10n.
4. **Context rail/drawer** — selected-object facts and governed actions without losing the current workspace.

Phase 11.10b accepted these regions under `/workbench/`. The command palette remains navigation-safe; high-impact operations require their own accepted server contracts. The context rail remains fail-closed when no attributable selection exists.

## 5. Delivered and target capability workspaces

The accepted information architecture includes:

- Command Center — accepted in 11.10c;
- Threat Intelligence — accepted in 11.10d;
- IOC Explorer — accepted in 11.10d;
- Knowledge Graph — active functional migration in 11.10f;
- Exposure — 11.10i;
- Investigations — 11.10h;
- Analysis & Enrichment — accepted in 11.10e;
- Sharing & Exchange — 11.10g;
- Automation & Playbooks — 11.10k;
- Collection — 11.10j;
- Governance & Evidence — 11.10l;
- Operations and Administration — 11.10m.

A route foundation is not feature acceptance and must not display fabricated operational metrics or state.

## 6. Object-centric interaction model

A canonical intelligence object, IOC, CVE, threat actor, campaign, source, case or other governed entity can be selected from compatible workspaces. The common context model supports, where attributable, canonical identity, severity/classification, confidence, provenance/markings, linked intelligence, enrichment/analysis state, relationships, cases/tasks, sharing/approval state, audit timeline and actions allowed to the current principal.

Phase 11.10d established deep object investigation: search hits remain discovery projections while selected detail/provenance comes separately from canonical DTMO persistence. Phase 11.10e extended the object context into persisted analysis history.

Phase 11.10f extends object context into OpenCTI graph/entity evidence. `/workbench/intelligence/graph?item=<uuid>` retrieves persisted mapping context from DTMO. Browser state never becomes graph evidence and OpenCTI is not queried directly by the browser.

## 7. Frontend state model

### 7.1 Server state

Canonical state is retrieved from DTMO APIs. TanStack Query manages request lifecycle and stale-state behavior. Browser caches never become authoritative product state.

### 7.2 URL state

Workspace, object identity, filters, pagination and safe investigation context should be URL-addressable where practical without embedding secrets. The `item` query parameter carries only canonical UUID context for analysis/graph deep links.

### 7.3 Ephemeral UI state

Drawer visibility, local sort direction, temporary form state and presentation preferences may remain client-local. Only non-sensitive preferences such as theme may be persisted locally.

### 7.4 Security-sensitive state

Credentials, API secrets, private keys, upstream tokens and approval authority are never ordinary persistent frontend state. Production authentication follows the configured identity/bearer-token trust model and server-side authorization remains authoritative.

## 8. Authorization and authority boundaries

Role-aware rendering is a usability feature, not a security control. Every governed operation remains server-authorized.

The frontend preserves:

- least privilege;
- **server-side RBAC**;
- **human/service identity separation**;
- read-only auditor behavior;
- administrator self-protection and final-admin protections;
- case-handoff authority separate from publication/share authority;
- human review and external-share approval separation;
- **no local-compromise inference** from enrichment/graph presence;
- no publication authority from a connector call, analyzer result, MISP match, OpenCTI mapping/relationship or TheHive case.

Phase 11.10d search/canonical detail require `read:intelligence`. Phase 11.10e analysis history/capabilities require `read:intelligence` while explicit IntelOwl/Cortex execution requires `review:intelligence`. Phase 11.10f OpenCTI capability/graph/entity detail is read-only and requires `read:intelligence`.

## 9. API and integration boundary

The detailed browser/API contract is `docs/architecture/UI_API_CONTRACT.md`.

All frontend capabilities must either reuse an existing governed `/api/v1/...` endpoint with required authorization/audit semantics or add a bounded DTMO API contract in the same feature slice before the UI depends on it.

Current accepted/active examples are:

- `/health` and `/api/v1/ui/session` for shell context;
- `/api/v1/command-center` for accepted 11.10c operational orientation;
- `/api/v1/intelligence/search` and `/api/v1/intelligence/{item_id}/workspace` for accepted 11.10d discovery/detail;
- `/api/v1/analysis/capabilities`, `/api/v1/analysis/items/{item_id}/history`, `/api/v1/intelowl/items/{item_id}/enrich` and `/api/v1/analysis/items/{item_id}/cortex` for accepted 11.10e analysis;
- `/api/v1/opencti/capabilities`, `/api/v1/opencti/items/{item_id}/graph` and `/api/v1/opencti/entities/{mapping_id}` for active 11.10f read-only OpenCTI graph/entity evidence.

None makes the browser an upstream service client.

## 10. OpenCTI graph safety boundary

OpenCTI remains a separate upstream service behind the accepted DTMO integration/persistence boundary.

- feature/configuration state is not live-health evidence;
- the browser receives no OpenCTI token and does not invoke `/graphql`;
- canonical DTMO item identity is the graph root;
- graph/entity nodes derive from persisted OpenCTI/STIX mappings;
- the current persistence boundary does not durably store generic OpenCTI entity-to-entity relationship topology;
- only proven `canonical-mapping` edges are rendered;
- missing topology must **fail closed** and cannot be inferred from labels, entity types, co-occurrence or visual proximity;
- empty persisted mapping state is not proof of upstream absence;
- graph/entity presence, confidence or markings do not prove local exposure, exploitability, compromise or attribution certainty;
- existing persistence carries no external-share authority and no local-compromise proof.

## 11. Design-system boundary

The visual and interaction contract is `docs/ux/DESIGN_SYSTEM.md`. The workbench baseline includes semantic tokens, dark operations and accessible light modes, consistent surfaces, skip link/visible keyboard focus, responsive navigation/context behavior, reduced-motion handling, non-colour-only state and explicit loading/degraded/empty truth rather than synthetic data.

## 12. Migration from current UI

The migration is incremental and bounded:

1. Phase 11.10a architecture/design contracts — `PASS / REPOSITORY_COMPLETE`.
2. Phase 11.10b canonical application shell — `PASS / REPOSITORY_COMPLETE`.
3. Phase 11.10c Command Center — `PASS / REPOSITORY_COMPLETE`.
4. Phase 11.10d Unified Intelligence Workspace — `PASS / REPOSITORY_COMPLETE`.
5. Phase 11.10e IntelOwl/Cortex integrated analysis — `PASS / REPOSITORY_COMPLETE`.
6. **Phase 11.10f OpenCTI graph/entity workspace** — active.
7. Phase 11.10g–11.10n migrate remaining capabilities one bounded slice at a time.
8. Phase 11.10o performs consolidation/full functional acceptance and retires obsolete UI paths where safe.
9. Phase 11.10p executes fresh production-equivalent validation only after immutable candidate freeze.

The declared canonical built product route is `/workbench/`. `/ui/console` and prior UI routes remain temporary migration compatibility paths, not parallel feature-development targets.

## 13. Build and deployment contract

The accepted build contract requires exact-pinned direct dependencies in `frontend/package.json`, committed `frontend/package-lock.json`, `npm ci`, TypeScript checking before Vite build, hashed assets/no production source maps, separate immutable Node build stage, no Node/npm in final Python runtime, only `frontend/dist` in supported runtime, same-origin FastAPI serving, strict self-origin CSP, immutable hashed-asset caching, exact-head frontend asset evidence and continued final-container SBOM/vulnerability/artifact-attestation controls.

This build integration creates no second browser ingress or upstream credential path.

## 14. Observability and truthful failure

The browser distinguishes authentication/authorization failure, validation failure, upstream dependency degradation, canonical backend failure, empty canonical data and stale/read-only degraded mode.

For 11.10f specifically:

- OpenCTI configuration is not rendered as live service health;
- an empty persisted mapping set is not represented as global OpenCTI absence;
- missing graph/entity detail remains unavailable rather than reconstructed from incomplete display data;
- unpersisted relationship topology is not synthesized;
- repository/browser fixtures remain engineering evidence, not operational evidence.

Server-side correlation/request IDs remain authoritative for governed actions.

## 15. Accessibility

The accepted shell baseline provides semantic navigation/main/context regions, skip-to-content, visible focus, keyboard route navigation and Ctrl/Cmd+K palette, responsive reflow/mobile navigation, dark/light semantic themes, reduced-motion handling and non-colour-only status treatment.

Phase 11.10f adds responsive graph/entity composition and a keyboard-accessible entity list as an equivalent navigation surface alongside SVG. Full role-aware and feature-specific WCAG 2.2 AA acceptance remains Phase 11.10n plus final 11.10o consolidation.

## 16. Evidence boundary

Phase 11.10a–11.10e repository/browser acceptance remains accepted within each bounded scope. Phase 11.10f exact-head CI may prove read-only OpenCTI graph/entity routes, persisted mapping/revision rendering, explicit topology limitation, browser/API trust boundaries and fail-closed behavior within repository-controlled scope.

None proves completeness or health of live upstream integrations, production-equivalent deployment/continuity, independent external assurance or production authorization. The graphical reference remains a design target, not operational evidence.

## 17. Lifecycle and exit

Phase 11.10a–11.10e are **`PASS / REPOSITORY_COMPLETE`**.

Phase 11.10f may become **`PASS / REPOSITORY_COMPLETE`** only when the frontend build and dedicated repository/browser contract are green on one exact final head, existing security/accessibility/integration/runtime/supply-chain regressions remain green, and all professional lifecycle documentation is synchronized.

The only next bounded slice after 11.10f acceptance and merge is **Phase 11.10g — MISP Sharing & Exchange**.
