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
| Phase 11.5 MISP consolidation contract | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 12 | `NOT STARTED` |

DTMO is not production authorized.

## Repository-controlled evidence

Existing workflow families remain required. Each Phase 11 integration adds bounded integration tests without weakening previous quality, security, recovery, governance or documentation controls.

The **Phase 11 IntelOwl Integration Contract Gate** remains repository evidence for accepted Phase 11.3. The **Phase 11 OpenCTI Integration Contract Gate** remains repository evidence for accepted Phase 11.4. The active gate is the **Phase 11 MISP Consolidation Contract Gate**.

## Phase 11 gate sequence

### 11.1 Taranis architecture and gap assessment

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

### 11.2 Taranis canonical adapter

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

### 11.3 IntelOwl integration

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

### 11.4 OpenCTI integration

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

Accepted evidence covers the service/API/STIX/licensing contract, bounded GraphQL/STIX adapter, explicit OpenCTI/STIX↔DTMO identity mapping, immutable reconciliation history, database-enforced no-share/no-local-compromise invariants and PostgreSQL-before-checkpoint ordering. Repository acceptance is not live OpenCTI or production evidence.

### 11.5 MISP consolidation contract — active bounded gate

Required exact-head repository evidence:

- reviewed upstream baseline **MISP v2.5.44** is recorded;
- MISP remains a separate **AGPL-3.0** service/API boundary and MISP core source is not vendored;
- existing inbound `POST /events/restSearch` and governed outbound `POST /events/add` paths are identified as the capabilities to consolidate;
- MISP event/attribute/object UUIDs remain separate from DTMO canonical UUID identity;
- distribution, sharing-group and TLP/tag restrictions remain attributable and cannot be broadened on re-export;
- import does not grant `share_approved`, publication authority or local-compromise proof;
- outbound delivery requires attributable human DTMO review/share approval;
- service accounts, collectors, schedulers, IntelOwl, OpenCTI and MISP cannot grant DTMO sharing authority;
- destination events remain unpublished and successful `events/add` delivery is not publication/federation approval;
- deterministic replay reservation and `pending`/`success`/`uncertain` semantics prevent blind duplicate replay;
- uncertain delivery blocks automated replay pending operator reconciliation;
- MISP server push/pull synchronization and OpenCTI↔MISP automatic synchronization are excluded from the first consolidation boundary;
- runtime secrets, production HTTPS/certificate validation, least privilege and `401`/`403` fail-closed behavior remain mandatory;
- `README.md`, `docs/README.md`, current state, roadmap, security, QA and evidence index are synchronized;
- `docs/qa/PHASE11_5_MISP_CONSOLIDATION_CONTRACT_GATE.md`, Professional Documentation Gate, Phase 11 MISP Consolidation Contract Gate and all required exact-head workflows succeed on the same final head.

Repository acceptance does not establish live MISP credentials, effective production roles, remote-server trust, lawful live-data sharing, production synchronization/federation behavior, staging acceptance, independent assurance or production authorization.

Only after protected merge may the next bounded Phase 11.5 implementation PR introduce the single reconciled synchronization-state/persistence and authority-enforcement model. Phase 11.6 remains blocked until Phase 11.5 is repository-complete.

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

- ingestion/enrichment/graph/MISP synchronization creates candidate/context intelligence only;
- external sharing requires separate human approval;
- connectors, CI, service accounts and integrated platforms do not gain publication authority;
- IntelOwl analyzer verdicts, OpenCTI graph mappings and MISP event presence do not imply local compromise;
- human and machine roles remain separated;
- framework mappings remain explicit and do not imply blanket compliance;
- provenance, confidence, markings and MISP distribution/sharing restrictions are preserved across service boundaries;
- raw secret values are not committed as evidence;
- external integrations use dedicated identities and bounded scopes.

## Release decision rule

A PR may be merged only when required exact-head workflows for the final head are `completed/success` and the PR remains mergeable. Production authorization requires an explicit accountable Phase 12 `GO`.
