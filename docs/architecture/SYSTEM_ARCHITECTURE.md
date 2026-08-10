# DTMO System Architecture

Last updated: 2026-08-10

## Purpose

DTMO is an education-focused cyber threat intelligence platform that ingests, normalizes, enriches, stores and presents historical incidents, current threat intelligence, vulnerabilities, indicators, supplier risk and management reporting.

## Logical architecture

The system is organized into the following logical layers:

1. **Ingress and connectors** — provider-specific collection paths with explicit provenance, freshness, retry, timeout, replay and failure-isolation behavior.
2. **Normalization and enrichment** — conversion of provider payloads into internal models while preserving raw evidence references, provenance and confidence.
3. **Application/API layer** — authenticated APIs, search, analysis, workflow and approval controls.
4. **Persistence** — relational state, search/index state, cache/queue state and object evidence storage.
5. **Frontend** — operational and analytical user journeys with role-aware behavior and explicit approval boundaries.
6. **Observability** — metrics, health/readiness, request correlation, trace context, alerting and dashboards.
7. **Operations** — migrations, backup/recovery, runbooks, exercises, deployment and rollback controls.

## Principal runtime components

Repository-controlled environments model the application together with PostgreSQL, Redis, OpenSearch, object storage and an external TLS/reverse-proxy boundary. The Phase 8 application-container smoke intentionally executes only the DTMO application container and therefore does not establish full topology parity.

## Trust boundaries

Important trust boundaries include:

- external intelligence/provider networks to connector ingress;
- unauthenticated client to authenticated application boundary;
- user roles to privileged review/share-approval actions;
- application to persistence/search/object-storage services;
- CI/emulator environment to real staging/production environment;
- technical execution to human publication/share authority.

## Identity and authorization

Authorization is role-based and least-privilege oriented. Review and share approval are separate human authorities. Service accounts, connectors and automation do not receive publication/share-approval authority. Auditor/read-only behavior is separately constrained.

## Data and provenance

Normalized intelligence retains source provenance and confidence. Raw evidence is not silently discarded. Privacy-sensitive data should be minimized, and repository evidence excludes secret values, credentials, tokens and unnecessary personal data.

## Reliability

Connector behavior is designed around explicit state, retry, timeout, replay, freshness and failure isolation. Failure in one connector must not silently corrupt or authorize unrelated processing.

## Observability

The architecture exposes health/readiness, metrics, request correlation and distributed trace context. Queue, connector, storage, API and search health have dedicated bounded alerting evidence. Operational dashboards and runbooks provide response context.

## Recovery

Repository-controlled recovery gates cover migration and recovery behavior for multiple stores. This engineering evidence does not replace the external requirement for a complete production-equivalent backup/restoration exercise.

## Deployment architecture and staging boundary

Production readiness requires a real approved staging deployment with immutable application/container/release identity, infrastructure/runtime parity, approved secret-management identities, TLS/network restrictions, production-equivalent data handling, deployment/change evidence, rollback evidence and deployment-time security/advisory review.

The repository-controlled staging emulator and application-container runtime smoke are deliberately narrower and cannot substitute for this environment evidence.

## Security invariants

- RBAC and least privilege.
- Separation of duties.
- Human share approval separate from review and technical access.
- Provenance and confidence preservation.
- Privacy and data minimization.
- Auditable state transitions and request correlation.
- No secret values in repository evidence.
- No automatic publication from CI, connectors, recovery or runtime success.
