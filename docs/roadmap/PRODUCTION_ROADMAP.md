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
| RC13 | Functional unified-console acceptance | `REOPENED / BLOCKED_INTERNAL` |
| 8 | Real staging acceptance | `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST` |
| 9 | Independent external assurance | `NOT COMPLETE` |
| 10 | Production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

## RC13 — current reopened gate

RC13.1–RC13.5 and earlier owner acceptance remain historical evidence. Subsequent accountable owner testing controls the current decision.

### Completed repair sequence

1. PR #159 repaired refresh behavior, empty-data truthfulness, Chrome interactions, Administration clarity and graph empty states.
2. PR #160 repaired Compose runtime packaging for the Grafana reader provisioner.
3. PR #161 repaired Grafana datasource provisioning and added a real Grafana runtime health gate.
4. PR #163 repaired the source catalog secret-reference/bootstrap contract and was later owner-observed with bootstrap 200.
5. PR #165 repaired the local object-store credential contract and merged as `65440afea6cfa3c3300b25d577d746432cc95700`.
6. PR #167 repaired canonical connector commit visibility; exact head `bf18ef2c499edcf8399d1f91b80190937538fdce` completed every returned workflow successfully and merged as `e9a0926f9e13b603be759a7d7036058685ebc3cc`.

### Latest owner evidence

The post-#167 owner retest confirms local runtime startup and demonstrates multiple successful OpenSearch `201 Created` writes into `dtmo-intelligence-v1`. The source-to-interface flow nevertheless remains unaccepted because supported records can still fail canonical normalization:

- NVD can expose `ftp://` references that are not valid canonical/provenance `HttpUrl` values;
- supported advisory adapters can emit `security-advisory`, which is not a member of the persisted canonical `IntelligenceType` enum.

This is narrower than the #167 blocker: the commit path now progresses, but not every supported source record can cross the canonical ingest contract.

### Current bounded repair

Branch `rc13/source-record-normalization-contract`:

- normalizes the explicit supported alias `security-advisory` to canonical `advisory`;
- leaves canonical values unchanged and unknown values fail-closed;
- canonicalizes NVD CVEs to their stable NVD HTTPS detail URL while retaining upstream non-HTTP references only in raw evidence;
- preserves the canonical HTTP(S)-only URL policy;
- preserves #167 commit-before-success behavior;
- adds a dedicated exact-head source-record-normalization gate covering source adapters, connector persistence, source-to-intelligence and graphical dashboard contracts.

No repository PASS is claimed until every returned workflow on the final exact PR head is `completed/success`.

### Remaining RC13 acceptance after repair

The accountable project owner must retest current merged `main` and verify:

1. NVD runs complete without FTP URL validation failure;
2. supported advisory sources complete without enum mismatch;
3. raw evidence persists;
4. canonical intelligence is durably committed to PostgreSQL;
5. recent Intelligence appears in the canonical console;
6. Overview KPIs and dashboard metrics update truthfully;
7. native severity/source/trend/review graphics render from the ingested dataset;
8. refresh, Chrome navigation/operator controls, governed Administration and true empty states remain correct;
9. authorization/publication boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

## Documentation lineage

PR #168 was closed unmerged because the newest owner retest superseded its post-#167 reconciliation. Branch-only RUN-205 never became authoritative. RUN-204 remains immutable; RUN-206 records the current owner evidence.

## Phase 8 — paused external staging gate

Issue #158 remains open but paused. No Phase 8 evidence may advance while RC13 is blocked. After successful owner acceptance, Phase 8 may return to `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`.

Repository CI, Docker Compose and staging emulators cannot substitute for real staging or owner functional acceptance.

## Phase 9 — external assurance

Phase 9 covers independent penetration testing, representative load/stress validation, production-equivalent restoration, platform hardening, secrets-management acceptance and required operational/stakeholder approval.

## Phase 10 — production decision

Phase 10 is the formal production go/no-go and begins only after all prior gates are complete and reviewable.

## Exactly one next priority

**Complete the supported-source normalization repair, require complete exact-head CI, merge, then resume accountable owner functional retesting under issue #150.**
