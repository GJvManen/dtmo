# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from the current RC4.8 state to production readiness. It is executed through hourly PDCA runs and tracked in GitHub issue #3.

The release rule is strict: no phase is complete without objective evidence. Missing CI, security, recovery, performance, accessibility or external-assurance evidence blocks production readiness.

## Current baseline

- Application code, migrations, API, storage, search, graph, RBAC and documentation are present.
- Internal CI evidence is not yet consistently observable.
- External production acceptance gates in issue #1 remain open.
- Overall status remains `CI VALIDATION PENDING` until automated quality evidence is visible and successful.

## Phase 1 — CI and workflow integrity

### Objectives

- Regression-protect all release-critical GitHub Actions workflow structure.
- Validate required triggers, jobs, permissions, services, artifacts and gates.
- Make workflow execution independently observable through commit statuses, workflow-run evidence and artifacts.
- Add negative tests proving missing or malformed gates block release.

### Blocking gates

- Workflow contract tests pass.
- Required jobs and triggers are validated.
- Commit status or workflow-run evidence is observable.
- Failed or absent workflows cannot be interpreted as success.

## Phase 2 — Application security and identity

### Objectives

- Replace shared API-key-only trust with enterprise identity integration or a hardened reverse-proxy trust boundary.
- Strengthen RBAC and separation of duties.
- Add audit logging for all privileged operations.
- Add SAST, dependency, secrets and container scanning.

### Blocking gates

- Authentication and authorization tests pass.
- Privilege-escalation and negative RBAC tests pass.
- No hardcoded or example production secrets remain.
- Security scans have no unresolved critical findings.

## Phase 3 — Data integrity and recovery

### Objectives

- Validate PostgreSQL migrations and constraints.
- Verify MinIO raw-object immutability and checksums.
- Add backup, retention and restoration automation.
- Test full restoration of database, object storage and search index.

### Blocking gates

- Alembic upgrade/downgrade/upgrade succeeds.
- Restore test succeeds from a clean environment.
- Provenance and checksum integrity remain intact after recovery.
- Recovery time and recovery point objectives are documented and tested.

## Phase 4 — Live connector reliability and provenance

### Objectives

- Add controlled live canary runs for approved open-source connectors.
- Validate credentials, rate limits, licences and terms.
- Add retries, backoff, deduplication, source health and failure isolation.
- Ensure every imported record retains source, timestamp, confidence and raw evidence.

### Blocking gates

- Connector contract tests pass.
- Canary runs are observable and repeatable.
- Duplicate and malformed records are quarantined.
- No connector can publish intelligence without human review.

## Phase 5 — Performance and scalability

### Objectives

- Define representative education-sector intelligence volumes.
- Add API, PostgreSQL, OpenSearch and ingestion load tests.
- Establish latency, throughput and resource-use budgets.
- Test queue pressure, connector bursts and degraded dependencies.

### Blocking gates

- Search latency and dashboard response targets are met.
- Ingestion remains correct under representative load.
- No data loss occurs during dependency degradation.
- Capacity limits and scaling guidance are documented.

## Phase 6 — Frontend accessibility and operational UX

### Objectives

- Add browser-based end-to-end tests.
- Validate critical analyst, CISO and audit workflows.
- Test responsive behavior and keyboard navigation.
- Verify WCAG 2.2 AA compliance.

### Blocking gates

- Critical user journeys pass in supported browsers.
- No blocking accessibility defects remain.
- Error, loading and empty states are tested.
- UI permissions match backend RBAC.

## Phase 7 — Observability and incident operations

### Objectives

- Add service-level metrics, structured logs and traces.
- Define alerting for connector failures, queue backlog, storage integrity, API errors and search health.
- Create incident, outage, recovery and connector-failure runbooks.
- Add operational dashboards and on-call handover guidance.

### Blocking gates

- Alerts are tested with controlled failures.
- Logs and metrics provide correlation IDs and actionable evidence.
- Runbooks are complete and exercised.
- Operational ownership and escalation paths are documented.

## Phase 8 — Staging acceptance

### Objectives

- Deploy an environment equivalent to production.
- Run smoke, integration, migration, connector, recovery, performance and accessibility tests.
- Validate secrets management, TLS and network restrictions.

### Blocking gates

- Staging deployment is reproducible.
- All internal quality gates pass in staging.
- No unresolved blocker defects remain.
- Deployment acceptance evidence is retained.

## Phase 9 — External assurance

### Objectives

Complete the externally executed gates tracked in issue #1:

- independent penetration test;
- load and stress test;
- full backup and restoration exercise;
- connector licence, credential and terms validation;
- OpenSearch production hardening;
- operational acceptance by service owner, CISO/ISO and privacy function.

### Blocking gates

- Critical and high findings are resolved or formally accepted.
- External evidence is attached to the release record.
- Required stakeholders approve production use.

## Phase 10 — Production go/no-go

### Go criteria

- All phases above are complete with evidence.
- CI is green and independently observable.
- Release notes, SBOM, deployment manifest and rollback plan are complete.
- Backup and restoration are proven.
- Security, privacy, service-owner and operational approvals are recorded.
- No open blocker defects remain.

### No-go criteria

Any missing blocking evidence, unresolved critical defect, failed recovery test, inaccessible CI evidence, incomplete external assurance or absent approval results in `BLOCKED`.

## Hourly PDCA execution order

Each run performs exactly one bounded objective in this order unless a higher-severity blocker is discovered:

1. Phase 1 — CI and workflow integrity.
2. Phase 2 — Application security and identity.
3. Phase 3 — Data integrity and recovery.
4. Phase 4 — Live connector reliability and provenance.
5. Phase 5 — Performance and scalability.
6. Phase 6 — Frontend accessibility and operational UX.
7. Phase 7 — Observability and incident operations.
8. Phase 8 — Staging acceptance.
9. Phase 9 — External assurance coordination.
10. Phase 10 — Production go/no-go.

Every run must document Plan, Do, Check and Act, update the run log and QA evidence, and leave exactly one next priority.
