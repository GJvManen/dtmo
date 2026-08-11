# DTMO Current Project State

Last reconciled: **2026-08-11**

## Executive summary

DTMO `16.0.0rc12` has completed the repository-controlled engineering programme through Phase 7. Project-owner functional testing on 2026-08-11 demonstrated that the canonical console still required product-level remediation before external staging, so RC13 remains the active blocking programme.

Accepted RC13 slices:

- **RC13.1** — PR #151 merged as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2`; exact-head source → ingest → intelligence → Overview browser evidence passed.
- **RC13.2** — PR #152 merged as `b8c254c5d099cde5dca624aa85b17c320594847e`; exact-head native single-session analytics evidence passed.
- **RC13.3** — PR #153 merged as `2e1029a43f7b44d8525fb89197d0a10458a3e992`; exact-head governed Administration/RBAC evidence passed on head `b828b9b2dbb2f8794bfe7c13ec6e7dd0bdafb22f`, including RC4 Quality Gate #809 and RC13 Governed Administration RBAC Gate #3.

**RC13.4 — Governance knowledge surface** is the only current priority. DTMO remains **not production ready** and Phase 8 remains `PAUSED_PENDING_RC13`.

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
| RC13. Functional unified-console acceptance | `BLOCKED_INTERNAL` — RC13.1/13.2/13.3 accepted; RC13.4 current |
| 8. Real staging acceptance | `PAUSED_PENDING_RC13` |
| 9. Independent external assurance | `NOT COMPLETE` |
| 10. Production go/no-go | `NOT STARTED` |

## RC13 programme

### RC13.1 — source-to-intelligence functional path

Status: `PASS` within the RC13.1 evidence boundary.

The canonical console truthfully represents framework source state, supports register/enable/configure/run operations, processes results through canonical ingestion/indexing, shows fetched/inserted/indexed feedback, renders recent PostgreSQL-backed intelligence and refreshes useful Overview statistics.

### RC13.2 — single-session visual analytics

Status: `PASS` within the RC13.2 evidence boundary.

Native DTMO severity, source, connector-health and review-status analytics are the canonical user-facing Visual analytics surface. Normal analytics navigation performs no `/grafana/` request. Grafana remains a separately authenticated advanced/operations component; anonymous access and self-signup remain disabled.

### RC13.3 — Administration/RBAC

Status: `PASS` within the RC13.3 evidence boundary.

Accepted behavior includes persistent managed principals/role assignments, immutable built-in roles, human-admin + `manage:users` authorization, strict service-account isolation, administrator self-management blocking, last-managed-admin lockout protection, tamper-evident mutation auditing, canonical create/update/deactivate UI and explicit identity-provider/token reconciliation semantics. DTMO does not mint or silently rewrite active production bearer-token claims.

### RC13.4 — Governance knowledge surface

Status: `PENDING_CI` / current implementation priority.

RC13.4 adds a read-only authenticated governance snapshot and canonical Governance knowledge surface backed by `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`.

Coverage is intentionally truthful:

- **Normenkader IBP** — `UNMAPPED`; no control-level repository crosswalk exists yet.
- **MITRE ATT&CK** — `UNMAPPED`; no technique-level repository mapping dataset exists yet.
- **CVSS** — `CONTEXT_ONLY`; canonical ingest has `severity` and free `metadata`, but no first-class CVSS vector/base-score field.
- **DTMO security & release governance** — `MAPPED_INTERNAL`; six internal governance mappings point to concrete sections in `docs/security/SECURITY_OVERVIEW.md` and `docs/traceability/TRACEABILITY_MATRIX.md`.

The console also exposes non-negotiable authority boundaries and never infers missing external framework equivalences.

### RC13.5 — full functional acceptance

Execute one complete canonical-console browser journey on one exact head and record accountable project-owner functional acceptance. Only then may Phase 8 return to external-validation readiness.

## Source framework

The operational source adapters remain connected according to `docs/qa/SOURCE_CONNECTION_MATRIX.md`. RC13 does not reopen adapter acceptance; it repairs the operator-facing execution, analytics, administration and governance journeys over the accepted platform baseline.

Credentialed integrations continue to use logical secret references only. Runtime credential values remain outside the catalog, registry and repository evidence.

## Identity and authorization boundary

Production bearer tokens are externally issued and cryptographically validated. The managed RBAC registry records governed desired/provisioned principal-role state but does not rewrite already issued tokens. A role change therefore requires identity-provider reconciliation or token reissue before the external token claim changes.

## Phase 6 acceptance

Phase 6 remains `PASS`. On 2026-08-11 the project owner explicitly confirmed that the accessibility/operational UX scope had been personally checked and accepted. The repository does not invent unprovided environment/version or recording details.

## Governance boundary

RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, dashboard access, Administration access, Governance visibility, CI success or staging access cannot authorize publication.

## Exactly one current priority

**RC13.4 — exact-head accept the repository-backed Governance knowledge surface.** Phase 8 external staging validation remains paused until all RC13 blocking findings are resolved.
