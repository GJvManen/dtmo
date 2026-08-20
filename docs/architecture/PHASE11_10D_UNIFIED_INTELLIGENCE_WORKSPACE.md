# Phase 11.10d — Unified Intelligence Workspace

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**  
Lifecycle parent: **Phase 11.10 — IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED**  
Production state: **not production authorized**

## Objective

Phase 11.10d migrates governed intelligence discovery and investigation into the canonical `/workbench/` application shell. It replaces the Threat Intelligence placeholder with a functional read-only workspace and exposes the IOC Explorer as an indicator-oriented view over the same governed DTMO contracts.

This slice does not create a second intelligence backend. It reuses the accepted DTMO API and persistence boundaries:

- `GET /api/v1/intelligence/search` for authorized discovery through the DTMO search service;
- `GET /api/v1/intelligence/{item_id}/workspace` for canonical DTMO object detail and provenance.

## Trust path

Normal operation remains:

**browser → DTMO API → canonical DTMO service/persistence → governed integration adapter → upstream service**

The browser does not hold privileged upstream credentials and does not call Taranis, IntelOwl, OpenCTI, MISP, TheHive or Cortex directly.

## Functional contract

The Unified Intelligence Workspace provides:

1. explicit search; no demonstration records are inserted or rendered by default;
2. query text plus severity, minimum education relevance and result-limit filters;
3. clear search-backend unavailable state rather than a synthetic empty dataset;
4. result cards with attributable source, severity, education relevance, confidence and publication time where present;
5. selected-object retrieval from canonical DTMO persistence;
6. canonical severity, confidence/rationale, review status and separate share-approval state;
7. structured CVE/known-exploited/vendor/product context where recorded;
8. provenance links showing primary/secondary classification, content-integrity observation and source confidence;
9. IOC Explorer as a specialized discovery route over the same governed search and detail contracts;
10. responsive behavior within the accepted Phase 11.10b shell.

## Authority boundary

Both routes require server-authorized `read:intelligence`. UI visibility does not grant authority. Search and investigation grant no review, share approval, publication, connector execution, enrichment/analyzer execution, case handoff or administration permission.

Human review and dissemination authority remain distinct server-side workflows. The canonical identity strip continues to state that publication/share authority remains server-side and human-governed.

## Evidence semantics

Search results are discovery projections from the governed search service. They are not promoted to canonical truth until the selected object is retrieved from DTMO canonical persistence. A search returning zero results describes only the queried DTMO index and does not prove that an item is absent from every upstream source.

A search dependency failure is rendered as unavailable and must **fail closed**. A canonical-detail failure does not cause the browser to synthesize object fields from the search hit. Missing provenance remains missing.

Repository and browser CI for this slice **does not prove** live upstream-source completeness, upstream service health, production-equivalent deployment/continuity, independent assurance or production authorization.

## Compatibility boundary

The legacy `/ui/intelligence-workspace` and `/ui/console` surfaces remain compatibility paths during bounded migration. New intelligence UX development targets the canonical `/workbench/intelligence` route family.

## Acceptance package

- `frontend/src/UnifiedIntelligenceWorkspace.tsx`;
- `frontend/src/unified-intelligence.css`;
- `backend/tests/test_phase11_10d_unified_intelligence_workspace_contract.py`;
- `backend/tests/test_phase11_10d_unified_intelligence_workspace_browser.py`;
- `docs/user/UNIFIED_INTELLIGENCE_WORKSPACE.md`;
- `docs/qa/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE_GATE.md`;
- `.github/workflows/phase11-unified-intelligence-workspace.yml`.

After exact-head acceptance and merge, the only next bounded priority is **Phase 11.10e — IntelOwl/Cortex Integrated Analysis**.
