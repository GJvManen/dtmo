# DTMO Current Project State

Last reconciled: **2026-08-12**

## Executive summary

DTMO `16.0.0rc12` has accepted repository-controlled engineering through Phase 7. Repository-controlled RC13 repairs are green and merged through PR #163.

The latest accountable owner local retest had already progressed beyond the prior PR #160/#161 startup blockers. PR #163 subsequently repaired the source-catalog bootstrap HTTP 500 caused by the internal secret-reference contract mismatch.

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

- **PR #159 — console usability:** repository-controlled `PASS`; merged as `b4fffecc47f87b1edab8258514eaa130d949c195`.
- **PR #160 — Compose runtime packaging:** repository-controlled `PASS`; merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`; later owner run progressed beyond the former missing-file failure.
- **PR #161 — Grafana datasource provisioning:** repository-controlled `PASS`; merged as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`; later owner run progressed beyond the former duplicate-default restart loop.
- **PR #163 — source catalog secret-reference/bootstrap:** final exact head `4198f06e360929d3937065b8528237741cbe189a`; every returned workflow `completed/success`; merged with expected-head protection as `adc027143f1274c604a16446fe1ad2bdc7bc835f`.

PR #163 introduces one logical secret-reference canonicalization boundary, accepts executable `env:VARIABLE`, normalizes legacy `env://VARIABLE`, preserves opaque external secret-manager references, rejects raw secrets and regression-tests the complete supported catalog bootstrap twice for idempotency and disabled-by-default registration.

## Acceptance boundary

Repository-controlled CI and runtime gates establish repair evidence only. They do not manufacture accountable project-owner acceptance. RC13 remains open until the owner retests current merged `main` and explicitly accepts the product behavior.

## Required owner retest

Verify on current merged `main`:

1. local Compose startup remains successful;
2. Grafana remains healthy;
3. supported source catalog bootstrap succeeds without HTTP 500 and is idempotent;
4. bootstrapped sources remain disabled until explicitly enabled;
5. source validation/run controls behave truthfully;
6. Overview `Alles vernieuwen` visibly refreshes and returns to an enabled state;
7. with no intelligence data, status reports `Geen intelligence data · bronstatus geladen`, not `Data bijgewerkt`;
8. Chrome navigation and operator buttons work;
9. the version number remains absent from product navigation;
10. Administration clearly presents `Gebruikers & rollen` without duplicate source operations;
11. empty intelligence graphs explicitly report no data;
12. after a successful source run with valid local configuration, Intelligence, Overview and analytics update truthfully.

The earlier MinIO `InvalidAccessKeyId` is not classified as a repository defect because the owner explicitly identified the local `.env` as incorrect and asked to skip that point.

## Phase 8 boundary

The Phase 8 intake/deployment identity record from PR #157 remains fail-closed preparatory evidence. Issue #158 remains paused. No real staging, pentest or production-readiness progression is allowed until RC13 is explicitly accepted.

## Security and governance boundaries

Credentialed integrations store logical secret references only; raw secret values remain forbidden. Production bearer tokens remain externally issued. RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, analytics, Administration, Governance, CI or staging access cannot authorize publication.

## Exactly one current priority

**Accountable project-owner local Compose and functional console retest of current merged `main`.**
