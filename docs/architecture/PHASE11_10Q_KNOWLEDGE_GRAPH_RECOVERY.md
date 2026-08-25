# Phase 11.10q Knowledge Graph recovery

## Purpose

The canonical Knowledge Graph must be usable without requiring an operator to know or paste an internal DTMO UUID. The normal path discovers recent canonical intelligence roots from DTMO persistence and lets the operator select a root before loading the persisted OpenCTI/STIX projection. When canonical persistence contains no graph roots yet, the graph workspace now also exposes the existing governed population control so the operator can execute an already-enabled source and reload roots without leaving the canonical workflow.

## Operator flow

1. Open **Knowledge Graph** from the canonical workbench.
2. DTMO reads `/api/v1/command-center` and presents recent canonical intelligence as selectable graph roots.
3. If no canonical roots exist, the workspace exposes `ThreatIntelligencePopulation`, which lists governed sources through `/api/v1/admin/sources` and permits execution only for sources that are already enabled.
4. A source run uses the existing same-origin `/api/v1/admin/sources/{source_id}/run` contract with request attribution. After ingestion, **Reload recent intelligence** re-reads `/api/v1/command-center`; the graph workspace then presents any newly persisted roots.
5. Selecting a root loads `/api/v1/opencti/items/{item_id}/graph` for that canonical object.
6. Persisted OpenCTI mapping nodes can be selected to inspect durable entity evidence and revision history.
7. Manual UUID entry remains available only under an advanced troubleshooting/deep-link control; it is no longer the primary operator workflow.

## Evidence and authority boundaries

Graph-root discovery and population operate against canonical DTMO persistence and existing governed source-execution contracts. The browser does not query OpenCTI directly. The graph workspace cannot activate a source, change endpoints or credentials, grant review/share/publication authority, or infer source/upstream health from an empty result or failed run. Those authority boundaries remain server-side and in Sources & Collection / Administration.

A missing root list is not evidence of upstream absence or health. OpenCTI entity-to-entity topology is rendered only when DTMO has durably persisted that topology; otherwise the view is limited to canonical-root-to-mapping context. Graph presence is contextual evidence and does not prove maliciousness, local compromise, review approval, sharing authority or publication authority.

## Acceptance evidence

`backend/tests/test_phase11_10q_knowledge_graph_discovery.py` enforces canonical root discovery, empty-state governed population/reload, secondary-only UUID entry and the evidence boundaries. `.github/workflows/phase11-10q-knowledge-graph-discovery.yml` runs that contract plus a full canonical frontend build against the exact PR head.

Repository CI is not owner functional acceptance and is not live, staging, production-equivalent or external-assurance evidence.
