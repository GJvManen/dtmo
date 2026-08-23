# Phase 11.10q — IOC Explorer functional recovery

## Scope

The canonical `/workbench/intelligence/iocs` route now exposes an IOC inventory backed only by persisted observables from governed DTMO enrichment executions.

## Canonical data path

`IntelOwlEnrichmentRecord` is the persistence boundary for an analyst-authorized enrichment execution. The record already carries the observable type, observable value, handling classification, analyzers, result status, canonical intelligence item identifier and execution timestamp. The new read-only `GET /api/v1/iocs` projection joins those records to the canonical `IntelligenceItem` so the workbench can display source, severity and confidence without deriving or scraping indicators from free text.

The endpoint requires `read:intelligence`. It does not grant review, connector execution, sharing, publication, responder or case-mutation authority.

## Operator workflow

IOC Explorer loads the persisted inventory without requiring a blind search or internal UUID. Operators can filter by observable text/context, observable type, severity, canonical source and minimum confidence. Each persisted observable provides direct object-driven pivots to Analysis & Enrichment, Knowledge Graph and Investigations using the canonical intelligence item identifier already associated with the record.

## Evidence boundary

IOC presence is enrichment evidence only. It does not establish that an observable is malicious, prove local compromise, establish upstream health or authorize external sharing. DTMO does not synthesize an IOC inventory from arbitrary intelligence titles, summaries or search text. If no governed observables have been persisted, the interface remains explicitly empty and points the analyst to the governed enrichment workflow.

## Acceptance impact

This slice removes the empty/search-only IOC Explorer blocker at repository level and adds deterministic contract/browser coverage. It is progress toward Phase 11.10q functional recovery, not owner functional acceptance, staging evidence, production-equivalent validation or external-assurance evidence. PR #316 remains draft while other recovery blockers remain.
