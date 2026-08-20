# DTMO Security Overview

Last updated: **2026-08-20**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## Security objectives

DTMO protects confidentiality, integrity, availability, provenance, accountability and controlled dissemination of cyber threat intelligence. Source trust, identity, authorization, evidence and human decision boundaries remain explicit and enforceable.

DTMO is **not production authorized**. Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**; Phase 11 is `IN PROGRESS / ACTIVE`. Phase 11.1–11.9, Phase 11.10a and Phase 11.10b are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 remains **`IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`**; the active bounded gate is **Phase 11.10c Command Center**, `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 11.10d, Phase 11.11 and Phase 12 are `NOT STARTED`.

## Identity and access control

- **Server-side RBAC remains authoritative.**
- Human and service identities remain separate.
- `handoff:case` remains distinct from `approve:share`.
- Connectors, CI identities, Kubernetes service accounts, frontend controls and integrated platforms do not receive human publication/share or case-handoff authority.
- Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate service/API/licensing/provider boundaries.
- Enrichment, graph, exchange, case, build, deployment or evidence state does not establish DTMO-local exposure, exploitability or compromise.
- Missing, conflicting or unverifiable mandatory evidence must **fail closed**.

## Separation of duties

Human publication/share approval, case handoff, service execution, CI build identity, deployment, validation review, release signing and production authorization remain distinct authority domains. A connector, analyzer, Kubernetes workload, browser control, CI job, signed artifact or evidence validator cannot self-grant analyst approval or production authority.

## Accepted Phase 11 security baseline

Phase 11.8 accepted repository controls cover immutable runtime image identity, non-root/read-only workloads, workload identity, external secret delivery, ingress/TLS and network segmentation, HA/disruption controls, opt-in observability, recovery, software supply-chain hardening, capacity/resource planning and upgrade/rollback. The supply-chain baseline includes CycloneDX SBOMs, vulnerability evidence, minimal runtime surface, SHA-256 artifact identity and short-lived/OIDC signing patterns.

Phase 11.9 accepted the forward-first migration/application compatibility contract. Destructive changes require expand/migrate/contract; application rollback does not imply automatic database down migration.

Phase 11.10a accepted the frontend trust boundary **browser → DTMO API → governed integration adapter → upstream service**. Upstream service credentials do not become ordinary browser credentials. Role-aware presentation is not authorization.

Phase 11.10b accepted the separately built React/TypeScript/Vite `/workbench/` shell with committed dependency lockfile consumed by `npm ci`, build-stage-only Node/npm, strict same-origin CSP, immutable hashed assets, traversal-safe serving, responsive keyboard navigation, context rail and `/ui/console` as a migration **compatibility path**.

These are repository engineering controls and do not prove provider enforcement, live availability, successful recovery, production-equivalent operation or production authorization.

## Active Phase 11.10c Command Center security boundary

The Command Center is a **read-only** canonical projection. `/api/v1/command-center` requires `READ_INTELLIGENCE` and does not grant review, share, case, connector, analysis or administrative mutation authority.

Security invariants:

- metrics are derived from canonical DTMO persistence rather than hard-coded operational values;
- if canonical persistence cannot be observed, metric values remain `null` and the UI reports `unavailable` instead of synthesizing zero activity;
- Taranis, IntelOwl, OpenCTI, MISP, TheHive and Cortex configuration is separated from runtime observation;
- a feature flag or API base never produces a general `healthy` claim;
- persisted execution may be shown only as attributable observation and does not become a general upstream-health claim;
- role-aware quick-action visibility is convenience only and never replaces server-side authorization;
- no upstream secret, bearer token, private key or human approval authority is stored as ordinary frontend state;
- browser requests remain same-origin DTMO API calls rather than direct privileged service calls;
- UI error/degraded states must not fabricate intelligence, workload, integration health or compromise;
- repository/browser mocks remain engineering evidence only.

The dedicated Phase 11 Command Center Gate may prove exact-head repository read-model behavior, typecheck/build, fail-closed browser rendering and role-aware visibility. It **does not prove** live upstream integration health, production-equivalent operation, independent assurance or production authorization.

## Threat and vulnerability management

Vulnerability findings remain provenance-bound evidence. A green scan does not establish absence of unknown vulnerabilities; a governed finding cannot be silently suppressed. Exceptions must remain accountable, time-bounded and bound to the exact artifact/finding identity.

Frontend production dependency audit, container/package SBOMs and vulnerability controls remain regression gates during 11.10c. They do not establish vulnerability absence or production readiness.

## Secrets and signing identities

Raw runtime secrets, TLS private keys and long-lived signing keys do not belong in Git, Helm values, frontend storage, documentation evidence or screenshots. Release signing uses short-lived workload identity. Registry/deployment credentials remain deployment-owned secrets.

## Availability, capacity and recovery

Phase 11.8 HA, observability, capacity and recovery repository boundaries remain accepted. Real production-equivalent evidence remains deferred to 11.10p after 11.10o candidate completion and immutable freeze.

11.10p must provide fresh evidence for candidate identity, migration/compatibility, upgrade, health/readiness, representative saturation/capacity, recovery/continuity and rollback to the **exact prior immutable** application digest plus **post-rollback health**. Application rollback does not authorize **automatic database down migration**.

Every evidence item must identify the **same immutable** candidate and approved production-equivalent environment. Historical Phase 8 `PASS / OWNER_ACCEPTED` and Phase 9 `PASS / EXTERNAL_ASSURANCE_ACCEPTED` remain prior-candidate history and cannot satisfy the new candidate. Missing, inaccessible, placeholder, historical-only or mixed-candidate evidence must fail closed.

## Data protection and privacy

Artifact metadata, SBOMs, vulnerability evidence and Phase 11.10 manifests must avoid credentials, raw intelligence payloads, private notes and unnecessary personal data. Technical connectivity or evidence validation does not itself establish legal authority to collect, enrich, synchronize, publish or redistribute intelligence.

## Evidence boundary

Repository CI can prove repository-controlled contracts and exact-head outputs only. It cannot prove live Kubernetes behavior, real production-equivalent migration, upgrade, rollback, saturation, recovery, independent assurance or production authorization. Phase 11.11 remains `NOT STARTED` until Phase 11.10 is explicitly accepted; Phase 12 remains `NOT STARTED` until fresh assurance is accepted for the same candidate.
