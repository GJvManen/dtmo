# DTMO Roadmap — Production Readiness and Product Evolution

Last updated: **2026-08-17**

## Purpose

This roadmap separates production authorization from product evolution and platform industrialisation. Repository engineering, accountable acceptance, deployment-bound validation, independent assurance and production authorization remain distinct evidence classes.

## Current position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Repository-controlled engineering baseline | `PASS` |
| RC13 + owner retest | Unified-console functional acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | Vulnerability & CTI ecosystem integrations | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Production-equivalent validation and accountable acceptance | `PASS / OWNER_ACCEPTED` |
| Phase 9 | Independent external assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | Formal production go/no-go | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11.1–11.5 | Taranis, IntelOwl, OpenCTI and MISP integration boundaries | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.6 contract | TheHive incident/case handoff service/API/identity/licensing boundary | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 12 | New formal production go/no-go for integrated platform | `NOT STARTED` |

DTMO remains **not production authorized**. Phase 10 concluded with a no-go decision and Phase 11 remains the highest-priority programme.

## Historical readiness evidence

Phase 8 remains `PASS / OWNER_ACCEPTED` and Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate they actually covered. Those claims are historical and are not transferred to the materially changed Phase 11 platform.

## Phase 11 platform industrialisation

The authoritative detailed programme is `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md` and the fixed order remains Taranis → IntelOwl → OpenCTI → MISP → TheHive → conditional Cortex → integrated runtime → migration/compatibility → new validation → new assurance.

### Phase 11.1–11.5 — accepted integration baseline

**Status:** `PASS / REPOSITORY_COMPLETE`

Accepted repository evidence covers Taranis collection/assessment and canonical adaptation, IntelOwl bounded enrichment, OpenCTI graph integration and MISP governed exchange/synchronization state. These claims remain repository engineering evidence only.

### Phase 11.6 — TheHive incident/case handoff

**Status:** `IN PROGRESS / CONTRACT IN EXACT-HEAD VALIDATION`

The current slice is contract-only. The reviewed upstream baseline is TheHive 5.5.16 using public API v1 (`/api/v1`). Public API v0 is not used.

Active repository scope:

- TheHive remains a separate StrangeBee service; no upstream source is vendored;
- TheHive 5.3+ activated Community/Gold/Platinum license requirement is recorded as a live-deployment prerequisite for continued write operation;
- `POST /api/v1/case` is a future mutation candidate, not an automatic ingestion side effect;
- explicit human case-handoff approval under dedicated server-side RBAC is mandatory;
- case-handoff authority remains separate from DTMO publication/share authority;
- a later implementation must durably map DTMO canonical UUID, handoff/idempotency identity, TheHive case identity and organization context;
- mutable title/description/tag/assignee fields are not identity;
- TLP/PAP/access mappings cannot broaden authoritative source restrictions and unknown/unrepresentable mappings fail closed;
- ambiguous case-creation delivery blocks blind replay and requires reconciliation;
- a dedicated least-privilege non-human TheHive identity is required for any runtime adapter;
- attachments, raw source bodies, credentials, private enrichment and unrelated personal data are excluded by default;
- TheHive case lifecycle does not become canonical CTI truth, proof of local compromise or DTMO external-share authority;
- responders, Cortex execution, automatic MISP→TheHive automation, external sharing and administration remain excluded.

```mermaid
flowchart LR
    D[(DTMO canonical intelligence)] --> A{Human case-handoff approval?}
    A -->|no| N[No TheHive mutation]
    A -->|yes| V{Identity + provenance + TLP/PAP valid?}
    V -->|no| X[Fail closed]
    V -->|yes| R[(Durable handoff reservation)]
    R --> T[TheHive API v1\nPOST /api/v1/case]
    T -->|success| M[(DTMO↔TheHive case mapping)]
    T -->|ambiguous| U[Block blind replay]
    M --> H[TheHive case lifecycle]
    H -. cannot grant .-> S[DTMO share/publication authority]
```

Repository contract acceptance cannot establish live TheHive connectivity, activated entitlement, effective deployed permissions, target-organization/access configuration, privacy approval, real-data handling correctness, production-equivalent validation, independent assurance or production authorization.

After protected contract acceptance, the next bounded 11.6 slice may implement the minimum human-authorized case-handoff adapter and durable mutation reservation/reconciliation state.

### Phase 11.7–11.11

Subsequent phases remain governed by the fixed order. Cortex is adopted only if an accepted IntelOwl capability gap exists. Phase 11.8 covers Kubernetes/Helm/GitOps and platform hardening; 11.9 migration/compatibility; 11.10 fresh production-equivalent validation; 11.11 fresh independent assurance.

## Phase 12 — formal production GO/NO-GO

**Status:** `NOT STARTED`

Phase 12 starts only after one immutable integrated Phase 11 candidate has accepted Phase 11.10 production-equivalent validation and Phase 11.11 independent external assurance plus required production ownership/IAM/secrets/network/recovery/monitoring/privacy/legal/change approvals.

## Product and platform boundary

DTMO remains the education-sector CTI and decision-support layer with vulnerability context, provenance, canonical evidence semantics, explicit governance/framework relationships, governed Administration/RBAC and human-controlled external-sharing and case-handoff authority. Generic collection, IOC enrichment, CTI graph, exchange and case-management functions are integrated from mature projects instead of duplicated inside DTMO.

## Delivery and documentation discipline

Each material change requires one bounded pull request with explicit acceptance criteria, exact-head CI, expected-head protection, architecture/security/licensing/evidence boundaries and synchronized professional documentation. A code/integration PR is not mergeable if affected current-state, architecture, integration, security, QA/evidence, roadmap or user/admin documentation is stale.
