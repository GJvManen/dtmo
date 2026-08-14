# Owner Acceptance Polish — Contrast and Governance Visibility

## Status

`IMPLEMENTED_PENDING_EXACT_HEAD_CI_AND_OWNER_RETEST`

## Trigger

A real product acceptance run after the external framework test reported three remaining usability/functional defects:

1. Overview → Recent intelligence: source/meta text had insufficient contrast on the dark-blue intelligence cards.
2. Intelligence → Recent ingested: the same source/meta contrast defect was visible.
3. Governance: the explicit repository-backed framework crosswalk introduced by PR #187 was not visible in the highest composed canonical console.

The project owner also reported that the framework had been externally tested and otherwise worked as intended. That statement is retained as functional external-test feedback; it does not by itself establish Phase 8 production-equivalent staging acceptance because the immutable deployment-identity evidence remains separate.

## Root cause

The recent-intelligence cards receive severity classes such as `severity-informational`. The E1/E2 severity stylesheet used those same classes to set foreground colours intended for compact severity controls. Because the severity class is also applied to the full card, the foreground colour cascaded into source metadata and other card text on the dark-blue card surface.

The Governance crosswalk existed in the API and its own composition layer, but later E3/E6 composition layers build the canonical page from `framework_experience._PAGE`. The canonical page therefore continued to load the framework JavaScript while omitting the later server-side crosswalk panel/script composition.

## Repair

- keep severity semantics and coloured severity pills/borders, while forcing recent-intelligence body/meta/link text to accessible high-contrast foreground colours;
- make the Governance crosswalk enhancement resilient to higher composition layers by augmenting the already-loaded framework experience script;
- dynamically add the crosswalk panel only when it is absent and initialize it once;
- retain the existing explicit API `/api/v1/governance/control-crosswalk` as the source of mapping truth;
- add a dedicated owner-acceptance regression gate.

## Claim boundary

This repair does not mark owner acceptance complete until the exact-head CI matrix succeeds and the real console is manually retested. It also does not convert external functional testing into Phase 8 staging evidence.
