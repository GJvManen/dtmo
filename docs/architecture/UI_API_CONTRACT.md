# DTMO UI/API Contract

Status: **Phase 11.10a — PASS / REPOSITORY_COMPLETE; Phase 11.10b — ACTIVE SHELL APPLICATION**  
Last updated: **2026-08-20**

## Purpose

This accepted contract defines how the DTMO Unified Operations Workbench consumes governed application capabilities. It prevents the browser from becoming an uncontrolled integration client and preserves server-side RBAC, auditability, provenance and human authority.

Phase 11.10b applies the contract to the canonical shell. It consumes only same-origin shell status/principal endpoints and does not introduce feature-specific governed writes.

## 1. Mandatory request path

Normal product operations use:

**DTMO browser → DTMO `/api/v1/...` → authorization/audit → canonical service → governed integration adapter**.

Equivalently, the architectural invariant remains **browser → DTMO API → governed integration adapter → upstream service**.

The browser must not directly invoke Taranis AI, IntelOwl, OpenCTI, MISP, TheHive or Cortex for governed product workflows.

## 2. API principles

Frontend-facing APIs must be:

- versioned under `/api/v1/...` for governed application capability contracts;
- server-authorized for every protected read/write;
- explicit about canonical identity and provenance;
- deterministic about loading/success/empty/partial-failure/error state;
- auditable for governed writes;
- safe to retry only where the endpoint contract explicitly permits it;
- incapable of granting publication/share authority by technical success alone.

The existing `/health` endpoint may be consumed by the shell as a same-origin platform-health signal; it is not a governed business write and does not confer authorization.

## 3. Canonical resource families

The target workbench may consume or extend governed resource families for:

- `/api/v1/console/...` — command-center summaries and canonical operational views;
- `/api/v1/intelligence/...` — intelligence objects, search, review context and timelines;
- `/api/v1/sources/...` — source registry, validation, scheduling and execution;
- `/api/v1/vulnerabilities/...` — CVE/exposure intelligence;
- `/api/v1/integrations/intelowl/...` — governed enrichment;
- `/api/v1/integrations/cortex/...` — bounded analyzer execution;
- `/api/v1/integrations/opencti/...` — graph/entity/relationship operations;
- `/api/v1/integrations/misp/...` — governed exchange preparation and synchronization;
- `/api/v1/integrations/thehive/...` — human-authorized case operations;
- `/api/v1/governance/...` — explicit provenance-backed framework/control mappings and evidence;
- `/api/v1/admin/...` — governed administration;
- `/api/v1/operations/...` — runtime/integration health where exposed to authorized users.

These are target resource families, not a claim that every route already exists. A later UI slice must add and test a missing backend contract before depending on it.

Phase 11.10b uses `/api/v1/ui/session` for attributable shell principal context when authorized and `/health` for platform status. Command Center feature APIs remain Phase 11.10c scope.

## 4. Object identity

Every frontend object must use a stable DTMO canonical identifier where one exists. Mutable labels, display names or vendor-specific names must not become security-sensitive identity keys.

External identifiers may be shown as attributable context, for example STIX IDs, MISP event/attribute IDs, TheHive case identifiers, Cortex job IDs or analyzer/provider identifiers.

Phase 11.10b does not fabricate an object identity when none is selected; the context rail explicitly remains in a no-selection state.

## 5. Authentication and authorization

Production identity remains externally established according to the configured DTMO trust model. Frontend behavior may adapt to the authenticated principal for usability, but authorization is enforced on the server.

The browser must not:

- treat hidden buttons as authorization;
- synthesize roles or approval authority;
- persist production API secrets as ordinary browser preferences;
- use upstream service credentials directly for normal product actions.

Phase 11.10b stores only a non-sensitive theme preference locally. **Server-side RBAC** remains authoritative.

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

Phase 11.10b intentionally exposes no high-impact governed command from its command palette; it is navigation-only.

## 7. Human authority boundaries

The API contract preserves separate decisions for:

- intelligence review;
- case handoff/case mutation;
- external share/publication approval;
- administrative authorization;
- playbook approval where required.

Technical integration success cannot collapse these decisions into one implicit permission. Human/service identity separation also remains explicit.

## 8. Enrichment and analysis results

IntelOwl and Cortex outputs are evidence inputs. Normalized DTMO responses should distinguish analyzer/provider, observation/verdict, attributable confidence, timestamps, permitted raw-evidence references, provenance and failures/timeouts/partial results.

No enrichment result alone proves local compromise or grants external sharing authority.

## 9. OpenCTI graph results

OpenCTI-derived graph/entity responses must preserve attributable identity, markings, confidence and relationship semantics. Graph presence does not prove local exposure or compromise.

## 10. MISP exchange

MISP operations exposed to the browser must distinguish read/synchronization from outbound sharing. The target UI flow is:

**prepare → review → explicit share approval → publish/synchronize when authorized**.

The browser must never convert a correlation, feed match or draft into publication authority.

## 11. TheHive case operations

TheHive operations must preserve the accepted case-handoff authority boundary. Case creation/update authority remains separate from publication/share authority. The UI must show the resulting case/task state rather than assuming success from a local button click.

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

Phase 11.10b shell state distinguishes pending, unavailable/unknown and healthy platform/principal context without converting missing data into success.

## 13. Partial failure

Composite command-center and object-context views must represent partial failure truthfully. One unavailable integration must not silently convert the entire view into false success, and where isolation is safe it must not unnecessarily make unrelated canonical read paths unavailable.

Command Center composite-state implementation begins in Phase 11.10c; 11.10b does not manufacture composite status.

## 14. Caching and freshness

Frontend caching is a performance mechanism only. APIs and UI components must expose relevant freshness timestamps/state for operational data. A cached response is never promoted to current evidence when its freshness is unknown.

TanStack Query in the shell controls request lifecycle only; it does not become canonical product truth.

## 15. Audit and correlation

Governed writes must remain attributable to the authenticated principal/service identity. Request IDs or equivalent correlation identifiers should connect browser action, DTMO API handling and downstream adapter activity without exposing secrets.

Phase 11.10b introduces no new governed write path.

## 16. Frontend escape hatches and compatibility paths

A link to an advanced upstream administration interface may exist only when normal DTMO workflows do not require it, it is clearly labelled as a separate service/security boundary, separate authentication/authorization is not weakened and DTMO does not claim actions taken there as canonical DTMO audit evidence unless separately ingested and attributable.

During bounded migration, `/ui/console` remains a **compatibility path**. It is not an upstream service escape hatch and not a parallel target for new feature development. The supported built canonical product route is `/workbench/`.

## 17. Evidence boundary

Passing this contract test or the Phase 11.10b shell/browser gate proves repository-controlled interface and shell boundaries only. It **does not prove** live upstream service behavior, production-equivalent operation, independent assurance or production authorization.

Phase 11.10a remains `PASS / REPOSITORY_COMPLETE`; Phase 11.10b remains `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` until its final exact head is fully green and merged.
