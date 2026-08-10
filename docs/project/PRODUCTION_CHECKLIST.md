# DTMO Production Acceptance Checklist

Last updated: 2026-08-10

## Repository-controlled readiness

- [x] Phase 1 CI/workflow integrity accepted.
- [x] Phase 2 application security and identity internal gates accepted.
- [x] Phase 3 data integrity and recovery internal gates accepted.
- [x] Phase 4 connector reliability and provenance internal gates accepted.
- [x] Phase 5 performance/scalability internal gates accepted.
- [ ] Phase 6 genuine VoiceOver/NVDA real-environment evidence complete.
- [x] Phase 7 observability and incident operations accepted.
- [ ] Phase 8 real staging acceptance complete.
- [ ] Phase 9 external assurance complete.
- [ ] Phase 10 production go/no-go approved.

## Phase 8 deployment-parity prerequisites

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

## Phase 8 acceptance execution

- [ ] Staging smoke tests executed against approved deployment.
- [ ] Integration tests executed against approved deployment.
- [ ] Migration validation executed against approved deployment.
- [ ] Connector validation executed against approved deployment.
- [ ] Recovery/rollback executed against approved deployment.
- [ ] Performance validation executed against approved deployment.
- [ ] Accessibility validation executed against approved deployment.
- [ ] Observability/alerting validation executed against approved deployment.

## Phase 9 external assurance

- [ ] Independent penetration test completed and findings dispositioned.
- [ ] Representative load/stress test completed.
- [ ] Full backup/restoration exercise completed.
- [ ] Production platform hardening verified, including OpenSearch security.
- [ ] Example credentials replaced through approved secrets-management path.
- [ ] Operational acceptance recorded by accountable service/security/privacy stakeholders.
- [ ] Staging deployment acceptance recorded.
- [ ] Production deployment acceptance recorded.

## Governance and release controls

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

Current decision: **NO-GO** until every blocking checkbox above has objective evidence or an explicitly approved risk disposition where policy permits.
