# DTMO Current Project State

Last reconciled: **2026-08-12**

## Executive summary

DTMO `16.0.0rc12` has accepted repository-controlled engineering through Phase 7. RC13 console repair PR #159 passed its complete exact-head workflow matrix and merged as `b4fffecc47f87b1edab8258514eaa130d949c195`, but the accountable post-merge owner retest is not yet complete.

A fresh local `docker compose up --build` owner retest attempt on 2026-08-12 exposed a runtime packaging blocker: the `grafana-db-provision` service invokes `/app/tools/provision_grafana_reader.py`, while the runtime Dockerfile did not package that repository file into the image.

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

## Current RC13 blocker

The post-#159 owner retest reached local Compose startup but failed before the repaired console could be re-accepted:

```text
grafana-db-provision-1 | python: can't open file '/app/tools/provision_grafana_reader.py': [Errno 2] No such file or directory
grafana-db-provision-1 exited with code 2
```

Repository inspection confirms:

- `docker-compose.yml` correctly calls `python tools/provision_grafana_reader.py`;
- `tools/provision_grafana_reader.py` exists and implements the least-privilege Grafana database-reader provisioning path;
- the runtime `Dockerfile` copied `backend` and `database` but omitted that required tool.

This is a runtime packaging defect, not accepted owner-test evidence.

## Current repair state

The targeted branch `rc13/compose-grafana-provisioner-packaging`:

- copies only `tools/provision_grafana_reader.py` into `/app/tools/` in the canonical runtime image;
- adds a static packaging assertion to the existing Grafana reader contract test;
- adds `RC13 Compose Runtime Packaging Gate`, which builds the runtime image and verifies that the provisioner exists and compiles inside it.

The repair is `PENDING_CI`. No pass is claimed until every returned workflow on the final exact PR head is `completed/success`.

## Historical evidence boundary

PR #159 exact-head CI and prior RC13 browser evidence remain valid repository-controlled point-in-time evidence. They do not establish current accountable owner acceptance because the subsequent local startup attempt found a new blocker.

## Phase 8 boundary

The Phase 8 intake/deployment identity record from PR #157 remains fail-closed preparatory evidence. Issue #158 remains paused. No external staging, pentest or production-readiness progression is allowed while RC13 remains blocked.

## Security and governance boundaries

Credentialed integrations use logical secret references only. Production bearer tokens remain externally issued. RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, analytics, Administration, Governance, CI or staging access cannot authorize publication.

## Exactly one current priority

**Complete the Compose runtime packaging repair, pass complete exact-head CI, merge, then resume the accountable project-owner RC13 functional retest.**
