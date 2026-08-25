# Integrated Analysis Workspace

Status: **Phase 11.10q functional recovery — object-driven analysis implemented; exact-head validation required**

The **Analysis & Enrichment** workspace at `/workbench/analysis` combines persisted IntelOwl enrichment and Cortex analyzer evidence for canonical DTMO intelligence objects without requiring opaque UUID copy/paste as the primary workflow.

## Select an object

The primary target surface discovers **recent canonical intelligence from DTMO persistence**. Select an object to load its persisted IntelOwl/Cortex history. The manual canonical UUID field remains only under **Advanced deep link / troubleshooting**.

A pivot from IOC Explorer carries the canonical item plus the selected `observable_type` and `observable_value` into Analysis & Enrichment. This pre-populates the explicit execution target; it does not execute an analyzer automatically.

Threat Intelligence object detail now also exposes a direct **Analyze & enrich** pivot. It carries only the canonical item identifier into `/workbench/analysis`; Analysis then reloads persisted history through the server-authorized DTMO API. Following this pivot does not execute an analyzer automatically and does not grant `review:intelligence` authority.

If canonical target discovery is unavailable, the page fails closed and does not infer an empty object inventory or platform health.

## Read-only access

A principal with `read:intelligence` can inspect:

- recent canonical intelligence targets;
- whether IntelOwl and Cortex capabilities are enabled;
- the explicit observable/analyzer allowlists exposed by DTMO;
- persisted IntelOwl history;
- persisted Cortex analyzer history and stored Cortex result payloads;
- job identity, status and applicable analyzer metadata;
- the evidence boundary attached to the combined history.

Enabled/configured capability does not mean the upstream service is healthy.

## Run analysis

Execution requires the server-side `review:intelligence` permission. A read-only principal sees target discovery and history but the **Run IntelOwl** and **Run Cortex** controls remain disabled.

For an authorized reviewer:

1. select recent canonical intelligence, arrive through an object-driven IOC pivot, or follow the direct Threat Intelligence object pivot;
2. verify the selected observable type and value;
3. for IntelOwl, preserve the required handling classification and choose explicit allowlisted analyzers;
4. for Cortex, choose one explicit allowlisted analyzer and a TLP value from 0 through 3;
5. start the chosen engine explicitly;
6. review the persisted job/history and result in the corresponding history panel.

There is no automatic IntelOwl-to-Cortex fallback, no automatic analyzer discovery, and no automatic execution merely because a user follows a pivot.

## Interpretation

**Enrichment is evidence, not a verdict.** IntelOwl and Cortex results do not prove local compromise by themselves. Both histories remain bounded by `External share: no` and `Local compromise proven: no`; analyzer output has no external-share or publication authority.

Cortex is analyzer-only. Responders and other external side-effect actions are not exposed through this workspace.

## Failure behavior

The workspace must **fail closed**. An upstream, policy, canonical-object or persistence failure is presented as an error. DTMO does not synthesize a success result, healthy upstream state, empty evidence conclusion, approval state or compromise conclusion.

## Production boundary

Repository/browser CI can validate exact-head interaction and authority boundaries, but it does **not prove** live analyzer availability or provider authorization, production-equivalent operation, independent assurance or production authorization. Phase 11.10q remains blocked until the owner functional retest accepts the canonical interface.
