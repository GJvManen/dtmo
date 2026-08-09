# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's current release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3.

The release rule is strict: no phase is complete without objective evidence. Missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks production readiness.

## Current status — 2026-08-09

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — Application security and identity: `PASS` for the internal roadmap gates; production identity/secrets acceptance remains represented in external gates where applicable.
- Phase 3 — Data integrity and recovery: `PASS` for internal automated gates; full external backup/restoration exercise remains tracked separately.
- Phase 4 — Live connector reliability and provenance: `PASS` for internal gates; live-provider acceptance evidence is separately tracked in issue #1.
- Phase 5 — Performance and scalability: `PASS` for internal automated gates.
- Phase 6 — Frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA execution on supported real hosts. Automated browser, keyboard, responsive, supported-browser, contrast, resize, reflow, text-spacing and focus-order evidence is accepted. Browser/DOM automation is not treated as a substitute for real assistive-technology behavior.
- Phase 7 — Observability and incident operations: `IN PROGRESS`.
- Phase 8 — Staging acceptance: `NOT STARTED`.
- Phase 9 — External assurance: `NOT COMPLETE`; tracked in issue #1.
- Phase 10 — Production go/no-go: `NOT STARTED`.

### Latest accepted Phase 7 evidence

RC10.1 request observability is `PASS`:

- PR #80 exact head `01a175e12da7c8af8566178a2d7e6b34a57d58bc`;
- 34/34 registered workflows successful;
- retained artifact `9040196394`;
- digest `sha256:6792020994d94b0484cb84140d202433303eceb82565f8598ffd5937940531d6`;
- 5/5 JUnit tests successful;
- safe correlation IDs, structured request-log context, bounded route-template request metrics, request-latency metrics and in-flight request metrics evidenced;
- merged as `1675d88bb24dcd50e20545f49b26dd7cc2810d97`.

Phase 7 remains incomplete because distributed tracing, controlled alerting, operational dashboards, runbooks, on-call handover and ownership/escalation evidence remain open.

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
- Verify bounded WCAG 2.2 AA critical-journey evidence and genuine assistive-technology behavior separately.

### Blocking gates

- Critical user journeys pass in supported browsers.
- No blocking automated accessibility defects remain.
- Error, loading and empty states are tested.
- UI permissions match backend RBAC.
- Genuine VoiceOver/NVDA behavior is evidenced on supported real host/browser/screen-reader combinations.

### Current decision

`BLOCKED_EXTERNAL` only for the final genuine assistive-technology evidence requirement. RC9.16 defines the required execution matrix and evidence contract.

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

### Current decision

`IN PROGRESS`. RC10.1 request observability is accepted. Exactly one next priority is RC10.2 controlled connector-failure alerting with actionable alert, correlation and recovery/clear evidence.

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

Any missing blocking evidence, unresolved critical defect, failed recovery test, inaccessible CI evidence, incomplete accessibility evidence, incomplete external assurance or absent approval results in `BLOCKED`.

## PDCA execution order

Each run performs exactly one bounded objective in roadmap order unless a higher-severity blocker is discovered or an earlier phase is blocked only by an explicitly external dependency that cannot be executed in the current environment.

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

Every run must document Plan, Do, Check and Act, update the run log and QA evidence, preserve explicit claim boundaries, and leave exactly one next priority.
