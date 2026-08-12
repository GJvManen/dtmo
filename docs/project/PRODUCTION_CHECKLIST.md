# DTMO Production Readiness Checklist

Release baseline: **16.0.0rc12**  
Current state: **RC13 accepted; Phase 8 ready to begin**

This checklist is the formal high-level control list for progressing DTMO from the accepted engineering/product baseline to production approval.

## Evidence rules

A checklist item is complete only when its required evidence exists and is reviewable. The following never count as `PASS`:

- configured but unexecuted tests;
- queued/in-progress workflows;
- skipped/cancelled/failed workflows;
- stale evidence from a previous exact PR head;
- inaccessible or inferred evidence;
- synthetic/local evidence presented as real staging/external evidence.

Historical evidence remains immutable. New evidence may supersede the current decision without rewriting history.

## 1. Repository-controlled engineering baseline

- [x] CI/workflow integrity controls accepted.
- [x] Application security and identity controls accepted.
- [x] Data integrity, migration and recovery controls accepted.
- [x] Connector reliability, provenance and failure handling accepted.
- [x] Performance/scalability engineering gates accepted.
- [x] Browser/accessibility/operational UX gates accepted.
- [x] Observability, alerting and operational runbook gates accepted.
- [x] Open-source governance gate accepted.
- [x] Exact-head protected merge discipline established.

**Decision:** Phases 1–7 `PASS`.

## 2. Functional product acceptance

- [x] Unified Overview functions as a usable operator surface.
- [x] Intelligence reads durable canonical application state.
- [x] Sources & Catalog operations function through the canonical console.
- [x] Supported source execution reaches raw evidence, canonical persistence and search/index representation.
- [x] Native Visual Analytics renders canonical analytical state.
- [x] Administration supports governed principal/role assignment operations and safety controls.
- [x] Governance knowledge surface presents truthful framework/mapping state.
- [x] Chrome/browser interaction and truthful empty-data behavior accepted.
- [x] Accountable project-owner functional acceptance recorded.

**Decision:** RC13 `PASS / OWNER_ACCEPTED`.

## 3. Phase 8 — production-equivalent staging identity

### 3.1 Environment identity

- [ ] Approved staging environment identifier.
- [ ] Accountable staging owner.
- [ ] Approved reachable access path / endpoint.
- [ ] Environment purpose/classification documented.

### 3.2 Immutable deployment identity

- [ ] Exact deployed DTMO release recorded.
- [ ] Exact Git commit recorded.
- [ ] Application image digest recorded.
- [ ] Supporting service image digests recorded.
- [ ] Deployment/change record linked to the immutable identity.
- [ ] Rollback target/procedure linked to the same release.

### 3.3 Infrastructure and configuration parity

- [ ] Infrastructure/runtime inventory captured.
- [ ] Database/search/cache/object-storage versions recorded.
- [ ] Configuration parity against approved target documented.
- [ ] Required deviations explicitly risk-assessed and approved.
- [ ] Persistence/backup/restore configuration documented.

### 3.4 Identity, secrets and least privilege

- [ ] Staging application identity is distinct from infrastructure/root identities.
- [ ] Service identities use least-privilege permissions.
- [ ] Human/admin and service-account roles remain separated.
- [ ] Secrets are sourced from approved secret-management mechanisms.
- [ ] No raw secret values are committed to repository evidence.
- [ ] Local-development AIStor root/bootstrap credential exception is not used in staging.
- [ ] No production credentials are present in staging.

### 3.5 Network and transport security

- [ ] TLS endpoint/certificate/termination evidence recorded.
- [ ] Approved ingress/access restrictions recorded.
- [ ] Required egress/source connectivity documented.
- [ ] Administrative/operational access path documented.
- [ ] Grafana remains separately authenticated and not anonymously exposed.

### 3.6 Data handling and privacy

- [ ] Staging data classification documented.
- [ ] Test/sanitized data approach approved.
- [ ] Production personal data is not introduced without explicit approval.
- [ ] Retention/deletion expectations documented.
- [ ] Evidence exports exclude unnecessary personal data and secrets.

### 3.7 Deployment-time security review

- [ ] Application dependency/security review completed for the deployed identity.
- [ ] Container/base-image review completed.
- [ ] Relevant CVE/vendor advisory review completed.
- [ ] Outstanding findings have accountable disposition.

## 4. Phase 8 — deployed functional validation

All checks below must execute against the **same immutable staging deployment identity**.

- [ ] Health/readiness endpoints accepted.
- [ ] Authentication and authorization validated with approved staging identity provider/configuration.
- [ ] Source catalog/bootstrap validated.
- [ ] Supported source execution validated.
- [ ] Raw evidence persistence validated.
- [ ] Canonical PostgreSQL intelligence persistence validated.
- [ ] OpenSearch indexing/search validated.
- [ ] Overview/Intelligence/Visual Analytics validated.
- [ ] Administration/RBAC boundaries validated.
- [ ] Governance/read-only knowledge boundary validated.
- [ ] Review/external-share separation validated.
- [ ] Operational metrics/alerts/dashboard access validated.
- [ ] Backup/restore or agreed staging recovery evidence completed.
- [ ] Accountable staging acceptance recorded.

**Phase 8 may be marked `PASS` only after this evidence is complete and consistent.**

## 5. Phase 9 — independent external assurance

- [ ] Independent penetration test completed.
- [ ] Findings triaged and remediated/accepted by accountable owners.
- [ ] Representative production-equivalent load/stress validation completed.
- [ ] Recovery/restore validation independently reviewed where required.
- [ ] Platform/container/runtime hardening independently reviewed.
- [ ] Secrets-management/IAM model independently reviewed.
- [ ] Operational monitoring/incident-response readiness reviewed.
- [ ] Legal/privacy/governance requirements independently reviewed where required.
- [ ] Residual-risk statement approved.

## 6. Phase 10 — formal production go/no-go

- [ ] Phase 8 evidence complete and accepted.
- [ ] Phase 9 evidence complete and accepted.
- [ ] Open critical/high production-blocking findings resolved or formally dispositioned.
- [ ] Production environment/ownership/support model approved.
- [ ] Production IAM/secrets/network architecture approved.
- [ ] Backup/recovery and rollback plan approved.
- [ ] Monitoring/on-call/escalation model approved.
- [ ] Data/privacy/legal requirements approved.
- [ ] Release/change window approved.
- [ ] Formal accountable stakeholder go/no-go decision recorded.

## 7. Post-RC13 product enhancements

These improvements are planned but are **not prerequisites for preserving the accepted RC13 baseline unless a later change introduces a regression**:

- [ ] shared severity semantics and informational/low/medium/high filters;
- [ ] manual governed source onboarding;
- [ ] richer trend analysis;
- [ ] first-class framework mapping model;
- [ ] richer role/permission Administration;
- [ ] deeper Governance framework/evidence views.

Any enhancement included in a future production candidate must itself satisfy the applicable exact-head, staging and assurance gates.

## Current release decision

**Proceed to Phase 8.1 staging identity/evidence. Do not approve production deployment yet.**
