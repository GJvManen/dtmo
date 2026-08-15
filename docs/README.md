# DTMO Documentation Portal

This directory contains the authoritative professional documentation for Dutch Threat Monitoring for Education (DTMO). It separates stable product, architecture, security, governance and readiness documentation from immutable operational history and CI evidence.

## Current controlled baseline

| Area | Current state |
|---|---|
| Software baseline | `16.0.0rc12` plus accepted post-RC13/E8 repository enhancements |
| Phases 1–7 | `PASS` |
| RC13 functional product acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Post-E8 external deployment and staging approval | `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE` |
| Phase 8.2–8.4 | `REPOSITORY CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED` |
| Phase 8.5 | `REPOSITORY CONTRACT COMPLETE / EXTERNAL OWNER DECISION REQUIRED` |
| Phase 9 independent assurance | `NOT COMPLETE` |
| Phase 10 production go/no-go | `NOT STARTED` |
| Production readiness | **Not complete** |

DTMO is not production ready. The next formal release objective is completion and accountable acceptance of the Phase 8 external evidence package against one immutable staging deployment identity, followed by independent Phase 9 assurance.

## Start here

| Audience | Primary documents |
|---|---|
| Executive / sponsor | [Executive Status](project/EXECUTIVE_STATUS.md), [Executive Decision View](project/EXECUTIVE_DECISION_VIEW.md), [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md) |
| Product / delivery | [Current State](project/CURRENT_STATE.md), [Production Roadmap](roadmap/PRODUCTION_ROADMAP.md) |
| Architecture / engineering | [Architecture Context](architecture/ARCHITECTURE_CONTEXT.md), [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) |
| Security / CISO | [Security Overview](security/SECURITY_OVERVIEW.md), [Threat Model](security/THREAT_MODEL.md), [Risk Register](security/RISK_REGISTER.md) |
| Governance / compliance | [Governance Mapping Registry](governance/GOVERNANCE_MAPPING_REGISTRY.md), [Data Classification & Retention](governance/DATA_CLASSIFICATION_RETENTION.md) |
| QA / release | [QA and Release Gates](qa/QA_AND_RELEASE_GATES.md), [Production Checklist](project/PRODUCTION_CHECKLIST.md), [Evidence Index](evidence/EVIDENCE_INDEX.md) |
| Operations | [Operating Model](operations/OPERATING_MODEL.md), [Operations Manual](operations/OPERATIONS_MANUAL.md) |
| External assessor | [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md), [Phase 9 External Assurance Gate](qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md), [System Architecture](architecture/SYSTEM_ARCHITECTURE.md), [Security Overview](security/SECURITY_OVERVIEW.md) |

## Documentation model

### Professional current-state layer

The following documents form the current decision-grade set and must remain mutually consistent:

- `README.md` and `docs/README.md`;
- `docs/project/CURRENT_STATE.md`;
- `docs/project/EXECUTIVE_STATUS.md`;
- `docs/project/EXECUTIVE_DECISION_VIEW.md`;
- `docs/project/PRODUCTION_READINESS_REPORT.md`;
- `docs/project/PRODUCTION_CHECKLIST.md`;
- `docs/roadmap/PRODUCTION_ROADMAP.md`;
- `docs/evidence/EVIDENCE_INDEX.md`;
- `docs/qa/QA_AND_RELEASE_GATES.md`;
- architecture/security/governance documents when their substantive boundaries change.

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
- no publication authority from connectors, CI, analytics, Administration, Governance or staging access;
- no inferred framework mappings or broad compliance claims from contextual relationships;
- no raw credentials/tokens in repository evidence;
- open findings, deviations and residual risks remain explicit.

## Governance and framework semantics

The governance model is explicit and provenance-backed. It includes versioned DTMO relationships to Normenkader IBP, MITRE ATT&CK, NIST CSF and vulnerability scoring/context semantics such as CVSS. E8.10 adds vulnerability-management evidence mapping, including Normenkader IBP SM.07 and related supporting evidence. A mapping is evidence of a defined relationship; it is not by itself a claim of full framework compliance, maturity or certification.

## Production-readiness evidence boundary

Phase 8 repository contracts now cover platform/identity validation, source-to-intelligence validation, operations/recovery and accountable staging acceptance. Formal Phase 8 closure still requires the real external evidence package to be complete, reviewable and bound to one immutable staging deployment identity with an explicit accountable owner decision.

Phase 9 requires independent assurance. Repository CI, Docker Compose, staging emulators, synthetic fixtures and internal self-attestation cannot substitute for independent penetration testing or other agreed external-assurance classes.

## Maintenance rule

Whenever lifecycle status, architecture, security boundaries, product scope or governance claims materially change, the professional current-state set must be reconciled together before merge. See [Current-State Documentation Reconciliation Gate](qa/CURRENT_STATE_RECONCILIATION.md) and [Documentation Standard](project/DOCUMENTATION_STANDARD.md).
