# DTMO QA and Release Gates

## Purpose

DTMO uses layered acceptance gates so that engineering confidence, accountable functional acceptance, external staging evidence, independent assurance and production authorization remain separate claims.

The model is fail-closed: a configured check or documented intention is not evidence. Each evidence class must be completed against the state it claims to support.

## Core release principles

1. **Exact-head evidence** — automated pull-request evidence belongs to the exact final PR head.
2. **New commit, new evidence** — a new commit invalidates earlier exact-head CI for that PR.
3. **No inferred PASS** — queued, in-progress, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
4. **Expected-head merge protection** — protected merge must reject a moved head.
5. **Evidence classes remain separate** — CI, owner acceptance, real staging, independent assurance and production authorization are not interchangeable.
6. **Deployment-bound evidence stays deployment-bound** — materially changed candidates require revalidation or explicit evidence rebinding.
7. **Historical evidence is immutable** — later decisions may supersede current status without rewriting historical run records.

## Gate families

| Gate family | Primary objective | Evidence boundary |
|---|---|---|
| Build & quality | Packaging, lint, typing, unit/integration correctness | Repository CI |
| Security & identity | Authentication, authorization, privileged actions and secret boundaries | Repository CI + staging + assurance |
| Data integrity & recovery | Migrations, persistence, integrity and recovery | Repository CI + staging/assurance |
| Connector reliability | Contract/state/retry/timeout/replay/freshness/provenance/failure isolation | Repository CI + deployed validation |
| Performance | Ingestion/read/concurrency/degraded behavior | Repository CI + representative external validation |
| Accessibility & browser UX | Keyboard/contrast/reflow/responsive/browser journeys | Repository CI + accountable functional acceptance |
| Observability & operations | Metrics/correlation/tracing/alerts/dashboards/runbooks | Repository CI + staging operations |
| Functional console | Canonical end-to-end product behavior | Repository CI + accountable owner acceptance |
| Governance | Mapping truth and authority separation | Repository CI + governance review |
| Staging identity/parity | Immutable production-equivalent deployment evidence | External Phase 8 |
| Source-to-intelligence | Real source retrieval through canonical analyst-visible intelligence | External Phase 8.3 |
| Operations/recovery | Recovery, rollback and operational continuity | External Phase 8.4 |
| Accountable staging acceptance | Consolidated Phase 8 owner decision | External Phase 8.5 |
| Independent assurance | Independent security/resilience/operational assessment | Phase 9 |
| Production decision | Formal accountable go/no-go | Phase 10 |

## Current acceptance status

| Stage | Status |
|---|---|
| Phases 1–7 | `PASS` |
| RC13 functional console | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Post-E8 external deployment/staging | `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE` |
| Phase 8.2–8.4 | `REPOSITORY CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED` |
| Phase 8.5 | `REPOSITORY CONTRACT COMPLETE / EXTERNAL OWNER DECISION REQUIRED` |
| Phase 9 | `NOT COMPLETE` |
| Phase 10 | `NOT STARTED` |

DTMO is not production ready.

## Repository-controlled evidence

The workflow portfolio covers build/quality, security/identity, connector contracts and failure handling, payload provenance, multi-store recovery, performance, accessibility/browser UX, observability/alerts/runbooks, source normalization/persistence, Administration/RBAC, Governance, object-storage/runtime contracts and staging-emulator/readiness support.

These workflows establish engineering evidence within their declared scope only.

## Functional owner acceptance

RC13 is `PASS / OWNER_ACCEPTED` because repository-controlled functional evidence was followed by explicit accountable owner testing and acceptance. This acceptance is not machine-generated and does not automatically extend to materially changed deployments or later external assurance claims.

## Phase 8 acceptance model

The post-E8 candidate has been externally deployed and successfully owner-tested in an approved production-equivalent staging environment. Formal Phase 8 closure still requires all accepted external evidence to be bound to one immutable staging deployment identity.

The repository contracts for Phase 8.2–8.5 are complete. External evidence must cover the declared platform/identity, source-to-intelligence, operations/recovery and accountable acceptance scopes. Repository staging emulators remain supporting engineering evidence only.

Phase 8 may be marked `PASS / OWNER_ACCEPTED` only when:

- the exact deployed release/commit and immutable image/runtime identity are recorded;
- accepted Phase 8.2, 8.3 and 8.4 evidence refers to the same candidate;
- deviations and residual risks are explicit;
- no unresolved release-blocking staging finding remains;
- the accountable Phase 8.5 decision is recorded.

## Phase 9 assurance model

Phase 9 starts after formal Phase 8 acceptance and requires independent evidence. Expected classes include penetration testing, hardening/configuration, IAM/secrets, load/stress, resilience/recovery, monitoring/incident response, relevant privacy/legal/governance review, assurance-time vulnerability review, finding triage, remediation/retest and residual-risk disposition.

Project self-attestation, repository CI and owner staging testing cannot substitute for independent assurance.

## Security and publication invariants

Release gates must preserve:

- ingestion creates candidate intelligence only;
- external sharing requires separate human approval;
- connectors, CI and service accounts do not gain publication authority;
- human and machine roles remain separated;
- privileged Administration remains least-privilege and auditable;
- Governance visibility does not grant publication/share authority;
- framework mappings are explicit rather than inferred and do not imply blanket compliance;
- provenance and confidence are preserved;
- raw secret values are not committed as evidence;
- Grafana is not made anonymously accessible for convenience.

## Release decision rule

A PR may be merged only when the required exact-head workflows for the final head are `completed/success` and the PR remains mergeable. A product phase may be accepted only after its additional non-CI evidence boundary is also satisfied.
