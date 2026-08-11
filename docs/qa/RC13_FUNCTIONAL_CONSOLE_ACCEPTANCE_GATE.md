# RC13 — Functional Console Acceptance Gate

Status: `BLOCKED_INTERNAL`

## Trigger

A project-owner functional test of `http://localhost:8000/` on 2026-08-11 found that the repository-controlled product was not yet functionally usable despite the earlier RC12 documentation close-out. This gate supersedes the previous Phase 8 handoff claim until the defects below are corrected and retested.

## Blocking findings

1. **Overview** — no useful graphical/statistical overview is visible by default.
2. **Intelligence** — no usable output is shown because the console has no default/recent intelligence presentation and the source-ingestion flow is not yet operational end to end from the console.
3. **Sources & Catalog** — refresh/register/run controls do not provide a complete working operator journey for the already connected source framework.
4. **Visual analytics** — embedded Grafana requires a separate Grafana authentication context and therefore is not a seamless default console experience.
5. **Administration** — role/user administration is not available from the unified console.
6. **Governance** — the console does not present the governance/control frameworks used by the project, including Normenkader IBP, MITRE ATT&CK and CVSS context.
7. **Navigation copy** — remove the non-user-facing legacy-shell compatibility notice from the menu.
8. **End-to-end data path** — operators must be able to register/activate/run accepted sources, ingest and normalize their records, and immediately see the resulting intelligence and statistics in the same product.

## Required acceptance journey

A fresh local/dev deployment must support the following from the canonical console without using legacy UI routes as the primary workflow:

1. open the canonical console;
2. view useful platform/source/intelligence statistics even when no intelligence has been ingested yet;
3. inspect the connected source catalog and distinguish built-in, registered, enabled, credential-blocked and research-only sources;
4. register supported framework sources from the console;
5. enable/disable eligible sources and update their polling interval;
6. manually execute an eligible source from the console;
7. see fetched/inserted/indexed results and connector health/status;
8. see newly ingested intelligence without requiring a separate external search action;
9. search intelligence when OpenSearch is available, with a canonical-database recent-items view remaining usable independently;
10. view graphical analytics without a separate Grafana login being a prerequisite for core functionality;
11. administer supported DTMO roles/user-role assignments through governed server-side APIs;
12. view the applicable governance frameworks and mappings in the Governance area;
13. retain RBAC, separation of duties, privacy, provenance, auditability, human review and separate share approval.

## RC13.1 — source-to-intelligence functional path

Status: `PASS` within the RC13.1 evidence boundary.

PR #151 merged on 2026-08-11 as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2` after the complete exact-head workflow set passed, including:

- `RC4 Quality Gate` run #803;
- `RC13 Functional Console Browser E2E Gate` run #5;
- the complete registered exact-head workflow set returned by GitHub for head `e881cf5db2a5d6868419425f1c6a7f6017dcfa83`.

RC13.1 accepted:

- canonical `GET /api/v1/console/recent-intelligence` backed by PostgreSQL rather than OpenSearch;
- truthful built-in source handling so CISA manual execution is visible in development when allowed;
- clear framework-source registration, disabled/enabled and runnable states;
- source run completion feedback with fetched/inserted/indexed values;
- automatic refresh of source status, dashboard statistics and recent intelligence after a feed run;
- useful native Overview charts for seven-day intelligence trend, severity and connector health;
- recent intelligence in both Overview and Intelligence without requiring an OpenSearch query;
- removal of the legacy `/ui/*` compatibility notice from the navigation;
- Chromium coverage of register → enable → run → ingest → recent intelligence → updated Overview behavior.

RC13 remains blocked because RC13.2–RC13.5 are not yet accepted.

## RC13.2 — single-session visual analytics

Status: `PENDING_CI`.

RC13.2 makes native DTMO analytics the canonical user-facing Visual analytics surface and removes the separately authenticated Grafana embed from normal console use without weakening Grafana authentication.

Implementation requirements:

- keep severity, source distribution, connector health and review-status native analytics visible in the canonical console;
- suppress the `.grafana-shell` in the shared design-system layer used by the unified console;
- route the RC13.2 design-system response before the legacy frontend CSS route;
- keep `GF_AUTH_ANONYMOUS_ENABLED=false` and `GF_USERS_ALLOW_SIGN_UP=false`;
- do not add a static Grafana user, anonymous role, bypass token or privilege expansion;
- retain Grafana as an authenticated operational/advanced deployment component outside the normal canonical user journey;
- add `RC13 Single-session Visual Analytics Gate` with static contract checks and a Chromium journey;
- require the Chromium journey to verify that native analytics render, Grafana controls are not visible, and normal Visual analytics navigation generates no `/grafana/` request;
- record machine-readable exact-head evidence and fail closed when missing or unsuccessful.

RC13.2 becomes `PASS` only after the complete exact-head workflow set, including `RC13 Single-session Visual Analytics Gate`, succeeds.

## Remaining RC13 slices after RC13.2

- **RC13.3** — governed Administration/RBAC user-role assignment management.
- **RC13.4** — Governance knowledge surface with Normenkader IBP, MITRE ATT&CK, CVSS and related project mappings.
- **RC13.5** — complete canonical-console functional browser acceptance and programme close-out.

## Phase 8 boundary

Phase 8 external staging validation is **paused** until this RC13 functional acceptance gate reaches `PASS`. Repository CI, a successful build, or the existence of UI controls is insufficient: the complete user journey must be executable and covered by browser/API tests on one exact head.

## Release rule

Do not claim `READY_FOR_EXTERNAL_VALIDATION`, production readiness, external staging acceptance or pentest readiness while any blocking finding above remains unresolved.
