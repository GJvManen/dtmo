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

## Phase 8 boundary

Phase 8 external staging validation is **paused** until this RC13 functional acceptance gate reaches `PASS`. Repository CI, a successful build, or the existence of UI controls is insufficient: the complete user journey must be executable and covered by browser/API tests on one exact head.

## Release rule

Do not claim `READY_FOR_EXTERNAL_VALIDATION`, production readiness, or external pentest readiness while any blocking finding above remains unresolved.
