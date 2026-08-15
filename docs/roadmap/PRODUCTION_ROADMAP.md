# DTMO Roadmap — Production Readiness and Product Evolution

Last updated: **2026-08-15**

## Purpose

This roadmap separates production authorization from product evolution and platform industrialisation. Repository engineering, accountable acceptance, external staging evidence, independent assurance and production authorization remain distinct evidence classes.

## Current position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Repository-controlled engineering baseline | `PASS` |
| RC13 + owner retest | Unified-console functional acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | Vulnerability & CTI ecosystem integrations | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Production-equivalent validation and accountable acceptance | `PASS / OWNER_ACCEPTED` |
| Phase 9 | Independent external assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | Formal production go/no-go | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11 | Integrated platform industrialisation | `IN PROGRESS / ACTIVE` |
| Phase 12 | New formal production go/no-go for integrated platform | `NOT STARTED` |

DTMO remains **not production authorized**. Phase 10 concluded with a no-go decision and Phase 11 is now the highest-priority programme.

# Track A — Accepted historical readiness evidence

## Phase 8 — production-equivalent staging acceptance

**Status:** `PASS / OWNER_ACCEPTED`

The accepted Phase 8 evidence remains historical evidence for the candidate it covered. It is not reused as acceptance of a materially changed Phase 11 integrated platform.

## Phase 9 — independent external assurance

**Status:** `PASS / EXTERNAL_ASSURANCE_ACCEPTED`

The accepted Phase 9 assurance remains historical evidence for the candidate it covered. It is not reused as assurance of a materially changed Phase 11 integrated platform.

## Phase 10 — production go/no-go

**Status:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`

The accountable decision is recorded in `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`. Production authorization was not granted.

# Track B — Phase 11 platform industrialisation

**Status:** `IN PROGRESS / ACTIVE`

The authoritative detailed programme is `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`.

The fixed priority order is:

1. Taranis AI architecture and gap assessment;
2. Taranis → DTMO canonical adapter;
3. IntelOwl enrichment integration;
4. OpenCTI knowledge-graph integration;
5. MISP consolidation;
6. TheHive incident/case handoff;
7. Cortex decision only if IntelOwl is insufficient for a validated requirement;
8. Kubernetes/Helm/GitOps and platform hardening;
9. migration and compatibility;
10. new production-equivalent validation;
11. new independent external assurance.

## Phase 11.1 — Taranis AI architecture and gap assessment

**Status:** `IN PROGRESS / ACTIVE`

The initial assessment concludes that DTMO should retain education-sector CTI, vulnerability context, governance and governed sharing authority while Taranis provides generic OSINT collection, analyst assessment and structured reporting through a service-to-service integration.

Required completion items:

- exact REST/OpenAPI endpoint inventory;
- source/news/story/report schema mapping;
- stable IDs, replay and deduplication rules;
- authentication/service-account model;
- provenance/TLP/classification transformation rules;
- polling/SSE integration decision;
- deprecation map for duplicated DTMO generic collection functions;
- trust-boundary abuse cases;
- licensing review for service integration and redistribution documentation;
- Phase 11.2 adapter contracts and rollback criteria.

See `docs/architecture/TARANIS_PLATFORM_INTEGRATION_ASSESSMENT.md`.

## Phase 11.2–11.11

Subsequent phases execute one bounded objective at a time in the priority order defined above. No later phase may silently bypass red exact-head CI, unresolved licensing/security blockers or a required external evidence gate.

# Track C — Phase 12 production authorization

## Phase 12 — formal production go/no-go

**Status:** `NOT STARTED`

Phase 12 begins only after the integrated Phase 11 candidate has:

- passed production-equivalent validation against one immutable deployment identity;
- completed independent external assurance against that same integrated candidate;
- closed or formally dispositioned release blockers;
- obtained production environment/owner/support, IAM/secrets/network, backup/recovery/rollback, monitoring/on-call/IR, privacy/legal/governance and change authorization.

Phase 12 is fail-closed. A `GO` applies only to the explicitly approved immutable integrated release identity.

# Product and platform boundary

DTMO's differentiating scope remains:

- education-sector CTI and decision support;
- vulnerability prioritization and context;
- provenance and canonical evidence semantics;
- explicit governance/framework relationships;
- governed Administration/RBAC;
- human-controlled external-sharing authority.

Generic collection, IOC enrichment, CTI graph, case management and report-publishing capabilities should be integrated from mature open-source projects where practical rather than rebuilt inside DTMO.

# Delivery and documentation discipline

Each material change requires one bounded pull request with a primary objective, explicit acceptance criteria, exact-head CI where applicable, architecture/security/evidence boundaries and professional documentation updates.

Historical evidence remains immutable. The current documentation layer must consistently show Phase 10 `NO-GO`, Phase 11 `IN PROGRESS / ACTIVE` and Phase 12 `NOT STARTED` until later accountable decisions change that state.

## Immediate next steps

1. Complete Phase 11.1 Taranis API/data-model/identity/licensing assessment.
2. Define and test the Phase 11.2 canonical adapter contract.
3. Implement the Taranis → DTMO adapter only after 11.1 exits green.
4. Continue in the fixed integration priority order through Phase 11.11.
5. Enter Phase 12 only after the new integrated evidence package is accepted.