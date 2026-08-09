# RC8.8 — Capacity Limits and Scaling Guidance

Status: `PASS`

## Objective

Close the final internal Phase-5 documentation gate by converting accepted RC8.1–RC8.7 evidence into conservative capacity and scaling guidance. This document is an engineering operating envelope, not a production sizing claim and not a substitute for issue #1's independent representative load/stress test.

## Evidence basis

The accepted Phase-5 workload contract defines the following synthetic target envelope:

- 250 education organisations;
- 200 analyst/CISO/audit users;
- 50 peak concurrent users;
- 1,000,000 intelligence records;
- 500,000 vulnerability records;
- 5,000,000 IOC records;
- 20,000,000 graph edges;
- 2,000,000 raw-evidence objects / 500 GiB raw evidence;
- 100 API reads/s and 25 API writes/s;
- 40 search requests/s and 10 dashboard requests/s;
- 100 sustained ingestion records/s;
- 250 burst ingestion records/s for 600 seconds;
- connector parallelism 20.

Accepted internal evidence also includes:

- RC8.2: 500/500 API reads successful at 100.142 requests/s, p95 1.878 ms, p99 11.059 ms, 0.0% errors on the bounded CI fixture;
- RC8.5: 250/250 synthetic records accepted under queue/connector burst, queue depth 40/40, 170 backpressure events, zero data loss, zero duplicate candidates, recovery 0.602 s;
- RC8.6: 100/100 records delivered through an injected downstream outage, 20 buffered, zero data loss/duplicate candidates, recovery 1.013 s;
- RC8.7: concurrency 20 observed with 40 reads and 40 unique ingests, read p95 5.876 ms, 0.0% errors and zero data loss on the final accepted exact head.

All figures above are bounded synthetic CI observations. They must not be extrapolated linearly into production capacity.

## Internal capacity limits

Until representative staging and external load/stress evidence exists, DTMO must treat the RC8.1 profile as the maximum *unvalidated production planning envelope*, not as certified production capacity.

The following fail-closed limits apply to planning and pre-production acceptance:

| Dimension | Internal planning ceiling | Action at or above ceiling |
|---|---:|---|
| Peak concurrent users | 50 | scale test environment and run representative load/stress before production approval |
| API reads | 100 req/s | scale API replicas only after database/search dependency headroom is observed |
| API writes | 25 req/s | validate write-path DB saturation and lock/connection pressure |
| Search | 40 req/s | validate OpenSearch heap, shard, latency and rejection metrics |
| Dashboard | 10 req/s | validate aggregate/query fan-out and browser latency |
| Sustained ingestion | 100 records/s | add workers only with queue, DB and search headroom evidence |
| Burst ingestion | 250 records/s for 600 s | backpressure is mandatory; zero loss/duplicate tolerance remains |
| Connector parallelism | 20 | increase only after provider limits and queue recovery remain within budget |
| Queue recovery | <= 900 s after burst | breach is a release/operations blocker until root cause is understood |
| Error rate | <= 1.0% | breach blocks capacity increase |
| Data loss | 0 records | any loss is a blocker |
| Duplicate candidates | 0 records | any duplicate candidate breach is a blocker |

## Resource headroom rules

The accepted workload profile sets pre-production average resource ceilings of 70% API CPU, 75% API memory, 70% PostgreSQL CPU and 75% OpenSearch heap. Production scaling must therefore preserve at least the complementary average headroom at representative load and must also inspect saturation/rejection indicators rather than CPU alone.

A scale-out decision is triggered before a sustained resource ceiling is breached, or earlier when latency/error/queue budgets degrade. Scaling one tier is not accepted if it shifts saturation to PostgreSQL, OpenSearch, object storage or the queue.

## Scaling guidance

1. **API tier:** prefer horizontal stateless replicas behind a health-checked load balancer. Increase replicas only while PostgreSQL connections, search pressure and downstream error rates remain inside observed budgets.
2. **Ingestion workers:** scale horizontally in bounded increments. Preserve idempotency, provenance, deduplication and queue backpressure; worker count must never be used to bypass provider rate limits.
3. **PostgreSQL:** measure connection usage, CPU, I/O latency, locks and slow queries under representative staging load before increasing API/worker concurrency. Capacity changes require backup/recovery invariants to remain intact.
4. **OpenSearch:** production sizing remains externally blocked until security hardening and representative load/stress evidence exist. Validate shard topology, heap, GC, search/index latency and rejected operations before raising search or ingest limits.
5. **Object/raw evidence storage:** size against the 500 GiB planning dataset plus retention, backup and restore requirements. Storage growth must preserve checksum/provenance integrity and immutable raw-evidence controls.
6. **Queue/backpressure:** retain bounded buffering. A queue-depth increase is not a substitute for downstream capacity; recovery must remain within the 900-second contract with zero data loss and zero duplicate candidates.

## Capacity review triggers

Re-run capacity validation when any of the following changes materially:

- peak user or request targets increase by >= 20%;
- ingestion or connector parallelism increases by >= 20%;
- dataset cardinality or raw-evidence storage increases by >= 25%;
- PostgreSQL/OpenSearch topology, versions or major configuration change;
- queue implementation, retry/backoff logic, deduplication or connector scheduling changes;
- latency/error/resource budgets are breached;
- a new high-severity vulnerability/advisory requires performance-relevant mitigation;
- production architecture differs materially from the staging/load-test architecture.

## Security, privacy and governance invariants

Capacity changes cannot weaken RBAC, separation of duties, auditability, provenance, privacy or publication controls. Synthetic load execution must not use production personal data. `reviewed` and `share approved` remain separate states, human share approval remains mandatory, and service accounts may not approve sharing.

## External assurance boundary

This guidance does **not** satisfy or close issue #1's:

- independent representative load/stress test;
- production OpenSearch security/hardening gate;
- staging/production deployment acceptance;
- secrets-manager replacement gate;
- operational acceptance by service owner, CISO/ISO and privacy function.

Representative external testing must determine actual production saturation points and may lower these planning ceilings. It must not raise them without retained evidence and explicit release approval.

## Acceptance evidence

PR #48 exact head `979191a7db64a97e4ccc250ff9a24e6735d63158` completed all 19 registered GitHub Actions workflows successfully. The PR was merged with expected-head protection as `62b34472948d0f301104ddd452e14efb945fa6bd`.

This satisfies the internal Phase-5 blocking requirement that capacity limits and scaling guidance are documented. The internal Phase-5 roadmap gate is therefore `PASS` while issue #1's external load/stress, production OpenSearch hardening, staging, external assurance and production approval gates remain open.

## Decision rule

RC8.8 is `PASS` only for the bounded internal Phase-5 documentation gate described above. No production capacity certification or external assurance is implied.
