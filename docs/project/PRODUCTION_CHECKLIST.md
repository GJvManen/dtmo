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
  - [x] RC13.4 — Governance knowledge surface accepted via PR #154.
  - [ ] RC13.5 — complete canonical-console browser acceptance recorded on one exact head.
  - [ ] accountable project-owner functional retest of the complete repaired local product recorded.
- [ ] Phase 8 — real staging acceptance complete.
- [ ] Phase 9 — external assurance complete.
- [ ] Phase 10 — production go/no-go approved.

## RC13.4 — Governance knowledge surface

- [x] Authenticated read-only governance API accepted.
- [x] Canonical Governance pane renders framework coverage.
- [x] Normenkader IBP is visibly `UNMAPPED` because no repository control crosswalk exists.
- [x] MITRE ATT&CK is visibly `UNMAPPED` because no repository technique mapping dataset exists.
- [x] CVSS is visibly `CONTEXT_ONLY` while no first-class vector/base-score field exists.
- [x] Internal DTMO governance mappings have repository provenance.
- [x] Authority boundaries are visible and do not grant publication/share authority.
- [x] No external framework equivalence is inferred.
- [x] `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md` is authoritative and consistent with runtime output.
- [x] `RC13 Governance Knowledge Surface Gate` succeeded on exact head `0a227cb9f3972504287a6f7f064d6df18b76fbed`.
- [x] Complete registered exact-head workflow set succeeded before PR #154 merge as `21672aaf1cf097228699810660eaac167da842d6`.

## RC13.5 — complete functional browser acceptance

- [ ] `RC13 Full Functional Console Acceptance Gate` succeeds on the exact final PR head.
- [ ] One Chromium browser context covers Overview → Intelligence → Sources & Catalog → Visual analytics → Administration → Governance.
- [ ] Eligible framework source register/enable/run is executed through the canonical console fixture.
- [ ] Source execution result is visible as fetched/inserted/indexed state.
- [ ] Resulting Intelligence and Overview state update in the same browser session.
- [ ] Native severity/source/connector/review analytics render from the resulting state.
- [ ] Normal product navigation makes no `/grafana/` request or second-login dependency.
- [ ] Governed RBAC create/update/deactivate remains functional with unique mutation request IDs.
- [ ] Administrator self-management protection remains visible/enforced.
- [ ] Governance framework coverage, repository mapping provenance and authority boundaries render in the same session.
- [ ] No connector, analytics, Administration or Governance action grants publication authority.
- [ ] Complete registered exact-head workflow set succeeds before merge.
- [ ] After merge, accountable project-owner functional retest of the repaired local product is explicitly accepted.

## Phase 8 — deployment-parity package

**PAUSED_PENDING_RC13.** Do not execute or credit these items until RC13.5 exact-head acceptance and the accountable owner functional retest are both complete.

All items must refer to the same immutable staging deployment identity.

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

Current decision: **NO-GO pending RC13.5, accountable owner retest and Phases 8–10**.

The only current engineering action is RC13.5 complete functional browser acceptance. External Phase 8 staging validation remains paused until the exact-head gate and owner functional retest are both accepted.
