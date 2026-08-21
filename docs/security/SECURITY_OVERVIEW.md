# DTMO Security Overview

Last updated: **2026-08-21**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## Security objectives

DTMO protects confidentiality, integrity, availability, provenance, accountability and controlled dissemination of cyber threat intelligence. Source trust, identity, authorization, evidence and human decision boundaries remain explicit and enforceable.

DTMO is **not production authorized**. Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**; Phase 11 is `IN PROGRESS / ACTIVE`. Phase 11.1–11.9 and Phase 11.10a–11.10h are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 remains **`IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`**; the active bounded gate is **Phase 11.10i Vulnerability & Exposure Center**, `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 11.10j, Phase 11.10p, Phase 11.11 and Phase 12 are `NOT STARTED`.

## Identity and access control

- **Server-side RBAC remains authoritative.**
- Human and service identities remain separate.
- `read:intelligence` controls intelligence discovery, canonical object reading, analysis history/capability reads, OpenCTI graph/entity reads, MISP sharing-state reads, TheHive investigation-state reads and the vulnerability analytics projection consumed by the Exposure workspace.
- `review:intelligence` controls explicit intelligence review and remains distinct from external sharing approval.
- `approve:share` controls human external sharing approval and requires a different human principal than the recorded reviewer.
- `handoff:case` controls explicit human TheHive case mutation and remains distinct from `approve:share`.
- Service accounts cannot perform human review/share approval or human case handoff.
- Connectors, analyzers, graph clients, CI identities, Kubernetes service accounts, frontend controls and integrated platforms do not receive human publication/share or case-handoff authority.
- Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate service/API/licensing/provider boundaries.
- Enrichment, graph, exchange, case, vulnerability, build, deployment or evidence state does not establish DTMO-local exposure, exploitability or compromise.
- Missing, conflicting or unverifiable mandatory evidence must **fail closed**.

## Separation of duties

Human review, publication/share approval, case handoff, analyzer execution, graph/context reading, vulnerability prioritization, CI build identity, deployment, validation review, release signing and production authorization remain distinct authority domains. A connector, analyzer, graph node, vulnerability record, Kubernetes workload, browser control, CI job, signed artifact or evidence validator cannot self-grant analyst approval or production authority.

## Accepted Phase 11 security baseline

Phase 11.8 accepted repository controls cover immutable runtime image identity, non-root/read-only workloads, workload identity, external secret delivery, ingress/TLS and network segmentation, HA/disruption controls, opt-in observability, recovery, software supply-chain hardening, capacity/resource planning and upgrade/rollback. The supply-chain baseline includes CycloneDX SBOMs, vulnerability evidence, minimal runtime surface, SHA-256 artifact identity and short-lived/OIDC signing patterns.

Phase 11.9 accepted the forward-first migration/application compatibility contract. Destructive changes require expand/migrate/contract; application rollback does not imply automatic database down migration.

Phase 11.10a accepted the frontend trust boundary **browser → DTMO API → governed integration adapter → upstream service**. Upstream service credentials do not become ordinary browser credentials. Role-aware presentation is not authorization.

Phase 11.10b accepted the separately built React/TypeScript/Vite `/workbench/` shell with committed dependency lockfile consumed by `npm ci`, build-stage-only Node/npm, strict same-origin CSP, immutable hashed assets, traversal-safe serving, responsive keyboard navigation, context rail and `/ui/console` as a migration **compatibility path**.

Phase 11.10c–11.10h accepted Command Center, Unified Intelligence, Integrated Analysis, OpenCTI graph/entity, human-governed MISP Sharing & Exchange and TheHive Investigations & Cases while preserving server-side authority, provenance and fail-closed evidence semantics.

These are repository engineering controls and do not prove provider enforcement, live availability, successful recovery, production-equivalent operation or production authorization.

## Active Phase 11.10i Vulnerability & Exposure security boundary

The Exposure workspace is governed by same-origin DTMO APIs. UI state does not create authorization and the browser never receives scanner credentials or upstream vulnerability-service credentials.

Security invariants:

- canonical vulnerability analytics reads remain server-authorized through `read:intelligence`;
- `/workbench/exposure` consumes the DTMO vulnerability analytics projection and does not create a parallel browser-side authority path or datastore;
- CVSS, EPSS, CISA KEV, CWE and vendor/product mappings are prioritization evidence only;
- vulnerability intelligence presence does not prove that a local asset is affected, exposed, exploitable or compromised;
- absence of a vulnerability record does not prove safety or absence of exposure;
- raw-evidence references retain integrity/provenance semantics where available;
- missing, malformed, inaccessible or degraded evidence remains explicit and **fails closed**;
- no remediation, scanner execution, publication/share or case-creation authority is introduced by this read-only workspace;
- configuration and source registration are not promoted to live vulnerability-source health;
- browser and repository fixtures remain engineering evidence only.

The dedicated Phase 11 Vulnerability Exposure Workspace Gate may prove exact-head repository/frontend contracts and fail-closed UI behavior. It **does not prove** live vulnerability-provider health, asset inventory completeness, local exposure, exploitability, compromise, remediation, production-equivalent operation, independent assurance or production authorization.

## Accepted TheHive and MISP authority boundaries

Phase 11.10h TheHive Investigations & Cases is `PASS / REPOSITORY_COMPLETE`. Canonical investigation reads require `read:intelligence`; case mutation remains a separate explicit human `handoff:case` action. TheHive token and organization context remain server-side; ambiguous handoff evidence requires manual reconciliation.

Phase 11.10g MISP Sharing & Exchange preserves `read:intelligence`, `review:intelligence` and separate human `approve:share`; authoritative handling restrictions and deterministic replay protections remain binding. Exported MISP events remain `published=false` and no Publish or Synchronize authority is exposed.

## Threat and vulnerability management

Vulnerability findings remain provenance-bound evidence. A green scan does not establish absence of unknown vulnerabilities; a governed finding cannot be silently suppressed. Exceptions must remain accountable, time-bounded and bound to the exact artifact/finding identity.

Phase 11.10i extends the user-facing prioritization surface, not the underlying authority model. CVSS severity, EPSS probability and KEV listing status can inform analyst priority but cannot be transformed into an unsupported claim about local asset state.

Frontend production dependency audit, container/package SBOMs and vulnerability controls remain regression gates during 11.10i. They do not establish vulnerability absence or production readiness.

## Secrets and signing identities

Raw runtime secrets, TLS private keys, MISP API keys, TheHive API tokens, scanner/upstream vulnerability-service credentials and long-lived signing keys do not belong in Git, Helm values, frontend storage, documentation evidence or screenshots. Release signing uses short-lived workload identity. Registry/deployment credentials remain deployment-owned secrets.

## Availability, capacity and recovery

Phase 11.8 HA, observability, capacity and recovery repository boundaries remain accepted. Real production-equivalent evidence remains deferred to 11.10p after 11.10o candidate completion and immutable freeze.

11.10p must provide fresh evidence for candidate identity, migration/compatibility, upgrade, health/readiness, representative saturation/capacity, recovery/continuity and rollback to the **exact prior immutable** application digest plus **post-rollback health**. Application rollback does not authorize **automatic database down migration**.

Every evidence item must identify the **same immutable** candidate and approved production-equivalent environment. Historical Phase 8 `PASS / OWNER_ACCEPTED` and Phase 9 `PASS / EXTERNAL_ASSURANCE_ACCEPTED` remain prior-candidate history and cannot satisfy the new candidate. Missing, inaccessible, placeholder, historical-only or mixed-candidate evidence must **fail closed**.

## Data protection and privacy

Artifact metadata, SBOMs, vulnerability evidence and Phase 11.10 manifests must avoid credentials, raw intelligence payloads, private notes and unnecessary personal data. Technical connectivity or evidence validation does not itself establish legal authority to collect, enrich, synchronize, publish, create cases or redistribute intelligence.

## Evidence boundary

Repository CI can prove repository-controlled contracts and exact-head outputs only. It cannot prove live Kubernetes behavior, live upstream completeness or health, real production-equivalent migration, upgrade, rollback, saturation, recovery, independent assurance or production authorization. Phase 11.11 remains `NOT STARTED` until Phase 11.10 is explicitly accepted; Phase 12 remains `NOT STARTED` until fresh assurance is accepted for the same candidate.
