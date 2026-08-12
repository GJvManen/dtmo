# DTMO Operations Manual

Last updated: **2026-08-12**  
Baseline: **16.0.0rc12 / RC13 accepted**

## Purpose

This manual describes the durable operational control model for DTMO. Component-specific procedures and commands remain in the relevant runbooks and repository configuration.

Operational incident chronology belongs in tickets/run evidence rather than this manual.

## Daily operational checks

Operators should verify:

- application health/readiness;
- PostgreSQL, OpenSearch, Redis and object-storage health;
- connector/source state and freshness;
- queue/backlog condition;
- recent alert state;
- search/storage integrity signals;
- scheduled source activity;
- relevant operational dashboards;
- unresolved incident/change items.

Operational review must preserve privacy: do not copy raw sensitive payloads, tokens or credentials into tickets/chat/repository evidence unless explicitly required and approved.

## Access and authority

Operational access is role-based and least privilege.

Technical access does not grant:

- intelligence review authority;
- external-share approval;
- publication authority;
- human administrator authority to service accounts.

Review and external-share approval remain separate human decisions.

## Connector and source operations

Connector/source failures are handled using the accepted controls for:

- state;
- retry/backoff;
- timeout;
- replay;
- freshness;
- failure isolation;
- normalization/provenance;
- canonical persistence.

Troubleshooting should preserve source/provider provenance, timestamps, correlation identifiers and confidence/context.

A search-index write or raw-object write is not by itself proof of canonical application persistence; durable canonical state is PostgreSQL-backed.

## Monitoring and alerting

DTMO has repository-controlled engineering evidence for:

- request observability;
- distributed trace context;
- queue backlog;
- connector failures;
- storage integrity;
- API errors;
- search health;
- operational dashboards;
- runbook-linked response behavior.

Real environment notification/delivery integrations must be separately accepted where required.

## Incident handling

1. Confirm the alert/incident and affected scope.
2. Preserve correlation identifiers and privacy-safe evidence.
3. Determine affected confidentiality, integrity, availability, provenance and dissemination controls.
4. Contain without weakening RBAC or approval boundaries.
5. Recover using approved procedures.
6. Validate service health and canonical data integrity.
7. Validate that search/index and raw evidence are consistent with canonical state where relevant.
8. Record timeline, decisions, actions and residual risk in the operational evidence system.
9. Escalate according to accountable ownership and runbooks.

## Backup and recovery

Repository-controlled recovery evidence establishes engineering confidence across the relevant persistence components.

Production-equivalent acceptance additionally requires environment-specific backup/restore evidence with:

- immutable target identity;
- recovery procedure/version;
- measured outcomes;
- integrity validation;
- accountable sign-off.

## Change and release management

Every deployable candidate must have an immutable identity. Changes must be traceable to reviewed source, complete required exact-head CI and an approved target environment.

A new commit invalidates earlier PR-head CI evidence for that PR.

Production release must not proceed while blocking Phase 8/9/10 gates remain incomplete.

## Phase 8 staging operations

Phase 8 is ready to begin and requires one real approved production-equivalent staging deployment.

Before staging acceptance testing is credited, populate `docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md` with externally reviewable evidence for:

- environment/owner;
- endpoint/access path;
- release/commit/image digests;
- infrastructure/runtime inventory;
- configuration parity;
- least-privilege identities/secrets references;
- TLS/network controls;
- data/sanitization/no-production-credential evidence;
- deployment/change and rollback records;
- deployment-time security review.

All staging acceptance suites must bind to that same identity.

## Rollback

Every staged/production release requires a known rollback target and procedure tied to the same release/deployment identity.

Rollback is not complete until:

- application health is restored;
- canonical data integrity is validated;
- authorization/security controls are revalidated;
- source/search/observability dependencies are validated as applicable.

## Secrets and credentials

- Secret values are not stored in repository documentation/evidence.
- Staging/production use approved secret-management paths.
- Application/service identities are least privilege.
- Infrastructure root/admin identities are separate from application identities.
- The local AIStor root/bootstrap credential compatibility exception must not be used as a staging/production identity pattern.
- Example/default credentials must never remain in accepted production configuration.

## Vulnerability and advisory review

Deployment-time security review considers applicable public threat intelligence, CVEs and vendor advisories against the immutable target release/platform.

Record:

- source/provenance;
- review time;
- target component/version;
- applicability;
- confidence;
- disposition/remediation.

## Accessibility and operator UX

The current engineering/product baseline has accepted accessibility/browser evidence and accountable functional acceptance.

Future UX changes must continue to preserve keyboard, focus, contrast, reflow, text-size/spacing, responsive and supported-browser coverage. Environment-specific assistive-technology validation may be repeated where required by the target acceptance scope.

## Operational acceptance

Production operation ultimately requires accepted Phase 8 and Phase 9 evidence plus accountable Phase 10 approval of ownership/support, security/privacy, monitoring/on-call, deployment/change and recovery controls.
