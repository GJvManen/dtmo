# DTMO QA and Release Gates

## Purpose

DTMO uses layered acceptance gates so that engineering confidence, functional product acceptance, external staging evidence, independent assurance and production authorization remain distinct claims.

The gate model is intentionally fail-closed. A configured check is not evidence; a workflow must execute successfully against the required exact state before it can support an acceptance decision.

## Core release principles

1. **Exact-head evidence** — automated pull-request evidence belongs to the exact final PR head.
2. **New commit, new evidence** — any new commit invalidates earlier green CI for that PR.
3. **No inferred PASS** — queued, in-progress, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
4. **Expected-head merge protection** — merge is protected against a moved PR head.
5. **Evidence classes remain separate** — repository CI, accountable owner acceptance, real staging and independent assurance are not interchangeable.
6. **Historical evidence is immutable** — later evidence can change the current decision without rewriting earlier run records.

## Gate families

| Gate family | Primary objective | Evidence boundary |
|---|---|---|
| Build & quality | Compile, packaging, lint, type safety and unit/integration correctness | Repository CI |
| Security & identity | Authentication, authorization, privileged action and secrets boundaries | Repository CI + later staging/assurance |
| Data integrity & recovery | Migrations, persistence, integrity and recovery | Repository CI + later staging/assurance |
| Connector reliability | Contract, state, retry, timeout, replay, freshness, provenance and failure isolation | Repository CI + deployed validation |
| Performance | Ingestion/read/concurrency/degraded dependency behavior | Repository CI + representative external validation |
| Accessibility & browser UX | Keyboard, contrast, reflow, responsive/browser journeys | Repository CI + accountable functional acceptance |
| Observability & operations | Metrics, correlation, tracing, alerts, dashboards and runbooks | Repository CI + staging operations |
| Functional console | End-to-end canonical product behavior | Repository CI + accountable owner acceptance |
| Source/persistence contract | Raw evidence, canonical commit and index/search behavior | Repository CI + staging validation |
| Governance | Truthful mapping claims and authority separation | Repository CI + governance review |
| Open source governance | License, notices, security/contribution policy | Repository CI |
| Staging identity/parity | One immutable production-equivalent deployment and configuration evidence | Real external Phase 8 evidence |
| External assurance | Independent security/resilience/operational review | Phase 9 evidence |
| Production decision | Formal accountable go/no-go | Phase 10 approval |

## Current acceptance status

| Stage | Status |
|---|---|
| Phases 1–7 repository-controlled engineering | `PASS` |
| RC13 functional console | `PASS / OWNER_ACCEPTED` |
| Phase 8 real staging | `READY / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY` |
| Phase 9 independent assurance | `NOT COMPLETE` |
| Phase 10 production go/no-go | `NOT STARTED` |

## Repository-controlled gate coverage

The current workflow portfolio covers, among other areas:

- RC4 Quality Gate;
- open-source governance;
- connector contracts, state, freshness, retry, timeout, replay and failure isolation;
- payload provenance;
- multi-store and OpenSearch recovery;
- ingestion/read/concurrency/degraded-dependency performance;
- keyboard, contrast, reflow, text resize/spacing, responsive layout and supported browsers;
- request observability, trace context, queue/search/storage/connectors alerting and runbook exercises;
- canonical source catalog/bootstrap and source execution contracts;
- canonical connector commit visibility;
- source-record normalization;
- functional console/browser acceptance;
- native visual analytics;
- governed Administration/RBAC;
- Governance knowledge surface;
- object-storage migration/runtime contracts;
- Grafana provisioning/runtime contracts;
- Phase 8 staging readiness/emulator engineering contracts.

These workflows establish engineering evidence only within their declared scopes.

## Functional owner acceptance

RC13 is complete because the repository-controlled functional evidence was followed by explicit accountable owner testing and acceptance of the merged product.

Owner acceptance is not machine-generated and is not implied by green CI. If future owner testing identifies a product regression, the relevant current functional gate can be reopened without modifying historical evidence.

## Phase 8 acceptance model

Phase 8 starts only from an accepted functional product baseline and requires a real production-equivalent staging environment.

Every Phase 8 evidence item must bind to the same immutable deployment identity, including:

- environment and owner;
- endpoint/access path;
- release/commit and image digests;
- infrastructure/runtime versions;
- configuration parity;
- IAM/secrets references and least privilege;
- TLS/network controls;
- data handling/sanitization;
- deployment/change and rollback records;
- deployment-time security review.

Repository staging emulators are preparatory engineering evidence and cannot satisfy Phase 8 by themselves.

## Security and publication invariants

Release gates must preserve the following invariants:

- ingestion creates candidate intelligence only;
- external sharing requires separate human approval;
- connectors, CI and service accounts do not gain publication authority;
- human and machine roles remain separated;
- Administration changes remain least-privilege and auditable;
- Governance visibility does not grant publication/share authority;
- external framework mappings are not inferred;
- provenance and confidence are preserved;
- no raw secret values are committed as evidence;
- no anonymous Grafana access or authentication bypass is introduced for convenience.

## Product enhancement gating

Post-RC13 product enhancements are delivered as bounded PRs. Each enhancement must:

1. define explicit acceptance criteria;
2. include focused unit/contract/browser evidence where appropriate;
3. preserve accepted RC13 behavior;
4. preserve security/governance invariants;
5. pass the complete exact-head workflow set before merge;
6. be validated in staging if it is part of the Phase 8 candidate deployment.

The first planned enhancement combines shared severity semantics and filters for Overview and Intelligence.

## Release decision rule

A PR may be merged only after all returned release-critical workflows for the exact final head are `completed/success` and the PR remains mergeable. A product or phase may be accepted only after its additional non-CI evidence boundary is also satisfied.
