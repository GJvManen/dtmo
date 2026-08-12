# DTMO Current Project State

Last reconciled: **2026-08-12**

## Executive summary

DTMO `16.0.0rc12` has accepted repository-controlled engineering through Phase 7. Repository-controlled RC13 repairs through PR #165 are complete and exact-head green.

PR #165 exact head `48688977836cf3305b9d90c064e945de00eefb49` completed every returned workflow with `completed/success` and merged with expected-head protection as `65440afea6cfa3c3300b25d577d746432cc95700`.

The latest owner run before #165 confirmed the #163 source-catalog repair functionally, then exposed the local object-store credential mismatch repaired by #165. The repaired end-to-end product has not yet been owner-accepted.

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

## Repository-controlled RC13 repair evidence

- PR #159 console usability: merged `b4fffecc47f87b1edab8258514eaa130d949c195`.
- PR #160 Compose runtime packaging: merged `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`.
- PR #161 Grafana datasource provisioning: merged `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`.
- PR #163 source catalog bootstrap contract: exact head `4198f06e360929d3937065b8528237741cbe189a`, complete returned workflow matrix success, merged `adc027143f1274c604a16446fe1ad2bdc7bc835f`, later owner-observed bootstrap `200 OK`.
- PR #165 local object-store credential contract: exact head `48688977836cf3305b9d90c064e945de00eefb49`, complete returned workflow matrix success, merged `65440afea6cfa3c3300b25d577d746432cc95700`.

PR #165 makes local-development Compose use one internally consistent AIStor identity for the API and local object store. This is a development-only exception. Staging/production-equivalent deployments continue to require a distinct least-privilege `AISTOR_APP_ACCESS_KEY/AISTOR_APP_SECRET_KEY` application identity.

## Owner acceptance still required

On current merged `main`, the accountable owner must verify:

1. local Compose startup remains successful;
2. Grafana remains healthy;
3. supported source catalog bootstrap remains successful and idempotent;
4. bootstrapped sources remain disabled by default until explicitly enabled;
5. a supported source can fetch and persist raw evidence without object-store authentication failure;
6. source validation/run controls behave truthfully;
7. ingested records appear truthfully in Intelligence, Overview and analytics;
8. `Alles vernieuwen` shows real loading/success/failure behavior and re-enables;
9. empty intelligence reports `Geen intelligence data · bronstatus geladen`, not false success;
10. Chrome navigation/operator controls work without page errors;
11. Administration clearly presents `Gebruikers & rollen` without duplicate source operations;
12. empty graphs explicitly state no data;
13. authorization/publication boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

## Documentation and audit notes

RUN-20260812-202 remains immutable point-in-time evidence from before #165 exact-head completion. It is not rewritten.

PR #164 was closed unmerged because newer owner evidence superseded its status before merge. Its branch-only RUN-201 never became authoritative on `main`.

The earlier assistant tooling incident that briefly created and deleted an empty `dummy` file left no repository-tree difference; it remains transparently recorded in RUN-20260812-202.

## Phase 8 boundary

The Phase 8 intake/deployment identity record from PR #157 remains fail-closed preparatory evidence. Issue #158 remains paused. No real staging, pentest or production-readiness progression is allowed until RC13 is explicitly owner-accepted.

## Security and governance boundaries

Credentialed integrations store logical secret references only; raw secret values remain forbidden. Production bearer tokens remain externally issued. RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Local-development object-store credential reuse is not a staging/production permission model. Source execution, analytics, Administration, Governance, CI or staging access cannot authorize publication.

## Exactly one current priority

**Run the accountable project-owner RC13 local functional retest on current merged `main` containing PR #165.**
