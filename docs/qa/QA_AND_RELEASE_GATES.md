# DTMO QA and Release Gates

## Purpose

DTMO uses layered acceptance gates so engineering confidence, accountable functional acceptance, external staging evidence, independent assurance and production authorization remain separate claims. The model is fail-closed: configured checks or documented intentions are not evidence.

## Core release principles

1. **Exact-head evidence** — automated pull-request evidence belongs to the exact final PR head.
2. **New commit, new evidence** — a new commit invalidates earlier exact-head CI for that PR.
3. **No inferred PASS** — queued, in-progress, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
4. **Expected-head merge protection** — protected merge must reject a moved head.
5. **Evidence classes remain separate** — CI, owner acceptance, real staging, independent assurance and production authorization are not interchangeable.
6. **Deployment-bound evidence stays deployment-bound** — materially changed candidates require impact assessment and appropriate revalidation.
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
| Production-equivalent staging | Platform, source pipeline, recovery and accountable staging acceptance | Phase 8 |
| Independent assurance | Independent security/resilience/operational assessment | Phase 9 |
| Production decision | Formal accountable go/no-go | Phase 10 |

## Current acceptance status

| Stage | Status |
|---|---|
| Phases 1–7 | `PASS` |
| RC13 functional console | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | `PASS / OWNER_ACCEPTED` |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | `IN PROGRESS / DECISION REQUIRED` |

DTMO is not production authorized until Phase 10 records `GO`.

## Repository-controlled evidence

The workflow portfolio covers build/quality, security/identity, connector contracts and failure handling, payload provenance, multi-store recovery, performance, accessibility/browser UX, observability/alerts/runbooks, source normalization/persistence, Administration/RBAC, Governance and runtime/readiness support. These workflows establish engineering evidence within their declared scope only.

## Accepted non-CI evidence

RC13 is `PASS / OWNER_ACCEPTED`. Phase 8 is `PASS / OWNER_ACCEPTED`. Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`. These are distinct accountable/external evidence classes and are not represented as machine-generated repository CI outcomes.

## Phase 10 production-decision model

Phase 10 requires accepted Phase 8 and Phase 9 evidence plus production-specific approvals for environment/ownership/support, immutable release identity, IAM/secrets/network, backup/recovery/rollback, monitoring/on-call/escalation, incident-response handover, privacy/data/legal/governance, open findings/residual risk, change/release authorization and go-live/rollback authority.

Any missing mandatory input, unresolved release-blocking finding, unaccepted residual risk or material release-identity mismatch is `NO-GO / BLOCKED` until resolved and appropriately revalidated.

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

A PR may be merged only when required exact-head workflows for the final head are `completed/success` and the PR remains mergeable. A lifecycle phase may be accepted only after its additional non-CI evidence boundary is satisfied. Phase 10 production authorization requires an explicit accountable `GO`.