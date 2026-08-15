# RC13 — Functional Unified-Console Acceptance Gate

**Status:** `PASS / OWNER_ACCEPTED`  
**Acceptance date:** 2026-08-12  
**Document role:** historical functional acceptance boundary; current production-readiness status is maintained in `docs/project/CURRENT_STATE.md` and the production roadmap.

## Objective

RC13 established that the repository-controlled DTMO components operated together as a usable canonical product rather than only as individually passing APIs, workflows or UI fragments.

The gate required both repository-controlled functional/browser evidence on the accepted code state and explicit accountable project-owner functional acceptance of the merged product.

## Accepted canonical journey

The accepted product boundary covered:

1. **Overview** — KPIs, source/runtime state, recent intelligence, truthful refresh and empty states;
2. **Intelligence** — durable canonical PostgreSQL intelligence with provenance/investigation context;
3. **Sources & Catalog** — catalog bootstrap, enable/disable state and supported source execution;
4. **Source-to-intelligence flow** — upstream fetch, raw evidence retention, normalization, durable canonical commit and search/index support;
5. **Visual Analytics** — native analytical views;
6. **Administration** — governed principal/role assignment management and safety controls;
7. **Governance** — framework/mapping knowledge with explicit evidence truth states;
8. **Browser interaction** — canonical navigation and controls under supported browser evidence;
9. **Authorization boundaries** — review/share approval and privileged authority separation.

## Functional acceptance criteria

RC13 acceptance required usable application startup/navigation, governed source/catalog operations, supported normalization/persistence, canonical PostgreSQL commit before durable-success reporting, truthful Intelligence/Overview/analytics behavior, governed Administration/RBAC, evidence-backed Governance claims and preservation of publication/share authority boundaries.

## Evidence classes

### Repository-controlled evidence

The RC13 workflow portfolio covered the functional console, browser journeys, visual analytics, Administration/RBAC, Governance, source catalog, persistence, normalization and supporting runtime behavior. Repository CI was necessary but not sufficient for owner acceptance.

### Accountable owner acceptance

After final product retesting, the accountable project owner explicitly accepted the functional product. That decision is preserved as the RC13 `PASS / OWNER_ACCEPTED` evidence class.

## Accepted security and governance boundaries

RC13 acceptance did not alter the authority model:

- server-side RBAC and least privilege remained authoritative;
- service identities did not gain human/admin authority through execution;
- administrator safeguards remained in place;
- source execution created technical/candidate intelligence state only;
- review and external-share approval remained distinct human-governed actions;
- Governance visibility did not create publication authority;
- provenance and raw evidence remained traceable;
- CI/browser fixtures could not create staging, independent-assurance or production acceptance.

## Later product evolution

The post-RC13 enhancement line subsequently delivered severity/classification filtering, governed manual source onboarding, richer trends and vulnerability analytics, versioned provenance-backed framework mappings, deeper Administration/RBAC, deeper Governance evidence views and the E8 vulnerability/CTI ecosystem capabilities.

These later capabilities do not rewrite the historical RC13 acceptance boundary. They are governed by their own repository evidence and, where included in the production candidate, by the applicable Phase 8/9 evidence requirements.

## Phase transition — historical versus current state

At the time RC13 was accepted, the next lifecycle objective was entry into Phase 8. That point-in-time transition is historical context only.

The current project state has progressed substantially: the post-E8 candidate has been externally deployed/tested in an owner-approved production-equivalent staging environment, the Phase 8.2–8.5 repository contracts are complete, and formal Phase 8 closure now depends on external evidence consolidation and accountable owner acceptance against one immutable staging identity.

## Final RC13 decision

**PASS / OWNER_ACCEPTED.**
