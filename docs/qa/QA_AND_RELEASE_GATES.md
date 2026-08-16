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
| Phase 11.4 OpenCTI contract | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.4 OpenCTI read-only adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.4 OpenCTI persistence | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 12 | `NOT STARTED` |

DTMO is not production authorized.

## Repository-controlled evidence

Existing workflow families remain required. Each Phase 11 integration adds bounded integration tests without weakening previous quality, security, recovery, governance or documentation controls.

The **Phase 11 IntelOwl Integration Contract Gate** remains repository evidence for accepted Phase 11.3. The **Phase 11 OpenCTI Integration Contract Gate** now covers the accepted contract/read adapter and the active canonical persistence slice.

## Phase 11 gate sequence

### 11.1 Taranis architecture and gap assessment

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

### 11.2 Taranis canonical adapter

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

### 11.3 IntelOwl integration

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

### 11.4 OpenCTI contract

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

### 11.4 OpenCTI read-only adapter

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

Accepted evidence covers bounded GraphQL `stixCoreObjects` retrieval, stable OpenCTI/STIX identity, entity allowlists, marking/confidence/provenance preservation, fail-closed malformed state, bounded pagination and explicit `commit_page(page)` semantics.

### 11.4 OpenCTI canonical persistence — active bounded gate

Required exact-head repository evidence:

- migration `0012_opencti_mapping_persistence` follows `0011_intelowl_enrichment_history`;
- `opencti_object_mappings` preserves DTMO item identity, OpenCTI internal ID and STIX ID explicitly;
- `opencti_mapping_revisions` preserves immutable attributable snapshots;
- unchanged replay is idempotent through SHA-256 snapshot hashes;
- changed upstream state creates one new immutable revision;
- conflicting OpenCTI/STIX identity drift and ambiguous mappings fail closed;
- entity type, parent types, markings/TLP/PAP context, confidence, timestamps, external references and provenance remain preserved;
- database constraints enforce `external_share_authorized=false` and `local_compromise_proven=false`;
- PostgreSQL commit completes before `commit_page(page)` advances durable cursor state;
- database commit failure leaves the checkpoint unchanged;
- replay remains safe when DB commit succeeds but checkpoint replacement fails;
- connector registration, MISP synchronization, enrichment, TheHive case creation, report publication, OpenCTI security administration and arbitrary GraphQL mutation remain excluded;
- `README.md`, `docs/README.md`, current state, roadmap, security, integration, operations, QA and evidence index are synchronized;
- `docs/qa/PHASE11_4_OPENCTI_PERSISTENCE_GATE.md`, Professional Documentation Gate, Phase 11 OpenCTI Integration Contract Gate and all other required exact-head workflows succeed on the same final head.

Repository acceptance does not establish live OpenCTI connectivity, deployed credentials, effective production RBAC/marking segregation, production STIX interoperability/performance, privacy approval, HA/recovery, independent assurance or production authorization.

Only after protected merge and lifecycle reconciliation may Phase 11.4 become `PASS / REPOSITORY_COMPLETE`. Phase 11.5 remains blocked until then.

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
- IntelOwl analyzer verdicts and OpenCTI graph mappings do not imply local compromise;
- human and machine roles remain separated;
- framework mappings remain explicit and do not imply blanket compliance;
- provenance, confidence and markings are preserved across service boundaries;
- raw secret values are not committed as evidence;
- external integrations use dedicated identities and bounded scopes.

## Release decision rule

A PR may be merged only when required exact-head workflows for the final head are `completed/success` and the PR remains mergeable. Production authorization requires an explicit accountable Phase 12 `GO`.
