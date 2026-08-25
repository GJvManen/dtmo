# Phase 11.10q — Functional Recovery Acceptance

## Status

`BLOCKED / OWNER FUNCTIONAL REJECTION`

The owner functional retest on 2026-08-24 rejects the current candidate despite green exact-head repository CI. The canonical Operations Workbench is not yet a professional, usable replacement for the legacy interface because the underlying DTMO components are not integrated end-to-end into the new interface and the default operator experience remains empty or non-functional across multiple primary workflows.

Green repository CI is not sufficient acceptance for Phase 11.10q. The canonical interface must be usable by an operator against the real same-origin DTMO API/persistence stack and must not require fallback to `/ui/*` compatibility views for primary administration, source collection or operational workflows.

## Owner retest findings — 2026-08-24

| Area | Current acceptance state | Owner finding / required remediation |
| --- | --- | --- |
| Framework integrations | BLOCKED | Required platform integrations are not operational by default. The canonical Administration surface must expose the complete supported integration configuration, readiness and activation path; bundled/default deployments must arrive in an actionable state without hidden legacy-only setup. |
| Threat Intelligence | BLOCKED | No usable content is present. A normal deployment must provide governed source bootstrap/execution and attributable initial/recent intelligence without requiring legacy setup. |
| IOC Explorer | BLOCKED | No usable IOC content is present. IOC inventory must be populated from canonical intelligence and expose real pivots from the new interface. |
| Knowledge Graph | BLOCKED | Does not work in the normal/default operator path. Root discovery, relationships and OpenCTI-backed/canonical graph behavior must be available from the new interface. |
| Vulnerability & Exposure Center | BLOCKED | No usable vulnerability/exposure content is present. Governed source ingestion must populate canonical vulnerability data and expose filtering and pivots. |
| Investigations | BLOCKED | Does not work in the normal/default operator path. TheHive/investigation capability must be integrated into the canonical interface rather than depend on legacy setup or hidden configuration. |
| Analysis & Enrichment | BLOCKED | No usable content/results are present. IntelOwl/Cortex actions, configuration state and result/history visibility must work from selected canonical objects. |
| Sharing & Exchange | BLOCKED | Does not work in the normal/default operator path. Review/approval/MISP exchange must be operable from the canonical interface. |
| Automation & Playbooks | BLOCKED | Does not work in the normal/default operator path. Playbooks/jobs/schedules and observable execution must be available without legacy fallback. |
| Sources & Collection | BLOCKED | Primary source/collection workflows currently work only through the legacy interface. The canonical workbench must own source bootstrap, registration, validation, testing, activation and execution end-to-end. |
| Operations | BLOCKED | No usable operational content is present in the canonical workspace. Runtime health, telemetry, connector state, alerts and actionable navigation must be migrated from the legacy Operations view. |
| Administration | BLOCKED | The canonical workspace lacks the functions required for normal administration; effective functions remain legacy-only. Users/roles, integration configuration, security administration and audit/navigation must be available from the new interface according to RBAC. |

## Structural diagnosis

The repository contains multiple functional React workspaces and server-side APIs, but the current product still has an integration gap between those slices and the canonical shell/runtime defaults. Tests that prove individual components, API contracts or mocked journeys therefore do not establish a usable product. The remediation must now focus on **canonical integration parity and default operational usability**, not on additional isolated component gates.

The first confirmed shell defect is now under remediation: the canonical Administration route previously fell through to the generic `WorkspaceFoundation` placeholder even though `AdministrationWorkspace.tsx` existed. The canonical IOC route also used the generic unified-intelligence IOC mode rather than the dedicated IOC Explorer workspace. These routes are now wired to their dedicated React components on the remediation branch. This is necessary but not sufficient; default data and runtime integration behavior remain blocked.

The canonical Operations route is now backed by same-origin runtime health, telemetry, alert and connector-capability contracts rather than the generic placeholder. As a further acceptance hardening step, the canonical primary navigation no longer exposes the legacy `Compatibility console` link. Legacy `/ui/*` routes remain compatibility endpoints only; they are no longer presented as a normal operator escape hatch from the canonical shell. This does not constitute owner acceptance and does not remove any other BLOCKED row above.

Administration now exposes integration configuration and governed identity/RBAC management through canonical same-origin APIs. This recovery slice additionally migrates privileged bearer-token revocation and read-only append-only audit evidence into the canonical `/administration` route, preserving `revoke:tokens`, `read:audit`, human-admin/service-account boundaries, request IDs and persistent server-side audit storage. Legacy CISO/Auditor pages remain compatibility endpoints only. Administration remains BLOCKED pending owner retest and any remaining readiness/default-runtime findings.

## Mandatory remediation order

1. **Eliminate legacy-only primary flows.** Route every canonical menu item to its actual functional workspace and migrate remaining Operations/Administration functionality out of `/ui/*` compatibility pages.
2. **Make Administration the real control plane.** Surface integration endpoints, enablement/readiness, identity/RBAC, security controls and audit navigation in the canonical workbench with server-side authorization.
3. **Make Sources & Collection self-sufficient.** Bootstrap the supported source catalog in the canonical interface, expose disabled/enabled/readiness state, and allow validate/test/run without legacy setup.
4. **Establish a default data path.** A standard supported deployment must have at least one governed, attributable source path capable of populating canonical intelligence and vulnerability data. Empty screens may remain valid only when the operator has an explicit actionable remediation path.
5. **Reconnect downstream workspaces to canonical data.** Threat Intelligence → IOC Explorer → Knowledge Graph / Exposure → Analysis / Investigations → Sharing must operate as selectable object-driven flows.
6. **Integrate framework services.** OpenCTI, TheHive, IntelOwl, Cortex, MISP, AIL and Taranis readiness/configuration must be visible and actionable from the new interface. Missing credentials/configuration must explain exactly what is required; bundled/configured services must not remain silently disabled.
7. **Migrate Operations.** Bring runtime health, telemetry, connector state and alerts into `/operations` in the canonical React application.
8. **Run a real owner retest.** Acceptance requires the owner to complete normal operator journeys without opening a legacy `/ui/*` route.

## Owner functional retest protocol

The next acceptance step after a fully green exact-head CI cycle is a manual owner retest against the exact candidate being evaluated. Repository-controlled browser gates — including any workflow whose historical name contains `Owner Retest` — remain regression evidence only when they use fixtures, request interception or synthetic data. They cannot change any row in this document from `BLOCKED` to accepted.

Before the retest, record the exact candidate SHA and verify that the running DTMO instance was built from that SHA. Do not reuse evidence from an earlier SHA. The owner must use the canonical workbench routes and normal operator credentials/roles; no primary step may require a `/ui/*` compatibility page, direct database manipulation, hidden bootstrap command or manual canonical UUID entry when the object is discoverable in the interface.

The owner retest must exercise these normal operator journeys end-to-end:

1. **Administration and framework readiness:** inspect MISP, AIL, Taranis, IntelOwl, Cortex, OpenCTI and TheHive readiness; verify missing configuration is actionable from canonical Administration and a configured integration is not silently disabled. Verify identity/RBAC, security administration and audit evidence remain role-authorized and that credentials are never rendered back to the browser.
2. **Sources & Collection:** discover or register a governed source, validate/test it where supported, activate it with the required authority, execute collection and observe the resulting persisted source state without opening a legacy view.
3. **Threat Intelligence population and discovery:** use the governed source path to populate or refresh canonical intelligence, confirm attributable recent/default discovery, and select a persisted intelligence object from the canonical interface.
4. **IOC Explorer and graph/exposure pivots:** derive/select persisted IOC inventory from canonical intelligence, use real object pivots, open Knowledge Graph discovery/population and Vulnerability & Exposure filtering/population without free-text UUID as the primary path.
5. **Analysis and Investigations:** pivot from a selected canonical object into Analysis & Enrichment and Investigations; confirm persisted history/results/state are visible, mutations remain separately authorized, and no analyzer or case handoff is performed merely by navigation.
6. **Sharing & Exchange:** pivot from the selected object into review/share state, exercise the human review/share approval path appropriate to the test role, and verify navigation alone does not grant MISP export, publication or synchronization authority.
7. **Automation & Playbooks:** select an executable playbook/job, perform a bounded authorized run where appropriate, refresh runtime observation, and verify durable latest-state evidence is distinguishable from a complete immutable run history or provider-health claim.
8. **Command Center and Operations:** verify canonical metrics/trends, integration readiness, runtime health, telemetry, connector state, alerts and actionable navigation contain real same-origin DTMO state and do not require a legacy Operations page.
9. **Legacy escape-hatch check:** complete the whole retest with no primary workflow opening or requiring `/ui/*`. Compatibility routes may exist but cannot be needed for completion.

For every journey, record `PASS` or `FAIL` plus the exact observed blocker. A `PASS` requires the server-authorized action and resulting state/evidence to be observable; button presence, an empty-state explanation, a mocked journey or green CI alone is insufficient. Any failed journey keeps the corresponding row above `BLOCKED` and #316 draft.

Only an explicit owner acceptance statement after this retest may clear the owner functional rejection. After that acceptance — and not before — freeze a new candidate, repeat production-equivalent validation against that frozen SHA, and only then restart independent external assurance. Do not reuse prior staging, production-equivalent or external-assurance evidence as proof for the new candidate.

## Non-negotiable acceptance rules

- A primary workflow that requires the legacy interface is a release blocker.
- An empty-state-only workspace is not functionally complete unless it contains a working operator path that can populate or configure the required data from the same canonical interface.
- A configured bundled integration that remains silently disabled is not acceptable default product behavior.
- A button that only renders but does not complete its server-authorized action is not functionally complete.
- Manual UUID entry is not an acceptable primary workflow when DTMO can discover/select the object itself.
- Component mocks may be used for unit tests, but cannot be the sole proof for critical functional journeys.
- Repository-controlled bootstrap/sample content must be visibly labelled and must never be promoted as live-source, staging, production-equivalent or external-assurance evidence.
- The unmocked same-origin gate is repository-controlled evidence only and does not override an owner functional rejection.
- Phase 11.10q remains blocked until an owner functional retest explicitly accepts the canonical interface without legacy dependency for the primary workflows above.
