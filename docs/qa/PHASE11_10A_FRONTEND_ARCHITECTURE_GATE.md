# Phase 11.10a Frontend Architecture Gate

Status: **IN PROGRESS / REPOSITORY ARCHITECTURE CONTRACT**

## Objective

Accept the architecture, information architecture, design-system and browser/API security contract required before implementation of the next-generation DTMO Unified Operations Workbench.

This gate is deliberately bounded. It does not accept the new shell, migrated product capabilities, production-equivalent execution, independent assurance or production use.

## Required repository artifacts

- `docs/architecture/FRONTEND_ARCHITECTURE.md`
- `docs/architecture/UI_API_CONTRACT.md`
- `docs/ux/UNIFIED_OPERATIONS_WORKBENCH.md`
- `docs/ux/INFORMATION_ARCHITECTURE.md`
- `docs/ux/DESIGN_SYSTEM.md`
- `backend/tests/test_phase11_10a_frontend_architecture_contract.py`
- `.github/workflows/phase11-frontend-architecture.yml`

## Acceptance criteria

### A. Canonical product boundary

- one canonical DTMO browser application is the target;
- normal governed workflows use `browser → DTMO API → governed adapter → upstream service`;
- direct browser integration with Taranis AI, IntelOwl, OpenCTI, MISP, TheHive or Cortex is not the canonical operating model;
- legacy UI paths may exist only as temporary migration/compatibility paths.

### B. Security and authority

- server-side RBAC remains authoritative;
- role-aware UI does not become an authorization mechanism;
- human publication/share authority remains distinct;
- TheHive case authority remains distinct from publication/share authority;
- enrichment/graph presence does not prove local compromise;
- credentials/secrets are not ordinary persistent browser state;
- high-impact actions use explicit governed server-side operations.

### C. Information architecture

The target navigation includes Command Center, Intelligence, Exposure, Investigations, Analysis, Sharing, Automation, Collection, Governance, Operations and Administration.

The design includes a persistent/available selected-object context surface so analysts can traverse enrichment, relationships, cases, sharing and evidence without repeatedly rediscovering the same object in separate upstream UIs.

### D. Design system

- semantic tokens and reusable component families are defined;
- dark and light modes preserve semantics;
- loading, empty, stale, partial-failure and error states are distinct;
- severity/status is not conveyed by colour alone;
- accessibility requirements preserve or improve the accepted DTMO baseline;
- mockups/design visuals are explicitly non-operational evidence.

### E. Delivery order

The roadmap defines bounded candidate-completion slices 11.10a through 11.10p, with 11.10a active, 11.10b next and fresh production-equivalent validation only after interface consolidation/candidate freeze.

### F. Documentation

Current State, documentation portal, industrialisation roadmap and Evidence Index expose the 11.10a contract without rewriting historical Phase 8/9 or accepted Phase 11 evidence.

## Exact-head CI

`.github/workflows/phase11-frontend-architecture.yml` runs the dedicated contract test and emits an exact-head repository evidence artifact. A green workflow proves repository contract consistency only.

## Exit state

When all exact-head CI is green and professional documentation is synchronized, 11.10a may become:

`PASS / REPOSITORY_COMPLETE`

The next bounded priority is:

**Phase 11.10b — canonical application shell**.

Phase 11.10 overall remains `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` until the candidate-completion programme and fresh production-equivalent validation are complete and accountably accepted.