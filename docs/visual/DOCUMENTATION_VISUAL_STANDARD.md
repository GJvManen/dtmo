# DTMO Visual Documentation Standard

**Status:** Authoritative documentation standard  
**Applies to:** product, architecture, operations, security, governance, integration and assurance documentation  
**Baseline:** post-E8 / Phase 8–9 documentation line

## 1. Purpose

DTMO documentation must be usable by executives, analysts, administrators, engineers, auditors and external assurance parties without requiring repository archaeology. Text remains authoritative, but complex behavior should be accompanied by diagrams, workflows, tables or genuine product screenshots where these improve comprehension.

Visuals are explanatory documentation. They are not substitutes for test evidence, staging evidence, owner acceptance, independent assurance or production authorization.

## 2. Documentation information architecture

The professional documentation set is organized by audience and task:

1. **Product Guide** — capabilities, product concepts and major user journeys.
2. **User Guide** — analyst-facing console functions and workflows.
3. **Administrator Guide** — identities, RBAC, Administration, source governance and configuration.
4. **Architecture** — system context, components, data flows, trust boundaries and deployment topology.
5. **Security** — authentication, authorization, secrets, audit/correlation, security boundaries and failure behavior.
6. **Governance** — framework mappings, evidence semantics, classifications and approval boundaries.
7. **Operations** — observability, backup/recovery, rollback, degraded dependencies and incident operations.
8. **Integrations** — source connectors, MISP, AIL, OpenCVE, Vulnerability-Lookup and other governed integrations.
9. **Deployment** — local/development, production-equivalent staging and release/deployment identity.
10. **QA & Assurance** — repository gates, external staging validation, independent assurance and formal acceptance.
11. **Evidence** — evidence hierarchy, immutable identity binding and claim boundaries.
12. **Developer Reference** — API, internals, ADRs and development-only implementation material.

## 3. Required system workflow catalogue

The following workflows should have a maintained visual representation:

| ID | Workflow | Primary audience | Required representation |
|---|---|---|---|
| WF-01 | Source-to-intelligence | Analyst / engineer / auditor | end-to-end flowchart |
| WF-02 | Vulnerability prioritization | Analyst / CISO | CVSS + EPSS + KEV + relevance decision flow |
| WF-03 | MISP read and governed export | Analyst / approver | trust-boundary + approval workflow |
| WF-04 | AIL enrichment and correlation | Analyst | enrichment/correlation flow |
| WF-05 | Authentication and bearer trust | Administrator / security | sequence/trust-boundary diagram |
| WF-06 | RBAC and privileged Administration | Administrator / auditor | authorization decision workflow |
| WF-07 | Audit and correlation | Security / auditor | request-to-audit trace flow |
| WF-08 | Governance mapping and evidence | CISO / auditor | evidence-to-framework relationship flow |
| WF-09 | Observability | Operations | metrics/logs/audit/Grafana flow |
| WF-10 | Backup, recovery and rollback | Operations / assurance | recovery decision flow |
| WF-11 | Deployment and immutable identity | Release / assurance | release-to-staging identity chain |
| WF-12 | Phase 8–10 acceptance | Owner / assurance | lifecycle acceptance workflow |

## 4. Screenshot catalogue

Genuine product screenshots should be stored under `docs/visual/screenshots/` using stable, descriptive names. Minimum catalogue:

| ID | View | Target file |
|---|---|---|
| UI-01 | Overview / executive dashboard | `overview-dashboard.png` |
| UI-02 | Intelligence workspace | `intelligence-workspace.png` |
| UI-03 | Sources & Catalogue | `sources-catalogue.png` |
| UI-04 | Vulnerability analytics | `vulnerability-analytics.png` |
| UI-05 | MISP workspace/export | `misp-governed-workflow.png` |
| UI-06 | AIL correlation workspace | `ail-correlation-workspace.png` |
| UI-07 | Visual Analytics / Grafana | `visual-analytics.png` |
| UI-08 | Governance | `governance-frameworks.png` |
| UI-09 | Administration / RBAC | `administration-rbac.png` |
| UI-10 | Audit / operational evidence surface | `audit-correlation.png` |

## 5. Screenshot evidence rules

A screenshot labelled **product screenshot** must come from an actual DTMO runtime. Synthetic mock-ups, design concepts and generated illustrations must be labelled as conceptual and must never be presented as runtime evidence.

For every maintained product screenshot:

- capture the complete relevant viewport without browser or OS secrets;
- use a supported browser and a deterministic viewport where practical;
- use sanitized or demonstrably non-production data;
- redact tokens, credentials, personal data and restricted operational identifiers;
- record the capture context in `docs/visual/screenshots/README.md`;
- identify whether the capture is local/demo, production-equivalent staging or historical;
- do not infer deployment acceptance or external assurance from the image alone;
- replace screenshots when product navigation or major interaction behavior changes materially.

## 6. Diagram standard

Repository-native diagrams should use Mermaid when possible so that they are reviewable as text and render directly on GitHub. A diagram must:

- have a descriptive title and workflow ID;
- show systems/actors rather than implementation trivia;
- make human approval points explicit;
- show trust or authority boundaries where material;
- distinguish evidence/provenance from derived intelligence;
- show degraded/failure paths when these materially affect behavior;
- avoid implying compliance, remediation or publication authority that DTMO does not possess.

## 7. Page pattern

Major professional pages should use this order where applicable:

1. purpose and audience;
2. current lifecycle/status boundary;
3. workflow/system visual;
4. actor or component responsibilities;
5. step-by-step operational behavior;
6. security/governance boundaries;
7. failure/degraded behavior;
8. evidence and observability;
9. screenshots/examples;
10. related authoritative documents.

## 8. Accessibility

Visual documentation must remain understandable without color alone. Diagrams and screenshots require descriptive headings/captions and surrounding text that conveys the relevant meaning. Avoid tiny labels and excessively wide diagrams that are unreadable at normal GitHub zoom.

## 9. Maintenance and authority

- Current lifecycle truth remains governed by `docs/project/CURRENT_STATE.md`, `docs/roadmap/PRODUCTION_ROADMAP.md` and the documentation authority matrix.
- Visuals must be updated in the same PR when a material documented workflow changes.
- Historical screenshots and diagrams must be explicitly labelled historical if retained.
- External evidence must remain separately governed and immutable; visual-documentation cleanup must never rewrite historical acceptance evidence.
