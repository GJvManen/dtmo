# DTMO Next-Generation Information Architecture

Status: **Phase 11.10a — PASS / REPOSITORY_COMPLETE; Phase 11.10b — ACTIVE SHELL APPLICATION**

## Principle

Primary navigation is organized by operator intent, not by upstream product ownership. Service names remain visible as provenance, capability and health context.

Phase 11.10b applies this accepted information architecture to the canonical `/workbench/` shell. Route foundations do not imply that the underlying feature workspace has already been implemented or accepted.

## Canonical navigation tree

### Home

- Command Center

### Intelligence

- Threat Intelligence
- IOC Explorer
- Threat Actors & Campaigns
- Knowledge Graph
- Threat Hunting

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

Phase 11.10b implements the global navigation shell, navigation-only command palette, environment/platform status, principal context, context rail container and theme preference. Notifications, candidate identity and feature actions appear only when later bounded contracts provide attributable data and authority.

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

The rail must never infer an unavailable fact merely because an upstream integration is configured. Phase 11.10b therefore starts with the explicit `Geen object geselecteerd` state rather than placeholder object facts.

## Command palette

The end-state palette may support safe navigation and governed actions such as search, object open, case creation, enrichment, graph navigation, source runs, sharing preparation and approvals.

In **Phase 11.10b the command palette is navigation-only**. High-impact commands are deliberately absent until their own bounded server/API authorization contracts are implemented and accepted.

## Role-aware defaults

Role-aware defaults may change the landing page and visible navigation groups, but they do not define authorization.

- Executive: Command Center, risk/exposure, incidents, governance.
- CISO: intelligence, exposure, cases, governance, approvals.
- SOC Analyst: investigations, intelligence, analysis, automation.
- CTI Analyst: intelligence, graph, analysis, collection, sharing.
- Incident Responder: investigations, tasks, analysis, playbooks.
- Administrator: collection, operations, administration.
- Auditor: evidence, governance, audit and read-only operational context.

Full role-aware presentation acceptance remains Phase 11.10n. **Server-side RBAC** remains authoritative throughout.

## Responsive behavior

Desktop uses persistent navigation and optional persistent context rail. Tablet may collapse either region into drawers. Small mobile view prioritizes read-only situational awareness and explicitly supported low-risk actions; complex case/graph/playbook editing is not forced into an unsafe or unusable mobile layout.

Phase 11.10b implements the responsive shell baseline and mobile navigation/context behavior. Feature-specific responsive acceptance remains in later slices.

## Migration rule

Existing Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance functionality must be mapped into this architecture before any legacy route is retired. No capability may disappear merely because navigation changes.

`/workbench/` is the canonical built application route. `/ui/console` remains a temporary **compatibility path** while migration proceeds and is not a parallel feature-development target.

## Evidence boundary

The accepted information architecture and its 11.10b route/shell implementation are repository product-design evidence only. They do not prove that later feature workspaces are functionally complete, that upstream services were exercised, that production-equivalent validation occurred or that production is authorized.
