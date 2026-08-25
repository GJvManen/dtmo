# Automation & Playbooks Workspace

The canonical **Automation & Playbooks** workspace is available at `/workbench/automation`. It presents DTMO-owned scheduler observations and bounded connector playbooks without exposing upstream credentials or granting autonomous remediation authority.

## What operators can see

The scheduler panel shows jobs reported by the DTMO `/health` control plane. The playbook catalog is derived from `/connectors`; it distinguishes enabled capability, scheduled registration and manual-run availability. Missing scheduler or connector data is shown as unavailable rather than converted into a healthy or zero-risk state.

Phase 11.10q adds an explicit **Refresh runtime observation** action. This re-reads the same-origin scheduler and connector control-plane state. A successful manual run also triggers a fresh observation automatically so the operator does not have to treat stale pre-run state as current.

The workspace now also reads `/api/v1/source-center/status` after entry, explicit refresh and successful execution. For the selected playbook this surfaces the latest persisted connector state when available: health state, last successful observation, last failed observation, consecutive failure count and isolation-until state. This gives the operator durable latest-state evidence across browser refreshes without introducing a second persistence model.

## Running a bounded playbook

Select a connector-backed playbook and use **Run bounded collection playbook** only when you are an authorized human principal. The browser sends the action to DTMO; DTMO performs the connector call server-side. `manage:connectors` remains the authoritative execution permission and the workspace does not provide a browser-side bypass.

The browser also fails closed when a connector does not advertise `manual_run_available`. It will show the connector in the catalog for observability but will not invoke the manual execution endpoint from the workbench.

The returned execution evidence is shown directly: connector, status, attempts, record count, inserted/indexed counts, connector alert state and correlation identifier when returned by DTMO. A successful run may collect and ingest attributable intelligence. A successful automation run does not prove source truth, compromise or containment and does not create a case, remediate an asset, complete intelligence review, approve external sharing, publish intelligence or grant production authorization.

## Service accounts and credentials

Service-account browser sessions are not represented as human execution authority in this workspace. Scheduled service execution remains server-owned. Connector tokens, API keys and other upstream credential values remain server-side and are never displayed in the workspace.

## Evidence interpretation

Scheduler status proves only what the current DTMO runtime reports about registered jobs. A connector result proves only the browser-observed bounded execution and its returned ingest/index result. The Source Center observation is separate, persisted latest-state evidence when available; it is **not a complete immutable run history** and absence of a matching persisted source record does not prove that no execution has occurred. Neither current runtime state nor persisted connector state proves upstream availability, source truth, compromise, remediation success, production readiness or production authorization. CI/browser fixtures are repository evidence only and must not be treated as production-equivalent validation.
