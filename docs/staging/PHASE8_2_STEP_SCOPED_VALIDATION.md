# Phase 8.2 — Step-Scoped Validation

**Status:** `ACTIVE`

## Purpose

Phase 8.2 is executed sequentially from 8.2.1 through 8.2.13. External evidence may therefore be collected and reviewed one validation class at a time before the complete Phase 8.2 manifest is ready.

Step-scoped validation exists only to verify that one named check is internally complete and bound to the same immutable staging deployment identity. It does not grant Phase 8.2 `PASS`, does not replace accountable review of the referenced external evidence and does not permit evidence to be mixed across deployments.

## Required identity fields for every accepted step

Each step-scoped evidence validation requires:

- `environment_id`;
- `phase8_1_identity_fingerprint`;
- `deployed_commit` as a full lowercase 40-character Git SHA;
- `application_image_digest` as an immutable `sha256:` digest;
- `deployment_identity_fingerprint` matching the manifest identity fields;
- `evidence_location_reference`;
- `validated_by`;
- `validated_at`.

The named check must have `result: PASS` and a non-placeholder `evidence_reference`.

## CLI

Validate one check while later Phase 8.2 checks remain `NOT_RUN`:

```bash
python3 tools/phase8_platform_validation.py <manifest.json> --check application_health_readiness
python3 tools/phase8_platform_validation.py <manifest.json> --check postgres_connectivity_migrations
```

Step-scoped validation requires `phase8_2_pass: false` and `phase8_pass: false`.

Validate the complete Phase 8.2 package only after all 12 checks are complete:

```bash
python3 tools/phase8_platform_validation.py <manifest.json>
```

## Current execution order

1. `application_health_readiness` — Phase 8.2.1;
2. `postgres_connectivity_migrations` — Phase 8.2.2;
3. `opensearch_health_search` — Phase 8.2.3;
4. `redis_coordination` — Phase 8.2.4;
5. `object_storage_read_write` — Phase 8.2.5;
6. `bearer_token_trust` — Phase 8.2.6;
7. `rbac_enforcement` — Phase 8.2.7;
8. `human_service_account_separation` — Phase 8.2.8;
9. `privileged_administration_controls` — Phase 8.2.9;
10. `audit_correlation` — Phase 8.2.10;
11. `prometheus_metrics` — Phase 8.2.11;
12. `grafana_dashboards` — Phase 8.2.12;
13. complete manifest/accountable decision — Phase 8.2.13.

## Evidence boundary

Repository CI validates the manifest contract only. A step may be accepted only when the referenced evidence was observed on the owner-approved production-equivalent staging deployment and is attributable to the same immutable deployment identity used for the rest of Phase 8.2.
