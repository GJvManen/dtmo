# Phase 11.10q Knowledge Graph recovery

## Purpose

The canonical Knowledge Graph must be usable without requiring an operator to know or paste an internal DTMO UUID. The normal path now discovers recent canonical intelligence roots from DTMO persistence and lets the operator select a root before loading the persisted OpenCTI/STIX projection.

## Operator flow

1. Open **Knowledge Graph** from the canonical workbench.
2. DTMO reads `/api/v1/command-center` and presents recent canonical intelligence as selectable graph roots.
3. Selecting a root loads `/api/v1/opencti/items/{item_id}/graph` for that canonical object.
4. Persisted OpenCTI mapping nodes can be selected to inspect durable entity evidence and revision history.
5. Manual UUID entry remains available only under an advanced troubleshooting/deep-link control; it is no longer the primary operator workflow.

## Evidence and authority boundaries

Graph-root discovery uses canonical DTMO persistence. The browser does not query OpenCTI directly. A missing root list is not evidence of upstream absence or health. OpenCTI entity-to-entity topology is rendered only when DTMO has durably persisted that topology; otherwise the view is limited to canonical-root-to-mapping context. Graph presence is contextual evidence and does not prove maliciousness, local compromise, review approval, sharing authority or publication authority.

## Acceptance evidence

`backend/tests/test_phase11_10q_knowledge_graph_discovery.py` enforces canonical root discovery, secondary-only UUID entry and the evidence boundaries. `.github/workflows/phase11-10q-knowledge-graph-discovery.yml` runs that contract plus a full canonical frontend build against the exact PR head.

Repository CI is not owner functional acceptance and is not live, staging, production-equivalent or external-assurance evidence.
