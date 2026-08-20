# DTMO Next-Generation Information Architecture

Status: **Phase 11.10a–11.10e — PASS / REPOSITORY_COMPLETE; Phase 11.10f — ACTIVE OPENCTI GRAPH/ENTITY WORKSPACE**

## Principle

Primary navigation is organized by operator intent, not by upstream product ownership. Service names remain visible as provenance, capability and health context.

Phase 11.10b established the canonical `/workbench/` shell. Phase 11.10c delivered the Command Center, Phase 11.10d delivered Threat Intelligence and IOC Explorer, Phase 11.10e delivered Analysis & Enrichment, and Phase 11.10f is the active functional migration of OpenCTI graph/entity context. Route foundations for later workspaces do not imply that those features are implemented or accepted.

## Canonical navigation tree

### Home

- Command Center — accepted in Phase 11.10c.

### Intelligence

- Threat Intelligence — accepted in Phase 11.10d.
- IOC Explorer — accepted in Phase 11.10d.
- Threat Actors & Campaigns — later bounded intelligence capability.
- Knowledge Graph — active in Phase 11.10f.
- Threat Hunting — later bounded intelligence capability.

### Exposure

- Vulnerabilities
- Assets
- Technology
- Prioritization

### Investigations

- Alerts
- Cases
- Tasks
- Investigation Timeline

### Analysis

- Enrichment — accepted in Phase 11.10e through governed IntelOwl execution/history.
- Cortex Analyses — accepted in Phase 11.10e through analyzer-only governed execution/history.
- Analysis History — accepted combined canonical-object view in Phase 11.10e.

### Sharing

- MISP Exchange — Phase 11.10g.
- Publication Queue
- Sharing Approvals

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

Phase 11.10e made `/workbench/analysis` functional. It uses DTMO capability/history APIs plus human-triggered IntelOwl and Cortex analyzer execution. History/capability reads require server-side `read:intelligence`; execution requires `review:intelligence`. Analyzer output does not prove local compromise or create sharing/publication authority.

## OpenCTI Graph / Entity placement

Phase 11.10f makes `/workbench/intelligence/graph` functional while preserving the canonical API and evidence model.

The browser calls only DTMO endpoints:

- `/api/v1/opencti/capabilities`;
- `/api/v1/opencti/items/{item_id}/graph`;
- `/api/v1/opencti/entities/{mapping_id}`.

Every read requires server-side `read:intelligence`. The browser does not receive an OpenCTI token and does not query `/graphql` directly.

The graph root is the canonical DTMO intelligence item. OpenCTI nodes come from persisted stable OpenCTI/STIX mappings. Because the accepted persistence boundary does not durably store generic OpenCTI entity-to-entity relationship topology, only attributable `canonical-mapping` edges may be rendered. Missing relationship evidence must **fail closed** rather than being inferred from labels, entity types, confidence, co-occurrence or visual proximity.

An empty mapping set is not an upstream-absence claim. OpenCTI configuration is not runtime health. Entity/graph presence does not prove local exposure, exploitability, compromise, attribution certainty or remediation state.

## Canonical object types

The workbench represents and navigates governed object classes where supported by canonical data, including intelligence items, indicators/IOCs, vulnerabilities/CVEs, threat actors/intrusion sets, campaigns, malware/tools, infrastructure/domain/IP/URL/hash, sources/connectors, cases, tasks, observables, analysis/enrichment jobs, MISP references, OpenCTI entity/mapping references, governance evidence and identity/role/runtime objects.

## Context rail contract

The right context rail is driven by selected attributable object state and may show identity/type, severity/classification, confidence, TLP/PAP/markings, provenance/source, related entities, enrichment/analysis counts, cases/tasks, vulnerabilities/exposure, sharing status, timeline/audit summary and authorized actions.

The rail must never infer an unavailable fact because an integration is configured. Until a feature slice integrates shared rail selection, feature-specific detail remains inside its governed workspace. Phase 11.10f therefore shows OpenCTI entity/revision detail inside the Knowledge Graph workspace while preserving the shell **Context rail contract**.

## Command palette

The end-state palette may support safe navigation and separately governed actions. The current command palette remains navigation-only; it cannot bypass server-side authorization.

## Role-aware defaults

Role-aware defaults may change landing page and visible navigation groups but do not define authorization. Executive, CISO, SOC Analyst, CTI Analyst, Incident Responder, Administrator and Auditor defaults remain distinct usability profiles. Full role-aware presentation acceptance remains Phase 11.10n. **Server-side RBAC** remains authoritative.

## Responsive behavior

Desktop uses persistent navigation and optional context rail. Tablet may collapse regions into drawers. Small mobile view prioritizes situational awareness and explicitly supported low-risk actions. Phase 11.10f adds responsive graph/entity composition plus an accessible entity list so navigation never depends on SVG interaction alone.

## Migration rule

Existing Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance functionality must be mapped into this architecture before legacy retirement. `/workbench/` is the canonical built product route. `/ui/console` and prior UI routes remain temporary **compatibility paths** and are not parallel feature-development targets.

## Candidate-completion state

- 11.10a frontend architecture/design — `PASS / REPOSITORY_COMPLETE`;
- 11.10b canonical shell — `PASS / REPOSITORY_COMPLETE`;
- 11.10c Command Center — `PASS / REPOSITORY_COMPLETE`;
- 11.10d Unified Intelligence Workspace — `PASS / REPOSITORY_COMPLETE`;
- 11.10e IntelOwl/Cortex integrated analysis — `PASS / REPOSITORY_COMPLETE`;
- 11.10f OpenCTI graph/entity workspace — `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- 11.10g MISP Sharing & Exchange — `NOT STARTED`;
- 11.10p fresh production-equivalent validation — `NOT STARTED / CANDIDATE FREEZE REQUIRED`;
- Phase 11.11 — `NOT STARTED`;
- Phase 12 — `NOT STARTED`.

DTMO remains **not production authorized**.

## Evidence boundary

This information architecture and its implemented routes are repository product-design/engineering evidence only. They do **not prove** live OpenCTI connectivity or health, complete upstream topology, local compromise, production-equivalent validation, independent assurance or production authorization. Missing or ambiguous operational evidence must **fail closed**.
