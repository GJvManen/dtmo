# Phase 8 External Deployment Identity Record

**Decision:** `OWNER_VERIFIED_EXTERNAL_DEPLOYMENT / IMMUTABLE_IDENTITY_BINDING_INCOMPLETE`  
**Phase 8 state:** `ACTIVE_EXTERNAL_VALIDATION`

## Purpose

This record is the authoritative fail-closed intake surface for the approved production-equivalent post-E8 staging deployment.

Repository preparation, Docker Compose and staging-emulator evidence do not populate external deployment facts. Values must be based on the real approved staging environment or deployment platform.

## 2026-08-15 owner evidence update

The accountable owner confirmed that:

- the post-E8 external deployment has been extensively and successfully tested; and
- the production-equivalent staging environment is approved.

This closes the prerequisite requiring a real external deployment and approved staging environment before Phase 8.2 can begin. It does not by itself establish the exact deployed commit, image digests or runtime identity. Those fields remain fail-closed until observed from the accepted deployment/deployment platform and bound to the same evidence package.

## Machine-readable state

```yaml
decision: OWNER_VERIFIED_EXTERNAL_DEPLOYMENT_IDENTITY_BINDING_INCOMPLETE
evidence_complete: false
phase8_pass: false
repository_reference_at_owner_update: 4e08bce5f73fa828d0748db1e14b82b95c602adb
rc13_functional_acceptance: PASS_OWNER_ACCEPTED
e8_repository_state: PASS_REPOSITORY_COMPLETE
external_deployment_owner_test: PASS_OWNER_VERIFIED
staging_environment_approval: PASS_OWNER_VERIFIED
environment_id: NOT_PROVIDED
accountable_staging_owner: NOT_PROVIDED
approved_endpoint: NOT_PROVIDED
deployed_release: NOT_PROVIDED
deployed_commit: NOT_PROVIDED
application_image_digest: NOT_PROVIDED
supporting_container_digests: NOT_PROVIDED
infrastructure_runtime_inventory: NOT_PROVIDED
configuration_parity_record: NOT_PROVIDED
secrets_manager_identity_references: NOT_PROVIDED
least_privilege_staging_identities: NOT_PROVIDED
tls_certificate_or_termination_evidence: NOT_PROVIDED
network_restriction_evidence: NOT_PROVIDED
data_class_and_sanitization_statement: NOT_PROVIDED
no_production_credentials_confirmation: NOT_PROVIDED
deployment_change_record: NOT_PROVIDED
rollback_target_and_procedure: NOT_PROVIDED
deployment_time_security_review: NOT_PROVIDED
external_validation_started: true
phase8_2_status: IN_PROGRESS
phase8_5_accountable_acceptance: NOT_RECORDED
```

`repository_reference_at_owner_update` identifies repository state at the time this record was updated; it is **not** asserted to be the deployed commit. `deployed_commit` remains authoritative for that external fact and stays `NOT_PROVIDED` until observed.

## Evidence rules

1. `environment_id`, approved endpoint, deployed commit and container digests must refer to the same accepted deployment.
2. The deployed identity must be immutable and independently observable from the real staging environment or approved deployment platform.
3. No secret value, bearer token, password, API key or unnecessary personal data may be committed to this record.
4. Logical secret-manager and identity references are allowed; secret values are not.
5. Local Docker Compose, application-container smoke tests, GitHub Actions emulators and source-controlled intent are supporting evidence only.
6. A `NOT_PROVIDED`, inaccessible, contradictory, stale or inferred field blocks the corresponding **formal immutable-identity acceptance claim**, but does not erase separately recorded owner evidence that the real deployment was tested and staging approved.
7. A later material redeployment requires a new deployment identity/evidence binding; evidence may not be mixed across identities.
8. Phase 8 may not become `PASS` until deployment-parity evidence and deployed-environment acceptance suites are complete against this same identity and accountable Phase 8.5 acceptance is recorded.

## Identity and least-privilege requirements

Staging must use a deployment-appropriate identity model:

- application/service identities are separate from infrastructure root/admin identities;
- human/admin and service-account roles remain separated;
- credential values come from approved secret-management mechanisms;
- repository evidence records references/identifiers only;
- local-development credential compatibility exceptions are not propagated into staging;
- production credentials are not reused.

## Evidence completion sequence

Without changing the already accepted deployment unless technically required, capture and verify:

1. approved staging environment identifier;
2. accountable staging owner reference;
3. approved reachable endpoint/access path;
4. exact deployed release/commit;
5. immutable application/supporting image digests;
6. infrastructure/runtime inventory;
7. configuration parity/deviations;
8. IAM/secrets references;
9. TLS/network controls;
10. data/sanitization/no-production-credential statement;
11. deployment/change and rollback records;
12. deployment-time security review.

The controlled collection procedure is [`PHASE8_IMMUTABLE_IDENTITY_INTAKE.md`](PHASE8_IMMUTABLE_IDENTITY_INTAKE.md). Its `tools/phase8_identity_manifest.py` collector is intentionally fail-closed: it validates manifest completeness and immutable identifier formats but does not manufacture or infer external staging facts.

Phase 8.2 platform/identity evidence may be collected in parallel, but it cannot receive formal `PASS` until it is bound coherently to this same immutable deployment identity.

## Phase 8 acceptance suites

Evidence must cover, against this identity:

- platform health/readiness and dependencies;
- authentication/RBAC and identity separation;
- source catalog and source execution;
- raw evidence storage and canonical persistence;
- OpenSearch index/search behavior;
- Overview/Intelligence/Visual Analytics;
- Administration/Governance authority boundaries;
- observability/operations;
- agreed recovery/rollback validation;
- accountable staging acceptance.

## Publication authority boundary

Staging ownership, deployment access, CI success or infrastructure administration never grants intelligence publication or external-share authority. Existing RBAC, human review and separate share approval remain authoritative.
