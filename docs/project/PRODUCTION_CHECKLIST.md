# DTMO Production Readiness Checklist

Last reconciled: **2026-08-15**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8 repository enhancements**

This checklist is the high-level decision control for progressing DTMO from accepted engineering/product maturity through external staging evidence, independent assurance and formal production authorization.

## Evidence rules

A checklist item is complete only when its required evidence exists, is attributable and is reviewable. Configured-but-unexecuted tests, queued/in-progress/skipped/cancelled/failed workflows, stale exact-head evidence, inaccessible evidence, inferred evidence, or synthetic/local evidence presented as external staging/assurance evidence do not count as `PASS`.

Historical evidence remains immutable and scoped to the state/deployment it actually covered.

## 1. Repository-controlled engineering baseline

- [x] CI/workflow integrity and exact-head protected merge discipline.
- [x] Application security, identity and authorization controls.
- [x] Data integrity, migrations and repository recovery contracts.
- [x] Connector reliability, provenance, retry/replay/timeout/failure handling.
- [x] Performance/scalability engineering gates.
- [x] Browser/accessibility/UX gates.
- [x] Observability, alerting and operational runbook gates.
- [x] Open-source governance controls.

**Decision:** Phases 1–7 `PASS`.

## 2. Functional product and E8 baseline

- [x] Unified operator shell accepted.
- [x] Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance accepted functionally.
- [x] Accountable RC13 owner acceptance recorded.
- [x] Shared severity/classification semantics and filters.
- [x] Governed manual source onboarding.
- [x] Native trend/vulnerability analytics.
- [x] Versioned governance/framework mappings.
- [x] Deeper Administration/RBAC management.
- [x] OpenCVE and Vulnerability-Lookup integrations.
- [x] Vulnerability prioritization and vendor/product relevance.
- [x] Governed MISP read and outbound-sharing boundaries.
- [x] Governed AIL read/enrichment/correlation.
- [x] Vulnerability-management evidence mapping with explicit semantic boundaries.

**Decision:** RC13 `PASS / OWNER_ACCEPTED`; E8.1–E8.10 `PASS / REPOSITORY_COMPLETE`.

## 3. Post-E8 staging deployment

- [x] Production-equivalent staging environment exists and is owner-approved.
- [x] Post-E8 deployment was externally and successfully owner-tested.
- [ ] Exact deployed release/commit is bound into the final evidence package.
- [ ] Immutable application and supporting image digests are bound into the final evidence package.
- [ ] Runtime/infrastructure identity and inventory are complete.
- [ ] Configuration parity and approved deviations are complete.
- [ ] Least-privilege IAM/service identities and secret-management references are complete.
- [ ] TLS/network/access-control evidence is complete.
- [ ] Staging data/sanitization and no-production-credential confirmation are complete.
- [ ] Deployment/change, rollback and deployment-time security/CVE review are complete.

## 4. Phase 8.2 — platform and identity validation

Repository contract: **complete**. External acceptance remains required against the same immutable staging identity.

- [ ] Application health/readiness accepted externally.
- [ ] PostgreSQL connectivity/migrations accepted externally.
- [ ] OpenSearch health/search accepted externally.
- [ ] Redis coordination accepted externally.
- [ ] Object-storage read/write/integrity accepted externally.
- [ ] Bearer-token trust boundary accepted externally.
- [ ] RBAC enforcement accepted externally.
- [ ] Human/service-account separation accepted externally.
- [ ] Privileged Administration controls accepted externally.
- [ ] Audit/correlation accepted externally.
- [ ] Prometheus metrics accepted externally.
- [ ] Grafana dashboards/authentication accepted externally.
- [ ] Complete Phase 8.2 evidence package bound to one deployment identity and accepted.

## 5. Phase 8.3 — source-to-intelligence validation

Repository contract: **complete**. External acceptance remains required.

- [ ] Approved real staging source selected and authorized.
- [ ] Real source retrieval observed with provenance/timestamp.
- [ ] Raw evidence retention/reference validated.
- [ ] Canonical normalization and PostgreSQL persistence validated.
- [ ] Deduplication/idempotency validated.
- [ ] OpenSearch visibility validated where applicable.
- [ ] Enrichment/correlation and vulnerability/CTI derivation validated within semantic boundaries.
- [ ] Intended API and canonical UI presentation validated.
- [ ] Severity/classification and governance mappings validated.
- [ ] Audit/correlation traceability validated end-to-end.
- [ ] Degraded upstream behavior is observable and does not fabricate intelligence.
- [ ] Evidence accepted against the same immutable staging identity.

## 6. Phase 8.4 — operations, recovery and rollback

Repository contract: **complete**. External acceptance remains required.

- [ ] Service restart/recovery behavior accepted.
- [ ] PostgreSQL backup/restore and integrity accepted.
- [ ] Object-storage recovery/reconstruction accepted where applicable.
- [ ] OpenSearch recovery/rebuild accepted where applicable.
- [ ] Redis/cache/coordination recovery accepted.
- [ ] Application rollback to an approved prior immutable release demonstrated.
- [ ] Migration recovery/forward-recovery boundaries demonstrated.
- [ ] IAM/secrets continuity after recovery validated.
- [ ] Metrics/logs/audit/correlation continuity validated.
- [ ] Degraded dependency operator visibility validated.
- [ ] RTO/RPO observations and deviations recorded.
- [ ] Change/incident/rollback references recorded and accepted.

## 7. Phase 8.5 — accountable staging acceptance

Repository acceptance contract: **complete**. External accountable decision remains required.

- [ ] One immutable staging deployment identity binds all accepted Phase 8 evidence.
- [ ] Phase 8.2 external evidence acceptance reference recorded.
- [ ] Phase 8.3 external evidence acceptance reference recorded.
- [ ] Phase 8.4 external evidence acceptance reference recorded.
- [ ] Approved deviations and residual staging risks recorded.
- [ ] No unresolved release-blocking staging finding remains.
- [ ] Rollback/change evidence recorded.
- [ ] Accountable owner/reviewer and decision timestamp recorded.
- [ ] Explicit `PASS / OWNER_ACCEPTED` or `BLOCKED` decision recorded.

**Phase 8 is not complete until all items above are satisfied.**

## 8. Phase 9 — independent external assurance

- [ ] Phase 8 is formally `PASS / OWNER_ACCEPTED`.
- [ ] Independent penetration test completed against the accepted candidate.
- [ ] Hardening/configuration review completed.
- [ ] IAM/secrets-management review completed.
- [ ] Representative production-equivalent load/stress validation completed.
- [ ] Resilience/recovery review completed.
- [ ] Monitoring/incident-response readiness reviewed.
- [ ] Privacy/legal/governance reviewed where required.
- [ ] Assurance-time dependency/CVE review completed.
- [ ] Findings triaged with severity, owner and due date.
- [ ] Release-blocking findings remediated and independently retested where required.
- [ ] Residual-risk disposition approved.
- [ ] Final `PASS / EXTERNAL_ASSURANCE_ACCEPTED` record completed.

## 9. Phase 10 — formal production go/no-go

- [ ] Phase 8 evidence complete and accepted.
- [ ] Phase 9 evidence complete and accepted.
- [ ] Open critical/high release-blocking findings resolved or formally dispositioned.
- [ ] Production environment/ownership/support model approved.
- [ ] Production IAM/secrets/network architecture approved.
- [ ] Backup/recovery/rollback plan approved.
- [ ] Monitoring/on-call/escalation model approved.
- [ ] Data/privacy/legal requirements approved.
- [ ] Release/change window approved.
- [ ] Formal accountable production go/no-go decision recorded.

## Current release decision

**Complete and accept Phase 8 external evidence. Do not approve production deployment. Phase 9 independent assurance follows only after Phase 8 formal acceptance.**
