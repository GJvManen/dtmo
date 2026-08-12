# DTMO Documentation Portal

This directory contains the authoritative professional documentation for the Dutch Threat Monitoring for Education (DTMO) platform.

The documentation is intentionally separated into **stable product/architecture documentation** and **operational evidence/history**. Architecture, security, governance, product and readiness documents describe the platform and its controlled state. PR-by-PR implementation notes, incident chronology and point-in-time evidence belong under `docs/development/`, GitHub issues and CI artifacts.

## Current baseline

- **Release:** `16.0.0rc12`
- **Repository-controlled engineering:** Phases 1–7 `PASS`
- **Functional unified-console acceptance:** RC13 `PASS / OWNER_ACCEPTED`
- **Current production-readiness stage:** Phase 8 — `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`
- **Independent external assurance:** Phase 9 `NOT COMPLETE`
- **Production go/no-go:** Phase 10 `NOT STARTED`
- **Production readiness:** **not complete**

## Start here

| Audience | Recommended document |
|---|---|
| Executive / sponsor | [Executive Status](project/EXECUTIVE_STATUS.md) |
| Product / delivery | [Current State](project/CURRENT_STATE.md) and [Production Roadmap](roadmap/PRODUCTION_ROADMAP.md) |
| Project governance | [Project Governance](project/PROJECT_GOVERNANCE.md) and [Documentation Standard](project/DOCUMENTATION_STANDARD.md) |
| Architecture / engineering | [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) |
| Security / CISO | [Security Overview](security/SECURITY_OVERVIEW.md) and [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md) |
| Governance / compliance | [Governance Mapping Registry](governance/GOVERNANCE_MAPPING_REGISTRY.md) |
| QA / release management | [QA and Release Gates](qa/QA_AND_RELEASE_GATES.md) and [Production Checklist](project/PRODUCTION_CHECKLIST.md) |
| Operations | [Operations Manual](operations/OPERATIONS_MANUAL.md) |
| Intelligence engineering | [Source Catalog](intelligence/SOURCE_CATALOG.md) and [Source Connection Matrix](qa/SOURCE_CONNECTION_MATRIX.md) |
| New contributors / reviewers | [Glossary](project/GLOSSARY.md) and [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) |

## Documentation building blocks

### 1. Product and project

- [Current Project State](project/CURRENT_STATE.md) — current capabilities, accepted boundaries, known limitations and active workstreams.
- [Executive Status](project/EXECUTIVE_STATUS.md) — decision-oriented summary for leadership and stakeholders.
- [Production Readiness Report](project/PRODUCTION_READINESS_REPORT.md) — consolidated readiness position across engineering, functional, staging, assurance and production gates.
- [Production Checklist](project/PRODUCTION_CHECKLIST.md) — evidence checklist for formal progression.
- [Production Roadmap](roadmap/PRODUCTION_ROADMAP.md) — phased route from accepted engineering baseline to production go/no-go.
- [Project Governance](project/PROJECT_GOVERNANCE.md) — ownership, authority, change, evidence and release-governance model.
- [Documentation Standard](project/DOCUMENTATION_STANDARD.md) — rules for maintaining professional documentation without mixing in operational chronology.
- [Glossary](project/GLOSSARY.md) — canonical terminology for architecture, evidence, governance and release-readiness concepts.

### 2. Architecture and UX

- [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) — logical components, data flow, persistence, trust boundaries, identity, analytics and deployment boundaries.
- [Frontend UX Architecture](ux/FRONTEND_UX.md) — canonical console information architecture and interaction principles.
- [API documentation](api/) — API contracts and supporting interface notes.

### 3. Security, privacy and identity

- [Security Overview](security/SECURITY_OVERVIEW.md) — security model, identities, authorization, privileged operations, secret handling and approval boundaries.
- [Security Policy](../SECURITY.md) — vulnerability reporting and security-contact policy.
- [ADR-001 — Evidence and Claim Boundaries](project/ADR/ADR-001-EVIDENCE-CLAIM-BOUNDARIES.md) — architectural rule separating engineering evidence from manual/external acceptance claims.

### 4. Intelligence and source governance

- [Source Catalog](intelligence/SOURCE_CATALOG.md) — supported source inventory and classification.
- [Source Connection Matrix](qa/SOURCE_CONNECTION_MATRIX.md) — connection/execution expectations and evidence status.
- [Safe Source Execution Gate](qa/SAFE_SOURCE_EXECUTION_GATE.md) — source-execution controls.
- [Intelligence Pipeline Release Gate](qa/INTELLIGENCE_PIPELINE_RELEASE_GATE.md) — canonical pipeline and persistence acceptance.

Credential values are never repository/catalog evidence. Credentialed integrations use logical secret references and runtime resolution.

### 5. Governance and framework mapping

- [Project Governance](project/PROJECT_GOVERNANCE.md) — project-level authority and decision model.
- [Governance Mapping Registry](governance/GOVERNANCE_MAPPING_REGISTRY.md) — authoritative framework mapping truth model.
- [Traceability Matrix](traceability/TRACEABILITY_MATRIX.md) — requirements/control/evidence traceability.
- [Evidence Index](evidence/EVIDENCE_INDEX.md) — structured evidence references.

Current framework truth remains explicit:

- Normenkader IBP — `UNMAPPED` at first-class control crosswalk level;
- MITRE ATT&CK — `UNMAPPED` at first-class technique crosswalk level;
- CVSS — `CONTEXT_ONLY` until first-class score/vector fields and mappings are implemented;
- DTMO internal security/release governance — repository-backed internal mappings.

Missing mappings are not inferred from free text, tags or semantic similarity.

### 6. QA and release assurance

- [QA and Release Gates](qa/QA_AND_RELEASE_GATES.md)
- [RC13 Functional Console Acceptance Gate](qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md)
- [Frontend Release Gate](qa/FRONTEND_RELEASE_GATE.md)
- [Frontend UX Release Gate](qa/FRONTEND_UX_RELEASE_GATE.md)
- [Phase 8 Staging Deployment-Parity Gate](qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md)
- [Phase 9 External Assurance Gate](qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md)
- [Open Source Governance](qa/OPEN_SOURCE_GOVERNANCE.md)

DTMO applies exact-head release discipline. A configured, queued, cancelled, skipped, failed, stale or inaccessible test is never treated as `PASS`. A new commit invalidates previous exact-head CI for the pull request.

### 7. Staging, operations and recovery

- [Phase 8 Deployment Identity Record](staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md) — fail-closed record for the real staging deployment identity.
- [Operations Manual](operations/OPERATIONS_MANUAL.md) — operational procedures and platform operations.
- [Performance documentation](performance/) — accepted performance evidence and boundaries.

The local Compose topology and staging emulators are supporting engineering evidence only. Real Phase 8 acceptance requires one approved production-equivalent environment and evidence tied to an immutable deployment identity.

### 8. Releases and historical evidence

- [16.0.0rc12 Release Notes](releases/16.0.0rc12.md)
- [Development Run Log](development/RUN_LOG.md)
- `development/runs/` — immutable point-in-time engineering and acceptance records.

Operational history is retained for auditability, but it must not replace the stable architecture/product documentation.

## Security and authority invariants

Across all documentation, the following remain authoritative:

- RBAC and least privilege;
- strict separation between human and service-account roles;
- administrator safety and separation of duties;
- provenance and confidence preservation;
- privacy and data minimization;
- tamper-evident auditability and request correlation;
- explicit human review and separate external-share approval;
- no publication authority from connectors, CI, dashboards, analytics, Administration, Governance or staging access;
- no inferred framework/control/technique mappings;
- no raw secrets in repository evidence.

## Current workstreams

Two distinct workstreams are active and must not be conflated:

1. **Production readiness:** Phase 8.1 real staging environment and immutable deployment identity.
2. **Product enhancement:** issue #171, beginning with shared accessible severity semantics/filtering across Overview and Intelligence, followed by manual source onboarding, trend analytics, first-class framework mapping, richer RBAC administration and deeper Governance.

Product enhancements do not automatically count as Phase 8/9/10 evidence; they require their own appropriate environment evidence when relevant.
