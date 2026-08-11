# RC13 — Functional Console Acceptance Gate

Status: `BLOCKED_INTERNAL`

## Trigger

A project-owner functional test of `http://localhost:8000/` on 2026-08-11 found that the repository-controlled product was not yet functionally usable despite the earlier RC12 documentation close-out. This gate supersedes the previous Phase 8 handoff claim until the defects below are corrected and retested.

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
11. administer supported DTMO principal/role assignments through governed server-side APIs;
12. view applicable governance frameworks, actual repository-backed mappings and explicit unmapped/context-only coverage in the Governance area;
13. retain RBAC, separation of duties, privacy, provenance, auditability, human review and separate share approval.

## RC13.1 — source-to-intelligence functional path

Status: `PASS` within the RC13.1 evidence boundary.

PR #151 merged on 2026-08-11 as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2` after complete exact-head success, including RC4 Quality Gate #803 and RC13 Functional Console Browser E2E Gate #5.

Accepted behavior includes truthful source state, register/enable/configure/run operations, ingest/index feedback, PostgreSQL-backed recent intelligence, useful Overview statistics and Chromium coverage of the complete source → intelligence journey.

## RC13.2 — single-session visual analytics

Status: `PASS` within the RC13.2 evidence boundary.

PR #152 merged on 2026-08-11 as `b8c254c5d099cde5dca624aa85b17c320594847e` after the complete exact-head workflow set succeeded, including RC4 Quality Gate #805, RC13 Functional Console Browser E2E Gate #6 and RC13 Single-session Visual Analytics Gate #1.

Accepted behavior keeps native severity, source, connector-health and review-status analytics as the canonical product surface while Grafana remains separately authenticated for advanced/operations use. Normal Visual analytics navigation makes no `/grafana/` request and no authentication bypass was introduced.

## RC13.3 — governed Administration/RBAC

Status: `PASS` within the RC13.3 evidence boundary.

PR #153 merged on 2026-08-11 as `2e1029a43f7b44d8525fb89197d0a10458a3e992`. Exact-head `b828b9b2dbb2f8794bfe7c13ec6e7dd0bdafb22f` completed the full workflow set successfully, including RC4 Quality Gate #809 and RC13 Governed Administration RBAC Gate #3.

Accepted behavior includes persistent managed principals/role assignments, immutable built-in roles, human-admin + `manage:users`, strict service-account isolation, self-management blocking, final-admin protection, tamper-evident mutation auditing, canonical create/update/deactivate UI and truthful external IdP/token-reissue semantics.

## RC13.4 — Governance knowledge surface

Status: `PENDING_CI` / current priority.

The authoritative registry is `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`.

RC13.4 acceptance requires:

- authenticated read-only `GET /api/v1/governance/knowledge`;
- canonical Governance rendering of framework coverage, real DTMO repository mappings and authority boundaries;
- Normenkader IBP visibly `UNMAPPED` until a control-level repository crosswalk exists;
- MITRE ATT&CK visibly `UNMAPPED` until a technique-level repository mapping dataset exists;
- CVSS visibly `CONTEXT_ONLY` while canonical ingest has severity/free metadata but no first-class vector/base-score field;
- internal DTMO governance mappings traceable to `docs/security/SECURITY_OVERVIEW.md` and `docs/traceability/TRACEABILITY_MATRIX.md`;
- no inferred framework/control/technique equivalence;
- a dedicated RC13 Governance Knowledge Surface Gate with repository contract tests and a Chromium Governance journey;
- complete exact-head workflow success before merge.

## Remaining RC13 slice after RC13.4

- **RC13.5** — complete canonical-console functional browser acceptance and programme close-out.

## Phase 8 boundary

Phase 8 external staging validation remains **paused** until the complete RC13 functional acceptance gate reaches `PASS`. Repository CI, a successful build, or the existence of UI controls is insufficient: the complete user journey must be executable and ultimately accepted by the accountable project owner.

## Release rule

Do not claim `READY_FOR_EXTERNAL_VALIDATION`, production readiness, external staging acceptance or pentest readiness while any RC13 blocking finding remains unresolved.
