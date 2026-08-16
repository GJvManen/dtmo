# DTMO Security Overview

Last updated: **2026-08-16**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## Security objectives

DTMO protects the confidentiality, integrity, availability, provenance, accountability and controlled dissemination of cyber threat intelligence used in an education context. Security controls are designed so that source trust, identity, authorization, evidence and human decision boundaries remain visible and enforceable.

DTMO is **not production authorized**. Phase 10 concluded `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11 is the active platform-industrialisation programme. Phase 11.1 and 11.2 are repository-complete. The Phase 11.3 IntelOwl contract is repository-complete and the bounded IntelOwl adapter is the active exact-head integration gate.

## Identity and authentication

Bearer tokens are externally issued and cryptographically validated according to the configured trust model. DTMO does not silently mint or rewrite active external token claims from managed local principal state.

Production identity requirements include approved issuer/audience/key trust, known role/principal-type claims, token-state validation where applicable and explicit reconciliation/reissue/revocation when role state changes.

Local/reference identity helpers are development conveniences, not production identity architecture.

External Phase 11 service integrations use dedicated non-human identities with the minimum required scope. Taranis remains read-only. The IntelOwl adapter requires a dedicated non-admin service identity, runtime-secret API token and HTTPS in production; a `403` is an authorization/configuration failure and never a reason to broaden privilege automatically.

## Identity and access control

- Server-side RBAC is authoritative.
- Human and service-account authorities remain separated.
- Least privilege and explicit role/permission scope are enforced server-side.
- Service accounts/connectors do not receive human review/share-approval authority.
- Auditor/read-only paths remain non-mutating.
- Privileged Administration actions require appropriate human authority.
- Administrator self-management and final-active-admin safeguards prevent lockout/escalation failure modes.
- Client-supplied role or identity values do not establish privilege.
- External-platform administrative/superuser authority is not required merely to support bounded DTMO integration.

## Separation of duties and publication authority

Technical success is not dissemination authority. Source execution, enrichment, analysis, review, external-share approval, Administration, security/CISO authority and audit access remain distinct responsibilities.

Connectors, CI, dashboards, analytics, Administration, Governance, staging access, infrastructure administration, Taranis publisher state and IntelOwl analyzer/job results do **not** automatically authorize external sharing or publication.

Existing DTMO human approval and governed MISP/export controls remain authoritative.

## Source and ingestion security

Source execution is fail-closed around approved profiles, endpoints, normalization semantics, provenance and source restrictions. Credentialed integrations use logical secret references; raw API keys, passwords or bearer tokens are not stored as repository/catalog evidence.

The accepted source ecosystem includes OpenCVE, CIRCL Vulnerability-Lookup, governed MISP read and separately governed outbound export, governed AIL read/enrichment/correlation and the Phase 11.2 Taranis read-only canonical integration. Taranis collection preserves stable upstream identity, provenance, handling restrictions, bounded replay/checkpoint semantics and explicit no-share authority.

Canonical ingestion preserves raw evidence/source context and requires durable canonical persistence before successful application-level ingestion is reported.

## Threat and vulnerability management

DTMO threat and vulnerability management preserves source provenance, separates external intelligence from local exposure evidence, and keeps CVE/CVSS/EPSS/KEV and enrichment signals attributable rather than treating them as proof of local compromise. Phase 11 enrichment extends this governed evidence model without weakening human review, RBAC, TLP/privacy or publication authority.

## Phase 11.3 IntelOwl enrichment security boundary

The IntelOwl service/API/security/licensing contract is accepted. The bounded adapter is implemented in the active repository slice and remains subject to exact-head acceptance. No live IntelOwl deployment, provider credential, durable enrichment-history persistence or production-equivalent behavior is claimed by this repository state.

```mermaid
flowchart LR
    C[(DTMO canonical observable)] --> P{Class + TLP/privacy + allowlist valid?}
    P -->|no| R[Review / reject submission]
    P -->|yes| I[IntelOwl API\ndedicated non-admin identity]
    I --> A[Allowlisted analyzer/playbook]
    A --> I
    I --> E[Attributed analyzer report]
    E --> V{Job ID + analyzer + size valid?}
    V -->|no| Q[Reject / quarantine fail closed]
    V -->|yes| N[DTMO enrichment normalization]
    N --> C
    I -. connectors_requested=[] .-> X[MISP / OpenCTI / Slack / Email side effects excluded]
    N -. no implicit authority .-> H[Human share/publication approval]
```

Required controls:

- only CVE, IP, domain, URL and hash are initially eligible observables;
- email and other generic personal-data observables remain disabled until explicit privacy/data-processing approval;
- analyzers/playbooks are explicitly allowlisted; newly available IntelOwl plugins are not automatically trusted;
- DTMO considers whether an analyzer sends data to an external provider before execution;
- unknown/missing TLP or handling state fails closed to review-required;
- `TLP:RED` or equivalent restricted material is not sent to external analyzers;
- bounded polling, result-size and retry behavior prevents retry storms and uncontrolled disclosure;
- IntelOwl external Connectors are excluded from the bounded enrichment path through an explicit empty connector request;
- immutable upstream job identity is verified before result acceptance;
- analyzer/job/result identity and timestamps are retained in provenance;
- analyzer verdicts such as malicious/suspicious are attributed context and are not local-compromise proof;
- malformed, oversized, unknown-analyzer or partial results remain explicit and fail closed where attribution/safety cannot be established.

## Vulnerability intelligence and enrichment semantics

DTMO supports governed vulnerability context including CVE, vendor/product, CWE, CVSS, EPSS, KEV and sighting evidence where sources support those fields. These signals inform prioritization and analysis but do not by themselves prove local exposure, exploitability, compromise or remediation completion.

IntelOwl enrichment adds another contextual evidence class. Provider/analyzer result, reliability, confidence/evaluation, DTMO relevance, local exposure evidence, severity and TLP/handling remain separate dimensions. A provider verdict must never silently become an assertion that a DTMO-managed environment is affected.

Explainable prioritization must retain input provenance and semantic boundaries rather than collapse external signals into unsupported certainty.

## Data protection and privacy

- Collect and retain only data needed for the defined intelligence purpose.
- Preserve source and enrichment provenance and confidence/context.
- Avoid unnecessary personal data in logs and retained evidence.
- Do not commit secret values, credentials or bearer tokens.
- Minimize evidence artifacts and restrict sensitive references.
- Staging data must use an approved synthetic/sanitized/representative approach unless explicitly authorized otherwise.
- Treat external enrichment as a potential disclosure of the observable to a provider.
- Do not enable email/generic personal-data enrichment until lawful purpose, data-processing basis, provider/transfer implications and retention have been explicitly reviewed.

## Persistence and integrity

Security-relevant data responsibilities are explicit:

- PostgreSQL — canonical application/RBAC/intelligence/mapping state;
- OpenSearch — supporting search/index representation;
- S3-compatible object storage — raw evidence;
- Redis — coordination/cache/queue runtime state;
- Prometheus/Grafana — operational telemetry.

Search/index, raw-object or external enrichment success alone does not replace canonical PostgreSQL truth. The current adapter slice does not yet claim durable enrichment-history persistence; that remains the next bounded Phase 11.3 integration step.

## Auditability and observability

Privileged/security-relevant activity is designed to retain actor/principal identity, action/resource context, request/correlation identifiers, before/after state where applicable and auditable event continuity. Operational troubleshooting must preserve correlation/provenance without copying unnecessary sensitive payloads into tickets or repository evidence.

Phase 11 enrichment observability must identify dependency, job/correlation context and outcome without logging API tokens, provider credentials or unnecessary observable payloads.

Prometheus and separately authenticated Grafana provide operational telemetry. Monitoring access does not create intelligence-review or publication authority.

## Supply chain and licensing security

- Exact-head CI is required before protected merge.
- A new commit invalidates earlier PR-head evidence for that PR.
- Open-source governance/licensing have dedicated controls.
- Dependency/container/advisory review must preserve provenance and applicability.
- Workflow configuration alone is not acceptance evidence.
- Service-to-service integration is preferred where it preserves licensing and trust boundaries.

DTMO is licensed under the **Apache License, Version 2.0** and maintains explicit security/contribution/licensing entry points. IntelOwl and pyIntelOwl remain separate AGPL-3.0 services; source vendoring, embedding, modification or redistribution is not authorized by this adapter slice and requires explicit licensing review.
