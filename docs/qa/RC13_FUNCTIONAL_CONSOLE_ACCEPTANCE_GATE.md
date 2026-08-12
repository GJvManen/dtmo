# RC13 — Functional Unified-Console Acceptance Gate

**Status:** `PASS / OWNER_ACCEPTED`  
**Acceptance date:** 2026-08-12

## Objective

RC13 establishes that the repository-controlled DTMO components operate together as a usable canonical product, not merely as individually passing APIs, workflows or UI fragments.

The gate requires both:

1. repository-controlled functional/browser evidence on the exact accepted code state; and
2. explicit accountable project-owner functional acceptance of the merged product.

## Accepted canonical journey

The accepted unified-console product boundary covers:

1. **Overview** — KPIs, source/runtime state, recent intelligence, truthful refresh and empty states;
2. **Intelligence** — durable canonical PostgreSQL intelligence with provenance/investigation context;
3. **Sources & Catalog** — catalog bootstrap, enable/disable state and supported source execution;
4. **Source-to-intelligence flow** — upstream fetch, raw evidence retention, normalization, durable canonical commit and search/index support;
5. **Visual Analytics** — native severity/source/connector/review analytical views;
6. **Administration** — governed principal/role assignment management and safety controls;
7. **Governance** — framework/mapping knowledge with explicit evidence truth states;
8. **Browser interaction** — canonical navigation and controls under supported browser evidence;
9. **Authorization boundaries** — review/share approval and privileged authority separation remain intact.

## Functional acceptance criteria

RC13 acceptance requires:

- successful canonical application startup and usable navigation;
- source and catalog operations accessible through the unified console;
- supported sources able to produce normalized records without invalid canonical type/reference failures;
- raw evidence persistence;
- canonical PostgreSQL intelligence committed before successful durable ingestion is reported;
- Intelligence views reading that canonical state;
- Overview/dashboard metrics derived from canonical intelligence;
- analytical graphics rendering truthful populated or empty states;
- reliable refresh lifecycle and no false `data updated` state for empty intelligence;
- Administration/RBAC controls remaining governed and auditable;
- Governance claims remaining evidence-backed and non-inferred;
- zero unauthorized privilege broadening or publication/share authority creation.

## Evidence classes

### Repository-controlled evidence

The RC13 workflow portfolio includes functional-console, browser, visual-analytics, Administration/RBAC, Governance, source-catalog, persistence-commit, source-normalization, Chrome/usability and supporting runtime gates.

Repository CI is necessary but not sufficient for owner acceptance.

### Accountable owner acceptance

Following the final merged RC13 repair baseline, the accountable project owner performed the functional product retest and explicitly reported:

> “Het project werkt! Gefelciteerd!”

This statement is recorded as successful accountable functional acceptance of the current RC13 baseline.

## Accepted security and governance boundaries

RC13 acceptance does not alter the project authority model:

- server-side RBAC and least privilege remain authoritative;
- service accounts cannot become human/admin authorities by execution;
- administrator safety protections remain in place;
- source execution creates technical/candidate intelligence state only;
- review and external-share approval remain distinct human-governed actions;
- Governance visibility does not create publication authority;
- missing framework mappings remain visibly unmapped;
- provenance and raw evidence remain traceable;
- CI/browser fixtures cannot create external staging or production acceptance.

## Post-acceptance enhancements

The owner identified additional desirable product improvements after declaring the project functional. They are explicitly classified as enhancements, not RC13 blockers:

- richer accessible severity colours and filtering in Overview;
- severity filtering in Intelligence;
- manual governed source onboarding;
- richer trend analysis and Visual Analytics;
- first-class framework mappings;
- deeper Administration role/right management;
- deeper Governance framework evidence views.

These are tracked in issue #171 and must be delivered in bounded, independently tested changes.

## Phase transition

With RC13 accepted, the project may enter Phase 8.

**Phase 8 state:** `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`.

Phase 8 still requires a real production-equivalent staging environment and evidence tied to one immutable deployment identity. Local Docker Compose, CI and staging emulators are not substitutes.

## Final RC13 decision

**PASS / OWNER_ACCEPTED.**

The gate may be reopened in the future only on new accountable evidence of a regression in the accepted functional boundary; historical evidence must remain immutable.
