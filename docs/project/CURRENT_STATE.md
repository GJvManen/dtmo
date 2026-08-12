# DTMO Current Project State

Last reconciled: **2026-08-12**

## Executive summary

DTMO `16.0.0rc12` has accepted repository-controlled engineering through Phase 7. Repository-controlled RC13 repairs #159–#161 remain valid.

The latest accountable owner local retest progressed beyond both recent startup blockers: `grafana-db-provision` exited with code 0, the API and Prometheus started, and Grafana 13.1.0 started without the former duplicate-default datasource restart loop.

The same retest then exposed a new repository defect: supported source-catalog bootstrap returns HTTP 500 because the Cisco catalog/runtime use the executable logical secret reference `env:CISCO_OPENVULN_TOKEN`, while the source registry rejected that syntax at write time.

**RC13 = `REOPENED / BLOCKED_INTERNAL`.**

**Phase 8 = `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`.**

DTMO remains **not production ready**.

## Phase status

| Phase | Status |
|---|---|
| 1. CI and workflow integrity | `PASS` |
| 2. Application security and identity | `PASS` |
| 3. Data integrity and recovery | `PASS` |
| 4. Connector reliability and provenance | `PASS` |
| 5. Performance and scalability | `PASS` |
| 6. Accessibility and operational UX | `PASS` |
| 7. Observability and incident operations | `PASS` |
| RC13. Functional unified-console acceptance | `REOPENED / BLOCKED_INTERNAL` |
| 8. Real staging acceptance | `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST` |
| 9. Independent external assurance | `NOT COMPLETE` |
| 10. Production go/no-go | `NOT STARTED` |

## Latest owner-retest evidence

### Confirmed resolved in the observed startup path

- PR #160 runtime packaging: the former `/app/tools/provision_grafana_reader.py` file-not-found failure did not recur; `grafana-db-provision` exited 0.
- PR #161 Grafana provisioning: Grafana started without `Only one datasource per organization can be marked as default` and without the former restart loop.
- migrations completed successfully;
- the API reached application startup complete;
- Prometheus reached ready state;
- gateway configuration completed.

This is owner-observed functional evidence for those bounded startup repairs. It is not full RC13 acceptance.

## Current RC13 blocker — source catalog bootstrap

The owner retest invoked the supported source-catalog bootstrap endpoint and received HTTP 500.

Repository inspection confirms the mismatch:

1. `backend/dtmo/source_catalog.py` defines Cisco's credential reference as `env:CISCO_OPENVULN_TOKEN`;
2. `backend/dtmo/credentialed_source_executor.py` resolves `env:VARIABLE` at runtime;
3. `backend/dtmo/sources.py` previously accepted only `vault://`, `secret://` and `env://` when writing registry entries.

That means one code-reviewed supported catalog entry was valid for its runtime executor but invalid for the registry used by `/api/v1/admin/sources/catalog/bootstrap`.

## Current repair state

The bounded branch `rc13/source-catalog-secret-ref-contract`:

- introduces one logical secret-reference validator/canonicalizer;
- accepts canonical executable `env:VARIABLE` references;
- normalizes legacy `env://VARIABLE` input to `env:VARIABLE`;
- retains opaque `vault://` and `secret://` references;
- rejects raw secrets and malformed references;
- makes the credentialed executor use the same canonicalization boundary;
- tests every supported catalog secret reference against registry validation;
- tests idempotent supported catalog bootstrap with all bootstrapped sources disabled by default;
- adds `RC13 Source Catalog Bootstrap Gate` with exact-head evidence.

The repair is `PENDING_CI`. No pass is claimed until every returned workflow on the final exact PR head is `completed/success`.

## Environment/configuration boundary

The same local log contains a MinIO `InvalidAccessKeyId` during a source run. The owner had explicitly identified the local `.env` as incorrect and instructed that configuration point to be skipped. It is therefore not classified here as a repository defect. The run also does not prove successful source ingestion.

## Historical RC13 repair evidence

- PR #159 console usability: repository-controlled `PASS`; merged as `b4fffecc47f87b1edab8258514eaa130d949c195`.
- PR #160 Compose runtime packaging: repository-controlled `PASS`; merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`.
- PR #161 Grafana datasource provisioning: repository-controlled `PASS`; final exact head `e471d6368639a45cee6dccadd353a9068e5205e9`; merged as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`.

Historical evidence is not rewritten; newer owner-observed evidence controls the current readiness decision.

## Phase 8 boundary

The Phase 8 intake/deployment identity record from PR #157 remains fail-closed preparatory evidence. Issue #158 remains paused. No real staging, pentest or production-readiness progression is allowed while RC13 is blocked.

## Security and governance boundaries

Credentialed integrations store logical secret references only; raw secret values remain forbidden. Production bearer tokens remain externally issued. RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, analytics, Administration, Governance, CI or staging access cannot authorize publication.

## Exactly one current priority

**Complete the source catalog secret-reference contract repair, require complete exact-head CI, merge, then resume accountable project-owner RC13 local functional retesting.**
