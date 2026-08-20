# DTMO Next-Generation Information Architecture

Status: **Phase 11.10a–11.10c — PASS / REPOSITORY_COMPLETE; Phase 11.10d — ACTIVE UNIFIED INTELLIGENCE WORKSPACE**

## Principle

Primary navigation is organized by operator intent, not by upstream product ownership. Service names remain visible as provenance, capability and health context.

Phase 11.10b established the canonical `/workbench/` shell. Phase 11.10c delivered the Command Center, and Phase 11.10d is the active functional migration of Threat Intelligence and IOC Explorer. Route foundations for later workspaces do not imply that those features are already implemented or accepted.

## Canonical navigation tree

### Home

- Command Center — accepted in Phase 11.10c.

### Intelligence

- Threat Intelligence — active in Phase 11.10d.
- IOC Explorer — active in Phase 11.10d.
- Threat Actors & Campaigns — later bounded intelligence capability.
- Knowledge Graph — Phase 11.10f.
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

- Enrichment
- Cortex Analyses
- Analysis History

### Sharing

- MISP Exchange
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

The accepted architecture defines these global surfaces when authorized:

- global search;
- command palette;
- notifications;
- selected object/context rail;
- current environment/candidate identity;
- principal/role context;
- help/documentation;
- theme and accessibility preferences.

The accepted shell implements global navigation, a navigation-only command palette, environment/platform status, principal context, context rail container and theme preference. Notifications, candidate identity and high-impact feature actions appear only when bounded contracts provide attributable data and authority.

## Unified Intelligence placement

Phase 11.10d makes the Intelligence domain functional without changing the authority model.

`/workbench/intelligence` provides explicit governed search and investigation. `/workbench/intelligence/iocs` provides an indicator-oriented entry point over the same DTMO contracts. The browser calls DTMO endpoints only:

- `/api/v1/intelligence/search` for index discovery;
- `/api/v1/intelligence/{item_id}/workspace` for canonical object detail and provenance.

Search results are discovery projections, not canonical truth. Selecting a result retrieves canonical DTMO state separately. Search/detail failures remain unavailable and must not be represented as synthetic empty or complete intelligence.

## Canonical object types

The workbench must be able to represent and navigate at least these governed object classes where supported by canonical data:

- intelligence item;
- indicator/IOC;
- vulnerability/CVE;
- threat actor/intrusion set;
- campaign;
- malware/tool;
- infrastructure/domain/IP/URL/hash;
- source/connector;
- case;
- task;
- observable;
- analysis/enrichment job;
- MISP event/attribute reference;
- OpenCTI entity/relationship reference;
- governance framework/control/mapping/evidence object;
- user/service identity/role/policy;
- runtime/integration health object.

## Context rail contract

The right context rail is driven by the selected object and may show:

- identity/title/type;
- severity/classification;
- confidence;
- TLP/PAP/markings where attributable;
- provenance/source;
- related entities;
- enrichment/analysis counts and state;
- cases/tasks;
- vulnerabilities/exposure;
- sharing status;
- timeline/audit summary;
- principal-authorized actions.

The rail must never infer an unavailable fact merely because an upstream integration is configured. Until a feature slice integrates a selected object into the shared rail, it retains the explicit `Geen object geselecteerd` state rather than placeholder object facts. Phase 11.10d therefore renders canonical detail inside its own governed investigation surface while preserving the shell rail contract.

## Command palette

The end-state palette may support safe navigation and governed actions such as search, object open, case creation, enrichment, graph navigation, source runs, sharing preparation and approvals.

The current command palette remains navigation-only. High-impact commands are deliberately absent until their own bounded server/API authorization contracts are implemented and accepted.

## Role-aware defaults

Role-aware defaults may change the landing page and visible navigation groups, but they do not define authorization.

- Executive: Command Center, risk/exposure, incidents, governance.
- CISO: intelligence, exposure, cases, governance, approvals.
- SOC Analyst: investigations, intelligence, analysis, automation.
- CTI Analyst: intelligence, graph, analysis, collection, sharing.
- Incident Responder: investigations, tasks, analysis, playbooks.
- Administrator: collection, operations, administration.
- Auditor: evidence, governance, audit and read-only operational context.

Full role-aware presentation acceptance remains Phase 11.10n. **Server-side RBAC** remains authoritative throughout. Phase 11.10d search and object reading require `read:intelligence` and grant no mutation authority.

## Responsive behavior

Desktop uses persistent navigation and optional persistent context rail. Tablet may collapse either region into drawers. Small mobile view prioritizes read-only situational awareness and explicitly supported low-risk actions; complex case/graph/playbook editing is not forced into an unsafe or unusable mobile layout.

The accepted shell implements the responsive navigation/context baseline. Phase 11.10d adds responsive intelligence search/result/detail composition. Feature-specific responsive acceptance continues in later slices.

## Migration rule

Existing Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance functionality must be mapped into this architecture before any legacy route is retired. No capability may disappear merely because navigation changes.

`/workbench/` is the canonical built application route. `/ui/console` and `/ui/intelligence-workspace` remain temporary **compatibility paths** while migration proceeds and are not parallel feature-development targets.

## Candidate-completion state

- 11.10a frontend architecture/design — `PASS / REPOSITORY_COMPLETE`;
- 11.10b canonical shell — `PASS / REPOSITORY_COMPLETE`;
- 11.10c Command Center — `PASS / REPOSITORY_COMPLETE`;
- 11.10d Unified Intelligence Workspace — `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- 11.10e IntelOwl/Cortex integrated analysis — `NOT STARTED`;
- 11.10p fresh production-equivalent validation — `NOT STARTED / CANDIDATE FREEZE REQUIRED`;
- Phase 11.11 — `NOT STARTED`;
- Phase 12 — `NOT STARTED`.

DTMO remains **not production authorized**.

## Evidence boundary

This information architecture and its implemented routes are repository product-design/engineering evidence only. They do not prove live upstream completeness or health, production-equivalent validation, independent assurance or production authorization. Missing or ambiguous operational evidence must **fail closed**.
