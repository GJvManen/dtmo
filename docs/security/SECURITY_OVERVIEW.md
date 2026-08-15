# DTMO Security Overview

Last updated: **2026-08-15**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8 repository enhancements**

## Security objectives

DTMO protects the confidentiality, integrity, availability, provenance, accountability and controlled dissemination of cyber threat intelligence used in an education context. Security controls are designed so that source trust, identity, authorization, evidence and human decision boundaries remain visible and enforceable.

## Identity and authentication

Bearer tokens are externally issued and cryptographically validated according to the configured trust model. DTMO does not silently mint or rewrite active external token claims from managed local principal state.

Production identity requirements include approved issuer/audience/key trust, known role/principal-type claims, token-state validation where applicable and explicit reconciliation/reissue/revocation when role state changes.

Local/reference identity helpers are development conveniences, not production identity architecture.

## Identity and access control

- Server-side RBAC is authoritative.
- Human and service-account authorities remain separated.
- Least privilege and explicit role/permission scope are enforced server-side.
- Service accounts/connectors do not receive human review/share-approval authority.
- Auditor/read-only paths remain non-mutating.
- Privileged Administration actions require appropriate human authority.
- Administrator self-management and final-active-admin safeguards prevent lockout/escalation failure modes.
- Client-supplied role or identity values do not establish privilege.

## Separation of duties and publication authority

Technical success is not dissemination authority. Source execution, analysis, review, external-share approval, Administration, security/CISO authority and audit access remain distinct responsibilities.

Connectors, CI, dashboards, analytics, Administration, Governance, staging access and infrastructure administration do **not** automatically authorize external sharing or publication.

## Source and ingestion security

Source execution is fail-closed around approved profiles, endpoints, normalization semantics, provenance and source restrictions. Credentialed integrations use logical secret references; raw API keys, passwords or bearer tokens are not stored as repository/catalog evidence.

The E8 source ecosystem includes OpenCVE, CIRCL Vulnerability-Lookup, governed MISP read and separately governed outbound export, and governed AIL read/enrichment/correlation. MISP sharing remains constrained by human approval and source/distribution semantics. AIL access does not grant autonomous crawler or mutation authority.

Canonical ingestion preserves raw evidence/source context and requires durable canonical persistence before successful application-level ingestion is reported.

## Vulnerability intelligence security semantics

DTMO supports governed vulnerability context including CVE, vendor/product, CWE, CVSS, EPSS, KEV and sighting evidence where sources support those fields. These signals inform prioritization and analysis but do not by themselves prove local exposure, exploitability, compromise or remediation completion.

Explainable prioritization must retain input provenance and semantic boundaries rather than collapse external signals into unsupported certainty.

## Data protection and privacy

- Collect and retain only data needed for the defined intelligence purpose.
- Preserve source provenance and confidence/context.
- Avoid unnecessary personal data in logs and retained evidence.
- Do not commit secret values, credentials or bearer tokens.
- Minimize evidence artifacts and restrict sensitive references.
- Staging data must use an approved synthetic/sanitized/representative approach unless explicitly authorized otherwise.

## Persistence and integrity

Security-relevant data responsibilities are explicit:

- PostgreSQL — canonical application/RBAC/intelligence/mapping state;
- OpenSearch — supporting search/index representation;
- S3-compatible object storage — raw evidence;
- Redis — coordination/cache/queue runtime state;
- Prometheus/Grafana — operational telemetry.

Search/index or raw-object success alone does not replace canonical PostgreSQL truth.

## Auditability and observability

Privileged/security-relevant activity is designed to retain actor/principal identity, action/resource context, request/correlation identifiers, before/after state where applicable and auditable event continuity. Operational troubleshooting must preserve correlation/provenance without copying unnecessary sensitive payloads into tickets or repository evidence.

Prometheus and separately authenticated Grafana provide operational telemetry. Monitoring access does not create intelligence-review or publication authority.

## Supply chain and CI security

- Exact-head CI is required before protected merge.
- A new commit invalidates earlier PR-head evidence for that PR.
- Open-source governance/licensing have dedicated controls.
- Dependency/container/advisory review must preserve provenance and applicability.
- Workflow configuration alone is not acceptance evidence.

DTMO is licensed under the **Apache License, Version 2.0** and maintains explicit security/contribution/licensing entry points.

## Threat and vulnerability management

Threat, CVE and vendor-advisory review must be target-specific where it supports a deployment or assurance decision. Record source/provenance, review time, affected component/version, applicability, confidence and remediation/disposition.

Phase 8 deployment-time review must be attributable to the accepted staging identity. Phase 9 assurance-time review must be independently assessed within the agreed assurance scope.

## Framework and governance claims

Framework mappings are security-relevant claims and therefore fail closed. Current controlled truth includes:

- Normenkader IBP — explicit partial DTMO control crosswalks and governed evidence relationships, including vulnerability-management evidence for `SM.07` and supporting controls;
- MITRE ATT&CK — explicit threat/detection/classification context and governed technique relationships;
- NIST CSF 2.0 — explicit DTMO control/outcome relationships;
- CVSS 4.0 — vulnerability-scoring context with explicit claim boundaries;
- DTMO internal security/release governance — repository-backed mappings.

Mappings are explicit, versioned/provenance-backed and non-inferred. A mapping does not imply complete compliance, certification, maturity, local exploitability or control effectiveness in a specific deployment unless corresponding evidence exists.

## Environment security

### Local/reference

Docker Compose provides engineering/reference evidence only. Development-only object-storage/bootstrap/admin credential compatibility patterns must not be reused as staging/production identity architecture.

### Staging

The post-E8 candidate has been externally deployed and owner-tested in an approved production-equivalent staging environment. Formal Phase 8 closure still requires complete evidence for immutable release/image/runtime identity, configuration parity, least-privilege IAM/secrets, TLS/network, controlled data handling, no-production-credential reuse, rollback/change records, deployment-time security review and the external validation covered by Phase 8.2–8.5.

### Production

Production authorization remains a Phase 10 decision after accepted Phase 8 and independent Phase 9 assurance.

## External assurance

Phase 9 independent external assurance is `NOT COMPLETE`. It must cover the accepted candidate and include agreed penetration testing, hardening/configuration, IAM/secrets, load/stress, resilience/recovery, monitoring/incident response, relevant privacy/legal/governance and vulnerability-review evidence. Findings require explicit disposition and independent retest where release-blocking.

## Non-negotiable claim boundaries

- Missing, queued, failed, skipped, cancelled, stale, inferred or inaccessible evidence is not `PASS`.
- Repository CI does not create owner, staging or independent-assurance acceptance.
- Owner-verified staging deployment does not create independent assurance or production approval.
- Technical success does not authorize publication/share.
- Raw secrets are never documentation evidence.
- Framework mappings are never inferred and never imply blanket compliance.
