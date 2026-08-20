# Integrated Analysis Workspace

Status: **Phase 11.10e — IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**

The **Analysis & Enrichment** workspace at `/workbench/analysis` combines persisted IntelOwl enrichment and Cortex analyzer evidence for one canonical DTMO intelligence object.

## Open an object

Enter the canonical intelligence UUID and choose **Load analysis history**, or open the route with `?item=<uuid>`. The page retrieves stored analysis history through the DTMO API. If history cannot be retrieved, the page reports it as unavailable and does not display a fabricated empty history.

## Read-only access

A principal with `read:intelligence` can inspect:

- whether IntelOwl and Cortex capabilities are enabled;
- the explicit observable/analyzer allowlists exposed by DTMO;
- persisted IntelOwl history;
- persisted Cortex analyzer history;
- job identity, status and applicable analyzer metadata;
- the evidence boundary attached to the combined history.

Enabled/configured capability does not mean the upstream service is healthy.

## Run analysis

Execution requires the server-side `review:intelligence` permission. A read-only principal sees the workspace but the **Run IntelOwl** and **Run Cortex** controls remain disabled.

For an authorized reviewer:

1. select the canonical item;
2. enter an approved observable type and value;
3. for IntelOwl, preserve the required handling classification and choose explicit allowlisted analyzers;
4. for Cortex, choose one explicit allowlisted analyzer and a TLP value from 0 through 3;
5. start the chosen engine explicitly;
6. review the persisted result in the corresponding history panel.

There is no automatic IntelOwl-to-Cortex fallback and no automatic analyzer discovery.

## Interpretation

**Enrichment is evidence, not a verdict.** IntelOwl and Cortex results do not prove local compromise by themselves. Both histories are displayed with `External share: no` and `Local compromise proven: no` because analyzer output has no external-share or publication authority.

Cortex is analyzer-only. Responders and other external side-effect actions are not exposed through this workspace.

## Failure behavior

The workspace must **fail closed**. An upstream, policy, canonical-object or persistence failure is presented as an error. DTMO does not synthesize a success result, healthy upstream state, empty evidence conclusion, approval state or compromise conclusion.

## Production boundary

Repository/browser CI can validate exact-head interaction and authority boundaries, but it does **not prove** live analyzer availability or provider authorization, production-equivalent operation, independent assurance or production authorization. DTMO remains not production authorized while Phase 11.10 is in progress.
