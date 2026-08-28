# Automation & Playbooks Workspace

The canonical **Automation & Playbooks** workspace is available at `/workbench/automation`. It presents DTMO-owned scheduler observations and bounded collection playbooks without exposing upstream credentials or granting autonomous remediation authority.

## What operators can see

The scheduler panel shows jobs reported by the DTMO `/health` control plane. The playbook catalog combines the built-in `/connectors` capability inventory with executable governed registered sources from `/api/v1/source-center/status`. Built-in and registered-source paths remain distinct; the workspace does not create a second orchestration plane.

Missing scheduler, connector or persisted source data is shown as unavailable rather than converted into a healthy or zero-risk state. **Refresh runtime observation** explicitly re-reads scheduler, connector and Source Center state. A successful manual run also triggers this refresh automatically so stale pre-run state is not presented as current.

For the selected playbook, the workspace surfaces the latest persisted connector state when available: health state, last successful observation, last failed observation, consecutive failure count and isolation-until state. Built-in connector execution now records this same canonical connector runtime state, so a successful CISA KEV trigger can be observed durably after the immediate browser result. This remains latest-state evidence, not a complete immutable run history.

## Running a bounded playbook

Select a playbook and use **Run bounded collection playbook** only when you are an authorized human principal. Built-in connectors use their existing server-owned `/connectors/{id}/run` path. Governed registered sources use `/api/v1/admin/sources/{id}/run`. `manage:connectors` remains the authoritative execution permission and the server remains authoritative even when the browser disables a control.

The browser fails closed when a playbook does not advertise `manual_run_available` and, independently, when a registered source is disabled. A paused source can still advertise that it has a manual-run capability in the canonical model; capability does not override the source enabled-state gate. The browser therefore disables **Run bounded collection playbook** while the source is paused, matching the server-side enabled-state boundary. The returned execution evidence includes connector, status, attempts, record count, inserted/indexed counts, alert state and correlation identifier when returned by DTMO.

A successful collection run may persist attributable canonical intelligence and raw evidence. It does not prove source truth, compromise or containment and does not create a case, remediate an asset, complete intelligence review, approve external sharing, publish intelligence or grant production authorization.

## Reversible registered-source pause

For an enabled governed registered source, an authorized human can use **Pause registered source**. This uses the existing server-authorized source update API to set only that source's `enabled` state to `false`. It does not alter the scheduler itself and does not delete prior execution evidence.

When the pause succeeds, the current browser session retains one bounded rollback token for that source and exposes **Rollback this pause**. Only one unresolved pause can be held at a time. The rollback restores the enabled state that this browser session changed. It cannot erase canonical intelligence, raw evidence, audit records or connector health events, and it cannot undo an upstream side effect that already occurred. Closing the browser or losing the session-local rollback token does not silently mutate server state; an operator must then use the normal governed source administration path.

This control is a reversible DTMO configuration action, not incident remediation or a generic transaction rollback mechanism.

## Service accounts and credentials

Service-account browser sessions are not represented as human execution authority in this workspace. Scheduled service execution remains server-owned. Connector tokens, API keys and other upstream credential values remain server-side and are never displayed in the workspace.

## Evidence interpretation

Scheduler status proves only what the current DTMO runtime reports about registered jobs. A connector result proves only the recorded bounded execution and its returned ingest/index result. The Source Center observation is separate persisted latest-state evidence when available; it is **not a complete immutable run history**, and absence of a matching persisted source record does not prove that no execution has occurred.

A pause/rollback proves only the recorded registered-source enabled-state transition. Neither execution nor rollback proves upstream availability, source truth, compromise, containment, remediation success, case authority, external-share authority, publication authority, production readiness or production authorization. Repository-controlled CI/browser fixtures are repository evidence only and must not be treated as live-source, staging, production-equivalent or independent-assurance validation.
