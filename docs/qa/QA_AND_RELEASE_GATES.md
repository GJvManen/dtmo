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
9. **Professional documentation is a merge criterion** — code/integration work cannot merge when affected authoritative documentation or documentation contract tests are stale.

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
| Phase 11.1 | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.2 | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 IntelOwl contract | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 IntelOwl adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 governed execution/persistence | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 12 | `NOT STARTED` |

DTMO is not production authorized.

## Repository-controlled evidence

The existing workflow portfolio remains required for DTMO code touched during Phase 11. New integrations add bounded contracts and integration/runtime tests rather than weakening existing controls.

The **`Phase 11 IntelOwl Integration Contract Gate`** is the dedicated IntelOwl synchronization gate. For the active slice it validates the accepted contract and adapter together with governed execution/persistence tests and authoritative lifecycle documentation. Its success is repository engineering evidence only; it does not prove live IntelOwl connectivity, deployment permissions, analyzer quality or production behavior.

The companion `docs/qa/PHASE11_3_INTELOWL_GOVERNED_EXECUTION_GATE.md` defines the bounded execution/persistence acceptance criteria and non-evidence boundary.

## Phase 11 gate sequence

### 11.1 Taranis architecture and gap assessment

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

### 11.2 Taranis canonical adapter

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence includes authenticated read-only service integration, idempotent canonical ingestion, provenance/evidence retention, fail-closed TLP/classification, replay/deduplication, durable checkpointing/reconciliation, bounded detail/CTI retrieval, governed connector execution, degraded/partial failure handling, no publication-authority escalation and fully green exact-head/documentation gates.

### 11.3 IntelOwl contract

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

Accepted contract evidence includes the IntelOwl v6.7-compatible service/API boundary, dedicated non-admin identity, runtime-secret handling, TLS requirement, explicit observable/analyzer allowlists, TLP/privacy disclosure rules, analyzer/job/result provenance, bounded quota/rate-limit/failure semantics, exclusion of IntelOwl external Connectors, no-local-compromise semantics and the AGPL-3.0 service boundary.

### 11.3 IntelOwl adapter

**Repository status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence includes runtime-secret token configuration, production HTTPS and analyzer allowlist validation, approved observable classes, pre-disclosure handling checks, explicit `connectors_requested=[]`, bounded job submission/polling, immutable job identity, maximum result size, unknown-analyzer/malformed-result rejection, partial-success semantics, `429`/timeout behavior and authority metadata that neither proves local compromise nor grants external share/publication authority.

### 11.3 governed execution/persistence — active bounded gate

Required exact-head repository evidence:

- `POST /api/v1/intelowl/items/{item_id}/enrich` is feature-gated and requires `REVIEW_INTELLIGENCE`;
- the current service-account role cannot autonomously invoke the human review endpoint;
- requested analyzers remain constrained to the configured allowlist and are conservatively treated as external disclosure targets;
- `red`, `tlp:red` and `review-required` handling fails closed before external disclosure;
- `GET /api/v1/intelowl/items/{item_id}/history` requires `READ_INTELLIGENCE` and is non-mutating;
- migration `0011_intelowl_enrichment_history` upgrades and downgrades successfully;
- persistence verifies canonical item identity and remains idempotent for `(item_id, job_id)`;
- durable records preserve observable, handling, requested analyzer, status/partial state, attributed reports, upstream job identity and requesting human subject;
- database constraints enforce `external_share_authorized=false` and `local_compromise_proven=false`;
- IntelOwl external Connectors remain excluded through `connectors_requested=[]`;
- no enrichment outcome mutates canonical share approval;
- operational runbook, reviewer workflow, security/trust-boundary, retention/governance, roadmap, evidence-index, README/docs portal and current-state documentation remain synchronized;
- full exact-head CI and Professional Documentation Gate succeed on the same final head.

Repository acceptance does not establish live service-account permissions, provider credentials, analyzer quality, privacy approval, production-equivalent persistence/recovery, independent assurance or production authorization.

### 11.4 OpenCTI

OpenCTI remains blocked until the active 11.3 slice is fully green, merged with expected-head protection and Phase 11.3 is reconciled as repository-complete.

Required evidence includes STIX interoperability, entity identity/deduplication, confidence/marking/provenance preservation, graph synchronization failure handling and no duplicate custom graph authority inside DTMO.

### 11.5 MISP consolidation

Required evidence includes one authoritative inbound/synchronization model, conflict/replay handling, DTMO outbound approval remaining authoritative, distribution/TLP/sharing-group fail-closed behavior and no implicit share authority for automated components.

### 11.6 TheHive / 11.7 Cortex decision

Required evidence includes controlled case handoff with provenance/audit references and a documented Cortex decision based only on an accepted IntelOwl capability gap.

### 11.8 Integrated runtime

Required evidence includes Kubernetes/Helm/GitOps, immutable images, workload identities/external secrets, TLS/network policies, database/queue/storage durability and recovery, centralized observability, SBOM/scanning/signing/attestation, capacity, upgrade and rollback tests.

### 11.9 Migration and compatibility

Required evidence includes migration correctness/rollback, preservation of canonical intelligence/provenance/classification/governance and explicit disposition of existing E8 integrations.

### 11.10–11.11 Integrated validation and assurance

The integrated candidate must receive fresh production-equivalent validation and fresh independent external assurance against the same immutable deployment identity. Prior Phase 8/9 evidence remains historical and cannot satisfy these gates by itself.

## Phase 12 production-decision model

Phase 12 is `NOT STARTED`. It requires accepted Phase 11 validation/assurance plus production-specific approvals. Missing mandatory input, unresolved release-blocking findings, unaccepted residual risk or material release-identity mismatch is `NO-GO / BLOCKED`.

## Security and publication invariants

Release gates must preserve:

- ingestion/enrichment creates candidate/context intelligence only;
- external sharing requires separate human approval;
- connectors, CI, service accounts and integrated publishers do not gain publication authority;
- IntelOwl analyzer verdicts/evaluations do not imply local compromise;
- IntelOwl external Connectors are not enabled merely for enrichment;
- human and machine roles remain separated;
- privileged Administration remains least-privilege and auditable;
- framework mappings remain explicit and do not imply blanket compliance;
- provenance and confidence are preserved across service boundaries;
- raw secret values are not committed as evidence;
- external integrations use dedicated identities and bounded scopes.

## Release decision rule

A PR may be merged only when required exact-head workflows for the final head are `completed/success` and the PR remains mergeable. A lifecycle phase may be accepted only after its additional evidence boundary is satisfied. Production authorization requires an explicit accountable Phase 12 `GO`.
