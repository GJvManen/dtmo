# Phase 11.10f — OpenCTI Graph / Entity Workspace Gate

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**

## Acceptance objective

Accept the OpenCTI graph/entity workspace only when one exact PR head proves the repository-controlled implementation while preserving the Phase 11.4 OpenCTI identity, provenance, marking and authority boundaries.

## Required exact-head evidence

The final exact head must prove:

- `/workbench/intelligence/graph` is a functional canonical workbench route;
- browser code calls DTMO APIs only and contains no privileged OpenCTI token or direct `/graphql` request;
- `GET /api/v1/opencti/capabilities`, `GET /api/v1/opencti/items/{item_id}/graph` and `GET /api/v1/opencti/entities/{mapping_id}` require server-side `read:intelligence`;
- the graph root is a canonical DTMO intelligence item;
- OpenCTI nodes are backed by persisted `OpenCTIObjectMapping` records;
- edges are labelled `canonical-mapping` and are never represented as OpenCTI entity-to-entity topology;
- `upstream_relationship_topology_persisted=false` remains explicit until a separately accepted persistence contract exists;
- entity detail exposes stable OpenCTI/STIX identity, type, markings, confidence, external references, snapshot identity and immutable revision history where recorded;
- `external_share_authorized=false` and `local_compromise_proven=false` invariants remain enforced;
- empty mapping evidence does not claim upstream absence;
- dependency failure renders unavailable rather than an empty graph;
- frontend typecheck/build and deterministic browser acceptance succeed;
- Phase 11.4 OpenCTI contract/persistence regressions remain green;
- professional current-state, evidence, QA and roadmap documentation is synchronized.

## Exact-head workflow

Workflow: `.github/workflows/phase11-opencti-graph-workspace.yml`

It checks out the exact PR head, verifies the checkout identity, runs `npm ci` and the production frontend build, executes 11.10f plus Phase 11.4 repository contracts, starts the exact-head DTMO application, runs browser acceptance and uploads non-sensitive repository evidence.

## Claim boundary

A green gate proves repository-controlled behavior only. It does **not prove** live OpenCTI connectivity/health, completeness of OpenCTI knowledge, production-scale graph correctness, local exposure or compromise, external-share authority, production-equivalent operation, independent assurance or production authorization.

## Merge rule

Do not merge while any workflow on the final exact head is queued, in progress, failed, cancelled or otherwise non-successful. After every registered exact-head workflow is `completed/success` and the PR is mergeable, mark it ready and merge with `expected_head_sha` protection.

The next bounded priority after accepted merge is **Phase 11.10g — MISP Sharing & Exchange**.
