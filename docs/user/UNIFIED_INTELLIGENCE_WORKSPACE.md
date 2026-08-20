# Unified Intelligence Workspace

The DTMO Unified Intelligence Workspace is the canonical analyst surface for searching and investigating intelligence records during Phase 11.10d.

## Open the workspace

Use:

- `/workbench/intelligence` for general threat-intelligence discovery;
- `/workbench/intelligence/iocs` for indicator-oriented discovery.

Both views use the same governed DTMO API. The IOC Explorer is not a direct connector to external intelligence platforms.

## Search

Enter at least two characters and optionally narrow the query by:

- severity: critical, high, medium, low or informational;
- minimum education relevance from 0 to 100;
- maximum returned results from 1 to 200.

Search executes only after **Search intelligence** is selected. The workspace does not show synthetic examples or default threat records.

If the DTMO search service is unavailable, the workspace reports **Search service unavailable**. It does not convert a failed dependency into an empty-result claim.

## Investigate a result

Select a result to retrieve the canonical DTMO object. The detail view can show:

- source and canonical URL;
- severity;
- education relevance;
- confidence score, level and rationale;
- review status;
- separate sharing approval state;
- CVE identifiers and known-exploited context;
- vendor/product context;
- tags;
- provenance records and source-integrity observations.

A search hit is discovery evidence. Canonical object detail is retrieved separately from DTMO persistence. If canonical detail cannot be retrieved, the search hit is not silently promoted into a complete object.

## Authority

The workspace is read-only and requires `read:intelligence`. Searching or viewing an object does not grant review, publication, sharing approval, connector execution, analyzer execution, case mutation or administrative authority. Those permissions remain server-side and separately governed.

## Evidence boundary

A zero-result search does not prove that every upstream source lacks matching intelligence. Repository/browser evidence also does not prove live upstream health, production-equivalent operation, independent assurance or production authorization. DTMO remains **not production authorized** while Phase 11 continues.
