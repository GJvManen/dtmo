# DTMO Current Project State

Last reconciled: **2026-08-12**

## Executive summary

DTMO `16.0.0rc12` has accepted repository-controlled engineering through Phase 7. PR #167 repaired the canonical connector commit boundary, completed every returned workflow on exact head `bf18ef2c499edcf8399d1f91b80190937538fdce`, and merged as `e9a0926f9e13b603be759a7d7036058685ebc3cc`.

The subsequent accountable owner retest confirms the repair moved source ingestion further: local services start, Grafana and API are healthy, source/admin/read endpoints return 200, and multiple documents are created in `dtmo-intelligence-v1` with OpenSearch `201 Created` responses.

The same retest exposes a narrower repository-controlled blocker before complete source-to-interface acceptance:

1. NVD can supply a non-HTTP `ftp://` external reference. Using that external reference as the canonical/provenance URL violates the intentional HTTP(S)-only canonical ingest schema and produces an `IntelligenceIngestRequest` validation error.
2. Supported advisory adapters can emit `security-advisory`, while the canonical persisted `IntelligenceType` enum uses `advisory`, producing an SQLAlchemy enum/statement failure.

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

## Valid recent repair evidence

- PR #159 console usability — repository-controlled PASS.
- PR #160 Compose runtime packaging — repository-controlled PASS.
- PR #161 Grafana datasource provisioning — repository-controlled PASS.
- PR #163 source catalog secret-reference/bootstrap — repository-controlled PASS and later owner-observed bootstrap 200.
- PR #165 local object-store credential contract — repository-controlled PASS; merged `65440afea6cfa3c3300b25d577d746432cc95700`.
- PR #167 canonical connector commit/console visibility — repository-controlled PASS; exact head `bf18ef2c499edcf8399d1f91b80190937538fdce`; merged `e9a0926f9e13b603be759a7d7036058685ebc3cc`.

Historical evidence remains immutable. Newer owner-observed evidence controls current readiness.

## Current bounded repair — supported-source normalization

The repair branch `rc13/source-record-normalization-contract` keeps normalization at the canonical connector boundary:

- explicit supported alias `security-advisory` normalizes to canonical `advisory`;
- canonical enum values pass unchanged;
- unknown connector item types remain fail-closed;
- NVD CVE canonical/provenance URLs use the stable HTTPS `https://nvd.nist.gov/vuln/detail/<CVE>` page even when raw NVD references include FTP or another non-HTTP scheme;
- raw upstream NVD references remain preserved in raw evidence;
- the existing HTTP(S)-only `HttpUrl` security boundary is not relaxed;
- PR #167 commit-before-success behavior remains covered.

A dedicated `RC13 Source Record Normalization Gate` covers the normalization regressions together with source adapter, connector ingestion, canonical console and graphical dashboard contracts.

No repository PASS is claimed until every returned workflow on the final exact PR head is `completed/success`.

## Documentation lineage

PR #168 was closed without merge because this newer owner evidence superseded its post-#167 owner-retest-pending reconciliation. Its branch-only RUN-205 is not authoritative on `main`. RUN-204 remains immutable historical evidence. RUN-206 records the new owner evidence and current repair decision.

## Required owner retest after repair

After the repair is exact-head green and merged, verify on current merged `main`:

1. local Compose startup/Grafana/API remain healthy;
2. source catalog and source operations remain functional;
3. NVD completes without FTP canonical/provenance validation failure;
4. Chrome, Mozilla, NCSC and other supported advisory sources do not fail on `security-advisory` enum mismatch;
5. raw evidence persists successfully;
6. canonical PostgreSQL intelligence commits successfully;
7. recent Intelligence appears in the canonical console;
8. Overview KPIs and dashboard summary update truthfully;
9. severity/source/trend/review graphics render from those records;
10. `Alles vernieuwen`, Chrome controls, Administration and true empty states remain functional;
11. authorization/publication boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

## Phase 8 boundary

Issue #158 remains paused. No real staging, independent assurance or production-readiness progression is allowed while RC13 is blocked. The staging least-privilege identity model remains unchanged and separate from local-development credential exceptions.

## Security and governance boundaries

RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, analytics, Administration, Governance, CI or staging access cannot authorize publication.

## Exactly one current priority

**Complete the supported-source normalization repair, require complete exact-head CI, merge, then resume accountable project-owner RC13 functional retesting.**
