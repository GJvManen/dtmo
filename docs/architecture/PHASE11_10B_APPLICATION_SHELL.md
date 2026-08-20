# Phase 11.10b — Canonical Application Shell

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**  
Parent stage: **Phase 11.10 — IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED**  
Predecessor: **Phase 11.10a — PASS / REPOSITORY_COMPLETE**

## Purpose

Phase 11.10b implements the browser-shell foundation accepted in Phase 11.10a. It replaces the standalone prototype frontend entry with a separately built React/TypeScript/Vite application and declares `/workbench/` as the canonical browser application route.

This is intentionally a shell slice. Command Center data and feature-specific workspaces are not implemented here; those remain bounded Phase 11.10c–11.10n work.

## Implemented shell boundary

The bounded implementation provides:

- React + TypeScript + Vite build foundation;
- React Router under `/workbench/`;
- TanStack Query request lifecycle for shell server state;
- task-oriented primary navigation following the accepted information architecture;
- persistent global top bar with safe navigation/command palette;
- environment/platform status from the DTMO origin;
- authenticated-principal context from `/api/v1/ui/session` when available;
- object context rail with an explicit no-selection state;
- dark/light semantic theme tokens;
- skip link, visible focus, keyboard command palette, responsive navigation and reduced-motion handling;
- same-origin serving of built assets by FastAPI;
- strict self-origin CSP for the canonical index;
- immutable cache headers for hashed frontend assets;
- `/ui/console` retained only as a migration compatibility path.

## Canonical route and compatibility

The supported route model is:

- `/` → redirect to `/workbench/`;
- `/workbench/...` → canonical React workbench;
- `/ui/console` → temporary compatibility console during bounded migration.

When source-only Python tests run without a built `frontend/dist`, `/workbench/` fails safely to the existing compatibility console. Supported container builds always create and package `frontend/dist` before runtime image construction.

The compatibility fallback exists to keep accepted historical browser contracts testable while the new candidate is built. It is not a second feature-development target.

## Build and supply-chain model

The Docker build has a dedicated frontend build stage. The Node build image is pinned by immutable digest; production runtime remains the existing Python runtime image and receives only the built static assets, not Node/npm tooling.

The final accepted 11.10b state requires:

- committed npm dependency lockfile;
- `npm ci` for the accepted dependency graph;
- exact direct dependency versions;
- frontend dependency audit;
- exact-head typecheck/build;
- deterministic built-asset SHA-256 inventory;
- existing container SBOM/vulnerability gates to continue covering the final runtime image.

## Security and authority invariants

The shell does not change DTMO authority:

**browser → DTMO API → authorization/audit → canonical service → governed adapter → upstream service**.

The browser does not receive upstream service credentials and does not directly invoke Taranis AI, IntelOwl, OpenCTI, MISP, TheHive or Cortex for governed operations.

Role-aware presentation never replaces server-side RBAC. Review, case authority, external share/publication approval, playbook approval and administration remain separate server-side decisions.

The command palette in 11.10b is navigation-only. It cannot execute a high-impact governed action.

## Truthful state boundary

No placeholder number, graph, case, incident, vulnerability, connector state or approval state may be presented as live data. Workspace routes that are not yet implemented explicitly identify their later bounded delivery slice.

The context rail begins with `Geen object geselecteerd` and does not infer facts merely because an integration is configured.

## Accessibility and responsive baseline

The shell establishes:

- semantic navigation/main/context landmarks;
- skip-to-content link;
- visible keyboard focus;
- Ctrl/Cmd+K command palette;
- logical route navigation;
- responsive drawer navigation on small screens;
- context drawer behavior below the desktop layout threshold;
- no colour-only platform status;
- light/dark semantic themes;
- reduced-motion behavior.

Feature-specific WCAG acceptance continues in later slices and Phase 11.10n.

## Evidence boundary

Phase 11.10b repository evidence can prove only the exact-head dependency/build contract, same-origin static serving, shell route behavior, accessibility/responsive shell journey and preserved documentation/security boundaries.

It does **not** prove:

- live upstream integration behavior;
- functional Command Center or later feature workspaces;
- production-equivalent deployment/continuity;
- independent external assurance;
- production authorization.

## Exit criteria

Phase 11.10b may become **PASS / REPOSITORY_COMPLETE** only when:

1. the canonical React shell builds from a committed lockfile;
2. `/` resolves to the built `/workbench/` application in the supported runtime;
3. browser acceptance proves navigation, command palette, context rail and responsive shell behavior;
4. legacy console remains a clearly bounded compatibility path;
5. frontend and container supply-chain gates are green;
6. professional lifecycle, roadmap, QA and evidence documents are synchronized;
7. all registered workflows for the exact final head are completed/success.

After acceptance, the only next bounded priority is **Phase 11.10c — Command Center**.
