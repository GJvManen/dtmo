# DTMO Current Project State

Last reconciled: **2026-08-11**

## Executive summary

DTMO `16.0.0rc12` has completed the repository-controlled engineering programme through Phase 7. Project-owner functional testing on 2026-08-11 demonstrated that the canonical console still required product-level remediation before external staging, so RC13 remains the active blocking programme.

Accepted RC13 slices:

- **RC13.1** — PR #151 merged as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2`; exact-head source → ingest → intelligence → Overview browser evidence passed.
- **RC13.2** — PR #152 merged as `b8c254c5d099cde5dca624aa85b17c320594847e`; exact-head native single-session analytics evidence passed, including RC4 Quality Gate #805, RC13 Functional Console Browser E2E Gate #6 and RC13 Single-session Visual Analytics Gate #1.

**RC13.3 — governed Administration/RBAC** is the only current priority. DTMO remains **not production ready** and Phase 8 remains `PAUSED_PENDING_RC13`.

## Phase status

| Phase | Status |
|---|---|
| 1. CI and workflow integrity | `PASS` |
| 2. Application security and identity | `PASS` |
| 3. Data integrity and recovery | `PASS` |
| 4. Connector reliability and provenance | `PASS` |
| 5. Performance and scalability | `PASS` |
| 6. Accessibility and operational UX | `PASS` — project-owner manual/external acceptance on 2026-08-11 |
| 7. Observability and incident operations | `PASS` |
| RC13. Functional unified-console acceptance | `BLOCKED_INTERNAL` — RC13.1/13.2 accepted; RC13.3 current |
| 8. Real staging acceptance | `PAUSED_PENDING_RC13` |
| 9. Independent external assurance | `NOT COMPLETE` |
| 10. Production go/no-go | `NOT STARTED` |

## RC13 programme

### RC13.1 — source-to-intelligence functional path

Status: `PASS` within the RC13.1 evidence boundary.

The canonical console now truthfully represents built-in/framework source state, supports register/enable/configure/run operations for accepted adapters, processes source results through canonical ingestion/indexing, shows fetched/inserted/indexed feedback, renders recent PostgreSQL-backed intelligence without requiring OpenSearch search and refreshes useful Overview statistics after ingestion.

### RC13.2 — single-session visual analytics

Status: `PASS` within the RC13.2 evidence boundary.

PR #152 established native DTMO severity, source, connector-health and review-status analytics as the canonical user-facing Visual analytics surface. Normal analytics navigation performs no `/grafana/` request and does not expose a separate-login Grafana embed. Grafana remains available as a separately authenticated advanced/operations component; anonymous access and sign-up remain disabled.

### RC13.3 — Administration/RBAC

Status: `PENDING_CI` / current implementation priority.

The RC13.3 implementation adds:

- persistent `managed_principals` and `managed_role_assignments` records;
- an immutable server-side role catalog derived from `Role` and `ROLE_PERMISSIONS`;
- human-admin + `manage:users` authorization for RBAC administration;
- strict human versus `service_account` assignment validation;
- self-management blocking so an administrator cannot change their own managed assignment;
- last-managed-admin protection against administrative lockout;
- atomic tamper-evident audit events for create/update mutations;
- canonical Administration UI for principal creation, role assignment, activation/deactivation and role inspection;
- explicit identity-provider/token reconciliation semantics: DTMO does not mint or silently rewrite active production bearer-token role claims;
- a dedicated RC13 Governed Administration RBAC Gate covering persistence/security contracts and a Chromium create/update journey.

Built-in security roles remain code-controlled. RC13.3 deliberately does **not** introduce arbitrary custom token roles because production token validation accepts the known `Role` contract and machine principals must remain isolated to `service_account`.

### RC13.4 — Governance knowledge surface

Expose the actual project governance/control context, including Normenkader IBP, MITRE ATT&CK, CVSS and repository-backed mappings, without inventing mappings that are not present in DTMO evidence.

### RC13.5 — full functional acceptance

Execute one complete canonical-console browser journey on one exact head and record accountable project-owner functional acceptance. Only then may Phase 8 return to external-validation readiness.

## Source framework

The operational source adapters remain connected according to `docs/qa/SOURCE_CONNECTION_MATRIX.md`. RC13 does not reopen adapter acceptance; it repairs the operator-facing execution, analytics, administration and governance journeys over the accepted platform baseline.

Credentialed integrations continue to use logical secret references only. Runtime credential values remain outside the catalog, registry and repository evidence.

## Identity and authorization boundary

Production bearer tokens are externally issued and cryptographically validated. The managed RBAC registry records governed desired/provisioned principal-role state but does not rewrite already issued tokens. A role change therefore requires identity-provider reconciliation or token reissue before the external token claim changes.

This boundary prevents the browser Administration interface from becoming a token-forging mechanism and preserves existing issuer/audience/signature validation, token revocation, least privilege and service-account constraints.

## Phase 6 acceptance

Phase 6 remains `PASS`. On 2026-08-11 the project owner explicitly confirmed that the accessibility/operational UX scope had been personally checked and accepted. The repository does not invent unprovided environment/version or recording details.

## Governance boundary

RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, dashboard access, Administration access, CI success or staging access cannot authorize publication.

## Exactly one current priority

**RC13.3 — complete and exact-head accept governed Administration/RBAC.** Phase 8 external staging validation remains paused until all RC13 blocking findings are resolved.
