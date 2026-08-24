# Phase 11.10q — IOC Explorer functional recovery

## Scope

The canonical `/workbench/intelligence/iocs` route exposes an IOC inventory backed only by persisted observables from governed DTMO enrichment executions.

## Canonical data path

`IntelOwlEnrichmentRecord` is the persistence boundary for an analyst-authorized enrichment execution. The record already carries the observable type, observable value, handling classification, analyzers, result status, canonical intelligence item identifier and execution timestamp. The read-only `GET /api/v1/iocs` projection joins those records to the canonical `IntelligenceItem` so the workbench can display source, severity and confidence without deriving or scraping indicators from free text.

The endpoint requires `read:intelligence`. It does not grant review, connector execution, sharing, publication, responder or case-mutation authority.

## Operator workflow

IOC Explorer loads the persisted inventory without requiring a blind search or internal UUID. Operators can filter by observable text/context, observable type, severity, canonical source and minimum confidence. Each persisted observable provides direct object-driven pivots to the canonical Threat Intelligence object, Analysis & Enrichment, Knowledge Graph and Investigations using the canonical intelligence item identifier already associated with the record.

The Threat Intelligence route accepts `?item=<canonical-id>` as a read-only deep link. The identifier is not treated as browser authority or trusted object content: the workspace retrieves detail again from `/api/v1/intelligence/{item_id}/workspace`, so provenance, review state, share state and confidence remain server-derived canonical evidence. Selecting an object from the normal recent/search list also preserves that canonical item deep link in browser history.

This bidirectional pivot removes the need to copy an internal UUID or repeat a search merely to return from an IOC to its originating intelligence object.

## Evidence boundary

IOC presence is enrichment evidence only. It does not establish that an observable is malicious, prove local compromise, establish upstream health or authorize external sharing. DTMO does not synthesize an IOC inventory from arbitrary intelligence titles, summaries or search text. If no governed observables have been persisted, the interface remains explicitly empty and points the analyst to the governed enrichment workflow.

Deep-link presence likewise proves nothing about object validity. A missing, unauthorized or unavailable canonical item fails closed through the existing server-authorized detail endpoint and is surfaced as unavailable rather than fabricated.

## Acceptance impact

This slice improves IOC inventory/pivot usability at repository level by adding a direct canonical source-object pivot and preserving the existing Analysis, Graph and Investigation pivots. It is progress toward Phase 11.10q functional recovery, not owner functional acceptance, staging evidence, production-equivalent validation or external-assurance evidence. PR #316 remains draft while hard blockers in `docs/roadmap/FUNCTIONAL_RECOVERY_ACCEPTANCE.md` remain.
