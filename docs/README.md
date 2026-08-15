# DTMO Documentation Portal

This directory contains the authoritative professional documentation for Dutch Threat Monitoring for Education (DTMO). It separates stable product, architecture, security, governance and readiness documentation from immutable operational history and CI evidence.

## Current controlled baseline

| Area | Current state |
|---|---|
| Software baseline | `16.0.0rc12` plus accepted post-RC13/E8 repository enhancements |
| Phases 1–7 | `PASS` |
| RC13 functional product acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 production-equivalent staging | `PASS / OWNER_ACCEPTED` |
| Phase 9 independent assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 production go/no-go | `IN PROGRESS / DECISION REQUIRED` |
| Production readiness | **Not production authorized until Phase 10 GO** |

The active release objective is the formal Phase 10 production decision. Completion of Phase 8 and Phase 9 satisfies staging and independent-assurance prerequisites but does not itself authorize production.

## Start here

| Audience | Primary documents |
|---|---|
| Executive / sponsor | [Executive Status](project/EXECUTIVE_STATUS.md), [Executive Decision View](project/EXECUTIVE_DECISION_VIEW.md), [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md), [Phase 10 Go/No-Go](production/PHASE10_PRODUCTION_GO_NO_GO.md) |
| Product / delivery | [Product Guide](product/PRODUCT_GUIDE.md), [Current State](project/CURRENT_STATE.md), [Production Roadmap](roadmap/PRODUCTION_ROADMAP.md) |
| Analyst / reviewer | [User Guide](user/USER_GUIDE.md), [System Workflows](architecture/SYSTEM_WORKFLOWS.md), [Screenshot Catalogue](visual/screenshots/README.md) |
| Administrator | [Administrator Guide](administration/ADMINISTRATOR_GUIDE.md), [Security Overview](security/SECURITY_OVERVIEW.md), [System Workflows](architecture/SYSTEM_WORKFLOWS.md) |
| Architecture / engineering | [Architecture Context](architecture/ARCHITECTURE_CONTEXT.md), [System Architecture](architecture/SYSTEM_ARCHITECTURE.md), [System Workflows](architecture/SYSTEM_WORKFLOWS.md) |
| Security / CISO | [Security Overview](security/SECURITY_OVERVIEW.md), [Threat Model](security/THREAT_MODEL.md), [Risk Register](security/RISK_REGISTER.md), [Identity/RBAC workflows](architecture/SYSTEM_WORKFLOWS.md) |
| Governance / compliance | [Governance Mapping Registry](governance/GOVERNANCE_MAPPING_REGISTRY.md), [Data Classification & Retention](governance/DATA_CLASSIFICATION_RETENTION.md), [Governance evidence workflow](architecture/SYSTEM_WORKFLOWS.md) |
| QA / release | [QA and Release Gates](qa/QA_AND_RELEASE_GATES.md), [Production Checklist](project/PRODUCTION_CHECKLIST.md), [Evidence Index](evidence/EVIDENCE_INDEX.md), [Phase 10 Go/No-Go](production/PHASE10_PRODUCTION_GO_NO_GO.md) |
| Operations | [Operating Model](operations/OPERATING_MODEL.md), [Operations Manual](operations/OPERATIONS_MANUAL.md), [Recovery workflow](architecture/SYSTEM_WORKFLOWS.md) |
| External assessor | [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md), [Phase 9 External Assurance Gate](qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md), [System Architecture](architecture/SYSTEM_ARCHITECTURE.md), [Security Overview](security/SECURITY_OVERVIEW.md) |

## Professional product manuals

- [Product Guide](product/PRODUCT_GUIDE.md) — product purpose, surfaces, major workflows, vulnerability semantics and authority boundaries;
- [User Guide](user/USER_GUIDE.md) — analyst/reviewer navigation, search, filtering, vulnerability triage, AIL/MISP context and degraded-state behavior;
- [Administrator Guide](administration/ADMINISTRATOR_GUIDE.md) — identities, RBAC, privileged Administration, source governance, secrets, MISP sharing boundaries and audit/correlation.

These guides are linked to canonical system workflows rather than duplicating incompatible process descriptions.

## Visual system documentation

- [System Workflows](architecture/SYSTEM_WORKFLOWS.md) contains maintained source-to-intelligence, vulnerability, identity/RBAC, Administration, MISP, AIL, audit, governance, observability, recovery, deployment-identity and production-readiness workflows.
- [Visual Documentation Standard](visual/DOCUMENTATION_VISUAL_STANDARD.md) defines how diagrams and screenshots are structured, labelled, reviewed and kept current.
- [Product Screenshot Catalogue](visual/screenshots/README.md) defines the governed screenshot set.

The governed screenshot catalogue contains UI-01 through UI-10. Each published PNG is tied to a reviewed DTMO runtime capture using sanitized fixtures where applicable. These visuals are documentation illustrations: they do not prove live-source connectivity, external staging activity, independent assurance or production authorization.

## Documentation model

### Professional current-state layer

The following documents form the current decision-grade set and must remain mutually consistent:

- `README.md` and `docs/README.md`;
- `docs/project/CURRENT_STATE.md`;
- `docs/project/EXECUTIVE_STATUS.md`;
- `docs/project/EXECUTIVE_DECISION_VIEW.md`;
- `docs/project/PRODUCTION_READINESS_REPORT.md`;
- `docs/project/PRODUCTION_CHECKLIST.md`;
- `docs/project/DOCUMENTATION_STATUS.md`;
- `docs/roadmap/PRODUCTION_ROADMAP.md`;
- `docs/evidence/EVIDENCE_INDEX.md`;
- `docs/qa/QA_AND_RELEASE_GATES.md`;
- `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`.

See [Documentation Status and Authority](project/DOCUMENTATION_STATUS.md) for the authority and currency model.

### Operational and immutable evidence layer

PR chronology, workflow/run identifiers, point-in-time blockers and immutable evidence records belong under `docs/development/`, GitHub issues/pull requests and CI artifacts. Historical records are not rewritten to match later project decisions.

## Product and architecture scope

The repository-complete product baseline provides one governed console across Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance. The E8 line adds OpenCVE, Vulnerability-Lookup, governed MISP read/export, governed AIL read/enrichment/correlation, explainable vulnerability prioritization, vulnerability analytics and provenance-backed vulnerability-management framework mappings.

PostgreSQL remains canonical application state; OpenSearch is the search/index representation; S3-compatible object storage retains raw evidence; Redis provides coordination; Prometheus and separately authenticated Grafana provide operational observability.

## Security and authority invariants

Across all documentation the following remain authoritative:

- server-side RBAC and least privilege;
- human/service-account separation;
- privileged Administration safeguards and auditable actions;
- provenance/confidence preservation and data minimization;
- separate human review and external-share approval;
- no publication authority from connectors, CI, analytics, Administration, Governance, staging acceptance or production authorization;
- no inferred framework mappings or broad compliance claims from contextual relationships;
- no raw credentials/tokens in repository evidence;
- open findings, deviations and residual risks remain explicit.

## Governance and framework semantics

The governance model is explicit and provenance-backed. It includes versioned DTMO relationships to Normenkader IBP, MITRE ATT&CK, NIST CSF and vulnerability scoring/context semantics such as CVSS. E8.10 adds vulnerability-management evidence mapping, including Normenkader IBP SM.07 and related supporting evidence. A mapping is evidence of a defined relationship; it is not by itself a claim of full framework compliance, maturity or certification.

## Production-readiness evidence boundary

Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`. These are distinct accountable/external evidence classes. Repository CI, Docker Compose, staging emulators, synthetic fixtures and internal self-attestation are not represented as substitutes for them.

Phase 10 is a separate accountable authorization decision. DTMO remains not production authorized until all required production decision inputs are accepted and an explicit `GO` is recorded.

## Maintenance rule

Whenever lifecycle status, architecture, security boundaries, product scope or governance claims materially change, the professional current-state set must be reconciled together before merge. Visuals that explain a materially changed workflow must be updated in the same change. See [Current-State Documentation Reconciliation Gate](qa/CURRENT_STATE_RECONCILIATION.md), [Documentation Standard](project/DOCUMENTATION_STANDARD.md) and [Visual Documentation Standard](visual/DOCUMENTATION_VISUAL_STANDARD.md).