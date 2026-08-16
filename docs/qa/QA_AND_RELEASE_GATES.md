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
8. **One bounded Phase 11 objective per PR** — unrelated architecture work is not stacked behind red CI.
9. **Professional documentation is a merge criterion** — code/integration work cannot merge when affected authoritative documentation or documentation-contract tests are stale.

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
| Governance | Mapping truth and authority separation | Repository CI + governance review |
| Platform integration | API/data-model interoperability, provenance, identity, replay/dedupe and migration | Phase 11 repository + integration evidence |
| Integrated runtime | Kubernetes/Helm/GitOps, secrets, network, HA/recovery, observability and supply-chain controls | Phase 11 deployed validation |
| Independent assurance | Independent assessment of integrated candidate | Phase 11 external assurance |
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
| Phase 11.1 Taranis | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.2 Taranis adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 IntelOwl integration | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.4 OpenCTI contract | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 12 | `NOT STARTED` |

DTMO is not production authorized.

## Repository-controlled evidence

Existing workflow families remain required. Each Phase 11 integration adds a bounded contract/integration gate without weakening previous quality, security, recovery, governance or documentation controls.

The **Phase 11 IntelOwl Integration Contract Gate** remains evidence for repository-complete Phase 11.3. It does not become live-provider or production evidence.

The active **Phase 11 OpenCTI Integration Contract Gate** validates `docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md`, its professional documentation set, the synchronized lifecycle status and the OpenCTI documentation contract test.

## Phase 11 gate sequence

### 11.1 Taranis architecture and gap assessment

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

### 11.2 Taranis canonical adapter

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

Accepted evidence includes authenticated read-only service integration, idempotent canonical ingestion, provenance/evidence retention, fail-closed TLP/classification, replay/deduplication, durable checkpointing/reconciliation, bounded detail/CTI retrieval, governed connector execution and degraded/failure handling.

### 11.3 IntelOwl integration

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

Accepted evidence includes the IntelOwl service/API/licensing contract, bounded analyzer adapter, production HTTPS/token/analyzer allowlist checks, privacy/TLP fail-closed behavior, immutable job identity, bounded polling/result validation, explicit partial success, governed human execution, durable enrichment history and no-share/no-local-compromise invariants.

### 11.4 OpenCTI contract — active bounded gate

Required exact-head repository evidence:

- reviewed OpenCTI baseline `7.260811.0` is recorded;
- Community Edition Apache-2.0 and separately licensed Enterprise Edition are distinguished;
- DTMO remains a separate service/API consumer and vendors no OpenCTI source;
- GraphQL, STIX 2.1, TAXII 2.1 and access-controlled streams are bounded;
- the initial implementation path is read-oriented;
- dedicated non-human least-privilege identity and marking access are mandatory;
- administrator/`Bypass all capabilities` and connector privileges are not routine requirements;
- OpenCTI internal/STIX identity and DTMO canonical UUID remain distinct and explicitly mapped;
- markings/TLP/PAP, confidence, provenance and timestamps are preserved;
- unknown/malformed markings, malformed/unsupported STIX and authorization failures fail closed;
- future pagination/stream replay must be bounded, restart-safe and idempotent;
- checkpoint/cursor advancement occurs only after durable accepted state;
- connector registration, MISP synchronization, enrichment, TheHive case creation and report publication are excluded from this first boundary;
- OpenCTI graph context cannot mutate DTMO external-share/publication authority or prove local compromise;
- `README.md`, `docs/README.md`, current state, roadmap, security, operations, QA and evidence index remain synchronized;
- `docs/qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md`, Professional Documentation Gate and all required exact-head CI succeed on the same final head.

Repository acceptance does not establish live OpenCTI connectivity, deployed credentials, effective production RBAC/marking segregation, real STIX graph interoperability/performance, privacy approval, production HA/recovery, independent assurance or production authorization.

### 11.4 next implementation gate

Only after the contract PR is fully green and protected-merged may a new bounded PR implement the **read-only OpenCTI STIX/identity adapter with pagination/reconciliation and provenance preservation**.

### 11.5 MISP consolidation

Required evidence includes one authoritative inbound/synchronization model, conflict/replay handling, DTMO outbound approval remaining authoritative, distribution/TLP/sharing-group fail-closed behavior and no implicit share authority for automated components.

### 11.6 TheHive / 11.7 Cortex decision

Required evidence includes controlled case handoff with provenance/audit references and a documented Cortex decision based only on an accepted IntelOwl capability gap.

### 11.8 Integrated runtime

Required evidence includes Kubernetes/Helm/GitOps, immutable images, workload identities/external secrets, TLS/network policies, database/queue/storage durability and recovery, centralized observability, SBOM/scanning/signing/attestation, capacity, upgrade and rollback tests.

### 11.9 Migration and compatibility

Required evidence includes migration correctness/rollback and preservation of canonical intelligence/provenance/classification/governance.

### 11.10–11.11 Integrated validation and assurance

The integrated candidate must receive fresh production-equivalent validation and fresh independent external assurance against the same immutable deployment identity. Prior Phase 8/9 evidence remains historical and cannot satisfy these gates by itself.

## Phase 12 production-decision model

Phase 12 is `NOT STARTED`. It requires accepted Phase 11 validation/assurance plus production-specific approvals. Missing mandatory input, unresolved release-blocking findings, unaccepted residual risk or release-identity mismatch remains `NO-GO / BLOCKED`.

## Security and publication invariants

Release gates must preserve:

- ingestion/enrichment/graph synchronization creates candidate/context intelligence only;
- external sharing requires separate human approval;
- connectors, CI, service accounts and integrated publishers do not gain publication authority;
- IntelOwl analyzer verdicts and OpenCTI graph relationships do not imply local compromise;
- human and machine roles remain separated;
- framework mappings remain explicit and do not imply blanket compliance;
- provenance, confidence and markings are preserved across service boundaries;
- raw secret values are not committed as evidence;
- external integrations use dedicated identities and bounded scopes.

## Release decision rule

A PR may be merged only when required exact-head workflows for the final head are `completed/success` and the PR remains mergeable. Production authorization requires an explicit accountable Phase 12 `GO`.
