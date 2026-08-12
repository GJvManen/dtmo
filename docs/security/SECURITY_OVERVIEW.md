# DTMO Security Overview

Last updated: **2026-08-12**  
Baseline: **16.0.0rc12 / RC13 accepted**

## Security objectives

DTMO protects the confidentiality, integrity, availability, provenance, accountability and controlled dissemination of cyber threat intelligence used in an education context.

The security model assumes that threat-intelligence processing is useful only when source trust, identity, authorization and human decision boundaries remain visible and enforceable.

## Identity and authentication

Production bearer tokens are externally issued and cryptographically validated against the configured trust model. DTMO does not use managed local principal state to silently mint or rewrite active production token claims.

Production identity requirements include:

- approved issuer/audience/key trust;
- known role/principal-type claims;
- token-state validation where applicable;
- explicit reconciliation/token reissue or revocation when production role state changes.

Local/reference identity helpers are development conveniences and are not the production identity architecture.

## Authorization and least privilege

- Server-side RBAC is authoritative.
- Built-in role/permission boundaries are code-controlled.
- Human and service-account authorities remain separated.
- Service accounts/connectors do not receive human review/share-approval powers.
- Auditor/read-only paths remain non-mutating.
- Privileged Administration actions require appropriate human authority.
- Administrator self-management and final-active-admin safeguards prevent common lockout/escalation failure modes.

## Separation of duties and publication authority

Technical success is not dissemination authority.

The platform maintains separation between:

- source administration/execution;
- intelligence analysis;
- review;
- external-share approval;
- principal/role administration;
- security/CISO authority;
- audit/read-only access.

Connectors, CI, dashboards, Analytics, Administration, Governance, staging access and infrastructure administration do **not** automatically authorize external sharing or publication.

## Source and ingestion security

Source execution is fail-closed around supported profiles, endpoints, normalization types and provenance expectations.

Credentialed integrations use logical secret references. Raw API keys/passwords/tokens are not stored as source-catalog or repository evidence.

Canonical ingestion preserves raw evidence and source context while requiring durable canonical database persistence before successful application-level ingestion is reported.

## Data protection and privacy

- Collect and retain only data needed for the defined intelligence purpose.
- Preserve source provenance and confidence/context.
- Avoid unnecessary personal data in logs and retained evidence.
- Do not commit secret values, credentials or bearer tokens.
- Evidence artifacts must be minimized and privacy-safe.
- Staging data must use an approved synthetic/sanitized/representative approach unless explicitly authorized otherwise.

## Persistence and integrity

Security-relevant data responsibilities are explicit:

- PostgreSQL — canonical application/RBAC/intelligence state;
- OpenSearch — supporting search/index representation;
- S3-compatible object storage — raw evidence;
- Redis — coordination/cache/queue runtime state;
- Prometheus/Grafana — operational telemetry.

Search/index or raw-object success alone does not replace canonical PostgreSQL truth.

## Auditability

Privileged state changes are designed to retain:

- actor/principal identity;
- action/resource context;
- request/correlation identifier;
- before/after state where applicable;
- tamper-evident audit-chain properties.

Operational troubleshooting should preserve correlation and provenance without copying unnecessary raw sensitive payloads into tickets or repository evidence.

## Supply chain and CI security

- Exact-head GitHub Actions evidence is required before protected merge.
- A new commit invalidates earlier PR-head CI evidence.
- Open-source governance and licensing have dedicated controls.
- Dependency/container/advisory review must preserve provenance and applicability.
- Workflow configuration alone is not acceptance evidence.

DTMO is licensed under the **Apache License, Version 2.0** and maintains explicit security/contribution/licensing entry points.

## Threat and vulnerability management

Applicable public threat intelligence, CVEs and vendor advisories are reviewed against bounded objectives and target identities.

Deployment-time Phase 8/9 security review must be tied to the actual immutable target deployment and record:

- source/provenance;
- review time;
- affected component/version;
- applicability;
- confidence;
- disposition/remediation decision.

## Framework and governance claims

Framework mappings are security-relevant claims and therefore fail closed.

Current truth:

- Normenkader IBP — first-class control crosswalk `UNMAPPED`;
- MITRE ATT&CK — first-class technique crosswalk `UNMAPPED`;
- CVSS — `CONTEXT_ONLY`;
- internal DTMO governance mappings — repository-backed.

Future mappings require explicit framework/version, identifier, provenance, confidence/status and review state. Semantic similarity or free-text tagging does not establish equivalence.

## Environment security

### Local/reference

Docker Compose provides engineering/reference evidence only. A development-only object-storage bootstrap/admin credential compatibility mapping may exist locally and must not be reused as the staging/production identity model.

### Staging

Phase 8 requires:

- separate least-privilege application identities;
- approved secret-management references;
- TLS/network restrictions;
- immutable release/image identity;
- configuration parity;
- controlled data handling;
- no production credentials;
- rollback/change evidence;
- deployment-time security review.

### Production

Production authorization is a Phase 10 decision after accepted Phase 8 and independent Phase 9 assurance.

## External assurance

Independent Phase 9 assurance is still required. It must be target-specific, attributable and dated. Findings require explicit disposition and, where applicable, retest evidence.

## Incident and operations security

Accepted engineering evidence exists for observability, trace context, alerting, dashboards, runbooks and operational exercises. Production operation still requires environment-specific ownership, access, notification and escalation acceptance.

## Non-negotiable claim boundaries

- Missing, queued, failed, skipped, cancelled, stale, inferred or inaccessible evidence is not `PASS`.
- Repository CI does not create owner, staging or independent-assurance acceptance.
- Technical success does not authorize publication/share.
- Raw secrets are never documentation evidence.
- Framework mappings are never inferred.
