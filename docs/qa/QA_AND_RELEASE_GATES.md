# DTMO QA and Release Gates

## Purpose

DTMO uses layered acceptance gates so engineering confidence, accountable functional acceptance, external staging evidence, independent assurance, platform-integration evidence and production authorization remain separate claims. The model is fail-closed: configured checks or documented intentions are not evidence.

## Core release principles

1. **Exact-head evidence** — automated pull-request evidence belongs to the exact final PR head.
2. **New commit, new evidence** — a new commit invalidates earlier exact-head CI for that PR.
3. **No inferred PASS** — queued, in-progress, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
4. **Expected-head merge protection** — protected merge must reject a moved head.
5. **Evidence classes remain separate** — CI, owner acceptance, real staging, independent assurance, platform-integration evidence and production authorization are not interchangeable.
6. **Historical evidence is immutable** — later decisions may supersede current status without rewriting historical run records.
7. **One bounded Phase 11 objective per PR** — unrelated architecture work is not stacked behind red CI.
8. **Professional documentation is a merge criterion** — code/integration work cannot merge when affected authoritative documentation or documentation-contract tests are stale.

## Gate families

| Gate family | Primary objective | Evidence boundary |
|---|---|---|
| Build & quality | Packaging, lint, typing, unit/integration correctness | Repository CI |
| Security & identity | Authentication, authorization, privileged actions and secret boundaries | Repository CI + deployed validation + assurance |
| Data integrity & recovery | Migrations, persistence, integrity and recovery | Repository CI + deployed validation/assurance |
| Connector reliability | Contract/state/retry/timeout/replay/freshness/provenance/failure isolation | Repository CI + deployed validation |
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
| Phase 11.4 OpenCTI integration | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.5 MISP consolidation | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.6 TheHive handoff contract | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 12 | `NOT STARTED` |

DTMO is not production authorized.

## Repository-controlled evidence

Existing workflow families remain required. Each Phase 11 integration adds bounded integration tests without weakening previous quality, security, recovery, governance or documentation controls.

The accepted Taranis, IntelOwl, OpenCTI and MISP gates remain repository evidence for Phase 11.1–11.5. The active implementation gate is the **Phase 11 TheHive Handoff Contract Gate**.

## Phase 11 gate sequence

### 11.1–11.5 accepted boundaries

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

Accepted evidence covers Taranis architecture/adapter, IntelOwl bounded enrichment, OpenCTI graph integration and MISP authoritative governed exchange/synchronization state. Repository acceptance is not production evidence.

### 11.6 TheHive handoff contract — active bounded gate

Required exact-head repository evidence:

- TheHive 5.5.16 and public API v1 (`/api/v1`) are the reviewed upstream baseline;
- TheHive remains a separate StrangeBee service and no source is vendored;
- TheHive 5.3+ license activation requirement for continued write functionality is explicitly recorded as a deployment prerequisite;
- `POST /api/v1/case` is not invoked automatically and remains a mutation candidate only after explicit human-approved DTMO case handoff;
- case-handoff authority and DTMO publication/share authority are distinct server-side RBAC decisions;
- DTMO canonical UUID, handoff request/idempotency identity, TheHive case identity and organization context are treated as stable reconciliation identities;
- mutable title/description/tag/assignee state is not identity;
- ambiguous mutation delivery blocks blind replay;
- TLP/PAP/access mappings preserve or strengthen authoritative source restrictions and unknown/unrepresentable mappings fail closed;
- a dedicated least-privilege TheHive service identity is required and runtime secrets remain outside repository evidence;
- attachments, raw source bodies, credentials, private enrichment and unrelated personal data are excluded by default;
- TheHive case lifecycle does not become canonical CTI truth, proof of local compromise or DTMO external-share authority;
- responders, Cortex execution, automatic MISP→TheHive automation, external sharing and administration remain excluded;
- architecture, integration, operations, security, current-state, QA, evidence, roadmap and README/docs portal documentation remain synchronized;
- `docs/qa/PHASE11_6_THEHIVE_HANDOFF_CONTRACT_GATE.md`, Professional Documentation Gate, RC4 Quality Gate and the dedicated Phase 11 TheHive Handoff Contract Gate all succeed on the same exact head.

Repository acceptance does not establish live TheHive connectivity, activated entitlement, effective deployed permissions, target-organization configuration, privacy approval, real-data handling correctness, production-equivalent validation, independent assurance or production authorization.

Only after protected merge and lifecycle reconciliation may the contract become `PASS / REPOSITORY_COMPLETE`. The next bounded 11.6 slice may then implement the minimum human-authorized case-handoff adapter and durable mutation reconciliation state.

### 11.7 Cortex decision

Adopt Cortex only if an accepted capability-gap analysis proves IntelOwl cannot satisfy a validated requirement. TheHive integration is not itself evidence of a Cortex gap.

### 11.8 Integrated runtime

Required evidence includes Kubernetes/Helm/GitOps, immutable images, workload identities/external secrets, TLS/network policies, database/queue/storage durability and recovery, centralized observability, SBOM/scanning/signing/attestation, capacity, upgrade and rollback tests.

### 11.9 Migration and compatibility

Required evidence includes migration correctness/rollback and preservation of canonical intelligence/provenance/classification/governance.

### 11.10–11.11 Integrated validation and assurance

The integrated candidate must receive fresh production-equivalent validation and fresh independent external assurance against the same immutable deployment identity. Prior Phase 8/9 evidence remains historical and cannot satisfy these gates by itself.

## Phase 12 production-decision model

Phase 12 is `NOT STARTED`. It requires accepted Phase 11 validation/assurance plus production-specific approvals. Missing mandatory input, unresolved release-blocking findings, unaccepted residual risk or release-identity mismatch remains `NO-GO / BLOCKED`.

## Security and authority invariants

Release gates must preserve:

- ingestion/enrichment/graph/MISP synchronization creates candidate/context intelligence only;
- external sharing requires separate human approval;
- case handoff requires separate human approval;
- connectors, CI, service accounts and integrated platforms do not gain publication/share or case-handoff authority;
- IntelOwl verdicts, OpenCTI graph mappings, MISP event presence and TheHive case state do not imply local compromise;
- human and machine roles remain separated;
- framework mappings remain explicit and do not imply blanket compliance;
- provenance, confidence, markings and source restrictions are preserved across service boundaries;
- raw secret values are not committed as evidence;
- external integrations use dedicated identities and bounded scopes.

## Release decision rule

A PR may be merged only when required exact-head workflows for the final head are `completed/success` and the PR remains mergeable. Production authorization requires an explicit accountable Phase 12 `GO`.
