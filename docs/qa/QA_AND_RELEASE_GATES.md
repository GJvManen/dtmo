# DTMO QA and Release Gates

## Purpose

Every DTMO development step defines and evaluates explicit quality gates. A configured, queued, cancelled, failed or committed test that has not executed successfully on the required exact head is never `PASS`.

## Baseline blocking gates

| Domain | Blocking evidence |
|---|---|
| Build | Source compiles and required packages resolve |
| Unit and regression tests | New and affected logic executes successfully |
| Security | Authentication, authorization, secrets and input controls are verified |
| Governance | Human review, share approval and separation of duties are preserved |
| Data integrity | Provenance, confidence, constraints and migrations are verified |
| Privacy | Direct identifiers, purpose limitation, retention and legal holds are verified |
| Recovery | Clean targets restore or reconstruct successfully with integrity and timing evidence |
| Connector reliability | Live canary, persistent state, health history, isolation, provenance, governed contracts, retry, timeout, replay and quarantine recovery are evidenced |
| Performance | Accepted workload profile plus executed latency, throughput, error, integrity and resource evidence |
| Accessibility / UX | Critical journeys, keyboard, responsive, supported-browser and bounded accessibility evidence succeed; genuine AT remains separately evidenced |
| Observability | Correlated structured telemetry, bounded metrics and controlled alerting evidence succeed |
| Operations | Runbooks, alert exercises, ownership/escalation and handover evidence succeed |
| Release | All release-critical exact-head jobs and required retained evidence artifacts succeed |

## Current phase status — 2026-08-09

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — live connector reliability and provenance: `PASS` for internal roadmap gates.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates.
- Phase 6 — frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA evidence on supported real hosts.
- Phase 7 — observability and incident operations: `IN PROGRESS`.
- Phase 8 — staging acceptance: `NOT STARTED`.
- Phase 9 — external assurance: `NOT COMPLETE`.
- Phase 10 — production go/no-go: `NOT STARTED`.

## Accepted Phase 5 gates

RC8.1–RC8.8 are accepted for their bounded internal scopes. RC8.8 does **not** certify production capacity. Issue #1's independent representative production load/stress gate remains open and separate.

## Phase 6 gate status

RC9.1–RC9.15 contain accepted bounded browser/accessibility evidence. RC9.16 records the remaining real assistive-technology requirement. Phase 6 remains `BLOCKED_EXTERNAL` until genuine VoiceOver/NVDA behavior is retained from supported real host/browser/screen-reader combinations. Browser/DOM automation is not accepted as a substitute.

## Accepted Phase 7 gates

### RC10.1 request observability — `PASS`

PR #80 exact head `01a175e12da7c8af8566178a2d7e6b34a57d58bc` completed all 34 registered workflows successfully. Retained artifact `9040196394`, digest `sha256:6792020994d94b0484cb84140d202433303eceb82565f8598ffd5937940531d6`, independently evidenced safe correlation IDs, real structured request context, bounded route-template metrics, latency and in-flight metrics. JUnit: 5/5. Merge: `1675d88bb24dcd50e20545f49b26dd7cc2810d97`.

### RC10.2 controlled connector-failure alerting — `PASS`

PR #82 exact head `b38aeae44588e39e35339f4c4d9667947804b243` completed all 35 registered workflows successfully. Retained artifact `9040485255`, digest `sha256:96883158cfd790c3c6b21c2db819acbcbc03d431d4dd79bb32038b6ff258de25`, independently evidenced terminal failure signaling, Prometheus alert metric/rule, safe correlation evidence, actionable operator guidance, raw-error exclusion, repeat-raise suppression and successful recovery/clear behavior. JUnit: 4/4. Merge: `f6680423860389288d9feced34592294d774bf4a`.

### RC10.3 bounded queue-backlog alerting — `PASS`

PR #84 exact head `8058b476298eee4bcd2942d9cca54384ec12aa74` completed all 36 registered workflows successfully. Retained artifact `9040996591`, digest `sha256:42aaad1424d7c1ad40accd056b4746ea6fb328a561b24df5ebc293c0425b1910`, independently evidenced bounded queue identifiers, queue depth/capacity/utilization metrics, 80% raise/50% clear hysteresis, safe correlation evidence, actionable operator guidance, accepted RC8 queue-pressure reuse and observer-only behavior. JUnit: 5/5. Merge: `42ccbe04cbc1081f93e4a155243627b5a3038573`.

RC10.2/RC10.3 do not claim pager/e-mail/chat delivery. RC10.3 does not claim a separate deployed durable queue service. Storage-integrity, API-error and search-health alerting remain open Phase-7 objectives.

## Workflow presence versus workflow evidence

Workflow configuration on `main` is not itself acceptance evidence. DTMO's release discipline requires:

1. a defined bounded gate;
2. execution on the exact final pull-request head;
3. successful completion of every registered required workflow;
4. inspection of retained evidence when specified;
5. expected-head protected merge;
6. documentation reconciliation without inflating the accepted claim.

Missing, queued, cancelled, failed or unexecuted workflows are not PASS.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- publication requires explicit human share approval by a principal different from the reviewer;
- service accounts and connectors may not review or approve sharing;
- connector, queue, recovery, replay, retry, timeout, performance or observability success never implies publication approval;
- provenance and confidence may not be silently discarded;
- secret or sensitive payload values may not be emitted into evidence;
- performance and controlled-failure fixtures must use synthetic or explicitly approved non-production data;
- missing or incomplete evidence blocks the corresponding acceptance claim.

## External assurance boundary

Issue #1 remains authoritative for independent/external production gates, including representative load/stress, penetration testing, full backup/restoration exercise, production OpenSearch hardening, staging/deployment acceptance, secrets-management acceptance where applicable and required operational/stakeholder approvals.

Internal PASS does not close those external gates.

## Current reconciliation gate

RUN-20260809-128 is `CI_VALIDATION_PENDING`. RC10.3 product acceptance is already `PASS` and merged, but the authoritative documentation update must independently complete all 36 registered workflows on its final exact head before protected merge.

## Exactly one next priority

Complete RUN-128 exact-head CI and protected merge. After that, Phase 7 / RC10.4 — implement bounded storage-integrity alerting with controlled integrity-failure/recovery evidence, actionable correlation, no raw sensitive payload leakage and retained exact-head evidence. API-error and search-health alerting remain later objectives.
