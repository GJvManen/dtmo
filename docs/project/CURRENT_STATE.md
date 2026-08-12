# DTMO Current Project State

Last reconciled: **2026-08-12**

## Executive summary

DTMO `16.0.0rc12` has accepted repository-controlled engineering through Phase 7. Repository-controlled RC13 repairs #159–#163 remain valid.

The latest accountable owner fresh-clone run confirms the bounded startup and catalog repairs on the observed path:

- `grafana-db-provision` exited with code 0;
- API health remained available;
- Grafana 13.1.0 started without the former duplicate-default datasource restart loop;
- `POST /api/v1/admin/sources/catalog/bootstrap` returned `200 OK` at `2026-08-12T10:21:39Z`.

The same run then exposed a new source-controlled local-development defect: CISA KEV was fetched successfully upstream, but raw-evidence landing failed with object-store `InvalidAccessKeyId`. `.env.example` supplied API credentials `dtmo/change-me-now` while local Compose started AIStor from separately required `MINIO_ROOT_USER/MINIO_ROOT_PASSWORD` inputs and provisioned no matching `dtmo` application identity.

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

### Confirmed resolved on the observed path

- PR #160 runtime packaging: the former `/app/tools/provision_grafana_reader.py` file-not-found failure did not recur; `grafana-db-provision` exited 0.
- PR #161 Grafana provisioning: Grafana started without `Only one datasource per organization can be marked as default` and without the former restart loop.
- PR #163 source catalog: supported catalog bootstrap returned `200 OK`; the earlier secret-reference HTTP 500 did not recur.
- migrations, API and Prometheus started successfully.
- source/catalog/status/administration/governance read endpoints returned successful responses during the UI session.

This is accountable owner-observed functional evidence for those bounded repairs. It is not full RC13 acceptance.

## Current RC13 blocker — local object-store credential contract

The fresh-clone owner run invoked CISA KEV. DTMO successfully downloaded the upstream CISA JSON, then failed while landing the first raw record in bucket `dtmo-raw` with `InvalidAccessKeyId`.

Repository inspection confirms the mismatch:

1. `.env.example` supplied `DTMO_MINIO_ACCESS_KEY=dtmo` and `DTMO_MINIO_SECRET_KEY=change-me-now` to the API;
2. `docker-compose.yml` starts local AIStor with separately required `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD`;
3. no local Compose service or repository script provisions a matching `dtmo` identity;
4. therefore a fresh-clone environment can start successfully but cannot complete source-to-intelligence persistence using the shipped local configuration contract.

This evidence supersedes the earlier assumption that the symptom was only an owner `.env` mistake.

## Current repair state

Branch `rc13/local-objectstore-credential-contract`:

- local-development Compose explicitly passes `MINIO_ROOT_USER/MINIO_ROOT_PASSWORD` to the API as its effective `DTMO_MINIO_ACCESS_KEY/DTMO_MINIO_SECRET_KEY`;
- `.env.example` no longer advertises unrelated runnable `dtmo/change-me-now` object-store defaults;
- documentation marks the shared local identity as development-only;
- staging keeps distinct required `AISTOR_APP_ACCESS_KEY/AISTOR_APP_SECRET_KEY` values and therefore preserves the least-privilege production-equivalent boundary;
- object-storage contract tests cover local consistency and staging separation;
- `RC13 Local Object-store Credential Contract Gate` renders the actual Compose configuration and validates effective credential equality on the exact PR head.

The repair is `PENDING_CI`. No repository pass is claimed until every returned workflow on the final exact PR head is `completed/success`.

## Historical RC13 repair evidence

- PR #159 console usability: repository-controlled `PASS`; merged as `b4fffecc47f87b1edab8258514eaa130d949c195`.
- PR #160 Compose runtime packaging: repository-controlled `PASS`; merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c` and subsequently owner-observed beyond its former blocker.
- PR #161 Grafana datasource provisioning: repository-controlled `PASS`; merged as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5` and subsequently owner-observed beyond its former restart loop.
- PR #163 source catalog secret-reference/bootstrap: repository-controlled `PASS`; exact head `4198f06e360929d3937065b8528237741cbe189a`; merged as `adc027143f1274c604a16446fe1ad2bdc7bc835f`; subsequently owner-observed bootstrap `200 OK`.

Historical evidence is not rewritten; newer owner-observed evidence controls the current readiness decision.

## Documentation and tooling audit note

PR #164 was closed unmerged because the new owner evidence made its status stale before merge. Its branch-only RUN-201 never became authoritative on `main`.

An assistant tooling error briefly created and then deleted an empty `dummy` file directly on `main`. The cleanup head is `0c3a4eb9f98cec875e3a80b92a61a1fe88b5ee92`. GitHub compare from the PR #163 merge commit to that cleanup head returned **no changed files**, so repository content is unchanged; the incident is recorded transparently in RUN-20260812-202.

## Remaining owner acceptance after repair

After the object-store repair is exact-head green and merged, verify on current `main`:

1. local Compose startup remains successful;
2. Grafana remains healthy;
3. supported source catalog bootstrap remains successful;
4. a supported source run can fetch and persist raw evidence without object-store authentication failure;
5. ingested records appear truthfully in Intelligence, Overview and analytics;
6. `Alles vernieuwen` shows real loading/success/failure behavior and re-enables;
7. empty intelligence reports `Geen intelligence data · bronstatus geladen`, not false success;
8. Chrome navigation/operator controls work without page errors;
9. Administration clearly presents `Gebruikers & rollen` without duplicate source operations;
10. empty graphs explicitly state no data;
11. authorization/publication boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

## Phase 8 boundary

The Phase 8 intake/deployment identity record from PR #157 remains fail-closed preparatory evidence. Issue #158 remains paused. No real staging, pentest or production-readiness progression is allowed while RC13 is blocked.

## Security and governance boundaries

Credentialed integrations store logical secret references only; raw secret values remain forbidden. Production bearer tokens remain externally issued. RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Local-development object-store credential reuse is not a staging/production permission model. Source execution, analytics, Administration, Governance, CI or staging access cannot authorize publication.

## Exactly one current priority

**Complete the local object-store credential contract repair, require complete exact-head CI, merge, then resume accountable project-owner RC13 local functional retesting.**
