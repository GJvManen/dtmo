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

Status: `PENDING_CI`.

The current RC13.1 branch implements:

- canonical `GET /api/v1/console/recent-intelligence` backed by PostgreSQL rather than OpenSearch;
- truthful built-in source handling so CISA manual execution is visible in development even when its scheduler feature flag is disabled;
- clear framework-source registration, disabled/enabled and runnable states;
- source run completion feedback with fetched/inserted/indexed values;
- automatic refresh of source status, dashboard statistics and recent intelligence after a feedrun;
- useful native Overview charts for seven-day intelligence trend, severity and connector health;
- recent intelligence in both Overview and Intelligence without requiring an OpenSearch query;
- native analytics as the default core Visual analytics experience, while Grafana is loaded only when an advanced dashboard is explicitly opened;
- removal of the legacy `/ui/*` compatibility notice from the navigation;
- a dedicated Chromium browser workflow that clicks register → enable → run and verifies that the resulting intelligence and Overview statistics appear.

RC13.1 becomes `PASS` only after the complete exact-head workflow set, including `RC13 Functional Console Browser E2E Gate`, succeeds.

## Remaining RC13 slices after RC13.1

- **RC13.2** — finalize single-session/default visual analytics behavior and advanced Grafana boundary.
- **RC13.3** — governed Administration/RBAC user-role assignment management.
- **RC13.4** — Governance knowledge surface with Normenkader IBP, MITRE ATT&CK, CVSS and related project mappings.
- **RC13.5** — complete canonical-console functional browser acceptance and programme close-out.

## Phase 8 boundary

Phase 8 external staging validation is **paused** until this RC13 functional acceptance gate reaches `PASS`. Repository CI, a successful build, or the existence of UI controls is insufficient: the complete user journey must be executable and covered by browser/API tests on one exact head.

## Release rule

Do not claim `READY_FOR_EXTERNAL_VALIDATION`, production readiness, external staging acceptance or pentest readiness while any blocking finding above remains unresolved.
