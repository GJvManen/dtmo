# Phase 8.2.2 — PostgreSQL Connectivity and Migration Validation

**Status:** `READY_FOR_EXTERNAL_EXECUTION`

## Objective

Validate PostgreSQL connectivity and migration state on the owner-approved production-equivalent staging deployment and bind the result to the same immutable deployment identity used by Phase 8.2.

## Preconditions

- owner-approved post-E8 staging deployment exists;
- Phase 8.2 is active;
- exact environment/deployed commit/application image identity must be captured before formal acceptance;
- PostgreSQL evidence must come from the approved staging runtime, not CI containers or local Docker Compose.

## Required checks

1. application can establish the expected PostgreSQL connection using the staging service identity;
2. connection uses the configured staging database endpoint and does not rely on production credentials;
3. current Alembic revision is observable;
4. database schema is at the expected repository migration head for the deployed release;
5. no unapplied or divergent migration state is present;
6. a read/write transaction succeeds with rollback or disposable evidence data so validation does not alter governed production-like content;
7. connection/migration evidence is timestamped and attributable to the accountable reviewer;
8. evidence reference contains no password, token, connection secret or unnecessary personal data.

## Evidence manifest mapping

Record the result in:

```json
"postgres_connectivity_migrations": {
  "result": "PASS",
  "evidence_reference": "restricted-evidence://..."
}
```

Validate the completed step with:

```bash
python3 tools/phase8_platform_validation.py <manifest.json> --check postgres_connectivity_migrations
```

## Acceptance

`PASS` requires successful external PostgreSQL connectivity and migration-state validation on the approved staging deployment, with evidence bound to the same immutable deployment fingerprint used by the rest of Phase 8.2.

Repository migration tests and RC4 PostgreSQL restore tests remain supporting regression evidence only and cannot substitute for this deployed-environment check.

## Next step

After 8.2.2 acceptance, proceed to **8.2.3 — OpenSearch health/search** against the same deployment identity.
