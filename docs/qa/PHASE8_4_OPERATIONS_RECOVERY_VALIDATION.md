# Phase 8.4 — Operations, Recovery and Rollback Validation

**Status:** `PREPARED / EXTERNAL EXECUTION REQUIRES ACCEPTED PRIOR PHASE IDENTITY`

## Objective

Validate operational resilience, recovery and rollback on the same immutable post-E8 production-equivalent staging deployment used for Phases 8.2 and 8.3. Repository CI, Docker-only recovery tests and synthetic fixtures are supporting evidence only.

## Entry conditions

- owner-approved production-equivalent staging exists;
- Phase 8.2 external evidence is accepted;
- Phase 8.3 source-to-intelligence evidence is accepted;
- the same immutable deployment fingerprint is available;
- no production credentials or unsanitized production data are used.

## Required validation chain

1. **Service recovery** — restart representative application/runtime services and verify readiness plus state continuity.
2. **PostgreSQL backup/restore** — demonstrate backup, restore and integrity on staging evidence.
3. **Object storage recovery** — where applicable, demonstrate backup/restore or reconstruction and integrity.
4. **OpenSearch recovery** — where applicable, demonstrate recovery/rebuild without fabricated intelligence.
5. **Cache/queue recovery** — verify Redis/coordination recovery, stale-state handling and idempotent continuation.
6. **Application rollback** — demonstrate rollback to an approved prior immutable release and controlled return forward.
7. **Migration recovery** — verify database migration rollback/forward-recovery boundaries and document irreversible migrations.
8. **IAM/secrets continuity** — verify service identities, authorization and secret references remain correct after recovery.
9. **Observability continuity** — verify metrics, logs, audit records and correlation identifiers across failure/recovery.
10. **Degraded dependencies** — verify operators can see dependency failure and DTMO does not invent or silently fabricate intelligence.
11. **RTO/RPO observations** — record measured recovery/data-loss observations and deviations from operational targets.
12. **Change/rollback evidence** — record change, incident or rollback references, reviewer and timestamps.

## Evidence manifest

Use `docs/staging/PHASE8_4_OPERATIONS_RECOVERY_EVIDENCE.template.json`. Store restricted evidence references rather than secrets or raw credentials.

Validate with:

```bash
python3 tools/phase8_4_operations_recovery_validation.py <manifest.json>
```

## Acceptance

`PASS / OWNER_ACCEPTED` requires a complete validator-clean manifest, all checks `PASS`, non-placeholder evidence references, reviewer/timestamp, and identity binding to the same immutable deployment used for accepted Phase 8.2/8.3 evidence. Evidence from different deployments must not be combined.

`phase8_pass` remains false until Phase 8.5 accountable staging acceptance is also complete.

Related: #243, #241, #239, #158, PR #242.
