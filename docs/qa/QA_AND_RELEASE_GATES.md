# DTMO QA and Release Gates

## Purpose

DTMO uses layered acceptance gates so repository engineering, accountable functional acceptance, deployment-bound validation, independent assurance and production authorization remain separate claims. The model is fail-closed: configured checks or documented intentions are not evidence.

## Core release principles

1. **Exact-head evidence** — pull-request evidence belongs to the exact final PR head.
2. **New commit, new evidence** — a new commit invalidates earlier exact-head CI for that PR.
3. **No inferred PASS** — queued, in-progress, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
4. **Expected-head merge protection** — protected merge must reject a moved head.
5. **Evidence classes remain separate** — CI, owner acceptance, production-equivalent validation, independent assurance and production authorization are not interchangeable.
6. **Historical evidence is immutable** — later lifecycle changes do not rewrite original evidence claims.
7. **One bounded Phase 11 objective per PR** — unrelated work is not stacked behind red CI.
8. **Professional documentation is a merge criterion** — code/integration work cannot merge when affected authoritative documentation or documentation-contract tests are stale.

## Current acceptance status

| Stage | Status |
|---|---|
| Phases 1–7 | `PASS` |
| RC13 functional console | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | `PASS / OWNER_ACCEPTED` — historical candidate |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` — historical candidate |
| Phase 10 | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11 | `IN PROGRESS / ACTIVE` |
| Phase 11.1–11.7b | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8a runtime foundation | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.9 migration/compatibility | `NOT STARTED` |
| Phase 11.10 production-equivalent validation | `NOT STARTED` |
| Phase 11.11 independent external assurance | `NOT STARTED` |
| Phase 12 | `NOT STARTED` |

DTMO is not production authorized.

## Gate families

| Gate family | Primary objective | Evidence boundary |
|---|---|---|
| Build & quality | Packaging, lint, typing, tests | Repository CI |
| Security & identity | Authentication, authorization, privileged actions, secrets | Repository CI + later deployed validation/assurance |
| Data integrity & recovery | Migration, persistence, integrity and recovery | Repository CI + later deployed validation/assurance |
| Connector reliability | Contract/state/retry/timeout/replay/provenance/failure isolation | Repository CI + later deployed validation |
| Governance | Mapping truth and authority separation | Repository CI + governance review |
| Platform integration | API/data-model interoperability and service-boundary controls | Phase 11 repository evidence |
| Integrated runtime | Kubernetes/Helm/GitOps, secrets, network, HA/recovery, observability, supply chain | Phase 11 repository + later deployed evidence |
| Independent assurance | Independent assessment of integrated candidate | Phase 11.11 external assurance |
| Production decision | Formal accountable go/no-go for integrated candidate | Phase 12 |

## Accepted Phase 11.1–11.7b boundaries

Taranis AI, IntelOwl, OpenCTI, MISP, TheHive and Cortex repository integration boundaries are accepted as `PASS / REPOSITORY_COMPLETE`. Their accepted contracts remain regression-protected and do not become deployment or production evidence.

The original Phase 11.7 Cortex no-adoption decision remains a historical accepted baseline. The later owner-required Phase 11.7b analyzer connector is a separate accepted repository boundary.

## Active Phase 11.8a runtime foundation gate

Required exact-head repository evidence:

- Helm chart renders the DTMO application workload from reviewed Git state;
- an immutable image digest is mandatory and mutable tag-only deployment is rejected;
- GitOps values contain non-secret desired state only;
- runtime configuration consumes an existing Kubernetes Secret and does not embed secret material in manifests;
- workload runs non-root with read-only root filesystem and dropped Linux capabilities;
- automatic service-account token mounting is disabled;
- readiness/liveness probes and explicit resources are present;
- a PodDisruptionBudget protects the stateless application workload;
- NetworkPolicy is fail-closed/default-deny and external egress requires explicit CIDR allowlisting;
- accepted service-to-service licensing, provenance, RBAC and human-authority boundaries remain unchanged;
- architecture, administration, operations, current-state, QA, evidence, roadmap, README/docs portal and applicable security/governance documentation remain synchronized;
- `docs/qa/PHASE11_8_RUNTIME_FOUNDATION_GATE.md`, Professional Documentation Gate, RC4 Quality Gate and the dedicated Phase 11 Runtime Foundation Gate succeed on the same exact head.

Repository acceptance does **not** establish target-cluster admission behavior, cloud IAM/workload identity, live secret-provider permissions, ingress/TLS, stateful/multi-zone HA, centralized observability, backup/recovery objectives, SBOM/scanning/signing/attestation, capacity, exercised upgrade/rollback, production-equivalent validation, independent assurance or production authorization.

## Subsequent bounded Phase 11.8 slices

After protected 11.8a acceptance, continue one bounded PR at a time for:

1. workload identity/external secrets plus ingress/TLS and finer network segmentation;
2. stateful/multi-zone HA and failure/disruption controls;
3. centralized metrics/logs/traces and operational alerting;
4. backup/recovery objectives and exercised restore evidence;
5. supply-chain SBOM/scanning/signing/attestation;
6. capacity, upgrade and rollback procedures with exercised evidence.

The exact split may be refined only while preserving one bounded objective per PR and the fixed Phase 11 order.

## Phase 11.9 migration and compatibility

Required evidence includes migration correctness/rollback and preservation of canonical intelligence, provenance, classification, governance and accepted service identities.

## Phase 11.10–11.11 integrated validation and assurance

The integrated candidate must receive fresh production-equivalent validation and fresh independent external assurance against the same immutable deployment identity. Prior Phase 8/9 evidence remains historical and cannot satisfy these gates.

## Phase 12 production-decision model

Phase 12 is `NOT STARTED`. It requires accepted Phase 11.10/11.11 evidence plus production-specific ownership, IAM/secrets/network/recovery/monitoring/privacy/legal/change approvals. Missing mandatory evidence, unresolved release-blocking findings or release-identity mismatch remains `NO-GO / BLOCKED`.

## Security and authority invariants

Release gates preserve:

- external sharing requires separate human approval;
- TheHive case handoff requires separate human approval;
- connectors, CI, Kubernetes service accounts and integrated platforms do not gain publication/share or case-handoff authority;
- enrichment/graph/exchange/case state does not itself imply local compromise;
- human and machine roles remain separated;
- provenance, confidence, markings and source restrictions remain preserved across service boundaries;
- raw secret values are not committed as evidence;
- external services remain separate identities and licensing/provider boundaries.

## Release decision rule

A PR may be merged only when all required exact-head workflows for the final head are `completed/success` and the PR remains mergeable. Production authorization requires an explicit accountable Phase 12 `GO`.