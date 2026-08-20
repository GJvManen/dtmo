# DTMO Next-Generation Information Architecture

Status: **Phase 11.10a–11.10g — PASS / REPOSITORY_COMPLETE; Phase 11.10h — ACTIVE THEHIVE INVESTIGATIONS & CASES**

## Principle

Primary navigation is organized by operator intent, not by upstream product ownership. Service names remain visible as provenance, capability and evidence context.

Phase 11.10b established the canonical `/workbench/` shell. Phase 11.10c delivered the Command Center, Phase 11.10d Threat Intelligence and IOC Explorer, Phase 11.10e Analysis & Enrichment, Phase 11.10f Knowledge Graph, Phase 11.10g governed Sharing & Exchange, and Phase 11.10h is the active functional migration of Investigations. Route foundations for later workspaces do not imply that those features are implemented or accepted.

## Canonical navigation tree

### Home
- Command Center — accepted in Phase 11.10c.

### Intelligence
- Threat Intelligence — accepted in Phase 11.10d.
- IOC Explorer — accepted in Phase 11.10d.
- Threat Actors & Campaigns — later bounded intelligence capability.
- Knowledge Graph — accepted in Phase 11.10f.
- Threat Hunting — later bounded intelligence capability.

### Exposure
- Vulnerabilities
- Assets
- Technology
- Prioritization

### Investigations
- Canonical investigation context — active in Phase 11.10h.
- TheHive case handoff — active through explicit human `handoff:case` authority.
- Durable handoff/reconciliation history — active in Phase 11.10h.
- Alerts / Tasks / Investigation Timeline — not synthesized; require future attributable persistence/readback before display as upstream state.

### Analysis
- Enrichment — accepted in Phase 11.10e through governed IntelOwl execution/history.
- Cortex Analyses — accepted in Phase 11.10e through analyzer-only governed execution/history.
- Analysis History — accepted combined canonical-object view in Phase 11.10e.

### Sharing
- MISP Exchange — accepted in Phase 11.10g.
- Sharing Approvals — accepted through canonical human review/share authority.
- Publication Queue — future separately governed capability; not granted by MISP export.

### Automation
- Playbooks
- Jobs
- Schedules
- Approval Queue

### Collection
- Sources
- Connectors
- Catalog
- Collection Runs

### Governance
- Frameworks
- Control Mappings
- Evidence
- Risk
- Audit

### Operations
- System Health
- Integrations
- Observability
- Runtime
- Backup & Recovery

### Administration
- Users
- Roles
- Permissions
- Policies
- Configuration

## Global surfaces

The accepted architecture defines global search, command palette, notifications, selected object/context rail, environment/candidate identity, principal/role context, help/documentation, theme and accessibility preferences where attributable and authorized.

The accepted shell implements global navigation, a navigation-only command palette, environment/platform status, principal context, context rail container and theme preference. High-impact feature actions appear only when bounded contracts provide attributable data and authority.

## Unified Intelligence placement

Phase 11.10d made the Intelligence domain functional through `/workbench/intelligence` and `/workbench/intelligence/iocs`, using DTMO search and canonical detail/provenance APIs. Search results are discovery projections, not canonical truth. Search/detail failures remain unavailable rather than becoming synthetic empty or complete intelligence.

## Integrated Analysis placement

Phase 11.10e made `/workbench/analysis` functional. History/capability reads require server-side `read:intelligence`; explicit IntelOwl/Cortex execution requires `review:intelligence`. Analyzer output does not prove local compromise or create sharing/publication authority.

## OpenCTI Graph / Entity placement

Phase 11.10f made `/workbench/intelligence/graph` functional through DTMO endpoints protected by `read:intelligence`. The graph root is the canonical DTMO intelligence item. OpenCTI nodes come from persisted stable OpenCTI/STIX mappings. Generic upstream relationship topology is not durably persisted; only attributable `canonical-mapping` edges are rendered and missing relationship evidence **fails closed**.

## Accepted MISP Sharing & Exchange placement

Phase 11.10g made `/workbench/sharing` functional while preserving the canonical API and human-authority model. Canonical reads require `read:intelligence`; review requires `review:intelligence`; share approval/export require `approve:share`. The share approver must differ from the reviewer. Service accounts cannot substitute for human authority. MISP-origin handling restrictions remain binding, deterministic replay evidence fails closed, and export creates `published=false` events only. Configuration is not runtime health and technical transfer does not prove publication/synchronization or local compromise.

## Active TheHive Investigations placement

Phase 11.10h makes `/workbench/investigations` functional without turning the browser into a TheHive client.

The browser calls only DTMO endpoints:

- `/api/v1/thehive/items/{item_id}/investigation` for canonical intelligence/provenance/handoff state;
- `/api/v1/thehive/items/{item_id}/cases` for explicit human-authorized case handoff.

Canonical state reads require `read:intelligence`; case mutation requires `handoff:case`. Service accounts cannot authorize human case handoff. TheHive credentials and organization context remain server-side.

Canonical provenance and source handling restrictions fail closed. Persisted `reserved` or `ambiguous` handoff state requires manual reconciliation and blocks a blind new UI case request. A delivered handoff proves only the stable case identity returned during creation.

The accepted Phase 11.6 persistence does not mirror generic TheHive alerts, tasks, case timeline, later upstream case state or responder results. Those facts are therefore not inferred. Configuration is not runtime health; case presence does not prove external sharing, remediation or local compromise.

## Canonical object types

The workbench represents and navigates governed object classes where supported by canonical data, including intelligence items, indicators/IOCs, vulnerabilities/CVEs, threat actors/intrusion sets, campaigns, malware/tools, infrastructure/domain/IP/URL/hash, sources/connectors, cases, tasks, observables, analysis/enrichment jobs, MISP references, OpenCTI entity/mapping references, governance evidence and identity/role/runtime objects. A listed object class is an architecture target, not evidence that upstream state is currently persisted.

## Context rail contract

The right context rail is driven by selected attributable object state and may show identity/type, severity/classification, confidence, TLP/PAP/markings, provenance/source, related entities, enrichment/analysis counts, cases/tasks, vulnerabilities/exposure, sharing status, timeline/audit summary and authorized actions where the corresponding evidence exists.

The rail must never infer an unavailable fact because an integration is configured. Until a feature slice integrates shared rail selection, feature-specific detail remains inside its governed workspace. This preserves the shell **Context rail contract**.

## Command palette

The end-state palette may support safe navigation and separately governed actions. The current command palette remains navigation-only; it cannot bypass server-side authorization.

## Role-aware defaults

Role-aware defaults may change landing page and visible navigation groups but do not define authorization. Executive, CISO, SOC Analyst, CTI Analyst, Incident Responder, Administrator and Auditor defaults remain distinct usability profiles. Full role-aware presentation acceptance remains Phase 11.10n. **Server-side RBAC** remains authoritative.

## Responsive behavior

Desktop uses persistent navigation and optional context rail. Tablet may collapse regions into drawers. Small mobile view prioritizes situational awareness and explicitly supported low-risk actions. Feature workspaces provide accessible non-visual alternatives where appropriate; sharing/case decisions never depend on colour alone.

## Migration rule

Existing Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance functionality must be mapped into this architecture before legacy retirement. `/workbench/` is the canonical built product route. `/ui/console`, `/ui/intelligence-workspace` and `/ui/misp-workspace` remain temporary **compatibility paths** and are not parallel feature-development targets.

## Candidate-completion state

- 11.10a frontend architecture/design — `PASS / REPOSITORY_COMPLETE`;
- 11.10b canonical shell — `PASS / REPOSITORY_COMPLETE`;
- 11.10c Command Center — `PASS / REPOSITORY_COMPLETE`;
- 11.10d Unified Intelligence Workspace — `PASS / REPOSITORY_COMPLETE`;
- 11.10e IntelOwl/Cortex integrated analysis — `PASS / REPOSITORY_COMPLETE`;
- 11.10f OpenCTI graph/entity workspace — `PASS / REPOSITORY_COMPLETE`;
- 11.10g MISP Sharing & Exchange — `PASS / REPOSITORY_COMPLETE`;
- 11.10h TheHive Investigations & Cases — `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- 11.10i Vulnerability & Exposure Center — `NOT STARTED`;
- 11.10p fresh production-equivalent validation — `NOT STARTED / CANDIDATE FREEZE REQUIRED`;
- Phase 11.11 — `NOT STARTED`;
- Phase 12 — `NOT STARTED`.

DTMO remains **not production authorized**.

## Evidence boundary

This information architecture and its implemented routes are repository product-design/engineering evidence only. They do **not prove** live MISP/OpenCTI/TheHive connectivity or health, publication/synchronization, complete upstream case state, responder execution, local compromise, production-equivalent validation, independent assurance or production authorization. Missing or ambiguous operational evidence must **fail closed**.
