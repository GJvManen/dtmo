# Automation & Playbooks Workspace

The canonical **Automation & Playbooks** workspace is available at `/workbench/automation`. It presents DTMO-owned scheduler observations and bounded connector playbooks without exposing upstream credentials or granting autonomous remediation authority.

## What operators can see

The scheduler panel shows jobs reported by the DTMO `/health` control plane. The playbook catalog is derived from `/connectors`; it distinguishes enabled capability, scheduled registration and manual-run availability. Missing scheduler or connector data is shown as unavailable rather than converted into a healthy or zero-risk state.

## Running a bounded playbook

Select a connector-backed playbook and use **Run bounded collection playbook** only when you are an authorized human principal. The browser sends the action to DTMO; DTMO performs the connector call server-side. `manage:connectors` remains the authoritative execution permission and the workspace does not provide a browser-side bypass.

A successful run may collect and ingest attributable intelligence. It does **not** prove source truth or compromise and does not create a case, contain or remediate an asset, complete intelligence review, approve external sharing, publish intelligence or grant production authorization.

## Service accounts and credentials

Service-account browser sessions are not represented as human execution authority in this workspace. Scheduled service execution remains server-owned. Connector tokens, API keys and other upstream credential values remain server-side and are never displayed in the workspace.

## Evidence interpretation

Scheduler status proves only what the current DTMO runtime reports about registered jobs. A connector result proves only the recorded bounded execution and its returned ingest/index result. CI/browser fixtures are repository evidence only and must not be treated as production-equivalent validation.
