# DTMO Next-Generation Information Architecture

Status: **Phase 11.10a — IN PROGRESS / TARGET INFORMATION ARCHITECTURE**

## Principle

Primary navigation is organized by operator intent, not by upstream product ownership. Service names remain visible as provenance, capability and health context.

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

The following are available independently of the current workspace when authorized:

- global search;
- command palette;
- notifications;
- selected object/context rail;
- current environment/candidate identity;
- principal/role context;
- help/documentation;
- theme and accessibility preferences.

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

The rail must never infer an unavailable fact merely because an upstream integration is configured.

## Command palette

The target keyboard command palette supports safe navigation and actions, for example:

- search intelligence;
- open IOC;
- create case;
- run enrichment;
- open graph;
- run source;
- prepare sharing package;
- open approvals;
- open system health.

High-impact commands must still require the same server-side authorization and explicit approval state as their normal UI equivalents.

## Role-aware defaults

Role-aware defaults may change the landing page and visible navigation groups, but they do not define authorization.

- Executive: Command Center, risk/exposure, incidents, governance.
- CISO: intelligence, exposure, cases, governance, approvals.
- SOC Analyst: investigations, intelligence, analysis, automation.
- CTI Analyst: intelligence, graph, analysis, collection, sharing.
- Incident Responder: investigations, tasks, analysis, playbooks.
- Administrator: collection, operations, administration.
- Auditor: evidence, governance, audit and read-only operational context.

## Responsive behavior

Desktop uses persistent navigation and optional persistent context rail. Tablet may collapse either region into drawers. Small mobile view prioritizes read-only situational awareness and explicitly supported low-risk actions; complex case/graph/playbook editing is not forced into an unsafe or unusable mobile layout.

## Migration rule

Existing Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance functionality must be mapped into this architecture before any legacy route is retired. No capability may disappear merely because navigation changes.