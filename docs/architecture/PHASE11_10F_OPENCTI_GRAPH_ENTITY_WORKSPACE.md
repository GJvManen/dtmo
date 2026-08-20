# Phase 11.10f — OpenCTI Graph / Entity Workspace

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**  
Last updated: **2026-08-20**

## Purpose

Phase 11.10f makes the canonical `/workbench/intelligence/graph` route functional using the already accepted OpenCTI integration and persistence boundary. The browser remains a DTMO client; it does not receive OpenCTI credentials and does not query OpenCTI GraphQL directly.

## Canonical trust path

**browser → DTMO API → canonical DTMO persistence → persisted OpenCTI/STIX mapping evidence**

OpenCTI remains a separate knowledge-graph service/API/licensing boundary. Server-side `read:intelligence` is required for every frontend-facing graph/entity read.

## Read API

Phase 11.10f adds:

- `GET /api/v1/opencti/capabilities` — feature/configuration and entity allowlist state, without a runtime-health claim;
- `GET /api/v1/opencti/items/{item_id}/graph` — one canonical DTMO root plus persisted OpenCTI/STIX mapping nodes and attributable `canonical-mapping` edges;
- `GET /api/v1/opencti/entities/{mapping_id}` — persisted OpenCTI identity, STIX identity/type, markings, confidence, external references, provenance, snapshot identity and immutable revision history.

The API is read-only in this slice.

## Graph truth boundary

The Phase 11.4 persistence baseline durably stores OpenCTI object mappings and immutable revisions, but it does **not** durably store OpenCTI entity-to-entity relationship topology. Phase 11.10f therefore renders only relationships DTMO can prove from persistence: the association between a canonical DTMO item and each persisted OpenCTI mapping.

The workspace MUST NOT invent, infer or visually imply upstream malware→campaign, indicator→infrastructure, actor→tool or other OpenCTI relationships that are not durably present in DTMO evidence.

An empty graph mapping set means only that DTMO has no persisted OpenCTI mapping evidence for that canonical item. It does not prove that OpenCTI has no related knowledge.

## Security and authority invariants

- browser code contains no OpenCTI token, privileged header or `/graphql` call;
- `read:intelligence` remains server-authoritative;
- `feature_opencti_read` and configured credentials are capability/configuration state, not a `healthy` claim;
- OpenCTI markings and confidence remain attributable context;
- graph/entity presence does not prove local exposure, exploitability, compromise, attribution certainty or remediation state;
- `external_share_authorized=false` and `local_compromise_proven=false` persistence invariants remain unchanged;
- no OpenCTI mutations, connectors, MISP synchronization, TheHive case creation or external publication/share operations are added.

## Browser experience

The workspace provides:

- canonical item UUID deep-link/load control;
- capability/configuration boundary strip;
- responsive SVG projection of canonical mapping evidence;
- accessible entity list as an equivalent non-visual navigation surface;
- selected entity detail with markings, confidence, external references and immutable revision history;
- explicit topology and evidence-boundary copy;
- fail-closed unavailable state when canonical graph data cannot be retrieved.

## Evidence boundary

The dedicated repository/browser gate may prove exact-head build, API routing, server-side read authorization, persisted graph/entity rendering, entity revision detail, explicit topology limitation and fail-closed browser behavior.

It does **not prove** live OpenCTI connectivity or health, completeness of OpenCTI knowledge, production-scale topology correctness, local exposure/compromise, external-share authority, production-equivalent operation, independent assurance or production authorization.

## Exit

Phase 11.10f may become `PASS / REPOSITORY_COMPLETE` only when every workflow registered for one exact final PR head is `completed/success`, professional lifecycle documentation is synchronized and the PR is merged with expected-head protection.

Only then may **Phase 11.10g — MISP Sharing & Exchange** begin.
