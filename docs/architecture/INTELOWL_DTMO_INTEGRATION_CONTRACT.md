# IntelOwl → DTMO Enrichment Integration Contract

Contract date: **2026-08-16**  
Phase: **11.3 — IntelOwl enrichment integration**  
Contract state: **`PASS / REPOSITORY_COMPLETE — ACCEPTED IMPLEMENTATION BASELINE`**

## Purpose

This document defines the accepted bounded service-to-service contract for introducing IntelOwl as DTMO's preferred generic IOC enrichment subsystem after repository completion of Phase 11.2 Taranis integration. It authorizes bounded adapter implementation under the controls below. Contract acceptance is repository evidence only and does not claim a live IntelOwl deployment, production-equivalent behavior, external-assurance acceptance or production authorization.

## Upstream baseline

The contract is based on the official IntelOwl project and documentation inspected on **2026-08-16**. The latest published upstream release inspected is **v6.7.0**. IntelOwl exposes REST APIs and official client libraries, uses API-token authentication and supports analyzers, connectors, playbooks, TLP-aware execution and job/report retrieval.

Primary upstream references:

- `https://github.com/intelowlproject/IntelOwl`;
- `https://github.com/intelowlproject/docs/blob/main/docs/IntelOwl/usage.md`;
- `https://github.com/intelowlproject/IntelOwl/releases/tag/v6.7.0`;
- `https://github.com/intelowlproject/pyintelowl`.

DTMO integrates through documented service APIs. IntelOwl implementation source is not vendored into DTMO.

## Responsibility boundary

| Capability | IntelOwl responsibility | DTMO responsibility |
|---|---|---|
| Generic observable enrichment | execute approved analyzers/playbooks | select governed enrichment policy and consume results |
| Provider credentials | manage analyzer-side provider secrets | never copy provider secrets from IntelOwl into DTMO evidence |
| Job execution | create and execute enrichment jobs | request only bounded approved jobs |
| Analyzer reports | produce raw analyzer/plugin results | preserve analyzer identity, timestamps and provenance |
| TLP execution restrictions | enforce configured plugin maximum TLP | never weaken upstream or local handling restrictions |
| Evaluation/data model | provide upstream evaluation/context where available | treat as enrichment context, not local-compromise proof |
| External connectors | optional IntelOwl capability | disabled/excluded from the initial DTMO path |
| Publication/sharing | not authoritative for DTMO | remains human-governed DTMO/MISP authority |
| Canonical intelligence | enrichment source only | DTMO remains canonical education-sector decision layer |

## Initial observable scope

The initial adapter is restricted to these observable classes:

- CVE;
- IP address;
- domain;
- URL;
- cryptographic hash.

Email and other personally identifying generic observables are **excluded by default**. They require an explicit privacy/data-processing decision before enablement.

## Required API surface

The implementation uses the smallest supported API surface necessary for enrichment. The accepted baseline includes:

| Purpose | Method | IntelOwl API class | DTMO rule |
|---|---|---|---|
| Submit observable analysis | `POST` | `/api/analyze_observable` | only approved observable classes and analyzer/playbook policy |
| Retrieve job state/results | `GET` | `/api/jobs/{job_id}` or the supported v6.7 job-detail equivalent | bounded polling until terminal state |
| Enumerate job/report data | `GET` | supported job/report API | retain raw result provenance and analyzer identity |
| Analyzer configuration discovery | `GET` | supported analyzer-config API / official client equivalent | allowlist validation only; never auto-enable arbitrary analyzers |
| Analyzer health | `GET` | `/api/analyzer/{analyzer_name}/healthcheck` or supported plugin-health equivalent | operational readiness signal only |

Endpoint names and request/response shapes must remain compatible with the target IntelOwl v6.7-compatible OpenAPI surface or official client behavior. If upstream API shape differs, this contract and implementation must be updated rather than silently guessing compatibility.

## Authentication and identity

1. DTMO uses a dedicated non-human IntelOwl service identity.
2. Authentication uses a secret-backed IntelOwl API token supplied at runtime.
3. The identity must not be an IntelOwl superuser or administrator merely to run enrichment.
4. TLS certificate verification is mandatory outside explicitly marked local development.
5. Tokens must not appear in repository configuration, logs, screenshots, raw evidence or error text.
6. `401` is an authentication/configuration failure with at most one bounded credential-refresh/reload path where supported.
7. `403` is an authorization failure and MUST NOT trigger automatic privilege escalation.

## Analyzer and provider governance

DTMO MUST NOT invoke every available IntelOwl analyzer by default. The adapter uses an explicit allowlist of approved analyzers or approved playbooks per observable class.

Each approved analyzer/playbook must have documented:

- provider/service name;
- internal versus external execution classification;
- supported observable classes;
- maximum permitted TLP/handling level;
- data sent externally;
- credential ownership;
- expected quota/rate-limit behavior;
- retention/privacy considerations;
- licensing/terms considerations where applicable.

Unknown, newly appearing or disabled analyzers are not automatically trusted or executed.

## TLP, privacy and external disclosure

IntelOwl's TLP controls are a useful execution guardrail, but DTMO remains responsible for its own handling policy.

- DTMO never submits an observable to an analyzer whose configured external-disclosure behavior conflicts with the DTMO handling level.
- `TLP:RED` or equivalent highly restricted material MUST NOT be sent to external analyzers.
- Missing or unknown TLP/handling data fails closed to a review-required state.
- IntelOwl `maximum_tlp` configuration does not authorize DTMO sharing.
- Email/generic personal data remain disabled until privacy/data-processing approval exists.

## Job identity, idempotency and replay

Canonical enrichment identity uses both DTMO input identity and upstream IntelOwl job/analyzer identity.

Minimum retained fields:

- DTMO canonical intelligence/observable identifier;
- submitted normalized observable value/type;
- IntelOwl instance identifier;
- upstream job ID;
- analyzer/playbook name and version/config identity where available;
- analyzer report/result identity where available;
- request timestamp, completion timestamp and retrieval timestamp;
- raw result/evidence reference;
- correlation/request ID;
- handling/TLP context.

Re-running enrichment may legitimately create a new IntelOwl job. DTMO MUST therefore distinguish **job replay** from **duplicate canonical intelligence**. A new enrichment observation updates/extends enrichment history; it does not duplicate the underlying canonical intelligence record.

## Result semantics

IntelOwl results are enrichment context. They MUST NOT be represented as proof that a DTMO-managed environment is compromised, vulnerable or exploited.

The adapter keeps separate dimensions for:

- analyzer result;
- analyzer/provider reliability;
- confidence/evaluation where supplied;
- DTMO relevance;
- local exposure evidence;
- severity;
- handling/TLP.

A provider verdict such as malicious/suspicious is retained with its source and timestamp. DTMO may derive a governed assessment only through an explicit documented mapping.

## Rate limits, quotas and bounded execution

The adapter is bounded by configuration for observable scope, requested analyzers, polling duration/interval, result size and retry/rate-limit behavior. Future governed execution must additionally bound batch/concurrency at its orchestration layer.

`429` and provider quota exhaustion cause bounded backoff/defer behavior. They do not cause uncontrolled retry storms or fallback to unapproved providers.

## Failure semantics

| Condition | Required behavior |
|---|---|
| connection/TLS failure | dependency degraded; bounded retry; no fabricated enrichment |
| `401` | bounded authentication recovery where supported, then fail/degrade |
| `403` | configuration/permission failure; no privilege escalation |
| `404` job after accepted submission | reconciliation/error evidence; do not fabricate a result |
| `429` | honor retry guidance where present; bounded backoff |
| `5xx` | bounded retry; preserve submitted job identity if known |
| malformed JSON/schema mismatch | quarantine/reject affected result; retain evidence; fail closed |
| analyzer/plugin failure | preserve analyzer failure separately from successful peer analyzers |
| partial job success | import only attributable successful results and retain failed-plugin state |
| unknown analyzer | do not execute/import as trusted without allowlist review |
| unknown TLP | restrictive review-required handling |

IntelOwl failure must not make unrelated DTMO read paths unavailable.

## Authority boundary

**IntelOwl external Connectors** are excluded from the bounded enrichment path. The integration MUST NOT enable IntelOwl Connectors, pivots or other actions that can create external side effects merely to perform enrichment. In particular, IntelOwl MISP/OpenCTI/Slack/email/abuse-submission connectors are outside this path.

No IntelOwl job success, connector capability, analyst evaluation, upstream tag or playbook result becomes DTMO external-share/publication approval. Existing DTMO human approval and governed MISP/export controls remain authoritative.

## Threat-model abuse cases

Phase 11.3 implementation tests cover or must continue to cover:

1. malicious/oversized observable values;
2. analyzer allowlist bypass attempts;
3. unknown analyzer returned by the server;
4. token leakage through errors/logging;
5. expired/revoked token;
6. TLP downgrade or missing handling context;
7. provider quota exhaustion and `429` behavior;
8. job ID collision/spoofing;
9. malformed/oversized analyzer reports;
10. partial job success with one or more failed analyzers;
11. stale result replay being treated as current evidence;
12. external connector side effects being requested accidentally;
13. upstream malicious verdict being misrepresented as local compromise;
14. IntelOwl outage while DTMO remains otherwise healthy.

## Licensing boundary

IntelOwl and pyIntelOwl are distributed under **AGPL-3.0**. DTMO remains a separate service/API consumer and does not vendor IntelOwl or pyIntelOwl source into the DTMO codebase.

If DTMO later distributes, embeds or modifies IntelOwl/pyIntelOwl components, or operates a modified network-facing IntelOwl service, the applicable AGPL source-availability and notice obligations require explicit licensing review before that architecture is accepted. This contract does not provide legal advice and does not authorize source redistribution.

## Phase 11.3 adapter acceptance contract

The bounded adapter PR must demonstrate:

- runtime-secret-backed dedicated API token;
- HTTPS verification/production HTTPS validation;
- approved observable classification and analyzer/playbook allowlist;
- bounded job submission and polling;
- deterministic correlation between DTMO observable, IntelOwl job and analyzer reports;
- result provenance with analyzer identity and timestamps/context;
- fail-closed TLP/privacy handling;
- no IntelOwl connector/share side effects in the enrichment path;
- quota/rate-limit and degraded dependency behavior;
- partial-success semantics without fabricated success;
- canonical enrichment that does not imply local compromise;
- contract/integration tests for auth/configuration, allowlist, identity mismatch, malformed/oversized results, partial failure, timeout and `429` handling;
- synchronized architecture, integration, security, operations, QA/evidence and roadmap documentation;
- exact-head CI and Professional Documentation Gate success.

Durable enrichment-history persistence, governed execution/RBAC wiring and full operational integration remain a subsequent bounded Phase 11.3 slice after this adapter is accepted.

## Evidence boundary

Repository acceptance of this contract proves only that the architecture boundary is documented and testable. Repository acceptance of the adapter proves only the tested repository behavior. Neither proves live IntelOwl connectivity, service-account permissions, provider credentials, production-equivalent deployment, analyzer operational quality, privacy approval for personal data, independent assurance or production authorization.

Historical Phase 8/9 evidence remains historical evidence for the earlier candidate and is not reused for the materially changed integrated platform.

## Decision

**`PHASE 11.3 CONTRACT BASELINE: ACCEPTED / REPOSITORY_COMPLETE — BOUNDED INTELOWL ADAPTER MAY PROCEED UNDER THIS CONTRACT`**.
