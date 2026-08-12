# DTMO Current Project State

Last reconciled: **2026-08-12**

## Executive summary

DTMO `16.0.0rc12` has accepted repository-controlled engineering through Phase 7. The subsequent RC13 product-repair sequence is also repository-green through PR #161:

- PR #159 repaired owner-observed console usability defects;
- PR #160 repaired the missing Grafana database-reader provisioner in the canonical runtime image;
- PR #161 repaired duplicate Prometheus datasource provisioning that caused Grafana 13.1.0 restart loops.

PR #161 final exact head `e471d6368639a45cee6dccadd353a9068e5205e9` completed every returned workflow successfully and merged with expected-head protection as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`.

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

## RC13 repair evidence

### PR #159 — console usability

Repository-controlled `PASS`; merged as `b4fffecc47f87b1edab8258514eaa130d949c195`.

Scope included truthful refresh/no-data behavior, Chrome interaction coverage, clearer Administration, graph empty states and removal of the navigation version badge.

### PR #160 — Compose runtime packaging

Repository-controlled `PASS`; merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`.

The canonical image now contains `tools/provision_grafana_reader.py`, and the runtime packaging gate verifies the required file boundary.

### PR #161 — Grafana datasource provisioning

Repository-controlled `PASS`; final exact head `e471d6368639a45cee6dccadd353a9068e5205e9`; merged as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`.

The obsolete duplicate Prometheus datasource file was removed. Directory-wide contracts now enforce unique datasource UIDs and at most one default datasource per organization. The RC13 Grafana Provisioning Runtime Gate starts Grafana 13.1.0 with the complete provisioning directory and requires a healthy API response without provisioning failure.

## Acceptance boundary

These repository-controlled results resolve the known code/configuration blockers but do **not** establish accountable project-owner acceptance. RC13 remains open until the owner retests current merged `main` and explicitly accepts the product behavior.

## Required owner retest

Verify on current local `main`:

1. `docker compose up --build` proceeds without the former Grafana provisioner file-not-found failure;
2. Grafana remains running and does not re-enter the duplicate-default datasource restart loop;
3. Overview `Alles vernieuwen` visibly refreshes and returns to an enabled state;
4. with no intelligence data, status reports `Geen intelligence data · bronstatus geladen`, not `Data bijgewerkt`;
5. main navigation and operator buttons work in Chrome;
6. the version number is absent from product navigation;
7. Administration presents `Gebruikers & rollen` clearly and does not duplicate source operations;
8. empty intelligence graphs clearly state that no data is available;
9. after a source run ingests records, Intelligence, Overview and graphs update truthfully.

## Phase 8 boundary

The Phase 8 intake/deployment identity record from PR #157 remains fail-closed preparatory evidence. Issue #158 remains paused. No real staging, pentest or production-readiness progression is allowed until RC13 is explicitly accepted after this owner retest.

## Security and governance boundaries

Credentialed integrations use logical secret references only. Production bearer tokens remain externally issued. RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, analytics, Administration, Governance, CI or staging access cannot authorize publication.

## Exactly one current priority

**Accountable project-owner local Compose and functional console retest of current merged `main`.**
