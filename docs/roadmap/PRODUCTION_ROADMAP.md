# DTMO Production Readiness Roadmap

## Purpose

This roadmap separates repository-controlled engineering acceptance, functional product acceptance and external staging/assurance/production approval. A phase is complete only when its own evidence boundary is satisfied.

## Current status — 2026-08-12

| Phase | Scope | Status |
|---|---|---|
| 1 | CI and workflow integrity | `PASS` |
| 2 | Application security and identity | `PASS` |
| 3 | Data integrity and recovery | `PASS` |
| 4 | Connector reliability and provenance | `PASS` |
| 5 | Performance and scalability | `PASS` |
| 6 | Accessibility and operational UX | `PASS` |
| 7 | Observability and incident operations | `PASS` |
| RC13 | Functional unified-console acceptance | `AWAITING_OWNER_RETEST_AFTER_REPAIR` |
| 8 | Real staging acceptance | `PAUSED_PENDING_RC13_OWNER_RETEST` |
| 9 | Independent external assurance | `NOT COMPLETE` |
| 10 | Production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

## RC13 — current acceptance gate

RC13.1–RC13.5 and earlier owner acceptance remain historical evidence. Subsequent accountable owner testing controls the current decision.

### Completed repair sequence

1. PR #159 repaired refresh behavior, empty-data truthfulness, Chrome interactions, Administration clarity and graph empty states.
2. PR #160 repaired Compose runtime packaging for the Grafana reader provisioner.
3. PR #161 repaired Grafana datasource provisioning and added a real Grafana runtime health gate.
4. PR #163 repaired the source catalog secret-reference/bootstrap contract and was later owner-observed with bootstrap 200.
5. PR #165 repaired the local object-store credential contract and merged as `65440afea6cfa3c3300b25d577d746432cc95700`.
6. PR #167 repaired canonical connector commit visibility and merged as `e9a0926f9e13b603be759a7d7036058685ebc3cc`.
7. PR #169 repaired supported-source normalization; final exact head `53aaa670c75a2f404337620bcf1a8df172efe583` completed every returned workflow successfully and merged as `4d182879d851cd22d22ff4f0bab795ed49ee0c1b`.

### PR #169 repository evidence

The repair:

- normalizes only supported alias `security-advisory` to canonical `advisory`;
- leaves canonical values unchanged and unknown values fail-closed;
- canonicalizes NVD CVEs to stable NVD HTTPS detail URLs while retaining upstream references in raw evidence;
- preserves the canonical HTTP(S)-only URL policy;
- preserves #167 commit-before-success behavior;
- keeps source adapter, connector persistence, source-to-intelligence and graphical dashboard regression coverage.

The initial #169 matrix exposed a README-only governance regression. Commit `53aaa670c75a2f404337620bcf1a8df172efe583` restored the required Apache/governance entry points; the complete final exact-head matrix then passed.

After merge, connector status handling created three additional commits on `main`, including an immediately restored README write. Compare merge `4d182879d851cd22d22ff4f0bab795ed49ee0c1b` to current repaired head `1fd006b8568a53c1171b9d127d50037ad0027568` returns `files: []`; no repository content differs from the #169 merge.

### Remaining RC13 acceptance

The accountable project owner must retest current `main` and verify:

1. NVD runs complete without FTP canonical/provenance validation failure;
2. supported advisory sources complete without enum mismatch;
3. raw evidence persists;
4. canonical intelligence is durably committed to PostgreSQL;
5. recent Intelligence appears in the canonical console;
6. Overview KPIs and dashboard metrics update truthfully;
7. native severity/source/trend/review graphics render from the ingested dataset;
8. `Alles vernieuwen`, Chrome navigation/operator controls, governed Administration and true empty states remain correct;
9. authorization, human review and separate external-share approval boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

## Documentation lineage

PR #168 was closed unmerged because newer owner evidence superseded its post-#167 reconciliation. Branch-only RUN-205 never became authoritative. RUN-206 remains immutable. RUN-207 records post-#169 repository acceptance and the owner-retest transition.

## Phase 8 — paused external staging gate

Issue #158 remains open but paused. No Phase 8 evidence may advance until explicit owner acceptance of RC13. After successful owner acceptance, Phase 8 may return to `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`.

Repository CI, Docker Compose and staging emulators cannot substitute for real staging or owner functional acceptance.

## Phase 9 — external assurance

Phase 9 covers independent penetration testing, representative load/stress validation, production-equivalent restoration, platform hardening, secrets-management acceptance and required operational/stakeholder approval.

## Phase 10 — production decision

Phase 10 is the formal production go/no-go and begins only after all prior gates are complete and reviewable.

## Exactly one next priority

**Run the accountable owner functional retest under issue #150 on current `main`.**
