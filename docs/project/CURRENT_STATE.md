# DTMO Current Project State

Last reconciled: **2026-08-11**

## Executive summary

DTMO `16.0.0rc12` has completed the repository-controlled engineering programme through Phase 7 and the RC11/RC12 source-framework and unified-console consolidation work. A project-owner functional test on 2026-08-11 subsequently demonstrated that the canonical console was **not yet functionally acceptable for external staging**.

The product-level blocker is now tracked as **RC13 functional unified-console acceptance** in issue #150 and `docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`.

DTMO is **not production ready** and Phase 8 is paused until RC13 passes.

## Phase status

| Phase | Status |
|---|---|
| 1. CI and workflow integrity | `PASS` |
| 2. Application security and identity | `PASS` |
| 3. Data integrity and recovery | `PASS` |
| 4. Connector reliability and provenance | `PASS` |
| 5. Performance and scalability | `PASS` |
| 6. Accessibility and operational UX | `PASS` — project-owner manual/external acceptance on 2026-08-11 |
| 7. Observability and incident operations | `PASS` |
| RC13. Functional unified-console acceptance | `BLOCKED_INTERNAL` — remediation in progress |
| 8. Real staging acceptance | `PAUSED_PENDING_RC13` |
| 9. Independent external assurance | `NOT COMPLETE` |
| 10. Production go/no-go | `NOT STARTED` |

## Functional acceptance findings

The project-owner test found the following blocking gaps in the canonical console:

- Overview lacked useful default graphical/statistical information.
- Intelligence had no default/recent data presentation and was unusable while the source-ingestion path was not working end to end.
- Sources & Catalog did not provide a reliable register/enable/run/ingest operator journey for the already connected framework.
- Visual analytics depended on a separate Grafana authentication context.
- Administration lacked governed role/user-role administration.
- Governance did not expose the frameworks and mappings used by DTMO, including Normenkader IBP, MITRE ATT&CK and CVSS context.
- Non-user-facing legacy compatibility copy was still exposed in the main navigation.

## RC13 programme

### RC13.1 — source-to-intelligence functional path

Current priority. The canonical console must correctly distinguish built-in and registry-backed sources, allow supported framework sources to be registered/enabled/executed, process fetched records through the canonical ingestion pipeline, and show the resulting recent intelligence and overview statistics without requiring a separate search action.

RC13.1 adds a dedicated Chromium functional journey that clicks the actual console controls and proves register → enable → run → ingest → recent intelligence → updated overview behavior.

### RC13.2 — visual analytics

Core analytics must work by default without requiring a separate Grafana login. Grafana may remain as an advanced governed analytics layer, but native product analytics cannot depend on it.

### RC13.3 — Administration/RBAC

Add governed user/role-assignment administration while preserving server-side RBAC and separation of duties.

### RC13.4 — Governance knowledge surface

Expose the control/framework context used by DTMO, including Normenkader IBP, MITRE ATT&CK, CVSS and related project mappings.

### RC13.5 — full functional acceptance

Execute one complete canonical-console browser journey on one exact head. Only then may Phase 8 return to external-validation readiness.

## Source framework

The operational source adapters remain connected according to `docs/qa/SOURCE_CONNECTION_MATRIX.md`. RC13 does not reopen adapter acceptance; it repairs the **operator-facing execution and data-visibility journey** over those accepted adapters.

Credentialed integrations continue to use logical secret references only. Runtime credential values remain outside the catalog, registry and repository evidence.

## Phase 6 acceptance

Phase 6 remains `PASS`. On 2026-08-11 the project owner explicitly confirmed that the accessibility/operational UX scope had been personally checked and accepted. The repository does not invent unprovided environment/version or recording details.

## Governance boundary

RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, dashboard access, CI success or staging access cannot authorize publication.

## Exactly one current priority

**RC13.1 — complete and accept the source-to-intelligence functional browser journey.** Phase 8 external staging validation remains paused until all RC13 blocking findings are resolved.
