# DTMO Security Overview

Last updated: 2026-08-10

## Security objectives

DTMO protects confidentiality, integrity, availability, provenance, accountability and controlled dissemination of cyber threat intelligence used in an education context.

## Identity and access control

- Role-based access control and least privilege are mandatory.
- Review and human share approval are separate authorities.
- The same technical success path cannot silently grant dissemination authority.
- Service accounts and connectors do not receive human review/share-approval powers.
- Auditor/read-only roles are constrained to non-mutating behavior.

## Separation of duties

Actions that materially change trust or dissemination state require distinct authority where defined by policy. Technical environment access, deployment access, CI access or operational access does not imply publication/share approval.

## Data protection and privacy

- Collect and retain only data needed for the defined intelligence purpose.
- Preserve source provenance and confidence.
- Avoid unnecessary personal data in logs and retained evidence.
- Do not commit secret values, credentials or tokens.
- Synthetic sensitive markers are used where leakage checks are required.

## Application security

Security controls include authenticated/authorized API behavior, secure session/token handling, security response headers, explicit production-mode validation, fail-closed connector behavior where appropriate and auditable state transitions.

## Supply-chain and CI security

- Exact-head GitHub Actions evidence is required for repository acceptance.
- Open-source governance and licensing have dedicated controls.
- Dependency and advisory review must preserve provenance and applicability.
- A successful workflow definition without executed evidence is not accepted as PASS.

## Threat and vulnerability management

Threat intelligence, CVE information and vendor advisories are reviewed when relevant to a bounded objective. Deployment-time review for Phase 8/9 must be tied to the actual immutable staged or production target and record source provenance, time, applicability and confidence.

## Logging and auditability

Logs and evidence should support correlation without exposing raw sensitive payloads. Request correlation, trace context, connector state, alerting and operational events are designed to be reviewable.

## Environment security

Repository emulator/runtime evidence does not establish production security. Real staging/production acceptance must demonstrate approved identities/secrets, TLS/network restrictions, platform hardening, immutable deployment identity, rollback/recovery and change control.

## External assurance

Independent penetration testing and other Phase 9 assurance evidence must be attributable, dated and target-specific. Findings require explicit disposition and, where applicable, retest evidence.

## Incident operations

Operational runbooks, alerting, dashboards, controlled exercises and on-call handover are part of the accepted Phase 7 evidence. Organizational staffing and real delivery-channel acceptance remain environment/operations responsibilities.

## Non-negotiable claim boundary

No missing, failed, skipped, cancelled, stale, inferred or inaccessible evidence is treated as PASS. No technical success automatically authorizes sharing or publication.
