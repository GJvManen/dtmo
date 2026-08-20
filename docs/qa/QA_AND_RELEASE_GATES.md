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
9. **External evidence remains external** — repository fixtures, emulators and CI artifacts cannot be promoted to production-equivalent observations.

## Current acceptance status

| Stage | Status |
|---|---|
| Phases 1–7 | `PASS` |
| RC13 functional console | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 10 | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11 | `IN PROGRESS / ACTIVE` |
| Phase 11.1–11.7b | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8 integrated runtime industrialisation | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.9 migration/compatibility | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10 production-equivalent validation | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` |
| Phase 11.11 independent external assurance | `NOT STARTED` |
| Phase 12 | `NOT STARTED` |

DTMO is **not production authorized**.

## Gate families

| Gate family | Primary objective | Evidence boundary |
|---|---|---|
| Build & quality | Packaging, lint, typing, tests | Repository CI |
| Security & identity | Authentication, authorization, privileged actions, secrets | Repository CI + deployed validation/assurance |
| Data integrity & recovery | Migration, persistence, integrity and recovery | Repository CI + deployed validation/assurance |
| Connector reliability | Contract/state/retry/timeout/replay/provenance/failure isolation | Repository CI + deployed validation |
| Governance | Mapping truth and authority separation | Repository CI + governance review |
| Platform integration | API/data-model interoperability and service-boundary controls | Phase 11 repository evidence |
| Integrated runtime | Kubernetes/Helm/GitOps, secrets, network, HA/recovery, observability, supply chain | Phase 11 repository + deployed evidence |
| Production-equivalent validation | Same-candidate live exercise of migration, upgrade, rollback, health, saturation and recovery | Phase 11.10 real-environment evidence |
| Independent assurance | Independent assessment of integrated candidate | Phase 11.11 external assurance |
| Production decision | Formal accountable go/no-go for integrated candidate | Phase 12 |

## Accepted Phase 11.1–11.9 boundaries

Taranis AI, IntelOwl, OpenCTI, MISP, TheHive and Cortex repository integration boundaries are accepted as `PASS / REPOSITORY_COMPLETE`. The original Phase 11.7 Cortex no-adoption decision remains a historical accepted baseline; the later owner-required analyzer connector is a separate accepted boundary.

Phase 11.8 is repository-complete across runtime foundation, workload identity/external secrets, ingress/TLS/network segmentation, HA/disruption, observability, backup/recovery, software supply-chain hardening, capacity/resource planning and upgrade/rollback controls. Phase 11.9 is repository-complete for the connected migration graph, forward-first sequencing and compatibility rules.

These accepted gates remain regression-protected and do not become live deployment or production evidence by themselves.

## Active Phase 11.10 production-equivalent validation gate

### Entry criteria

- Phase 11.1–11.9 remain accepted.
- One approved production-equivalent environment is identified.
- One immutable integrated candidate identity is available.
- Exact candidate and prior application image digests are known.
- Expected migration head and deployment revision are known.
- Monitoring, logs and audit/correlation are available to authorized reviewers.
- No production credential reuse or unsanitized production-data use occurs unless separately authorized.

### Required evidence classes

The complete package must include fresh external evidence for:

1. immutable candidate identity;
2. migration/compatibility;
3. upgrade;
4. rollback to the exact approved prior immutable digest;
5. health/readiness;
6. representative saturation/capacity behavior;
7. recovery/continuity.

Every evidence item must bind to the same candidate fingerprint and environment. Rollback must include successful post-rollback health evidence and must not automatically down-migrate the database.

### Repository controls

The repository supplies:

- `tools/phase11_production_equivalent_validation.py` for deterministic candidate fingerprinting and manifest validation;
- `backend/tests/test_phase11_10_production_equivalent_validation.py` for fail-closed contract coverage;
- `.github/workflows/phase11-production-equivalent-validation.yml` for repository-side contract evidence;
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md` for accountable execution;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json` as the external metadata template;
- this gate and the Evidence Index for review boundaries.

The template is intentionally invalid until real evidence replaces all placeholders. A validator PASS establishes metadata consistency only; reviewers must inspect the referenced external evidence.

### Fail-closed conditions

Phase 11.10 is blocked when:

- candidate/environment identity is missing or ambiguous;
- an image is identified only by a mutable tag;
- any required evidence class is missing or not `PASS`;
- evidence references are placeholders, historical Phase 8/9 records, repository CI only, emulators, synthetic fixtures or localhost observations;
- candidate fingerprints differ across evidence classes;
- rollback targets anything other than the exact prior immutable application digest;
- post-rollback health is missing or failed;
- release-blocking findings remain open;
- deviations lack accountable disposition;
- reviewer/observer/timestamp attribution is incomplete.

### Acceptance

Phase 11.10 becomes `PASS / OWNER_ACCEPTED` only after the complete external evidence package is reviewed and explicitly accepted by the accountable owner. Repository-green status alone cannot complete Phase 11.10.

## Phase 11.11 independent external assurance

**Status:** `NOT STARTED`.

Phase 11.11 may start only after Phase 11.10 acceptance and must assess the same immutable integrated candidate. A material candidate change requires a new Phase 11.10 evidence binding first. Historical Phase 9 assurance cannot satisfy this gate.

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
- raw secret values, TLS private keys and long-lived signing keys are not committed as evidence;
- network reachability does not grant application or human authority;
- signed artifact provenance does not grant production authorization;
- external services remain separate identities and licensing/provider boundaries.

## Release decision rule

A PR may be merged only when all required exact-head workflows for the final head are `completed/success` and the PR remains mergeable. Production authorization requires an explicit accountable Phase 12 `GO`.
