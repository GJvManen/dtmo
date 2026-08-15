# Phase 8.3 — Source-to-Intelligence Validation

**Status:** `PREPARED / EXTERNAL EXECUTION REQUIRES ACCEPTED PHASE 8.2 IDENTITY`

## Objective

Validate one real approved staging source end-to-end on the same immutable post-E8 staging deployment used for Phase 8.2. The chain must be attributable from upstream retrieval through canonical persistence and analyst-visible intelligence. Repository CI, synthetic fixtures and isolated connector tests are supporting evidence only.

## Entry conditions

- owner-approved production-equivalent staging environment exists;
- Phase 8.2 complete external evidence package is accepted;
- the exact Phase 8.2 deployment identity/fingerprint is available;
- the selected source/feed is approved for staging use;
- no production credentials are reused.

If the Phase 8.2 immutable deployment identity is not accepted, Phase 8.3 external PASS is blocked.

## Required validation chain

1. **Approved source** — record source identifier/type and approval reference.
2. **Retrieval** — trigger or observe a real staging fetch and record retrieval timestamp/provenance.
3. **Raw evidence** — confirm upstream/raw evidence is retained or referenced according to the DTMO evidence contract.
4. **Normalization** — confirm the payload becomes a canonical DTMO record with source provenance preserved.
5. **Idempotency/deduplication** — replay or re-observe representative material and confirm no fabricated duplicate intelligence is created.
6. **Persistence** — confirm canonical PostgreSQL persistence and, where applicable, OpenSearch indexing/search visibility.
7. **Enrichment/correlation** — confirm applicable enrichment/correlation behavior and semantic boundaries.
8. **Vulnerability/CTI derivation** — where supported by the source, verify CVSS/EPSS/KEV/vendor/product/CWE/sighting or CTI meaning without overclaiming source semantics.
9. **Presentation** — verify resulting intelligence through the intended API and canonical UI surfaces.
10. **Governance/classification** — verify severity/classification and applicable framework mappings remain consistent with provenance.
11. **Traceability** — verify audit/request/correlation identifiers permit end-to-end tracing.
12. **Degraded path** — verify an unavailable/failed upstream is visible and does not fabricate stale or invented intelligence.

## Evidence manifest

Use `docs/staging/PHASE8_3_SOURCE_INTELLIGENCE_EVIDENCE.template.json` as the fail-closed schema. Populate restricted evidence references rather than secrets, bearer tokens or raw credentials.

Validate with:

```bash
python3 tools/phase8_3_source_intelligence_validation.py <manifest.json>
```

## Acceptance

`PASS / OWNER_ACCEPTED` requires:

- the manifest is complete and validator-clean;
- `phase8_2_deployment_identity_fingerprint` identifies the same accepted immutable staging deployment used for Phase 8.2;
- all required chain checks are `PASS` with non-placeholder evidence references;
- reviewer and timestamp are recorded;
- no evidence is mixed across deployments;
- external staging behavior, not repository CI alone, supports the result.

`phase8_pass` remains false until Phase 8.4 and Phase 8.5 are also accepted.

Related: #241, #239, #158, PR #240.
