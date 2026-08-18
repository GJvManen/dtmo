# DTMO Production Readiness Checklist

Last reconciled: **2026-08-18**  
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
| Phase 11.1–11.8f | `PASS / REPOSITORY_COMPLETE` | Accepted integration/runtime boundaries |
| Phase 11.8g supply-chain hardening | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Repository supply-chain evidence |
| Phase 11.9–11.11 | `NOT STARTED` | Migration, validation and assurance |
| Phase 12 | `NOT STARTED` | Future production authorization |

Historical Phase 8/9 evidence remains candidate-bound and is not reused for the materially changed Phase 11 integrated candidate.

## Evidence rules

Repository CI, release signing, accountable acceptance, production-equivalent validation, independent assurance and production authorization are separate evidence classes. Missing mandatory evidence is not implicit acceptance.

## 1. Accepted baseline

- [x] Phases 1–7 repository engineering baseline.
- [x] RC13 functional owner acceptance.
- [x] E8.1–E8.10 repository-complete product evolution.
- [x] Historical Phase 8 and Phase 9 evidence preserved in original scope.
- [x] Phase 10 decision remains `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.
- [x] Phase 11.1–11.7b service/integration boundaries accepted.
- [x] Phase 11.8a–11.8f runtime foundation through recovery hardening accepted.
- [x] Human publication/share authority, separate TheHive case authority, provenance, RBAC and fail-closed evidence remain preserved.

## 2. Active Phase 11.8g — software supply-chain hardening

- [x] Exact PR-head checkout is defined.
- [x] Wheel build and SHA-256 identity are defined.
- [x] Python CycloneDX SBOM and dependency vulnerability evidence are defined.
- [x] Candidate container build, HIGH/CRITICAL vulnerability gate and CycloneDX SBOM are defined.
- [x] Release workflow defines short-lived OIDC-backed signed provenance and SBOM attestations.
- [x] Long-lived signing keys are excluded from repository configuration.
- [x] Administration, security, governance, operations, QA, evidence, roadmap, current-state and portal documentation are reconciled.
- [ ] Dedicated Phase 11 Supply Chain Hardening Gate green on final exact head.
- [ ] RC4 Quality Gate green on final exact head.
- [ ] Professional Documentation Gate green on final exact head.
- [ ] All other required exact-head regression gates green.
- [ ] Protected merge with expected-head protection.

### Explicitly deferred

- [ ] Capacity/resource planning and measurable saturation boundaries.
- [ ] Upgrade and rollback procedures with exercised evidence.
- [ ] Phase 11.9 migration/compatibility.
- [ ] Fresh Phase 11.10 production-equivalent validation.
- [ ] Fresh Phase 11.11 independent external assurance.
- [ ] Phase 12 formal production GO/NO-GO.

## 3. Fail-closed release conditions

A candidate claiming Phase 11.8g compliance is blocked when the exact artifact digest, required SBOM, vulnerability evidence or required release attestation cannot be established for that subject. A rebuilt artifact is not assumed equivalent to a previously accepted binary.

## 4. Service and authority boundaries

Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate service/licensing boundaries. Supply-chain metadata, signatures and CI execution grant no publication/share, case-handoff or responder authority and do not prove local compromise.

## Current release decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.8f are `PASS / REPOSITORY_COMPLETE`. Phase 11.8g is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. DTMO is not production authorized. Phase 12 is `NOT STARTED`.**
