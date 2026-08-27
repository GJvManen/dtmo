# Clean-install whole-product owner retest runbook

## Status

`EXTERNAL OWNER EXECUTION REQUIRED / CANDIDATE FREEZE BLOCKED`

This runbook is the authoritative operator procedure for repeating the whole-product functional acceptance after the 2026-08-26 owner rejection. It starts from a clean supported installation and keeps repository CI, external owner acceptance, production-equivalent validation and independent assurance as separate evidence classes.

A successful execution may support an explicit owner functional acceptance decision. It is not by itself production-equivalent validation, penetration-test evidence, independent assurance or production authorization.

## 1. Exact source identity

Before installation, record the exact `main` Git commit being evaluated. Do not reuse an earlier checkout or working tree. Any repository change after the retest begins creates a different candidate and invalidates the retest for the changed identity.

## 2. Clean supported installation

1. Clone the repository into a new directory at the exact recorded commit.
2. Confirm Docker Desktop/Engine and Docker Compose are available and healthy.
3. Run `python3 tools/bootstrap_local.py`.
4. Resolve every reported prerequisite rather than bypassing preflight. AIStor image identity and license are external prerequisites when required by the supported local topology.
5. Start the supported topology with `docker compose up --build`.
6. Wait for application and dependency health/readiness before browser acceptance.

Do not copy a prior `.env`, database volume, object-store volume, browser storage or generated test fixture into the clean installation. External integration credentials may be configured only through their supported server-side path and must not be committed to the repository or copied into evidence.

## 3. Reachability and default product readiness

Verify that the canonical application is reachable; primary navigation stays inside `/workbench/*`; Administration reports actionable integration readiness; bundled PostgreSQL, Redis, OpenSearch, object storage, Prometheus and Grafana dependencies are healthy through their supported path; Visual Analytics follows the supported single-session path; and unavailable external frameworks fail closed with clear configure/connect guidance.

## 4. First-data workflow

Use the supported Sources & Collection bootstrap/registration path to create or activate an attributable source safe for the test environment. Run collection and verify resulting canonical intelligence is persisted and visible after reload. Repository sample/bootstrap content must remain labelled and must never be represented as live-source truth.

## 5. Whole-product canonical acceptance matrix

| Workspace | Minimum acceptance journey |
| --- | --- |
| Command Center | Read current state, trends/readiness and navigate to attributable detail. |
| Threat Intelligence | Discover populated content; search/filter; open detail; pivot onward. |
| IOC Explorer | Inspect IOC/context; filter; pivot to source intelligence, graph, analysis or investigation. |
| Knowledge Graph | Open persisted graph/entity context and inspect attributable mapping/provenance. |
| Vulnerability & Exposure | Inspect CVSS/EPSS/KEV evidence; filter; pivot while preserving the no-local-exposure inference boundary. |
| Investigations | Select canonical intelligence, perform an authorized case handoff where configured, and observe durable handoff history. |
| Analysis & Enrichment | Execute an allowed enrichment/analyzer where configured and verify result/history survives reload. |
| Sharing & Exchange | Exercise review/share separation and an authorized unpublished delivery where configured; verify durable delivery/replay state. |
| Automation & Playbooks | Trigger an allowed bounded playbook and verify durable execution state and supported reversible control-plane behavior. |
| Sources & Collection | Register/bootstrap, validate/readiness, activate where authorized, run and observe durable source/connector state. |
| Governance & Evidence | Drill from framework to explicit DTMO control mapping, implementation reference and provenance; confirm mappings are not blanket compliance. |
| Operations | Inspect persisted connector runtime/run evidence, dependency health and operational navigation without acquiring mutation authority. |
| Administration | Save an authorized configuration change, reload to prove persistence, inspect identity/RBAC/security administration and restore test-only changes where appropriate. |

Record any browser error, API/server error, blank state, inert control, unexpected legacy dependency, stale result or unclear operator blocker as a failed acceptance observation.

## 6. Persistence and restart check

Reload and revisit representative durable state. Perform a normal supported application restart without deleting persistent volumes, wait for health/readiness, and verify expected durable state remains available. Transient UI state must not be represented as durable evidence.

## 7. Security and authority checks

Server-side RBAC remains authoritative; credentials remain server-side; provenance/raw-evidence binding remains attributable; missing evidence and unavailable integrations fail closed; intelligence review, case handoff, external-share approval, publication, connector execution, administration and production authorization remain separate authority domains. Enrichment, graph presence, vulnerability intelligence, automation success or connector success do not become automatic compromise, remediation or compliance conclusions.

## 8. Acceptance record

Record exact Git SHA; host/platform and Docker/Compose versions; clean-install timestamps; preflight result; external prerequisites; application/dependency health; first-data source/provenance result; PASS/FAIL plus concise observation for every canonical workspace; persistence/restart result; unresolved defects with reproduction steps; and explicit owner decision `ACCEPTED` or `REJECTED`.

Do not accept while any required workspace is blank, inert, unusable, dependent on an undocumented legacy-primary path, or has an unresolved required-function defect.

## 9. Lifecycle transition

If `REJECTED`, repair only verified root causes in bounded PRs, obtain fresh exact-head repository evidence and repeat the clean-install retest against the changed identity.

Only explicit owner `ACCEPTED` unblocks the next lifecycle step: synchronize authoritative documentation, freeze one immutable candidate from the accepted `main` state, and execute fresh Phase 11.10p production-equivalent validation against that exact candidate. Historical Phase 8/9 evidence does not transfer.