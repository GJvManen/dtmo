# DTMO Production Acceptance Checklist

Last updated: **2026-08-12**

## Repository-controlled and functional readiness

- [x] Phase 1 — CI/workflow integrity accepted.
- [x] Phase 2 — application security and identity accepted.
- [x] Phase 3 — data integrity and recovery accepted.
- [x] Phase 4 — connector reliability and provenance accepted.
- [x] Phase 5 — performance/scalability accepted.
- [x] Phase 6 — accessibility and operational UX accepted.
- [x] Phase 7 — observability and incident operations accepted.
- [ ] RC13 — functional unified-console acceptance currently complete.
  - [x] RC13.1–RC13.5 historical repository evidence complete.
  - [x] Earlier project-owner acceptance recorded on 2026-08-12.
  - [ ] Subsequent owner-observed Overview refresh defect repaired.
  - [ ] Empty-data status is truthful and never reports false update success.
  - [ ] Chrome button/navigation regression evidence succeeds with zero page/console errors.
  - [ ] Menu version badge removed.
  - [ ] Administration reorganized around governed users/roles.
  - [ ] Zero-only graph datasets render explicit empty states.
  - [ ] Complete exact-head workflow matrix succeeds on final repair head.
  - [ ] Repair merged with expected-head protection.
  - [ ] Accountable project-owner functional retest explicitly accepted after merge.
- [ ] Phase 8 — real staging acceptance complete.
- [ ] Phase 9 — external assurance complete.
- [ ] Phase 10 — production go/no-go approved.

## Current RC13 decision

`REOPENED / BLOCKED_INTERNAL`.

The prior `RC13 owner retest akkoord` remains historical evidence, but a subsequent owner retest found blocking canonical-console defects. Newer owner-observed evidence governs current readiness.

## Phase 8

Current decision: **`PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`**.

The fail-closed external deployment identity record from PR #157 remains preparatory evidence. Issue #158 is paused. No external staging evidence is credited while RC13 is reopened.

When Phase 8 resumes, all evidence must refer to the same immutable production-equivalent staging deployment identity:

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
- [ ] Deployment-time threat/CVE/vendor-advisory review.
- [ ] Project-owner Phase 8 staging acceptance.

## Phase 9 — external assurance

- [ ] Independent penetration test completed and findings dispositioned.
- [ ] Representative load/stress test completed.
- [ ] Full production-equivalent backup/restoration exercise completed.
- [ ] Production platform hardening verified, including OpenSearch security.
- [ ] Production secrets-management path accepted.
- [ ] Operational acceptance recorded by accountable service/security/privacy stakeholders.

## Phase 10 — governance and release controls

- [ ] No unresolved critical/high findings without approved risk disposition.
- [ ] RBAC and least privilege verified for production identities.
- [ ] Separation of duties verified.
- [ ] Human share approval remains separate from review and technical access.
- [ ] Privacy and data minimization reviewed.
- [ ] Provenance and confidence handling verified.
- [ ] Audit logging and correlation verified.
- [ ] No secret values, tokens or unnecessary personal data retained in repository evidence.
- [ ] Final production go/no-go decision recorded.

## Decision

Current decision: **NO-GO pending reopened RC13 acceptance and Phases 8–10**.

The only current priority is **issue #150 — canonical-console usability repair and owner retest**.
