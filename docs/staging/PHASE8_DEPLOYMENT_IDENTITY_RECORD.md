# Phase 8 External Deployment Identity Record

**Decision:** `PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`  
**Phase 8 entry state:** `READY_FOR_EXTERNAL_VALIDATION`

## Purpose

This record is the authoritative fail-closed Phase 8.1 intake surface for the first real approved production-equivalent staging deployment.

Repository preparation, Docker Compose and staging-emulator evidence do not populate external deployment facts. Values must be based on the real approved staging environment or deployment platform.

## Machine-readable state

```yaml
decision: PENDING_EXTERNAL_DEPLOYMENT_IDENTITY
evidence_complete: false
phase8_pass: false
release_target: 16.0.0rc12
accepted_repository_baseline_at_phase8_entry: 514b59809838317be8213bafc7422710663634e8
rc13_functional_acceptance: PASS_OWNER_ACCEPTED
environment_id: NOT_PROVIDED
accountable_staging_owner: NOT_PROVIDED
approved_endpoint: NOT_PROVIDED
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
external_validation_started: false
project_owner_staging_acceptance: NOT_RECORDED
```

## Evidence rules

1. `environment_id`, approved endpoint, deployed commit and container digests must refer to the same deployment.
2. The deployed identity must be immutable and independently observable from the real staging environment or approved deployment platform.
3. No secret value, bearer token, password, API key or unnecessary personal data may be committed to this record.
4. Logical secret-manager and identity references are allowed; secret values are not.
5. Local Docker Compose, application-container smoke tests, GitHub Actions emulators and source-controlled intent are supporting evidence only.
6. A `NOT_PROVIDED`, inaccessible, contradictory, stale or inferred field blocks the corresponding acceptance claim.
7. A later redeployment requires a new deployment identity/evidence binding; evidence may not be mixed across identities.
8. Phase 8 may not become `PASS` until deployment-parity evidence and deployed-environment acceptance suites are complete against this same identity and accountable staging acceptance is recorded.

## Identity and least-privilege requirements

Staging must use a deployment-appropriate identity model:

- application/service identities are separate from AIStor/database/platform root/admin identities;
- human/admin and service-account roles remain separated;
- credential values come from approved secret-management mechanisms;
- repository evidence records references/identifiers only;
- the local-development AIStor root/bootstrap credential compatibility exception is not propagated into staging;
- production credentials are not reused.

## Initial evidence sequence

Populate and independently verify, in order:

1. approved staging environment identifier;
2. accountable staging owner;
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

Only after the identity is coherent should deployed functional, operational and recovery suites be credited.

## Phase 8 acceptance suites

Evidence must then cover, against this identity:

- platform health/readiness;
- authentication/RBAC;
- source catalog and source execution;
- raw evidence storage;
- canonical PostgreSQL persistence;
- OpenSearch index/search behavior;
- Overview/Intelligence/Visual Analytics;
- Administration/Governance authority boundaries;
- observability/operations;
- agreed recovery/rollback validation;
- accountable staging acceptance.

## Publication authority boundary

Staging ownership, deployment access, CI success or infrastructure administration never grants intelligence publication or external-share authority. Existing RBAC, human review and separate share approval remain authoritative.
