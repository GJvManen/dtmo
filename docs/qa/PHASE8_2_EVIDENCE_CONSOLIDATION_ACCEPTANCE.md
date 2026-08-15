# Phase 8.2.13 — Evidence Consolidation and Acceptance

**Status:** `ACTIVE / EVIDENCE_CONSOLIDATION`

## Purpose

Phase 8.2.13 closes the Phase 8.2 production-equivalent staging validation only after all twelve external validation classes are complete and attributable to the same owner-approved, immutable Phase 8.2 deployment identity.

Repository CI and synthetic fixtures are supporting evidence only. They do not replace direct evidence from the approved staging deployment.

## Required immutable identity

The complete evidence package must contain one consistent set of:

- `environment_id`;
- `phase8_1_identity_fingerprint`;
- `deployed_commit` as a full lowercase 40-character Git SHA;
- `application_image_digest` as an immutable `sha256:` digest;
- `supporting_image_digests` where applicable;
- `deployment_identity_fingerprint` matching the identity fields;
- `evidence_location_reference`;
- `validated_by`;
- `validated_at`.

Evidence from different deployments, redeployments, image digests or staging identities must not be combined into one accepted Phase 8.2 package.

## Required Phase 8.2 checks

All twelve checks must be present with `result: PASS` and a non-placeholder `evidence_reference`:

1. `checks.application_health_readiness`;
2. `checks.postgres_connectivity_migrations`;
3. `checks.opensearch_health_search`;
4. `checks.redis_coordination`;
5. `checks.object_storage_read_write`;
6. `checks.bearer_token_trust`;
7. `checks.rbac_enforcement`;
8. `checks.human_service_account_separation`;
9. `checks.privileged_administration_controls`;
10. `checks.audit_correlation`;
11. `checks.prometheus_metrics`;
12. `checks.grafana_dashboards`.

Each evidence reference must point to restricted evidence appropriate to the check, without exposing secrets, bearer tokens or credentials in the repository.

## Complete validator

After all twelve checks are complete, set:

```json
"phase8_2_pass": true,
"phase8_pass": false
```

Then execute:

```bash
python3 tools/phase8_platform_validation.py <manifest.json>
```

The validator must return `Phase 8.2 platform and identity evidence: PASS` and the resulting `deployment_identity_fingerprint` must match the accepted package.

`phase8_pass` remains `false` because Phase 8.3, 8.4 and 8.5 still require acceptance against the same immutable staging deployment identity.

## Accountable review

The accountable reviewer must verify that:

- all twelve referenced results were observed on the owner-approved production-equivalent staging deployment;
- all evidence is attributable to the same immutable Phase 8.2 deployment;
- no evidence was copied from an older candidate or mixed across deployments;
- the evidence package contains no repository-visible secrets;
- any deviation is explicitly documented and accepted before Phase 8.2 can close.

## Acceptance

Phase 8.2.13 is `PASS / OWNER_ACCEPTED` only when the complete manifest passes the validator, every referenced external result is attributable to the same immutable deployment identity and the accountable reviewer accepts the evidence package.

Fail closed if any identity field, check result, evidence reference or accountable review item is missing or inconsistent.

Related: Issue #239, Issue #158, PR #212, PR #238.
