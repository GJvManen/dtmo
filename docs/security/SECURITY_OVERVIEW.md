# DTMO Security Overview

Last updated: **2026-08-21**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## Security and lifecycle state

DTMO protects confidentiality, integrity, availability, provenance, accountability and controlled dissemination of cyber threat intelligence. DTMO is **not production authorized**. Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. Phase 11 is `IN PROGRESS / ACTIVE`; Phase 11.1–11.9 and Phase 11.10a–11.10k are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 remains **`IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`** and the sole active bounded slice is **Phase 11.10l Governance & Evidence**, `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 11.10m–11.10o, Phase 11.11 and Phase 12 are `NOT STARTED`; Phase 11.10p is `NOT STARTED / CANDIDATE FREEZE REQUIRED`.

Phase 8 remains `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE`; Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`. Neither may be reused as assurance for the materially changed Phase 11 candidate.

## Identity and access control

- **Server-side RBAC remains authoritative.**
- Human and service identities remain separate.
- `read:intelligence` controls intelligence, analysis, graph, sharing-state, investigation, vulnerability and governance reads.
- `review:intelligence`, `approve:share` and `handoff:case` remain separate human authorities.
- `manage:connectors` governs connector/source administration and execution; browser controls are never an authorization boundary.
- Service accounts cannot perform human review/share approval or human case handoff.
- Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate service/API/licensing/provider boundaries.
- Missing, conflicting, stale or unverifiable mandatory evidence must **fail closed**.

## Separation of duties

Human review, external sharing approval, publication, case handoff, connector execution, analyzer execution, governance visibility, CI build identity, deployment, validation review, release signing and production authorization remain distinct authority domains. A connector, analyzer, graph node, vulnerability record, governance mapping, browser control, CI job, signed artifact or evidence validator cannot self-grant analyst approval or production authority.

## Accepted Phase 11 security baseline

Phase 11.8 accepted repository controls for immutable runtime identity, non-root/read-only workloads, workload identity, external secret delivery, ingress/TLS/network segmentation, HA/disruption, observability, recovery, software supply-chain hardening, capacity/resource planning and upgrade/rollback. Phase 11.9 accepted the forward-first migration/application compatibility contract; application rollback does not imply automatic database down migration.

Phase 11.10a established the canonical frontend trust boundary **browser → DTMO API → governed integration adapter/data contract → governed service/evidence source**. Phase 11.10b–11.10k accepted the application shell, Command Center, Unified Intelligence, IntelOwl/Cortex Analysis, OpenCTI graph, MISP Sharing & Exchange, TheHive Investigations & Cases, Vulnerability & Exposure, Sources & Collection and Automation & Playbooks while preserving server-side authority, provenance, replay protection and service-to-service credential boundaries.

Source, MISP, TheHive, analyzer, scanner and other upstream credential values remain server-side. Connectivity, enrichment, graph presence, vulnerability intelligence, case identity, transfer evidence, connector success or automation completion does not establish local compromise, publication authority, production-equivalent behavior or production authorization.

## Active Phase 11.10l Governance & Evidence security boundary

`/workbench/governance` consumes same-origin `GET /api/v1/governance/knowledge`, protected by `read:intelligence`. Governance data is assembled from repository-backed internal mappings and the explicit typed crosswalk in `backend/dtmo/governance_crosswalk.py`.

Security invariants:

- Normenkader IBP, MITRE ATT&CK and NIST CSF relationships are surfaced only where explicit typed repository mappings exist;
- the crosswalk is intentionally partial and no unrecorded framework/control/technique equivalence is inferred;
- CVSS remains scoring context and is not a compliance framework or proof of local exposure;
- a typed mapping is not certification, blanket compliance, audit acceptance or proof of environment effectiveness;
- governance visibility grants no review, case, remediation, connector, external-share, publication, administrative or production authority;
- missing or inaccessible governance evidence remains unavailable and **fails closed** rather than becoming PASS, compliant or zero risk;
- the browser receives no external framework-service credential and no privileged upstream credential;
- repository/browser fixtures are engineering evidence only.

## Threat and vulnerability management

Vulnerability findings remain provenance-bound evidence. CVSS, EPSS and KEV may inform analyst priority but cannot be transformed into unsupported claims about local asset state. A green scan does not establish absence of unknown vulnerabilities; a finding cannot be silently suppressed. Exceptions remain accountable, time-bounded and bound to exact evidence identity.

The repository-backed governance crosswalk includes an explicit Normenkader IBP `SM.07` relationship for DTMO threat/vulnerability intelligence capability. That relationship is scoped evidence support; it does not establish organizational maturity, complete control implementation, remediation completion or compliance.

## Secrets and signing identities

Raw runtime secrets, TLS private keys, MISP API keys, TheHive API tokens, connector/source secrets, scanner/upstream vulnerability credentials and long-lived signing keys do not belong in Git, frontend storage, documentation evidence or screenshots. Release signing uses short-lived workload identity; deployment credentials remain deployment-owned secrets.

## Availability, recovery and external evidence

Repository CI validates repository-controlled exact-head contracts only. It does not prove live Kubernetes behavior, live upstream completeness/health, real production-equivalent migration, upgrade, rollback, saturation, recovery, independent assurance or production authorization.

Phase 11.10p must run only after 11.10a–11.10o candidate completion and immutable freeze. It requires fresh evidence for the **same immutable candidate** covering identity, migration/compatibility, upgrade, health/readiness, representative saturation/capacity, recovery/continuity and exact-prior-digest rollback with post-rollback health. Historical Phase 8/9 evidence cannot satisfy this gate. Phase 11.11 independent assurance follows only after Phase 11.10 owner acceptance; Phase 12 is the later formal production decision.

## Data protection and privacy

Evidence, SBOMs, framework mappings and Phase 11.10 manifests must avoid credentials, raw intelligence payloads, private notes and unnecessary personal data. Technical connectivity or mapping visibility does not establish legal authority to collect, enrich, synchronize, publish, create cases or redistribute intelligence.
