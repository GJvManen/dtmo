# Canonical Functional Browser Matrix

Status: **IN PROGRESS / OWNER FUNCTIONAL RECOVERY REOPENED**

This QA contract exists because repository-green route/source contracts did not by themselves demonstrate a workable canonical product. Candidate freeze and Phase 11.10p remain blocked until required canonical functions are re-exercised and owner-observed blockers are closed.

## Slice 1 — route coverage and Administration persistence

The dedicated exact-head same-origin browser workflow must exercise the real built DTMO process without Playwright route interception and without external connector execution.

Required canonical routes in this slice:

- Command Center;
- Threat Intelligence;
- IOC Explorer;
- Knowledge Graph;
- Vulnerability & Exposure Center;
- Investigations;
- Analysis & Enrichment;
- Sharing & Exchange;
- Automation & Playbooks;
- Sources & Collection;
- Governance & Evidence;
- Operations;
- Administration.

Every route must render its canonical heading and must not depend on `/ui/*` navigation.

Administration additionally must prove a real browser mutation through the same-origin DTMO API and temporary repository-controlled persistence: change a disabled MISP endpoint, persist it, reload the page, observe the persisted value, and restore the original fixture state. The journey must use server-authorized `admin` permissions and must not execute the MISP connector.

## Slice 2 — Threat Intelligence real read/search/filter/detail

The canonical Threat Intelligence workspace must prove both recent/default discovery from temporary PostgreSQL persistence and text/severity/relevance search through the real repository-controlled OpenSearch projection. Search failure must stay explicit and must not be converted into a false empty result. Canonical detail and Analysis/Sharing pivots must remain available without `/ui/*` compatibility paths.

## Slice 3 — IOC Explorer real inventory/filter/pivot

The canonical IOC Explorer must read a real persisted `IntelOwlEnrichmentRecord` joined to its canonical intelligence item through `/api/v1/iocs`. The browser journey must exercise indicator/context, observable type, severity, source and minimum-confidence filters against that persisted record and must prove canonical pivots to source intelligence, Analysis & Enrichment, Knowledge Graph and Investigations.

This slice must not execute IntelOwl or any other external connector. Its fixture is repository-controlled persistence only. `external_share_authorized` and `local_compromise_proven` remain false; the test must not infer maliciousness, local compromise, upstream truth or share authority from IOC presence.

## Slice 4 — Knowledge Graph persisted mapping/entity journey

The canonical Knowledge Graph must prove a deep-link from one real temporary PostgreSQL intelligence item to DTMO-persisted OpenCTI/STIX mapping context. The browser journey must load the graph through `/api/v1/opencti/items/{item_id}/graph`, render the persisted mapping node, open its entity detail through `/api/v1/opencti/entities/{mapping_id}`, and expose its persisted revision, markings, confidence and authority boundaries.

This slice deliberately runs with the live OpenCTI connector feature disabled. It must not query OpenCTI upstream, infer missing upstream relationship topology, or promote graph presence into evidence of compromise, attribution or external-share authority. `external_share_authorized` and `local_compromise_proven` remain false.

## Evidence boundary

Passing these slices is repository-controlled browser evidence only. It is **not** owner acceptance, staging evidence, production-equivalent validation, penetration-test evidence, production authorization, or independent external assurance.

The following controls remain authoritative and must not be weakened by recovery work: server-side RBAC, provenance, fail-closed behavior, separate human review/share authority, responder/publication separation, and server-side credential boundaries.

## Remaining recovery

These slices do not claim that every function on every page has been proven. Recovery continues page-by-page with real read/mutation/filter/pivot/persistence/error-path journeys, fixing only verified failures one bounded change at a time. After Knowledge Graph, the next deep functional slice is Vulnerability & Exposure Center unless exact-head CI exposes an earlier blocker.
