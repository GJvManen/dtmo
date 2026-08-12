# DTMO Current Project State

Last reconciled: **2026-08-12**

## Executive summary

DTMO `16.0.0rc12` has accepted repository-controlled engineering through Phase 7.

PR #169 completed the latest bounded RC13 repair for supported-source normalization. Final exact head `53aaa670c75a2f404337620bcf1a8df172efe583` completed every returned workflow with `completed/success` and merged as `4d182879d851cd22d22ff4f0bab795ed49ee0c1b`.

The repair preserves the HTTP(S)-only canonical URL boundary, uses stable NVD HTTPS CVE detail pages for canonical/provenance, retains raw upstream references, maps only supported alias `security-advisory` to canonical `advisory`, rejects unknown item types fail-closed and preserves PR #167 commit-before-success behavior.

The initial #169 CI pass exposed a README-only governance regression. Commit `53aaa670c75a2f404337620bcf1a8df172efe583` restored the required Apache/governance entry points and the complete final exact-head matrix passed.

Post-merge connector status handling created three additional commits on `main`, including an immediately restored README write. Compare `4d182879d851cd22d22ff4f0bab795ed49ee0c1b` -> `1fd006b8568a53c1171b9d127d50037ad0027568` returns `files: []`; the current repository tree is identical to the #169 merge.

**RC13 = `AWAITING_OWNER_RETEST_AFTER_REPAIR`.**

**Phase 8 = `PAUSED_PENDING_RC13_OWNER_RETEST`.**

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
| RC13. Functional unified-console acceptance | `AWAITING_OWNER_RETEST_AFTER_REPAIR` |
| 8. Real staging acceptance | `PAUSED_PENDING_RC13_OWNER_RETEST` |
| 9. Independent external assurance | `NOT COMPLETE` |
| 10. Production go/no-go | `NOT STARTED` |

## Valid recent repair evidence

- PR #159 console usability — repository-controlled PASS.
- PR #160 Compose runtime packaging — repository-controlled PASS.
- PR #161 Grafana datasource provisioning — repository-controlled PASS.
- PR #163 source catalog secret-reference/bootstrap — repository-controlled PASS and later owner-observed bootstrap 200.
- PR #165 local object-store credential contract — repository-controlled PASS; merged `65440afea6cfa3c3300b25d577d746432cc95700`.
- PR #167 canonical connector commit/console visibility — repository-controlled PASS; merged `e9a0926f9e13b603be759a7d7036058685ebc3cc`.
- PR #169 supported-source normalization — repository-controlled PASS; exact head `53aaa670c75a2f404337620bcf1a8df172efe583`; complete returned workflow matrix `completed/success`; merged `4d182879d851cd22d22ff4f0bab795ed49ee0c1b`.

Historical evidence remains immutable. Newer owner-observed evidence controls current readiness.

## Documentation lineage

PR #168 was closed without merge because newer owner evidence superseded its post-#167 reconciliation. Branch-only RUN-205 never became authoritative on `main`. RUN-206 remains immutable point-in-time evidence. RUN-207 records the post-#169 repository acceptance, the connector status-handling incident and the transition back to owner-retest pending.

## Required owner retest

Verify on current `main`:

1. local Compose startup/Grafana/API remain healthy;
2. source catalog and source operations remain functional;
3. NVD completes without FTP canonical/provenance validation failure;
4. Chrome, Mozilla, NCSC and other supported advisory sources do not fail on `security-advisory` enum mismatch;
5. raw evidence persists successfully;
6. canonical PostgreSQL intelligence commits successfully;
7. recent Intelligence appears in the canonical console;
8. Overview KPIs and dashboard summary update truthfully;
9. severity/source/trend/review graphics render from those records;
10. `Alles vernieuwen`, Chrome controls, Administration and truthful empty states remain functional;
11. authorization, human review and separate external-share approval boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

## Phase 8 boundary

Issue #158 remains paused. No real staging, independent assurance or production-readiness progression is allowed until RC13 receives explicit accountable owner acceptance. The staging least-privilege identity model remains unchanged and separate from local-development credential exceptions.

## Security and governance boundaries

RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, analytics, Administration, Governance, CI or staging access cannot authorize publication.

## Exactly one current priority

**Run the accountable project-owner RC13 functional retest on current `main` and record the source-to-interface result.**
