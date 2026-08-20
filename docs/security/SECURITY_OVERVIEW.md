# DTMO Security Overview

Last updated: **2026-08-20**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## Security objectives

DTMO protects confidentiality, integrity, availability, provenance, accountability and controlled dissemination of cyber threat intelligence. Source trust, identity, authorization, evidence and human decision boundaries remain explicit and enforceable.

DTMO is **not production authorized**. Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**; Phase 11 is `IN PROGRESS / ACTIVE`. Phase 11.1–11.9 and Phase 11.10a–11.10g are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 remains **`IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`**; the active bounded gate is **Phase 11.10h TheHive Investigations & Cases**, `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 11.10i, Phase 11.10p, Phase 11.11 and Phase 12 are `NOT STARTED`.

## Identity and access control

- **Server-side RBAC remains authoritative.**
- Human and service identities remain separate.
- `read:intelligence` controls intelligence discovery, canonical object reading, analysis history/capability reads, OpenCTI graph/entity reads, MISP sharing-state reads and TheHive investigation-state reads.
- `review:intelligence` controls explicit intelligence review and remains distinct from external sharing approval.
- `approve:share` controls human external sharing approval and requires a different human principal than the recorded reviewer.
- `handoff:case` controls explicit human TheHive case mutation and remains distinct from `approve:share`.
- Service accounts cannot perform human review/share approval or human case handoff.
- Connectors, analyzers, graph clients, CI identities, Kubernetes service accounts, frontend controls and integrated platforms do not receive human publication/share or case-handoff authority.
- Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate service/API/licensing/provider boundaries.
- Enrichment, graph, exchange, case, build, deployment or evidence state does not establish DTMO-local exposure, exploitability or compromise.
- Missing, conflicting or unverifiable mandatory evidence must **fail closed**.

## Separation of duties

Human review, publication/share approval, case handoff, analyzer execution, graph/context reading, CI build identity, deployment, validation review, release signing and production authorization remain distinct authority domains. A connector, analyzer, graph node, Kubernetes workload, browser control, CI job, signed artifact or evidence validator cannot self-grant analyst approval or production authority.

## Accepted Phase 11 security baseline

Phase 11.8 accepted repository controls cover immutable runtime image identity, non-root/read-only workloads, workload identity, external secret delivery, ingress/TLS and network segmentation, HA/disruption controls, opt-in observability, recovery, software supply-chain hardening, capacity/resource planning and upgrade/rollback. The supply-chain baseline includes CycloneDX SBOMs, vulnerability evidence, minimal runtime surface, SHA-256 artifact identity and short-lived/OIDC signing patterns.

Phase 11.9 accepted the forward-first migration/application compatibility contract. Destructive changes require expand/migrate/contract; application rollback does not imply automatic database down migration.

Phase 11.10a accepted the frontend trust boundary **browser → DTMO API → governed integration adapter → upstream service**. Upstream service credentials do not become ordinary browser credentials. Role-aware presentation is not authorization.

Phase 11.10b accepted the separately built React/TypeScript/Vite `/workbench/` shell with committed dependency lockfile consumed by `npm ci`, build-stage-only Node/npm, strict same-origin CSP, immutable hashed assets, traversal-safe serving, responsive keyboard navigation, context rail and `/ui/console` as a migration **compatibility path**.

Phase 11.10c accepted the read-only canonical Command Center with fail-closed canonical metrics and explicit separation between configuration and runtime observation. Phase 11.10d accepted read-only Unified Intelligence where search projections remain distinct from canonical detail/provenance. Phase 11.10e accepted human-triggered IntelOwl/Cortex analysis with durable evidence, server-side execution authorization and no-compromise/no-share-authority invariants. Phase 11.10f accepted read-only OpenCTI graph/entity context over persisted mappings/revisions without inferring generic upstream relationship topology. Phase 11.10g accepted human-governed MISP Sharing & Exchange with separate review/share approval, authoritative handling restrictions, replay protection and `published=false` export only.

These are repository engineering controls and do not prove provider enforcement, live availability, successful recovery, production-equivalent operation or production authorization.

## Active Phase 11.10h TheHive Investigations & Cases security boundary

The Investigations workspace is governed by same-origin DTMO APIs. UI state does not create authorization and the browser never receives TheHive credentials or organization authorization.

Security invariants:

- canonical investigation-state reads require `read:intelligence`;
- case mutation remains a separate explicit human `handoff:case` action;
- service accounts cannot authorize TheHive case handoff;
- canonical provenance is required before mutation;
- TLP/PAP mappings fail closed;
- authoritative source handling restrictions cannot be broadened and authoritative MISP distribution/sharing-group restrictions require a deployment-approved TheHive access mapping;
- TheHive token and `X-Organisation` context remain server-side only;
- durable reservation precedes the external mutation;
- `reserved` and `ambiguous` handoff evidence requires manual reconciliation rather than blind UI replay;
- delivered handoff evidence proves only the stable case identity returned at creation time;
- alerts, tasks, case timeline, later upstream case state and responder results are not inferred because the accepted Phase 11.6 persistence/readback boundary does not contain them;
- case handoff grants no external-share/publication authority and no responder/autonomous incident-response authority;
- configuration is not promoted to live TheHive health;
- handoff/case identity does not prove downstream remediation or local compromise;
- repository/browser mocks remain engineering evidence only.

The dedicated Phase 11 TheHive Investigations Workspace Gate may prove exact-head repository/API/browser contracts, server-side authority separation, handling/reconciliation semantics and fail-closed UI behavior. It **does not prove** live TheHive health, licensing entitlement, production credentials/RBAC, organization membership, upstream case completeness, responder execution, production-equivalent operation, independent assurance or production authorization.

## Accepted Phase 11.10g MISP security boundary

The accepted MISP workspace preserves `read:intelligence`, `review:intelligence` and separate human `approve:share`; MISP-origin handling restrictions and deterministic replay protections remain binding. Exported MISP events remain `published=false` and no Publish or Synchronize authority is exposed. Configuration is not live MISP health and technical transfer is not evidence of downstream consumption or local compromise.

## Threat and vulnerability management

Vulnerability findings remain provenance-bound evidence. A green scan does not establish absence of unknown vulnerabilities; a governed finding cannot be silently suppressed. Exceptions must remain accountable, time-bounded and bound to the exact artifact/finding identity.

Frontend production dependency audit, container/package SBOMs and vulnerability controls remain regression gates during 11.10h. They do not establish vulnerability absence or production readiness.

## Secrets and signing identities

Raw runtime secrets, TLS private keys, MISP API keys, TheHive API tokens and long-lived signing keys do not belong in Git, Helm values, frontend storage, documentation evidence or screenshots. Release signing uses short-lived workload identity. Registry/deployment credentials remain deployment-owned secrets.

## Availability, capacity and recovery

Phase 11.8 HA, observability, capacity and recovery repository boundaries remain accepted. Real production-equivalent evidence remains deferred to 11.10p after 11.10o candidate completion and immutable freeze.

11.10p must provide fresh evidence for candidate identity, migration/compatibility, upgrade, health/readiness, representative saturation/capacity, recovery/continuity and rollback to the **exact prior immutable** application digest plus **post-rollback health**. Application rollback does not authorize **automatic database down migration**.

Every evidence item must identify the **same immutable** candidate and approved production-equivalent environment. Historical Phase 8 `PASS / OWNER_ACCEPTED` and Phase 9 `PASS / EXTERNAL_ASSURANCE_ACCEPTED` remain prior-candidate history and cannot satisfy the new candidate. Missing, inaccessible, placeholder, historical-only or mixed-candidate evidence must **fail closed**.

## Data protection and privacy

Artifact metadata, SBOMs, vulnerability evidence and Phase 11.10 manifests must avoid credentials, raw intelligence payloads, private notes and unnecessary personal data. Technical connectivity or evidence validation does not itself establish legal authority to collect, enrich, synchronize, publish, create cases or redistribute intelligence.

## Evidence boundary

Repository CI can prove repository-controlled contracts and exact-head outputs only. It cannot prove live Kubernetes behavior, live upstream completeness or health, real production-equivalent migration, upgrade, rollback, saturation, recovery, independent assurance or production authorization. Phase 11.11 remains `NOT STARTED` until Phase 11.10 is explicitly accepted; Phase 12 remains `NOT STARTED` until fresh assurance is accepted for the same candidate.
