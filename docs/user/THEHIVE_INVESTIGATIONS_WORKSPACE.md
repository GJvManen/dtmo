# TheHive Investigations Workspace

## Route

`/workbench/investigations`

Phase 11.10h replaces the shell placeholder with a functional investigation workspace backed only by DTMO APIs and canonical DTMO persistence.

## Open an investigation

Enter a canonical DTMO intelligence UUID or open the route with `?item=<uuid>`. Loading an item requires `read:intelligence` and shows only attributable canonical data:

- title and source;
- severity and review state;
- canonical provenance count;
- authoritative TLP tags recorded on the item;
- durable TheHive handoff history.

Opening an item does not grant case-creation authority.

## Create a TheHive case handoff

Case handoff requires the existing server-side `handoff:case` permission and an explicit human action. The workspace also requires:

- canonical provenance;
- enabled TheHive handoff feature;
- complete server-side TheHive API base/token/organization configuration;
- no authoritative MISP distribution/sharing-group restriction that lacks a deployment-approved TheHive access mapping;
- no unresolved `reserved` or `ambiguous` handoff in the current workspace state.

Provide a minimized reviewed summary and select TLP/PAP. The browser submits the request to DTMO; it never contacts TheHive directly and never receives the TheHive token.

## What a delivered result means

`delivered` means DTMO received a stable TheHive case identity/number from the case-creation response and persisted that handoff evidence. It does not mean that DTMO has read back the complete case or that any responder/remediation occurred.

## Ambiguous delivery

`ambiguous` means DTMO cannot prove whether the upstream mutation completed. The workspace displays **Manual reconciliation required** and disables a new case request from the UI. Do not treat ambiguous delivery as a normal retry condition.

## Alerts, tasks and timeline

Phase 11.10h does not display synthetic alerts, tasks or a case timeline. The accepted Phase 11.6 persistence boundary does not store/read those objects back from TheHive. Their absence in the workspace is therefore not evidence that TheHive has none.

## Authority boundaries

The workspace does not grant:

- external sharing/publication approval;
- TheHive responder execution;
- automatic incident-response authority;
- MISP publication/synchronization;
- local-compromise proof;
- TheHive platform/organization administration;
- production authorization.

Configuration is displayed as configuration only and is not a live-health claim.

## Failure behavior

If canonical investigation state cannot be loaded, the workspace shows `Investigation state unavailable` and does not infer an empty case set, healthy TheHive service or absence of compromise.

If case handoff is rejected, the server error is shown and durable state is reloaded so ambiguous/reserved evidence becomes visible rather than silently retried.
