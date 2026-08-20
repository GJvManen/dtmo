# DTMO UI/API Contract

Status: **Phase 11.10a–11.10f — PASS / REPOSITORY_COMPLETE; Phase 11.10g — ACTIVE MISP SHARING & EXCHANGE**  
Last updated: **2026-08-20**

## Purpose

This accepted contract defines how the DTMO Unified Operations Workbench consumes governed application capabilities. It prevents the browser from becoming an uncontrolled integration client and preserves server-side RBAC, auditability, provenance and human authority.

Phase 11.10b applied the contract to the canonical shell. Phase 11.10c added the Command Center, Phase 11.10d governed intelligence discovery/canonical investigation, Phase 11.10e human-triggered IntelOwl/Cortex analysis, Phase 11.10f read-only persisted OpenCTI graph/entity evidence, and Phase 11.10g applies the same contract to governed MISP Sharing & Exchange.

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
- explicit when a graph relationship, sharing decision or transfer state is unavailable rather than inferred.

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

### Accepted OpenCTI graph/entity routes

Phase 11.10f uses:

- `GET /api/v1/opencti/capabilities` — `read:intelligence`;
- `GET /api/v1/opencti/items/{item_id}/graph` — `read:intelligence`;
- `GET /api/v1/opencti/entities/{mapping_id}` — `read:intelligence`.

The browser never receives OpenCTI credentials and never calls OpenCTI `/graphql` directly.

### Active MISP Sharing & Exchange routes

Phase 11.10g uses:

- `GET /api/v1/sharing/items/{item_id}` — `read:intelligence`; sanitized canonical review/share/restriction/export state;
- `POST /api/v1/intelligence/{item_id}/review` — `review:intelligence`; human review with reviewer attribution;
- `POST /api/v1/intelligence/{item_id}/share-approval` — `approve:share`; separate human external-share approval;
- `POST /api/v1/intelligence/{item_id}/misp-export` — `approve:share`; transfer of an already reviewed/share-approved canonical revision to an unpublished MISP event.

MISP credentials remain server-side and the browser never calls a MISP `/events/...` endpoint directly.

## 4. Object identity

Every frontend object must use a stable DTMO canonical identifier where one exists. Mutable labels, display names or vendor-specific names must not become security-sensitive identity keys.

External identifiers may be shown as attributable context, including STIX IDs, MISP IDs, TheHive case IDs, Cortex job/analyzer IDs and OpenCTI object IDs.

Phase 11.10g sharing deep links use the canonical DTMO intelligence UUID. MISP export evidence preserves the deterministic current-revision event UUID and upstream event ID where confirmed.

## 5. Authentication and authorization

Production identity remains externally established according to the configured DTMO trust model. Frontend behavior may adapt to the authenticated principal for usability, but authorization is enforced on the server.

The browser must not treat hidden/disabled buttons as authorization, synthesize roles/approval authority, persist production API secrets as browser preferences, or use upstream credentials directly.

**Server-side RBAC** remains authoritative. Phase 11.10g keeps `read:intelligence`, `review:intelligence` and `approve:share` as distinct authorities. The recorded share approver must be a different human principal from the reviewer. Service accounts cannot substitute for human review/share authority or MISP export.

## 6. Governed writes

High-impact writes require clear intent and auditable server-side handling. Examples include source execution, analyzer initiation, case mutation, MISP publication preparation/synchronization, role changes, approvals and playbook execution.

A successful HTTP response establishes only the action defined by that endpoint. It does not imply unrelated authority.

Phase 11.10g reuses accepted governed writes rather than creating a browser-side approval model. Review cannot grant share approval. Share approval does not publish an event. MISP export cannot grant approval and creates the destination event with `published=false`.

## 7. Human authority boundaries

The API contract preserves separate decisions for intelligence review, case handoff/case mutation, external share/publication approval, administrative authorization and playbook approval.

Technical integration success cannot collapse these decisions into one implicit permission. Human/service identity separation remains explicit.

The 11.10g flow is **prepare → review → explicit share approval → publish/synchronize when authorized**. In this slice, the implemented export step stops before publication: the MISP event is created unpublished and no Publish or Synchronize action is exposed. Future publication/synchronization, if accepted, remains a separate governed decision.

## 8. Enrichment and analysis results

IntelOwl and Cortex outputs are evidence inputs. **No enrichment result alone proves local compromise** or grants external sharing authority. Accepted 11.10e persistence keeps external sharing unauthorized and local compromise unproven.

## 9. OpenCTI graph results

The accepted DTMO OpenCTI persistence boundary stores object mappings and immutable revisions but does not durably store generic OpenCTI entity-to-entity relationship topology. Graph roots are canonical DTMO intelligence items, OpenCTI nodes originate from persisted mappings, edges are `canonical-mapping` evidence only, missing topology must **fail closed**, and graph presence does not prove local exposure or compromise.

## 10. MISP exchange

MISP operations exposed to the browser must distinguish canonical review/share state, technical export and future publication/synchronization authority.

Phase 11.10g requires:

- authoritative reviewer and share-approver attribution;
- separate human reviewer and share approver;
- authoritative MISP-origin distribution, sharing-group and TLP restrictions before re-export;
- rejection of requested handling that weakens source restrictions;
- deterministic current-revision replay identity;
- automatic replay blocked by `pending`, `success` or `uncertain` evidence;
- uncertain delivery treated as requiring operator inspection;
- MISP event payload `published=false`;
- no browser Publish or Synchronize control;
- configuration never promoted to live MISP health;
- technical export never promoted to publication, synchronization, downstream receipt or local-compromise proof.

Missing or ambiguous sharing/handling evidence must **fail closed**.

## 11. TheHive case operations

TheHive operations must preserve the accepted **case handoff/case mutation** authority boundary. Case creation/update authority remains separate from publication/share authority. Functional workbench delivery remains Phase 11.10h.

## 12. Error model

User-visible errors must distinguish authentication/authorization failure, validation, not-found/conflict, dependency degradation/unavailability, rate limiting and canonical backend failure without leaking raw secrets or stack traces.

For 11.10g, canonical sharing-state failure is unavailable rather than approved/denied state. Export conflicts expose the bounded server reason without manufacturing success. Uncertain MISP delivery remains uncertain rather than success or automatic retry.

## 13. Partial failure

Composite views must represent partial failure truthfully. One unavailable integration must not silently convert the entire view into false success. Missing canonical sharing state, missing authoritative MISP restrictions and live MISP health are separate states and must not be conflated.

## 14. Caching and freshness

Frontend caching is a performance mechanism only. APIs and UI components must expose relevant freshness timestamps/state for operational data. Browser state never becomes canonical product truth, graph evidence or sharing authority.

## 15. Audit and correlation

Governed writes remain attributable to authenticated principals/service identities. Review records `reviewed_by`; share approval records `share_approved_by`; MISP export records request/replay/audit evidence. Browser state does not replace these server-side records.

## 16. Frontend escape hatches and compatibility paths

Advanced upstream administration may remain an explicitly separate service/security boundary, but cannot weaken DTMO authorization. `/ui/console`, `/ui/intelligence-workspace` and `/ui/misp-workspace` remain **compatibility paths**, not parallel targets for feature development. The supported built canonical route is `/workbench/`.

## 17. Evidence boundary

Passing this contract test or a Phase 11 workbench browser gate proves repository-controlled interface boundaries only. It **does not prove** live upstream service behavior, MISP publication/synchronization, production-equivalent operation, independent assurance or production authorization.

Phase 11.10a–11.10f are `PASS / REPOSITORY_COMPLETE`. Phase 11.10g remains `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` until its final exact head and all registered regressions are fully green and the bounded PR is merged with expected-head protection. The only next slice after acceptance is Phase 11.10h TheHive Investigations & Cases.
