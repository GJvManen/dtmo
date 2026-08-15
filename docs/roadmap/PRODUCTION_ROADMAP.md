# DTMO Roadmap — Production Readiness and Platform Industrialisation

Last updated: **2026-08-15**

## Purpose

This roadmap separates production authorization from product evolution and platform industrialisation. Repository engineering, external staging acceptance, independent assurance and final production authorization are distinct evidence classes and must not be conflated.

## Current position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Repository-controlled engineering baseline | `PASS` |
| RC13 + owner retest | Unified-console functional acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | Vulnerability & CTI ecosystem integrations | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Production-equivalent staging validation | `PASS / OWNER_ACCEPTED` |
| Phase 9 | Independent external assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | Formal production go/no-go | `NO-GO / INDUSTRIALISATION REQUIRED` |
| Phase 11 | Platform industrialisation | `ACTIVE / HIGHEST PRIORITY` |
| Phase 12 | Formal production go/no-go after industrialisation | `PLANNED` |

DTMO is **not production authorized**. Phase 10 has resulted in NO-GO for the current architecture. The active project priority is Phase 11 platform industrialisation; all unrelated product evolution is paused.

# Track A — Accepted prior evidence

## Phase 8 — production-equivalent staging acceptance

**Status:** `PASS / OWNER_ACCEPTED`

Phase 8 remains accepted historical evidence for the candidate architecture that was assessed. It must not automatically be reused for a materially changed integrated Phase 11 architecture.

## Phase 9 — independent external assurance

**Status:** `PASS / EXTERNAL_ASSURANCE_ACCEPTED`

Phase 9 remains accepted independent assurance for the candidate architecture that was assessed. Material architectural changes introduced by Phase 11 require new impact assessment and, before production authorization, independent assurance of the integrated candidate.

## Phase 10 — formal production go/no-go

**Status:** `NO-GO / INDUSTRIALISATION REQUIRED`

The current project does not receive production authorization. The NO-GO is not treated as a request for incremental documentation changes. It starts a deliberate industrialisation programme intended to replace bespoke commodity capabilities with mature platform integrations and harden the combined runtime.

# Track B — Phase 11 platform industrialisation

**Status:** `ACTIVE / HIGHEST PRIORITY`

Authoritative detailed roadmap: `docs/roadmap/PHASE11_PLATFORM_INDUSTRIALISATION.md`.

Priority sequence:

1. **11.1 Taranis AI architecture & gap assessment** — ACTIVE;
2. **11.2 Taranis -> DTMO canonical adapter**;
3. **11.3 IntelOwl enrichment subsystem**;
4. **11.4 OpenCTI knowledge graph integration**;
5. **11.5 MISP consolidation**;
6. **11.6 TheHive incident/case handoff**;
7. **11.7 production platform hardening**;
8. **11.8 migration and compatibility**;
9. **11.9 production-equivalent integrated validation**;
10. **11.10 independent external assurance**;
11. **Phase 12 formal production go/no-go**.

Cortex is optional and may only be introduced after IntelOwl if a concrete enrichment gap justifies the additional operational platform.

## Platform responsibility target

| Platform | Primary responsibility |
|---|---|
| Taranis AI | OSINT collection, worker orchestration, analyst assessment, report/publisher workflow |
| IntelOwl | generic IOC enrichment and analyzer orchestration |
| DTMO | education-sector CTI, vulnerability prioritisation, provenance policy, governance, assurance and accountable sharing |
| OpenCTI | STIX-oriented CTI knowledge graph and entity relationships |
| MISP | community CTI exchange under DTMO-governed outbound policy |
| TheHive | incident/case-management handoff |

## Work freeze

Until Phase 11 is complete or explicitly reprioritized, the following are paused:

- unrelated UI/product feature expansion;
- bespoke generic collectors;
- new provider-specific enrichment engines inside DTMO;
- custom STIX graph functionality;
- general case/ticketing development;
- custom generic publishing/report generation;
- non-essential features that materially change the integrated candidate.

Allowed exceptions are security fixes, dependency/CVE remediation, defects blocking Phase 11, and documentation/tests required by the active Phase 11 increment.

# Phase 12 — production authorization

**Status:** `PLANNED`.

Phase 12 is the next production go/no-go attempt after Phase 11. A GO may only be considered against one immutable integrated candidate after production-equivalent validation and independent external assurance of the material Phase 11 architecture.

# Delivery discipline

Every Phase 11 increment requires:

- bounded scope and acceptance criteria;
- architecture/security/licensing impact assessment where applicable;
- explicit source-of-truth and authority boundaries;
- regression protection for retained DTMO capability;
- exact-head CI before merge;
- professional current-state documentation update;
- explicit decision whether previous external evidence remains applicable.

Historical evidence remains immutable and scoped to the candidate it covered.

## Immediate next steps

1. Complete and accept Phase 11.1 Taranis/DTMO architecture and gap assessment.
2. Bound the Phase 11.2 read-only Taranis -> DTMO adapter PoC.
3. Implement the adapter through documented APIs, preserving provenance, TLP/classification, idempotency and authorization boundaries.
4. Proceed in order through IntelOwl, OpenCTI, MISP consolidation and TheHive before integrated platform hardening.
5. Revalidate the integrated architecture under Phase 11.9 and 11.10.
6. Conduct Phase 12 formal production go/no-go.