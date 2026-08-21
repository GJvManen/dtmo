# DTMO — Dutch Threat Monitoring for Education

DTMO is an open Cyber Threat Intelligence (CTI) platform for education-sector security teams. It combines governed threat-source operations, canonical intelligence, provenance, vulnerability intelligence, investigation, visual analytics, role-based administration and governance evidence in one controlled application.

> **Software baseline:** `16.0.0rc12` with accepted post-RC13, E8 and Phase 11 repository enhancements  
> **Engineering baseline:** Phases 1–7 `PASS`  
> **Functional acceptance:** RC13 `PASS / OWNER_ACCEPTED`  
> **Product evolution:** E8.1–E8.10 `PASS / REPOSITORY_COMPLETE`  
> **Historical staging evidence:** Phase 8 `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE`  
> **Historical independent assurance:** Phase 9 `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`  
> **Phase 10 production decision:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`  
> **Phase 11.1–11.9:** `PASS / REPOSITORY_COMPLETE`  
> **Phase 11.10:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`  
> **Phase 11.10a–11.10k:** `PASS / REPOSITORY_COMPLETE`  
> **Active bounded slice:** Phase 11.10l Governance & Evidence — `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`  
> **Phase 11.10m–11.10o:** `NOT STARTED`  
> **Phase 11.10p fresh production-equivalent validation:** `NOT STARTED / CANDIDATE FREEZE REQUIRED`  
> **Phase 11.11 independent external assurance:** `NOT STARTED`  
> **Phase 12 production decision:** `NOT STARTED`  
> **Production status:** **not production authorized**

## Why DTMO

Education environments combine broad digital estates, sensitive information, cloud dependencies and threats ranging from opportunistic exploitation to targeted campaigns. DTMO turns heterogeneous governed intelligence into traceable, reviewable and operationally useful security intelligence while preserving authorization, privacy, provenance and publication controls.

DTMO is built around five principles: **provenance first; fail closed; human authority remains human; least privilege by design; evidence-based governance**.

## Product capabilities

The canonical Unified Operations Workbench provides governed capabilities across the operational CTI lifecycle:

- **Command Center and Unified Intelligence** for current intelligence, IOC discovery, severity-aware triage, provenance and trends;
- **Sources & Catalog** for governed source registration, validation, test execution and collection control without exposing server-side credentials;
- **Integrated Analysis** through IntelOwl and the bounded Cortex analyzer connector, where enrichment remains evidence rather than an automated compromise verdict;
- **OpenCTI graph/entity exploration** using persisted topology and provenance without inventing relationships;
- **MISP Sharing & Exchange** under explicit human share/publication authority;
- **TheHive Investigations & Cases** with separate human case-handoff authority and durable reconciliation evidence;
- **Vulnerability & Exposure** using CVSS, EPSS, KEV and canonical vulnerability intelligence without inferring local exposure;
- **Visual Analytics** for governed operational and trend views inside the canonical application shell;
- **Automation & Playbooks** for bounded, policy-controlled orchestration that cannot self-grant human review or publication authority;
- **Administration** for role-aware, server-authorized operational controls;
- **Governance** for repository-backed framework mappings, provenance, authority boundaries and evidence interpretation.

## Architecture

DTMO separates browser presentation, canonical application state and upstream integration boundaries. PostgreSQL remains canonical application truth; Redis supports coordination, OpenSearch provides search projection, and S3-compatible object storage provides governed object persistence. Taranis AI, IntelOwl, OpenCTI, MISP, TheHive and Cortex remain separate governed service and licensing boundaries.

Normal frontend operations follow:

```mermaid
flowchart LR
    B[Browser] --> W[DTMO Unified Operations Workbench]
    W --> A[DTMO API]
    A --> R[Server-side RBAC + audit]
    R --> D[(Canonical PostgreSQL state)]
    R --> Q[Redis coordination]
    R --> O[OpenSearch projection]
    R --> S3[S3-compatible object storage]
    R --> G[Governed adapters and contracts]
    G --> T[Taranis AI]
    G --> I[IntelOwl]
    G --> C[Cortex analyzers]
    G --> OI[OpenCTI]
    G --> M[MISP]
    G --> H[TheHive]
```

The browser does not receive privileged upstream credentials. Role-aware presentation is a usability function; **server-side RBAC remains authoritative**. Human intelligence review, external-share approval, publication, TheHive case handoff, connector execution, administration and production authorization remain separate authority domains.

The accepted Phase 11.8 platform baseline includes Kubernetes/Helm/GitOps, workload identity, external secret delivery, ingress/TLS, network segmentation, HA/disruption controls, observability, backup/recovery, supply-chain hardening, capacity planning and upgrade/rollback. Phase 11.9 adds the connected forward-first migration/compatibility contract. Application rollback does not authorize automatic database down migration.

## Accepted Phase 11 service integration baseline

The accepted service phases remain explicit repository-complete boundaries and are not replaced by the later workbench UX:

- **Phase 11.3 IntelOwl** — governed enrichment integration remains `PASS / REPOSITORY_COMPLETE`; enrichment evidence does not establish local compromise or human publication/share authority.
- **Phase 11.4 OpenCTI** — knowledge-graph integration remains `PASS / REPOSITORY_COMPLETE`; persisted mappings and graph evidence are not inferred beyond recorded evidence.
- **Phase 11.5 MISP** — consolidation remains `PASS / REPOSITORY_COMPLETE`; transfer remains separate from publication and subject to DTMO human sharing authority.
- **Phase 11.6 TheHive** — incident/case handoff remains `PASS / REPOSITORY_COMPLETE`; case creation is a distinct explicit human authority and case identity does not prove compromise or remediation.
- **Phase 11.7 Cortex** — the historical decision gate remains accepted, with the later analyzer-only connector boundary preserving responder/remediation separation.

These accepted boundaries remain distinct service/licensing domains with server-side credentials and fail-closed evidence interpretation.

## Unified Operations Workbench

The canonical workbench now has repository-complete slices for frontend architecture, application shell, Command Center, Unified Intelligence/IOC Explorer, IntelOwl/Cortex Analysis, OpenCTI Graph/Entity, MISP Sharing & Exchange, TheHive Investigations & Cases, Vulnerability & Exposure, Sources & Collection and Automation & Playbooks.

**Phase 11.10l Governance & Evidence is active.** `/workbench/governance` consumes DTMO-owned same-origin governance APIs under server-side RBAC. It reuses the existing explicit repository-backed governance crosswalk rather than inventing a parallel compliance store.

The governance crosswalk contains scoped typed relationships for **Normenkader IBP**, **MITRE ATT&CK**, **NIST CSF 2.0** and **CVSS 4.0 context**. These are partial evidence relationships, not certification, blanket compliance, semantic equivalence, control-effectiveness proof or production authorization. Unrecorded framework objects remain unmapped and unavailable evidence fails closed.

## Authority and evidence boundaries

Service accounts, connectors, analyzers, CI identities and browser controls cannot self-grant human approval powers. Enrichment output does not prove compromise. Graph presence does not prove exposure. MISP transfer does not prove publication. TheHive case identity does not prove remediation. CVSS/EPSS/KEV do not prove local exposure. Source/automation success does not prove source truth. Governance mappings do not prove compliance or environment effectiveness.

Repository CI is exact-head engineering evidence only. It does **not** prove production-equivalent operation, owner acceptance, independent assurance or production authorization.

## Current maturity and release position

Phases 1–7, RC13, E8.1–E8.10 and Phase 11.1–11.9 are accepted repository baselines according to their authoritative evidence records. Phase 8 staging and Phase 9 external assurance remain accepted only as **historical candidate-bound evidence**. Because the integrated platform has materially changed, Phase 10 remains **NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED** until the new Phase 11 candidate completes its fresh validation and assurance sequence.

Phase 11.10a–11.10k are `PASS / REPOSITORY_COMPLETE`. Phase 11.10l remains `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 11.10p, Phase 11.11 and Phase 12 have not yet established production-equivalent validation, independent assurance or production authorization for the materially changed candidate.

## Product roadmap

Phase 11.10l must first reach one final unchanged exact head with every registered workflow `completed/success`, synchronized professional documentation, a mergeable PR and ready-for-review state. Merge uses squash plus expected-head protection. Only then may **11.10m Operations & Administration** start, followed by 11.10n role-aware UX/accessibility and 11.10o consolidation/full functional acceptance.

After 11.10o, one immutable candidate is frozen for **11.10p fresh production-equivalent validation**. Historical Phase 8/9 evidence cannot be reused for this materially changed candidate. Fresh **Phase 11.11 independent external assurance** follows against the same candidate, then **Phase 12** makes the formal accountable production GO/NO-GO.

## Documentation

Start with [`docs/README.md`](docs/README.md), [`docs/project/CURRENT_STATE.md`](docs/project/CURRENT_STATE.md), [`docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`](docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md), [`docs/security/SECURITY_OVERVIEW.md`](docs/security/SECURITY_OVERVIEW.md), [`docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`](docs/governance/GOVERNANCE_MAPPING_REGISTRY.md) and [`docs/evidence/EVIDENCE_INDEX.md`](docs/evidence/EVIDENCE_INDEX.md).

The active 11.10l package is documented in [`docs/architecture/PHASE11_10L_GOVERNANCE_EVIDENCE.md`](docs/architecture/PHASE11_10L_GOVERNANCE_EVIDENCE.md), [`docs/user/GOVERNANCE_EVIDENCE_WORKSPACE.md`](docs/user/GOVERNANCE_EVIDENCE_WORKSPACE.md) and [`docs/qa/PHASE11_10L_GOVERNANCE_EVIDENCE_GATE.md`](docs/qa/PHASE11_10L_GOVERNANCE_EVIDENCE_GATE.md).

## Open source and responsible use

DTMO is released under the **Apache License, Version 2.0**. Its open-source architecture does not weaken operational governance: upstream services keep their own licensing and service boundaries, credentials remain server-side, external sharing/publication requires explicit human authority, and repository evidence must not be misrepresented as production-equivalent validation or independent assurance.

Use DTMO only with authorized data sources, infrastructure and testing scopes. Preserve provenance, handling restrictions, privacy obligations and accountable human decision-making throughout the intelligence lifecycle.
