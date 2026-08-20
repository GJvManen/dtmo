# DTMO UI/API Contract

Status: **Phase 11.10a–11.10d — PASS / REPOSITORY_COMPLETE; Phase 11.10e — ACTIVE INTEGRATED ANALYSIS**  
Last updated: **2026-08-20**

## Purpose

This accepted contract defines how the DTMO Unified Operations Workbench consumes governed application capabilities. It prevents the browser from becoming an uncontrolled integration client and preserves server-side RBAC, auditability, provenance and human authority.

Phase 11.10b applied the contract to the canonical shell. Phase 11.10c added the read-only Command Center, Phase 11.10d added governed intelligence discovery/canonical investigation, and Phase 11.10e applies the same contract to human-triggered IntelOwl enrichment and analyzer-only Cortex execution/history.

## 1. Mandatory request path

Normal product operations use:

**DTMO browser → DTMO `/api/v1/...` → authorization/audit → canonical service → governed integration adapter**.

Equivalently, the architectural invariant remains **browser → DTMO API → governed integration adapter → upstream service**.

The browser **must not directly invoke Taranis AI, IntelOwl, OpenCTI, MISP, TheHive or Cortex** for governed product workflows.

## 2. API principles

Frontend-facing APIs must be:

- versioned under `/api/v1/...` for governed application capability contracts;
- **server-authorized** for every protected read/write;
- explicit about canonical identity and provenance;
- deterministic about loading/success/empty/partial-failure/error state;
- auditable for governed writes;
- safe to retry only where the endpoint contract explicitly permits it;
- incapable of granting publication/share authority by technical success alone;
- explicit when a returned capability is configuration state rather than runtime-health evidence.

The existing `/health` endpoint may be consumed by the shell as a same-origin platform-health signal; it is not a governed business write and does not confer authorization.

## 3. Canonical resource families

The workbench consumes or may extend governed resource families for:

- `/api/v1/command-center` and `/api/v1/console/...` — operational summaries and canonical views;
- `/api/v1/intelligence/...` — intelligence objects, search, review context and timelines;
- `/api/v1/analysis/...` — integrated analysis capability, history and bounded analyzer execution;
- `/api/v1/intelowl/...` — governed IntelOwl enrichment/history;
- `/api/v1/sources/...` — source registry, validation, scheduling and execution;
- `/api/v1/vulnerabilities/...` — CVE/exposure intelligence;
- `/api/v1/integrations/opencti/...` — graph/entity/relationship operations;
- `/api/v1/integrations/misp/...` — governed exchange preparation and synchronization;
- `/api/v1/integrations/thehive/...` — human-authorized case operations;
- `/api/v1/governance/...` — explicit provenance-backed framework/control mappings and evidence;
- `/api/v1/admin/...` — governed administration;
- `/api/v1/operations/...` — runtime/integration health where exposed to authorized users.

These are controlled resource families, not a claim that every target route already exists. A later UI slice must add and test a missing backend contract before depending on it.

### Current integrated-analysis routes

Phase 11.10e uses:

- `GET /api/v1/analysis/capabilities` — requires `read:intelligence`; reports configured feature/allowlist state only and makes no runtime-health claim;
- `GET /api/v1/analysis/items/{item_id}/history` — requires `read:intelligence`; returns persisted IntelOwl/Cortex evidence for the canonical item;
- `POST /api/v1/intelowl/items/{item_id}/enrich` — requires `review:intelligence`; preserves the accepted IntelOwl policy/persistence boundary;
- `POST /api/v1/analysis/items/{item_id}/cortex` — requires `review:intelligence`; executes one explicit allowlisted analyzer with explicit TLP.

The browser never receives IntelOwl/Cortex credentials and never calls their upstream APIs directly.

## 4. Object identity

Every frontend object must use a stable DTMO canonical identifier where one exists. Mutable labels, display names or vendor-specific names must not become security-sensitive identity keys.

External identifiers may be shown as attributable context, for example STIX IDs, MISP event/attribute IDs, TheHive case identifiers, Cortex job IDs or analyzer/provider identifiers.

Phase 11.10e binds both IntelOwl and Cortex evidence to the canonical DTMO intelligence UUID. Cortex persistence additionally validates the returned canonical identity and uses the stable Cortex job ID for idempotence.

## 5. Authentication and authorization

Production identity remains externally established according to the configured DTMO trust model. Frontend behavior may adapt to the authenticated principal for usability, but authorization is enforced on the server.

The browser must not:

- treat hidden or disabled buttons as authorization;
- synthesize roles or approval authority;
- persist production API secrets as ordinary browser preferences;
- use upstream service credentials directly for normal product actions.

**Server-side RBAC** remains authoritative. In Phase 11.10e, a principal with `read:intelligence` may inspect analysis capability/history while analyzer execution requires separate `review:intelligence` authority.

## 6. Governed writes

High-impact writes require clear intent and auditable server-side handling. Where applicable the frontend supplies a request/correlation identifier and receives an attributable result.

Examples include:

- source enable/disable or execution;
- enrichment/analyzer job initiation;
- case creation/update/task mutation;
- MISP draft preparation or governed publication request;
- role/permission changes;
- approval/review transitions;
- playbook execution or approval.

A successful HTTP response establishes only the action defined by that endpoint. It does not imply unrelated authority.

Phase 11.10e exposes explicit IntelOwl and Cortex execution only to principals for whom the server grants `review:intelligence`. Cortex remains analyzer-only: responders, automatic analyzer discovery, automatic IntelOwl-to-Cortex fallback and other side-effect actions remain outside this slice.

## 7. Human authority boundaries

The API contract preserves separate decisions for:

- intelligence review;
- case handoff/case mutation;
- external share/publication approval;
- administrative authorization;
- playbook approval where required.

Technical integration success cannot collapse these decisions into one implicit permission. Human/service identity separation also remains explicit.

Analyzer execution authority is not publication/share authority. A successful enrichment or analyzer job does not approve intelligence for sharing, create case authority, or authorize production.

## 8. Enrichment and analysis results

IntelOwl and Cortex outputs are evidence inputs. Normalized DTMO responses distinguish analyzer/provider, observation/verdict, attributable confidence where available, timestamps, permitted raw-evidence references, provenance and failures/timeouts/partial results.

**No enrichment result alone proves local compromise** or grants external sharing authority.

Phase 11.10e persists Cortex evidence with explicit invariants that external sharing remains unauthorized and local compromise remains unproven. IntelOwl retains the same accepted no-share/no-compromise evidence boundary.

Capability configuration is not runtime-health evidence. Failure to retrieve history or execute an analyzer must **fail closed**; the browser must not synthesize a successful result, healthy upstream state or empty-global-evidence conclusion.

## 9. OpenCTI graph results

OpenCTI-derived graph/entity responses must preserve attributable identity, markings, confidence and relationship semantics. Graph presence does not prove local exposure or compromise. The dedicated canonical graph/entity workspace remains Phase 11.10f scope.

## 10. MISP exchange

MISP operations exposed to the browser must distinguish read/synchronization from outbound sharing. The target UI flow is:

**prepare → review → explicit share approval → publish/synchronize when authorized**.

The browser must never convert a correlation, feed match or draft into publication authority.

## 11. TheHive case operations

TheHive operations must preserve the accepted **case handoff/case mutation** authority boundary. Case creation/update authority remains separate from publication/share authority. The UI must show the resulting case/task state rather than assuming success from a local button click.

## 12. Error model

User-visible errors must preserve enough structure to distinguish:

- `authentication_required`;
- `forbidden`;
- `validation_failed`;
- `not_found`;
- `conflict`;
- `dependency_degraded`;
- `dependency_unavailable`;
- `rate_limited`;
- `canonical_backend_failure`.

Raw upstream secrets, credentials, stack traces and sensitive payloads must not be leaked to the browser.

Phase 11.10e maps policy/canonical-object/upstream failures to bounded DTMO errors. The UI reports failed/unavailable analysis rather than fabricating a result.

## 13. Partial failure

Composite command-center, intelligence-object and analysis views must represent partial failure truthfully. One unavailable integration must not silently convert the entire view into false success, and where isolation is safe it must not unnecessarily make unrelated canonical read paths unavailable.

IntelOwl and Cortex histories remain separate evidence streams inside one analysis workspace. Failure of one engine does not authorize inference about the other.

## 14. Caching and freshness

Frontend caching is a performance mechanism only. APIs and UI components must expose relevant freshness timestamps/state for operational data. A cached response is never promoted to current evidence when its freshness is unknown.

Browser state never becomes canonical product truth or the durable analysis evidence store.

## 15. Audit and correlation

Governed writes must remain attributable to the authenticated principal/service identity. Request IDs or equivalent correlation identifiers should connect browser action, DTMO API handling and downstream adapter activity without exposing secrets.

Phase 11.10e persists the requesting principal with Cortex analysis history and preserves the existing attributable IntelOwl persistence model.

## 16. Frontend escape hatches and compatibility paths

A link to an advanced upstream administration interface may exist only when normal DTMO workflows do not require it, it is clearly labelled as a separate service/security boundary, separate authentication/authorization is not weakened and DTMO does not claim actions taken there as canonical DTMO audit evidence unless separately ingested and attributable.

During bounded migration, `/ui/console` and prior UI routes remain **compatibility paths**. They are not parallel targets for new feature development. The supported built canonical product route is `/workbench/`.

## 17. Evidence boundary

Passing this contract test or a Phase 11 workbench browser gate proves repository-controlled interface boundaries only. It **does not prove** live upstream service behavior, production-equivalent operation, independent assurance or production authorization.

Phase 11.10a–11.10d remain `PASS / REPOSITORY_COMPLETE`. Phase 11.10e remains `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` until its final exact head and all registered regressions are fully green and the bounded PR is merged with expected-head protection. The only next slice after acceptance is Phase 11.10f OpenCTI graph/entity workspace.
