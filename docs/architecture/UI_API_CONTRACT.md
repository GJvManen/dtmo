# DTMO UI/API Contract

Status: **Phase 11.10a–11.10g — PASS / REPOSITORY_COMPLETE; Phase 11.10h — ACTIVE THEHIVE INVESTIGATIONS & CASES**  
Last updated: **2026-08-20**

## Purpose

This accepted contract defines how the DTMO Unified Operations Workbench consumes governed application capabilities. It prevents the browser from becoming an uncontrolled integration client and preserves server-side RBAC, auditability, provenance and human authority.

Phase 11.10b applied the contract to the canonical shell. Phase 11.10c added the Command Center, Phase 11.10d governed intelligence discovery/canonical investigation, Phase 11.10e human-triggered IntelOwl/Cortex analysis, Phase 11.10f read-only persisted OpenCTI graph/entity evidence, Phase 11.10g governed MISP Sharing & Exchange, and Phase 11.10h applies the same contract to canonical TheHive Investigations & Cases.

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
- incapable of granting publication/share or case authority by technical success alone;
- explicit when capability/configuration state is not runtime-health evidence;
- explicit when a graph relationship, sharing decision, transfer or case state is unavailable rather than inferred.

The existing `/health` endpoint may be consumed by the shell as a same-origin platform-health signal; it is not a governed business write and does not confer authorization.

## 3. Canonical resource families

The workbench consumes governed resource families for command-center state, intelligence, analysis, OpenCTI graph/entity context, sources, vulnerabilities, MISP exchange, TheHive cases, governance, administration and operations.

### Accepted integrated-analysis routes

- `GET /api/v1/analysis/capabilities` — `read:intelligence`;
- `GET /api/v1/analysis/items/{item_id}/history` — `read:intelligence`;
- `POST /api/v1/intelowl/items/{item_id}/enrich` — `review:intelligence`;
- `POST /api/v1/analysis/items/{item_id}/cortex` — `review:intelligence`.

IntelOwl/Cortex credentials remain server-side.

### Accepted OpenCTI graph/entity routes

- `GET /api/v1/opencti/capabilities` — `read:intelligence`;
- `GET /api/v1/opencti/items/{item_id}/graph` — `read:intelligence`;
- `GET /api/v1/opencti/entities/{mapping_id}` — `read:intelligence`.

The browser never receives OpenCTI credentials and never calls OpenCTI `/graphql` directly.

### Accepted MISP Sharing & Exchange routes

- `GET /api/v1/sharing/items/{item_id}` — `read:intelligence`;
- `POST /api/v1/intelligence/{item_id}/review` — `review:intelligence`;
- `POST /api/v1/intelligence/{item_id}/share-approval` — `approve:share`;
- `POST /api/v1/intelligence/{item_id}/misp-export` — `approve:share`, creating an unpublished MISP event for already reviewed/share-approved state.

MISP credentials remain server-side and the browser never calls a MISP `/events/...` endpoint directly.

### Active TheHive investigation routes

Phase 11.10h uses:

- `GET /api/v1/thehive/items/{item_id}/investigation` — `read:intelligence`; sanitized canonical intelligence/provenance/handoff state;
- `POST /api/v1/thehive/items/{item_id}/cases` — `handoff:case`; explicit human-authorized case mutation using the accepted Phase 11.6 adapter.

TheHive API token and organization authorization remain server-side. The browser never calls upstream `/api/v1/case` directly.

## 4. Object identity

Every frontend object must use a stable DTMO canonical identifier where one exists. Mutable labels, display names or vendor-specific names must not become security-sensitive identity keys.

External identifiers may be shown as attributable context, including STIX IDs, MISP IDs, TheHive case IDs, Cortex job/analyzer IDs and OpenCTI object IDs.

Sharing and investigation deep links use the canonical DTMO intelligence UUID. TheHive handoff evidence preserves request identity and stable upstream case identity/number where confirmed.

## 5. Authentication and authorization

Production identity remains externally established according to the configured DTMO trust model. Frontend behavior may adapt to the authenticated principal for usability, but authorization is enforced on the server.

The browser must not treat hidden/disabled buttons as authorization, synthesize roles/approval authority, persist production API secrets as browser preferences, or use upstream credentials directly.

**Server-side RBAC** remains authoritative. Accepted MISP sharing keeps `read:intelligence`, `review:intelligence` and `approve:share` distinct. Phase 11.10h keeps `read:intelligence` and `handoff:case` distinct; service accounts cannot substitute for explicit human case-handoff authority.

## 6. Governed writes

High-impact writes require clear intent and auditable server-side handling. Examples include source execution, analyzer initiation, case mutation, MISP publication preparation/synchronization, role changes, approvals and playbook execution.

A successful HTTP response establishes only the action defined by that endpoint. It does not imply unrelated authority.

Accepted MISP writes preserve the rule that review cannot grant share approval, share approval does not publish an event, and MISP export cannot grant approval. Phase 11.10h case creation cannot grant external-share/publication or responder authority.

## 7. Human authority boundaries

The API contract preserves separate decisions for intelligence review, case handoff/case mutation, external share/publication approval, administrative authorization and playbook approval.

Technical integration success cannot collapse these decisions into one implicit permission. Human/service identity separation remains explicit.

The sharing lifecycle remains **prepare → review → explicit share approval → publish/synchronize when authorized**. The accepted 11.10g implementation stops at unpublished export; future publication/synchronization remains separately governed.

The Phase 11.10h case lifecycle is **inspect canonical evidence → explicit human case handoff → persist delivery/reconciliation evidence**. Later upstream case operations are not inferred from handoff success.

## 8. Enrichment and analysis results

IntelOwl and Cortex outputs are evidence inputs. **No enrichment result alone proves local compromise** or grants external sharing authority. Accepted 11.10e persistence keeps external sharing unauthorized and local compromise unproven.

## 9. OpenCTI graph results

The accepted DTMO OpenCTI persistence boundary stores object mappings and immutable revisions but does not durably store generic OpenCTI entity-to-entity relationship topology. Graph roots are canonical DTMO intelligence items, OpenCTI nodes originate from persisted mappings, edges are `canonical-mapping` evidence only, missing topology must **fail closed**, and graph presence does not prove local exposure or compromise.

## 10. MISP exchange

Accepted MISP behavior requires authoritative reviewer/share-approver attribution, separate human decisions, source handling preservation, replay protection, `published=false` event creation and no browser Publish/Synchronize control. Configuration never becomes live health and technical export never becomes publication, synchronization, downstream receipt or local-compromise proof.

## 11. TheHive case operations

TheHive operations preserve the accepted **case handoff/case mutation** authority boundary. Case creation authority remains separate from publication/share authority.

Phase 11.10h requires:

- canonical item/provenance before mutation;
- server-side `handoff:case` authorization and human principal;
- server-side TheHive token/organization only;
- fail-closed TLP/PAP and authoritative source handling;
- durable reservation before external mutation;
- attributable `reserved`, `delivered`, `ambiguous` and `failed` state;
- manual reconciliation for ambiguous/reserved state rather than blind UI replay;
- no inference of alerts, tasks, case timeline, later upstream case state or responder results where accepted persistence/readback has no evidence;
- no external-share authority or local-compromise proof from case presence;
- configuration not promoted to live TheHive health.

## 12. Error model

User-visible errors must distinguish authentication/authorization failure, validation, not-found/conflict, dependency degradation/unavailability, rate limiting and canonical backend failure without leaking raw secrets or stack traces.

For 11.10h, canonical investigation-state failure is unavailable rather than “no case” or “healthy”. Ambiguous TheHive delivery remains ambiguous/reconciliation-required rather than success or automatic retry.

## 13. Partial failure

Composite views must represent partial failure truthfully. One unavailable integration must not silently convert the entire view into false success. Missing canonical state, missing authoritative handling and live upstream health are separate states and must not be conflated.

## 14. Caching and freshness

Frontend caching is a performance mechanism only. APIs and UI components must expose relevant freshness timestamps/state for operational data. Browser state never becomes canonical product truth, graph evidence, sharing authority or TheHive case truth.

## 15. Audit and correlation

Governed writes remain attributable to authenticated principals/service identities. Review records reviewer identity, share approval records approver identity, MISP export records request/replay/audit evidence, and TheHive handoff records request ID, requesting human, organization and durable outcome/reconciliation state. Browser state does not replace these server-side records.

## 16. Frontend escape hatches and compatibility paths

Advanced upstream administration may remain an explicitly separate service/security boundary, but cannot weaken DTMO authorization. `/ui/console`, `/ui/intelligence-workspace` and `/ui/misp-workspace` remain **compatibility paths**, not parallel targets for feature development. The supported built canonical route is `/workbench/`.

## 17. Evidence boundary

Passing this contract test or a Phase 11 workbench browser gate proves repository-controlled interface boundaries only. It **does not prove** live upstream service behavior, MISP publication/synchronization, TheHive upstream case completeness/responder execution, production-equivalent operation, independent assurance or production authorization.

Phase 11.10a–11.10g are `PASS / REPOSITORY_COMPLETE`. Phase 11.10h remains `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` until its final exact head and all registered regressions are fully green and the bounded PR is merged with expected-head protection. The only next slice after acceptance is Phase 11.10i Vulnerability & Exposure.
