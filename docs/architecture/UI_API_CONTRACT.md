# DTMO UI/API Contract

Status: **Phase 11.10a–11.10e — PASS / REPOSITORY_COMPLETE; Phase 11.10f — ACTIVE OPENCTI GRAPH/ENTITY**  
Last updated: **2026-08-20**

## Purpose

This accepted contract defines how the DTMO Unified Operations Workbench consumes governed application capabilities. It prevents the browser from becoming an uncontrolled integration client and preserves server-side RBAC, auditability, provenance and human authority.

Phase 11.10b applied the contract to the canonical shell. Phase 11.10c added the Command Center, Phase 11.10d governed intelligence discovery/canonical investigation, Phase 11.10e human-triggered IntelOwl/Cortex analysis, and Phase 11.10f applies the same contract to read-only persisted OpenCTI graph/entity evidence.

## 1. Mandatory request path

Normal product operations use:

**DTMO browser → DTMO `/api/v1/...` → authorization/audit → canonical service → governed integration adapter**.

Equivalently, the architectural invariant remains **browser → DTMO API → governed integration adapter → upstream service**.

The browser **must not directly invoke Taranis AI, IntelOwl, OpenCTI, MISP, TheHive or Cortex** for governed product workflows.

## 2. API principles

Frontend-facing APIs must be:

- versioned under `/api/v1/...` for governed capability contracts;
- **server-authorized** for every protected read/write;
- explicit about canonical identity and provenance;
- deterministic about loading/success/empty/partial-failure/error state;
- auditable for governed writes;
- safe to retry only where explicitly permitted;
- incapable of granting publication/share authority by technical success alone;
- explicit when capability/configuration state is not runtime-health evidence;
- explicit when a graph relationship is unavailable rather than inferred.

The existing `/health` endpoint may be consumed by the shell as a same-origin platform-health signal; it is not a governed business write and does not confer authorization.

## 3. Canonical resource families

The workbench consumes governed resource families for command-center state, intelligence, analysis, OpenCTI graph/entity context, sources, vulnerabilities, MISP exchange, TheHive cases, governance, administration and operations.

### Accepted integrated-analysis routes

Phase 11.10e uses:

- `GET /api/v1/analysis/capabilities` — `read:intelligence`;
- `GET /api/v1/analysis/items/{item_id}/history` — `read:intelligence`;
- `POST /api/v1/intelowl/items/{item_id}/enrich` — `review:intelligence`;
- `POST /api/v1/analysis/items/{item_id}/cortex` — `review:intelligence`.

IntelOwl/Cortex credentials remain server-side.

### Active OpenCTI graph/entity routes

Phase 11.10f uses:

- `GET /api/v1/opencti/capabilities` — requires `read:intelligence`; reports feature/configuration state and allowed entity types without a runtime-health claim;
- `GET /api/v1/opencti/items/{item_id}/graph` — requires `read:intelligence`; returns one canonical DTMO root plus persisted OpenCTI mapping nodes and proven mapping edges;
- `GET /api/v1/opencti/entities/{mapping_id}` — requires `read:intelligence`; returns persisted stable OpenCTI/STIX identity, markings, confidence, external references, provenance, snapshot identity and immutable revision history.

The browser never receives OpenCTI credentials and never calls OpenCTI `/graphql` directly.

## 4. Object identity

Every frontend object must use a stable DTMO canonical identifier where one exists. Mutable labels, display names or vendor-specific names must not become security-sensitive identity keys.

External identifiers may be shown as attributable context, including STIX IDs, MISP IDs, TheHive case IDs, Cortex job/analyzer IDs and OpenCTI object IDs.

Phase 11.10f graph roots use canonical DTMO intelligence UUIDs. OpenCTI entity detail uses the persisted DTMO mapping UUID while preserving OpenCTI and STIX identities as attributable external identifiers.

## 5. Authentication and authorization

Production identity remains externally established according to the configured DTMO trust model. Frontend behavior may adapt to the authenticated principal for usability, but authorization is enforced on the server.

The browser must not treat hidden/disabled buttons as authorization, synthesize roles/approval authority, persist production API secrets as browser preferences, or use upstream credentials directly.

**Server-side RBAC** remains authoritative. Phase 11.10f is read-only and requires `read:intelligence` for every graph/entity endpoint.

## 6. Governed writes

High-impact writes require clear intent and auditable server-side handling. Examples include source execution, analyzer initiation, case mutation, MISP publication preparation/synchronization, role changes, approvals and playbook execution.

A successful HTTP response establishes only the action defined by that endpoint. It does not imply unrelated authority.

Phase 11.10f adds **no governed write**. It does not mutate OpenCTI, execute connectors, synchronize MISP, create TheHive cases or approve/publish intelligence.

## 7. Human authority boundaries

The API contract preserves separate decisions for intelligence review, case handoff/case mutation, external share/publication approval, administrative authorization and playbook approval.

Technical integration success cannot collapse these decisions into one implicit permission. Human/service identity separation remains explicit.

## 8. Enrichment and analysis results

IntelOwl and Cortex outputs are evidence inputs. **No enrichment result alone proves local compromise** or grants external sharing authority. Accepted 11.10e persistence keeps external sharing unauthorized and local compromise unproven.

## 9. OpenCTI graph results

OpenCTI-derived graph/entity responses must preserve attributable identity, markings, confidence, provenance and relationship semantics.

The current accepted DTMO OpenCTI persistence boundary stores object mappings and immutable revisions but does not durably store generic OpenCTI entity-to-entity relationship topology. Therefore:

- the graph root is the canonical DTMO intelligence item;
- OpenCTI nodes originate from persisted mappings;
- edges in 11.10f are `canonical-mapping` evidence only;
- `upstream_relationship_topology_persisted=false` is explicit;
- malware/campaign/actor/indicator/infrastructure relationships must not be inferred from co-occurrence, labels, entity types or visual proximity;
- empty persisted mappings are not an upstream-absence claim;
- graph presence does not prove local exposure or compromise;
- existing persistence grants no external-share authority and no local-compromise proof.

Missing or ambiguous topology must **fail closed**.

## 10. MISP exchange

MISP operations exposed to the browser must distinguish read/synchronization from outbound sharing. The target UI flow remains:

**prepare → review → explicit share approval → publish/synchronize when authorized**.

The browser must never convert a correlation, feed match or draft into publication authority. Phase 11.10g owns the bounded workbench implementation.

## 11. TheHive case operations

TheHive operations must preserve the accepted **case handoff/case mutation** authority boundary. Case creation/update authority remains separate from publication/share authority.

## 12. Error model

User-visible errors must distinguish authentication/authorization failure, validation, not-found/conflict, dependency degradation/unavailability, rate limiting and canonical backend failure without leaking raw secrets or stack traces.

For 11.10f, graph dependency failure is unavailable rather than an empty graph. Entity-detail failure must not reconstruct complete canonical evidence from incomplete display data.

## 13. Partial failure

Composite views must represent partial failure truthfully. One unavailable integration must not silently convert the entire view into false success.

For OpenCTI, missing persisted mapping evidence and unavailable canonical persistence are distinct states. Neither may be transformed into a claim about complete upstream OpenCTI knowledge.

## 14. Caching and freshness

Frontend caching is a performance mechanism only. APIs and UI components must expose relevant freshness timestamps/state for operational data. Browser state never becomes canonical product truth or graph evidence.

## 15. Audit and correlation

Governed writes remain attributable to authenticated principals/service identities. Phase 11.10f adds no new write; read-side identity/provenance remains attributable through canonical DTMO persistence and OpenCTI mapping/revision records.

## 16. Frontend escape hatches and compatibility paths

Advanced upstream administration may remain an explicitly separate service/security boundary, but cannot weaken DTMO authorization. `/ui/console` and prior UI routes remain **compatibility paths**, not parallel targets for feature development. The supported built canonical route is `/workbench/`.

## 17. Evidence boundary

Passing this contract test or a Phase 11 workbench browser gate proves repository-controlled interface boundaries only. It **does not prove** live upstream service behavior, production-equivalent operation, independent assurance or production authorization.

Phase 11.10a–11.10e are `PASS / REPOSITORY_COMPLETE`. Phase 11.10f remains `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` until its final exact head and all registered regressions are fully green and the bounded PR is merged with expected-head protection. The only next slice after acceptance is Phase 11.10g MISP Sharing & Exchange.
