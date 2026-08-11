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
12. view the applicable governance frameworks and mappings in the Governance area;
13. retain RBAC, separation of duties, privacy, provenance, auditability, human review and separate share approval.

## RC13.1 — source-to-intelligence functional path

Status: `PASS` within the RC13.1 evidence boundary.

PR #151 merged on 2026-08-11 as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2` after complete exact-head success, including RC4 Quality Gate #803 and RC13 Functional Console Browser E2E Gate #5.

Accepted behavior includes truthful source state, register/enable/configure/run operations, ingest/index feedback, PostgreSQL-backed recent intelligence, useful Overview statistics and Chromium coverage of the complete source → intelligence journey.

## RC13.2 — single-session visual analytics

Status: `PASS` within the RC13.2 evidence boundary.

PR #152 merged on 2026-08-11 as `b8c254c5d099cde5dca624aa85b17c320594847e` after the complete exact-head workflow set succeeded, including:

- RC4 Quality Gate #805;
- RC13 Functional Console Browser E2E Gate #6;
- RC13 Single-session Visual Analytics Gate #1.

Accepted behavior:

- native severity, source, connector-health and review-status analytics are the canonical product surface;
- normal Visual analytics navigation makes no `/grafana/` request;
- the separately authenticated Grafana shell is not exposed in normal canonical-console use;
- Grafana remains separately authenticated for advanced/operations use;
- Grafana anonymous access and self-signup remain disabled;
- no authentication bypass or privilege broadening was introduced.

## RC13.3 — governed Administration/RBAC

Status: `PENDING_CI` / current priority.

RC13.3 acceptance requires:

- persistent managed principals and managed role assignments;
- immutable built-in role definitions derived from the server-side `Role` and `ROLE_PERMISSIONS` policy;
- `manage:users` plus a human `admin` role for RBAC administration;
- service accounts restricted to `service_account` and never combinable with human/admin roles;
- administrator self-management blocked;
- the final active managed admin protected from removal/deactivation;
- create/update mutations recorded atomically in the existing tamper-evident audit chain with request IDs;
- canonical Administration UI for creating principals, assigning/changing roles and activate/deactivate operations;
- truthful token behavior: DTMO does not silently modify externally issued production bearer tokens; identity-provider reconciliation or token reissue is required;
- arbitrary custom token roles are not creatable from browser input;
- a dedicated `RC13 Governed Administration RBAC Gate` with persistence/security contracts and a real Chromium Administration journey;
- complete exact-head workflow success before merge.

## Remaining RC13 slices after RC13.3

- **RC13.4** — Governance knowledge surface with Normenkader IBP, MITRE ATT&CK, CVSS and repository-backed project mappings.
- **RC13.5** — complete canonical-console functional browser acceptance and programme close-out.

## Phase 8 boundary

Phase 8 external staging validation remains **paused** until the complete RC13 functional acceptance gate reaches `PASS`. Repository CI, a successful build, or the existence of UI controls is insufficient: the complete user journey must be executable and ultimately accepted by the accountable project owner.

## Release rule

Do not claim `READY_FOR_EXTERNAL_VALIDATION`, production readiness, external staging acceptance or pentest readiness while any RC13 blocking finding remains unresolved.
