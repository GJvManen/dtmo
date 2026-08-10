# DTMO Operations Manual

Last updated: 2026-08-10

## Purpose

This manual describes the operational control model for DTMO. Detailed commands and component-specific procedures remain in the relevant runbooks and repository configuration.

## Daily operational checks

Operators should verify service health/readiness, key metrics, connector state/freshness, queue/backlog condition, storage/search health, recent alert state, scheduled jobs and unresolved incident/change items.

Operational review must preserve privacy: avoid copying raw sensitive payloads into tickets, chat or repository evidence unless explicitly required and approved.

## Access and authority

Operational access is role-based and least privilege. Technical access does not grant intelligence review, publication or human share-approval authority. Review and share approval remain separate human decisions.

## Connector operations

Connector failures are handled using state, retry, timeout, replay, freshness and failure-isolation controls. Operators should preserve provider provenance, timestamps, correlation identifiers and confidence context during troubleshooting.

## Monitoring and alerting

DTMO has bounded evidence for request observability, distributed trace context, queue backlog, connector failures, storage integrity, API errors and search health. Operational dashboards aggregate these signals. Real notification/delivery integrations must be separately accepted where required.

## Incident handling

1. Confirm the alert/incident and affected scope.
2. Preserve correlation identifiers and relevant privacy-safe evidence.
3. Assess impact on confidentiality, integrity, availability, provenance and dissemination controls.
4. Contain without weakening RBAC or approval boundaries.
5. Recover using approved procedures.
6. Validate service health and data integrity.
7. Record timeline, decisions, actions and residual risk.
8. Escalate according to the operational runbooks and accountable ownership.

## Backup and recovery

Repository-controlled recovery evidence covers multiple persistence components and migration/recovery paths. Production operation additionally requires a complete production-equivalent backup/restoration exercise with retained evidence, measured recovery outcomes and accountable sign-off.

## Change and release management

Every deployable release should have an immutable identity. Changes must be traceable to reviewed source, successful required CI, release/deployment records and an approved target environment. Production release must not proceed while blocking roadmap/external gates remain incomplete.

## Staging deployment

Before Phase 8 acceptance testing, staging must have one approved immutable deployment identity and the complete ten-class deployment-parity evidence package defined in `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`.

## Rollback

Every staged/production release requires a known rollback target and procedure tied to the same release/deployment identity. Rollback does not complete acceptance until service health, integrity and security controls are revalidated.

## Secrets and credentials

Secret values are not stored in repository documentation or evidence. Staging and production identities must use approved secret-management paths and least privilege. Example/default credentials must not remain in accepted production configuration.

## Vulnerability and advisory review

Deployment-time security review must consider applicable public threat intelligence, CVEs and vendor advisories against the actual immutable target release/platform. Record sources, review time, applicability, confidence and disposition.

## Accessibility operations

Automated accessibility regression evidence remains useful, but genuine VoiceOver/NVDA behavior on supported real environments is still an external production-readiness dependency until evidenced.

## Operational acceptance

Production operation requires accountable acceptance from the relevant service, security and privacy stakeholders, plus deployment acceptance and the remaining external assurance defined by issue #1 and Phase 9.
