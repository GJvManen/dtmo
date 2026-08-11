# DTMO Current Project State

Last reconciled: **2026-08-11**

## Executive summary

DTMO `16.0.0rc12` has completed the repository-controlled engineering programme through Phase 7 and the RC11/RC12 product consolidation programme.

The platform now has:

- one canonical unified DTMO console;
- a governed source adapter framework and connected operational vendor catalog;
- integrated source administration and execution;
- threat intelligence investigation and management views;
- Grafana operational and intelligence analytics embedded through the same browser origin;
- least-privilege Grafana reporting access;
- established CI, security, recovery, performance, accessibility and observability gates.

DTMO is **not yet production ready**. The next formal gate is external staging validation.

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
| 8. Real staging acceptance | `READY_FOR_EXTERNAL_VALIDATION` |
| 9. Independent external assurance | `NOT COMPLETE` |
| 10. Production go/no-go | `NOT STARTED` |

## Current product baseline

### Unified console

The canonical product entry point is `/`, with `/ui/console` retained as an alias. Legacy role/workspace routes may remain for compatibility, but the intended product architecture is one unified shell.

Source operations, administration, intelligence investigation, graphical analytics and governance views are presented without weakening server-side RBAC or human approval boundaries.

### Source framework

The current operational vendor catalog is connected through accepted built-in or unified-framework adapters. Credentialed integrations carry logical secret references only; runtime secret values are not stored in the catalog or source registry.

The authoritative source status is maintained in [`SOURCE_CONNECTION_MATRIX.md`](../qa/SOURCE_CONNECTION_MATRIX.md).

### Analytics and observability

Grafana provides operational and intelligence dashboards through the managed same-origin `/grafana/` path. Intelligence reporting uses a dedicated least-privilege reporting role and explicit reporting views rather than the DTMO application database identity.

Prometheus metrics, request correlation, trace context, alerting and operational runbooks support the observability layer. Native accessible chart/table equivalents remain available in the DTMO console.

## Phase 6 acceptance

On **2026-08-11**, the project owner explicitly confirmed that Phase 6 was personally checked and accepted. This closes the remaining external/manual accessibility blocker as accountable owner attestation. The repository does not invent unprovided test-environment or recording details.

## Phase 8 handoff

The repository-controlled prerequisites are ready for external staging validation. After this final cleanup PR is accepted, the project owner will validate an approved production-equivalent staging deployment against the ten-class deployment-parity gate tied to one immutable `16.0.0rc12` deployment identity.

CI, Docker Compose and staging-emulator evidence are supporting engineering evidence and do not substitute for that external decision.

## Governance boundary

RBAC, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, dashboard access, CI success or staging access cannot authorize publication.

## Exactly one current priority

**Complete the final cleanup/documentation PR, then perform Phase 8 external staging validation against one immutable `16.0.0rc12` deployment identity.**
