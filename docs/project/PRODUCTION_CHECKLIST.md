# DTMO Production Acceptance Checklist

Last updated: **2026-08-11**

## Repository-controlled readiness

- [x] Phase 1 — CI/workflow integrity accepted.
- [x] Phase 2 — application security and identity accepted.
- [x] Phase 3 — data integrity and recovery accepted.
- [x] Phase 4 — connector reliability and provenance accepted.
- [x] Phase 5 — performance/scalability accepted.
- [x] Phase 6 — accessibility and operational UX accepted; project-owner manual/external acceptance recorded 2026-08-11.
- [x] Phase 7 — observability and incident operations accepted.
- [ ] RC13 — functional unified-console acceptance complete.
  - [x] RC13.1 — source register/enable/run → ingest/index → recent intelligence → Overview accepted via PR #151.
  - [x] RC13.2 — single-session Visual analytics accepted via PR #152.
  - [x] RC13.3 — governed Administration/RBAC accepted via PR #153.
  - [ ] RC13.4 — Governance knowledge surface accepted.
  - [ ] RC13.5 — complete canonical-console browser acceptance recorded on one exact head.
- [ ] Phase 8 — real staging acceptance complete.
- [ ] Phase 9 — external assurance complete.
- [ ] Phase 10 — production go/no-go approved.

## RC13.3 — governed Administration/RBAC

- [x] `managed_principals` persistence accepted.
- [x] `managed_role_assignments` persistence accepted.
- [x] Migration `0009_managed_rbac_assignments` accepted after `0008_grafana_reporting_views`.
- [x] Built-in role/permission catalog is server-side and immutable from browser input.
- [x] RBAC mutations require `manage:users` and a human `admin` role.
- [x] Service accounts are restricted to only `service_account`.
- [x] Administrator self-management is blocked server-side.
- [x] The last active managed admin cannot be removed or deactivated.
- [x] Create/update mutations append tamper-evident audit events with request IDs.
- [x] Canonical Administration tab can create a principal and assign roles.
- [x] Canonical Administration tab can change roles and activate/deactivate a principal.
- [x] UI makes identity-provider/token reconciliation requirements explicit.
- [x] Active production bearer tokens are never silently rewritten by managed assignment mutations.
- [x] `RC13 Governed Administration RBAC Gate` succeeded on exact head `b828b9b2dbb2f8794bfe7c13ec6e7dd0bdafb22f`.
- [x] Complete registered exact-head workflow set succeeded before PR #153 merge.

## RC13.4 — Governance knowledge surface

- [ ] Authenticated read-only governance API accepted.
- [ ] Canonical Governance pane renders framework coverage.
- [ ] Normenkader IBP is visibly `UNMAPPED` unless a repository control crosswalk exists.
- [ ] MITRE ATT&CK is visibly `UNMAPPED` unless a repository technique mapping dataset exists.
- [ ] CVSS is visibly `CONTEXT_ONLY` while no first-class vector/base-score field exists.
- [ ] Internal DTMO governance mappings have repository provenance.
- [ ] Authority boundaries are visible and do not grant publication/share authority.
- [ ] No external framework equivalence is inferred.
- [ ] `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md` is authoritative and consistent with runtime output.
- [ ] `RC13 Governance Knowledge Surface Gate` succeeds on the exact final PR head.
- [ ] Complete registered exact-head workflow set succeeds before merge.

## Phase 8 — deployment-parity package

**PAUSED_PENDING_RC13.** Do not execute or credit these items until RC13 reaches `PASS`.

All items must refer to the same immutable `16.0.0rc12` staging deployment identity.

- [ ] Approved staging environment identifier and accountable owner.
- [ ] Reachable staging endpoint through approved access path.
- [ ] Immutable deployed application/container image digests and release identity.
- [ ] Infrastructure/runtime versions and configuration-parity evidence.
- [ ] Approved secrets-manager references and least-privilege staging identities.
- [ ] TLS termination/certificate and network-restriction evidence.
- [ ] Production-equivalent data-class/sanitization statement.
- [ ] Explicit no-production-credential confirmation.
- [ ] Deployment/change record tied to immutable release identity.
- [ ] Rollback target/procedure tied to staged release.
- [ ] Deployment-time threat/CVE/vendor-advisory review with provenance, time and confidence.

## Phase 8 — external staging validation

- [ ] Staging smoke tests executed against the approved immutable deployment.
- [ ] Integration tests executed against the approved deployment.
- [ ] Migration validation executed against the approved deployment.
- [ ] Connector validation executed against the approved deployment.
- [ ] Recovery/rollback behavior validated against the approved deployment.
- [ ] Performance behavior validated against the approved deployment.
- [ ] Relevant accessibility/UX journeys validated in staging.
- [ ] Observability/alerting behavior validated in staging.
- [ ] Project-owner Phase 8 staging acceptance recorded.

## Phase 9 — external assurance

- [ ] Independent penetration test completed and findings dispositioned.
- [ ] Representative load/stress test completed.
- [ ] Full production-equivalent backup/restoration exercise completed.
- [ ] Production platform hardening verified, including OpenSearch security.
- [ ] Production secrets-management path accepted; example/default credentials are not used.
- [ ] Operational acceptance recorded by accountable service/security/privacy stakeholders.
- [ ] Required external findings have documented disposition.

## Phase 10 — governance and release controls

- [ ] No unresolved critical/high findings without approved risk disposition.
- [ ] RBAC and least privilege verified for production identities.
- [ ] Separation of duties verified.
- [ ] Human share approval remains separate from review and technical access.
- [ ] Privacy and data minimization reviewed.
- [ ] Provenance and confidence handling verified.
- [ ] Audit logging and correlation verified.
- [ ] No secret values, tokens or unnecessary personal data retained in repository evidence.
- [ ] SBOM/release manifest retained for production release.
- [ ] Deployment manifest tied to immutable release identity.
- [ ] Rollback plan approved and proven.
- [ ] Recovery targets and procedures approved.
- [ ] Incident/runbook ownership accepted.
- [ ] Final production go/no-go decision recorded.

## Decision

Current decision: **NO-GO pending RC13 and Phases 8–10**.

The only current action is RC13.4 repository-backed Governance knowledge. External Phase 8 staging validation remains paused until the complete RC13 functional gate is accepted.
