# DTMO QA and Release Gates

## Purpose

DTMO uses layered acceptance gates so engineering confidence, accountable functional acceptance, external staging evidence, independent assurance, platform-integration evidence and production authorization remain separate claims. The model is fail-closed: configured checks or documented intentions are not evidence.

## Core release principles

1. **Exact-head evidence** — automated pull-request evidence belongs to the exact final PR head.
2. **New commit, new evidence** — a new commit invalidates earlier exact-head CI for that PR.
3. **No inferred PASS** — queued, in-progress, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
4. **Expected-head merge protection** — protected merge must reject a moved head.
5. **Evidence classes remain separate** — CI, owner acceptance, real staging, independent assurance, platform-integration evidence and production authorization are not interchangeable.
6. **Deployment-bound evidence stays deployment-bound** — materially changed candidates require impact assessment and appropriate revalidation.
7. **Historical evidence is immutable** — later decisions may supersede current status without rewriting historical run records.
8. **One bounded Phase 11 objective per PR** — no stacking of unrelated architecture changes behind red CI.

## Gate families

| Gate family | Primary objective | Evidence boundary |
|---|---|---|
| Build & quality | Packaging, lint, typing, unit/integration correctness | Repository CI |
| Security & identity | Authentication, authorization, privileged actions and secret boundaries | Repository CI + deployed validation + assurance |
| Data integrity & recovery | Migrations, persistence, integrity and recovery | Repository CI + deployed validation/assurance |
| Connector reliability | Contract/state/retry/timeout/replay/freshness/provenance/failure isolation | Repository CI + deployed validation |
| Performance | Ingestion/read/concurrency/degraded behavior | Repository CI + representative external validation |
| Accessibility & browser UX | Keyboard/contrast/reflow/responsive/browser journeys | Repository CI + accountable functional acceptance |
| Observability & operations | Metrics/correlation/tracing/alerts/dashboards/runbooks | Repository CI + deployed operations |
| Functional console | Canonical end-to-end product behavior | Repository CI + accountable owner acceptance |
| Governance | Mapping truth and authority separation | Repository CI + governance review |
| Platform integration | API/data-model interoperability, provenance, identity, replay/dedupe and migration | Phase 11 repository + integration evidence |
| Integrated runtime | Kubernetes/Helm/GitOps, secrets, network, HA/recovery, observability and supply-chain controls | Phase 11 deployed validation |
| Independent assurance | Independent security/resilience/privacy/operational assessment of integrated candidate | Phase 11 external assurance |
| Production decision | Formal accountable go/no-go for integrated candidate | Phase 12 |

## Current acceptance status

| Stage | Status |
|---|---|
| Phases 1–7 | `PASS` |
| RC13 functional console | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | `PASS / OWNER_ACCEPTED` |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11 | `IN PROGRESS / ACTIVE` |
| Phase 12 | `NOT STARTED` |

DTMO is not production authorized.

## Repository-controlled evidence

The existing workflow portfolio remains required for DTMO code touched during Phase 11. New integrations add bounded contracts and integration/runtime gates rather than weakening existing controls.

## Phase 11 gate sequence

### 11.1 Taranis architecture and gap assessment

Required before adapter implementation:

- responsibility boundary accepted;
- exact API/OpenAPI inventory;
- schema/identity/provenance/classification mapping;
- replay/deduplication strategy;
- authentication/service-account design;
- licensing boundary accepted;
- integration threat-model abuse cases;
- adapter contract and rollback criteria.

### 11.2 Taranis canonical adapter

Required evidence:

- authenticated service-to-service contract;
- idempotent canonical ingestion;
- provenance/evidence retention;
- TLP/classification fail-closed behavior;
- replay/deduplication handling;
- degraded/partial failure behavior;
- no publication-authority escalation.

### 11.3 IntelOwl

Required evidence:

- dedicated service identity and secret handling;
- TLS verification outside local development;
- analyzer/result provenance;
- quota/timeout/failure isolation;
- privacy decision for email observables;
- semantic boundary that enrichment is not local exposure/compromise proof.

### 11.4 OpenCTI

Required evidence:

- STIX interoperability;
- entity identity/deduplication;
- confidence/marking/provenance preservation;
- graph synchronization failure handling;
- no duplicate custom graph authority inside DTMO.

### 11.5 MISP consolidation

Required evidence:

- one authoritative inbound/synchronization model;
- conflict/replay handling;
- DTMO outbound approval remains authoritative;
- distribution/TLP/sharing-group fail-closed behavior;
- automated collectors/publishers cannot gain implicit share authority.

### 11.6 TheHive / 11.7 Cortex decision

Required evidence:

- controlled case handoff with provenance/audit references;
- case state and canonical CTI remain separate;
- Cortex remains absent unless an explicit IntelOwl capability gap is accepted.

### 11.8 Integrated runtime

Required evidence:

- Kubernetes/Helm/GitOps deployment contract;
- immutable image versions/digests;
- workload identities and external secrets;
- TLS/network policies;
- PostgreSQL/Redis/storage durability and recovery;
- centralized audit/logging/metrics/alerting;
- SBOM/scanning/signing/attestation;
- capacity, upgrade and rollback tests.

### 11.9 Migration and compatibility

Required evidence:

- migration correctness and rollback;
- preservation of canonical intelligence, provenance, classification and governance;
- explicit disposition of existing E8 connectors/integrations;
- no silent data/authority loss.

### 11.10–11.11 Integrated validation and assurance

The integrated candidate must receive fresh production-equivalent validation and fresh independent external assurance against the same immutable deployment identity. Prior Phase 8/9 evidence remains historical and cannot satisfy these gates by itself.

## Phase 12 production-decision model

Phase 12 is `NOT STARTED`. It requires accepted Phase 11 validation/assurance plus production-specific approvals for environment/ownership/support, immutable release identity, IAM/secrets/network, backup/recovery/rollback, monitoring/on-call/escalation, incident-response handover, privacy/data/legal/governance, open findings/residual risk, change/release authorization and go-live/rollback authority.

Any missing mandatory input, unresolved release-blocking finding, unaccepted residual risk or material release-identity mismatch is `NO-GO / BLOCKED`.

## Security and publication invariants

Release gates must preserve:

- ingestion creates candidate intelligence only;
- external sharing requires separate human approval;
- connectors, CI, service accounts and integrated publishers do not gain publication authority;
- human and machine roles remain separated;
- privileged Administration remains least-privilege and auditable;
- framework mappings remain explicit and do not imply blanket compliance;
- provenance and confidence are preserved across service boundaries;
- raw secret values are not committed as evidence;
- external integrations use dedicated identities and bounded scopes;
- Grafana is not made anonymously accessible for convenience.

## Release decision rule

A PR may be merged only when required exact-head workflows for the final head are `completed/success` and the PR remains mergeable. A lifecycle phase may be accepted only after its additional evidence boundary is satisfied. Production authorization requires an explicit accountable Phase 12 `GO`.