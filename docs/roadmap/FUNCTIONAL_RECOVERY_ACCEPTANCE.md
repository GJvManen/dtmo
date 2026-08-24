# Phase 11.10q — Functional Recovery Acceptance

## Status

`BLOCKED / OWNER FUNCTIONAL REJECTION`

Green repository CI is not sufficient acceptance for Phase 11.10q. The canonical interface must be usable by an operator against the real same-origin DTMO API/persistence stack.

Repository-side recovery now also includes a dedicated exact-head, unmocked same-origin browser journey. That journey builds the canonical React workbench, starts the exact-head DTMO API against temporary PostgreSQL persistence, uses no Playwright route interception, performs a real disabled-by-default source registration through the browser, reads the persisted record back through the actual same-origin API, and visits every recovered canonical workspace. External connector execution is intentionally disabled. Passing that gate is repository evidence only and does **not** change this document to PASS; accountable owner functional acceptance is still required.

## Hard blockers

The following capabilities are release blockers until each is demonstrably usable in the canonical workbench:

| Area | Current acceptance state | Required proof before PASS |
| --- | --- | --- |
| Administration / Settings | BLOCKED | Governed configuration and integration settings can be inspected and changed from the canonical console where runtime mutation is supported; deployment-only settings are clearly identified with an actionable configuration path. |
| Threat Intelligence | BLOCKED | Opens with attributable recent/canonical intelligence or a governed bootstrap path; search is not the only way to obtain a usable starting view. |
| IOC Explorer | BLOCKED | Dedicated IOC inventory with indicator type/value, source, severity/confidence, timestamps, filtering and pivots to enrichment/graph/investigation. |
| Knowledge Graph | BLOCKED | Discoverable graph roots and populated relationships are available without manually pasting an internal UUID; same-origin persistence/API acceptance is required. |
| Exposure | BLOCKED | Vulnerability inventory is populated through governed source/bootstrap execution and supports CVSS/EPSS/KEV/vendor/product/CWE filtering and useful pivots. |
| Analysis & Enrichment | BLOCKED | An analyst can launch governed IntelOwl/Cortex actions from a selected intelligence/IOC object without manually copying opaque identifiers; execution/history/results are visible. |
| Sharing & Exchange | BLOCKED | A reviewed canonical object can be selected from the UI and moved through review/share approval/MISP export states without manual UUID entry; blocked states explain the exact missing authority/configuration. |
| Automation & Playbooks | BLOCKED | Playbook inventory, executable actions, job/history state and approval boundaries are visible and at least one deterministic governed workflow can be run end-to-end. |
| Sources & Collection | BLOCKED | Supported sources can be bootstrapped, enabled/disabled where allowed, validated, tested and run from the canonical workbench with visible runtime/result state. |
| Command Center | BLOCKED | Shows integration readiness/actionability plus operator-grade trends/graphs and links into the underlying workspaces. |

## Non-negotiable acceptance rules

- An empty-state-only workspace is not functionally complete.
- A button that only renders but does not complete its server-authorized action is not functionally complete.
- Manual UUID entry is not an acceptable primary workflow when DTMO can discover/select the object itself.
- Component mocks may be used for unit tests, but cannot be the sole proof for critical functional journeys.
- Repository-controlled bootstrap/sample content must be visibly labelled as such and must never be promoted as live-source, staging, production-equivalent or external-assurance evidence.
- The unmocked same-origin gate is repository-controlled evidence only: it does not establish live-source health, staging acceptance, production-equivalent validation, production authorization or independent assurance.
- Phase 11.10q remains blocked until an owner functional retest explicitly accepts the canonical interface.
