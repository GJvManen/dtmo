# DTMO Production Readiness Checklist

Last reconciled: **2026-08-17**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

This checklist controls the post-Phase-10 industrialisation programme and future Phase 12 production authorization decision.

## Current lifecycle status

| Stage | Status | Evidence class |
|---|---|---|
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` | Repository product evolution |
| Phase 8 | `PASS / OWNER_ACCEPTED` | Historical accountable staging acceptance |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` | Historical independent assurance |
| Phase 10 | `NO-GO / BLOCKED` | Accountable production decision |
| Phase 11 | `IN PROGRESS / ACTIVE` | Platform industrialisation |
| Phase 11.1–11.7b | `PASS / REPOSITORY_COMPLETE` | Accepted service/integration boundaries |
| Phase 11.8a runtime foundation | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Repository runtime foundation evidence |
| Phase 11.9–11.11 | `NOT STARTED` | Migration, validation and assurance |
| Phase 12 | `NOT STARTED` | Future production authorization |

Historical Phase 8/9 evidence remains candidate-bound and is not reused for the materially changed Phase 11 integrated candidate.

## Evidence rules

Repository CI, accountable acceptance, production-equivalent validation, independent assurance and production authorization are separate evidence classes. Missing mandatory evidence is not implicit acceptance.

## 1. Accepted historical baseline

- [x] Phases 1–7 repository engineering baseline.
- [x] RC13 functional owner acceptance.
- [x] E8.1–E8.10 repository-complete product evolution.
- [x] Phase 8 acceptance for the earlier candidate.
- [x] Phase 9 independent assurance for the earlier candidate.
- [x] Phase 10 production decision recorded as `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.

## 2. Accepted Phase 11.1–11.7b baseline

- [x] Taranis service/API/licensing boundary and canonical adapter accepted.
- [x] IntelOwl bounded enrichment integration accepted.
- [x] OpenCTI graph integration accepted.
- [x] MISP consolidation and authoritative synchronization-state model accepted.
- [x] TheHive minimal human-authorized case handoff accepted.
- [x] Original Phase 11.7 Cortex no-adoption decision preserved as historical evidence.
- [x] Later owner-required Phase 11.7b analyzer connector accepted separately.
- [x] Human publication/share authority remains distinct from technical service execution.
- [x] Provenance, RBAC and fail-closed evidence rules remain preserved.

**Decision:** `PASS / REPOSITORY_COMPLETE`.

## 3. Active Phase 11.8a — governed runtime foundation

- [x] Helm chart and GitOps-owned values added.
- [x] Immutable container image digest required.
- [x] Runtime configuration references an existing Secret; secret material is not stored in Git.
- [x] Pod runs non-root with read-only root filesystem and dropped capabilities.
- [x] Service-account token automounting disabled.
- [x] Readiness/liveness probes and resource defaults defined.
- [x] PodDisruptionBudget defined for the application workload.
- [x] Default-deny/fail-closed NetworkPolicy enabled.
- [x] External egress requires explicit CIDR allowlisting.
- [x] Architecture, administration, operations, QA, roadmap, current-state, evidence and portal documentation added/reconciled.
- [ ] Dedicated Phase 11 Runtime Foundation Gate green on final exact head.
- [ ] RC4 Quality Gate green on final exact head.
- [ ] Professional Documentation Gate green on final exact head.
- [ ] All other required exact-head regression gates green.
- [ ] PR protected-merged with expected-head protection.

### Explicitly deferred to later bounded Phase 11.8 slices

- [ ] Workload identity/external-secret provider implementation.
- [ ] Ingress/TLS and finer inter-service network segmentation.
- [ ] Stateful/multi-zone HA and disruption/failure exercises.
- [ ] Centralized metrics, logs, traces and service-level alerting.
- [ ] Backup/recovery objectives and exercised restore evidence.
- [ ] SBOM, vulnerability scanning, signing and attestation.
- [ ] Capacity, upgrade and rollback procedures with exercised evidence.

## 4. Service and authority boundaries

- [x] Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate service/licensing boundaries.
- [x] Kubernetes scheduling does not grant publication/share authority.
- [x] TheHive case-handoff authority remains separate and human-controlled.
- [x] Connector/service output does not itself prove local compromise.
- [x] Repository CI is not represented as target-cluster or production evidence.

## 5. Phase 11.9 — Migration and compatibility

- [ ] Canonical intelligence/provenance/classification/governance migration tested.
- [ ] Existing integration disposition documented with replacement and rollback paths.

## 6. Phase 11.10–11.11 — New validation and assurance

- [ ] One immutable integrated deployment identity established.
- [ ] New production-equivalent validation complete.
- [ ] New independent external assurance complete.
- [ ] Release-blocking findings remediated/retested or formally dispositioned.

## 7. Phase 12 — Formal production GO/NO-GO

- [ ] Phase 11 validation and assurance accepted.
- [ ] Production ownership, IAM/secrets/network, recovery, monitoring/support and privacy/legal/governance approvals recorded.
- [ ] Formal accountable `GO` or `NO-GO / BLOCKED` decision recorded.

## Current release decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.7b are `PASS / REPOSITORY_COMPLETE`. Phase 11.8a is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. DTMO is not production authorized. Phase 12 is `NOT STARTED`.**