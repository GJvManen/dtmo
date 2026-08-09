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

- Phase 1–5 internal roadmap gates: `PASS`.
- Phase 6: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA evidence on supported real hosts.
- Phase 7: `IN PROGRESS` with RC10.1, RC10.2 and RC10.3 accepted.
- Phase 8: `NOT STARTED`.
- Phase 9: `NOT COMPLETE`.
- Phase 10: `NOT STARTED`.

## Accepted Phase 7 gates

### RC10.1 request observability — `PASS`

PR #80 exact head `01a175e12da7c8af8566178a2d7e6b34a57d58bc` completed 34/34 workflows. Artifact `9040196394`, digest `sha256:6792020994d94b0484cb84140d202433303eceb82565f8598ffd5937940531d6`; JUnit 5/5; merge `1675d88bb24dcd50e20545f49b26dd7cc2810d97`.

### RC10.2 controlled connector-failure alerting — `PASS`

PR #82 exact head `b38aeae44588e39e35339f4c4d9667947804b243` completed 35/35 workflows. Artifact `9040485255`, digest `sha256:96883158cfd790c3c6b21c2db819acbcbc03d431d4dd79bb32038b6ff258de25`; JUnit 4/4; merge `f6680423860389288d9feced34592294d774bf4a`.

### RC10.3 bounded queue-backlog alerting — `PASS`

PR #84 exact head `8058b476298eee4bcd2942d9cca54384ec12aa74` completed 36/36 workflows. Artifact `9040996591`, digest `sha256:42aaad1424d7c1ad40accd056b4746ea6fb328a561b24df5ebc293c0425b1910`; 80% raise/50% clear hysteresis, bounded queue metrics, structured correlation, actionable guidance and RC8 queue-pressure reuse; JUnit 5/5; merge `42ccbe04cbc1081f93e4a155243627b5a3038573`.

RC10.2/RC10.3 do not claim external notification delivery. RC10.3 does not claim a separate deployed durable queue service. Storage-integrity, API-error and search-health alerting remain open.

## Workflow presence versus workflow evidence

Workflow configuration on `main` is not itself acceptance evidence. DTMO requires a bounded gate, execution on the exact final head, successful completion of every registered workflow, retained-evidence inspection when specified, expected-head protected merge, and documentation reconciliation without claim inflation.

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

Issue #1 remains authoritative for independent/external production gates. Internal PASS does not close those external gates.

## Current reconciliation gate

RUN-20260809-128 is `PASS` only in the final protected merged state after the final status-bearing exact head completes all 36 workflows. The first complete documentation head `118d10c7b3ac971176fb7390499397049d7b4269` already completed 36/36 successfully.

## Exactly one next priority

Phase 7 / RC10.4 — implement bounded storage-integrity alerting with controlled integrity-failure/recovery evidence, actionable correlation, no raw sensitive payload leakage and retained exact-head evidence. API-error and search-health alerting remain later objectives.
