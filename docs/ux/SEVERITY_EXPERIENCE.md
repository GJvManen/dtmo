# DTMO Severity Experience

Status: `ACCEPTED_MERGED`

## Purpose

The DTMO severity experience gives analysts and operators one consistent way to interpret and filter intelligence severity across **Overview** and **Intelligence** without changing the canonical intelligence model or inferring risk/framework relationships that are not present in source data.

This document is a stable product/UX contract. Exact pull-request, workflow and commit chronology belongs in `docs/development/runs/` and CI evidence.

## Canonical severity model

DTMO uses the existing canonical `IntelligenceSeverity` values:

| Severity | Product meaning | Visual semantic |
|---|---|---|
| `informational` | Context/information without an elevated severity classification | neutral/grey |
| `low` | Low-severity intelligence | green |
| `medium` | Medium-severity intelligence | amber/yellow |
| `high` | High-severity intelligence | red |
| `critical` | Critical-severity intelligence when present | distinct deep red |

Colour is supplementary. Every severity remains identifiable through text labels, filter labels, card structure, chart labels and table values. The interface must remain understandable when colour cannot be perceived.

## Shared filter contract

Overview and Intelligence expose the same multi-select severity state. The supported choices are informational, low, medium, high and critical.

Rules:

1. all severities are selected by default;
2. at least one severity must remain selected;
3. changing either filter surface updates the shared state and mirrors the other surface;
4. the reset action restores all severities;
5. filtered empty results are explicit and never reported as successful non-empty data;
6. filtering does not change, delete or reclassify canonical intelligence records.

## Overview behaviour

The active severity filter applies to canonical PostgreSQL-backed:

- Intelligence total;
- New intelligence in the last 24 hours;
- Average confidence for the selected intelligence set;
- Overview severity distribution;
- Overview recent-intelligence cards.

Source/catalog and connector-health metrics are operational dimensions and remain unfiltered by intelligence severity.

The severity chart uses semantic colour plus explicit severity labels and counts. Filtered KPI cards disclose that the value represents the selected severity set.

## Intelligence behaviour

### Recent intelligence

Recent canonical intelligence is filtered server-side against PostgreSQL. Cards expose both the severity text and semantic visual treatment.

### Search

The existing governed OpenSearch search API remains authoritative for search. When exactly one severity is active, the existing server-side `severity` query parameter is used. With multiple selected severities, the returned search result set is additionally filtered against the shared selected set in the browser.

No search/filter operation changes review status, share approval or publication authority.

## API composition

The severity experience adds a bounded console API:

- `GET /api/v1/console/severity-summary`

The existing recent-intelligence console path is composed with optional repeatable `severity` query parameters:

- `GET /api/v1/console/recent-intelligence?severity=high&severity=critical`

Both endpoints require the existing `read:intelligence` permission and query the canonical PostgreSQL `IntelligenceItem` model.

Unknown severity values fail closed with HTTP 400.

## Accessibility contract

- Severity is never encoded by colour alone.
- Every filter uses native checkboxes with text labels.
- Filter groups have an accessible group label.
- Filter state changes are reported through live status regions.
- Keyboard focus remains visible.
- Charts retain textual labels and tables with explicit counts.
- Empty filtered states contain explanatory text.

Existing RC9 accessibility/browser gates remain applicable.

## Security and governance boundaries

This enhancement does not alter:

- server-side RBAC;
- service-account/human-role separation;
- review authority;
- external share approval;
- source execution authority;
- provenance;
- audit requirements;
- Governance mapping truth rules.

Severity does not imply a Normenkader IBP control, MITRE ATT&CK technique or other framework mapping. Framework relationships remain `UNMAPPED`/`CONTEXT_ONLY` until explicit provenance-backed mappings are implemented.

## Architectural composition

The severity experience is composed over the accepted RC13 Governance + Administration page and registered before the historical console root routes. The existing RC13 routers remain available for their API/JavaScript resources and compatibility paths.

This avoids duplicating the console and keeps the severity enhancement bounded to presentation/filtering plus canonical read APIs.

## Acceptance criteria

The enhancement is accepted only when:

1. Overview and Intelligence both expose the shared filter controls;
2. filter state remains synchronized;
3. canonical recent intelligence is server-side filtered;
4. Overview filtered totals and severity distribution are internally consistent;
5. search composes with severity filtering;
6. filtered empty states are truthful;
7. informational/low/medium/high/critical remain textually distinguishable;
8. RC13 Administration and Governance remain present;
9. RC13 functional/browser and RC9 accessibility gates remain green;
10. the complete exact-head workflow matrix succeeds before merge.

## Release evidence

Accepted with complete exact-head CI and merged through PR #175 on 2026-08-12. Merge commit: `156843bfbe005c4207388cca6d9bbd0a7f89388a`.

The subsequent E3 source-onboarding, E4 analytics, E5/E7 framework-governance and E6 RBAC slices were delivered separately and do not alter the severity truth model above.
