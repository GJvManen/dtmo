# DTMO Staging Acceptance Plan

## Purpose

Define the minimum evidence required before DTMO staging can be accepted as production-equivalent. This document is a readiness contract only; it does not claim that a staging environment exists or that any staging test has executed.

## Environment parity contract

Staging acceptance requires retained evidence that the environment uses the same application artifact intended for production, immutable dependency/container versions, equivalent service topology, equivalent RBAC and identity boundaries, equivalent persistence/search/object-storage interfaces, and equivalent observability/alerting configuration. Environment-specific hostnames, credentials, keys and capacity values may differ.

## Required controls

1. **Deployment reproducibility** — source-controlled deployment procedure, immutable artifact references, configuration inventory and rollback procedure.
2. **Secrets and identity** — no production credentials in staging; secrets supplied through the approved secret-management path; least privilege and separation of duties preserved.
3. **TLS and network restrictions** — encrypted service ingress/egress where required, restricted management interfaces, explicit allowed network paths and no unintended public exposure.
4. **Data protection** — synthetic or approved non-production data only unless a separately approved controlled dataset is documented; provenance and auditability remain intact.
5. **Smoke and integration** — API/UI health, authentication/RBAC, search, connector, queue, storage and observability checks execute against the deployed environment.
6. **Migration** — schema/data migration procedure executes from a representative pre-upgrade state and proves forward compatibility and rollback/restore handling.
7. **Connector acceptance** — live/sandbox connector behavior, provenance, timeout/retry/failure isolation and human share approval remain enforced.
8. **Recovery** — backup/restore or equivalent recovery procedure is exercised with retained evidence; recovery does not bypass integrity/provenance controls.
9. **Performance** — representative staging load validates critical latency, throughput, queue and saturation thresholds without weakening Phase 5 limits.
10. **Accessibility/operational UX** — supported browser journeys are rerun in staging; genuine VoiceOver/NVDA remains a separate external prerequisite where applicable.
11. **Observability/incident operations** — metrics, logs, trace correlation, alert routes and runbook links are available without exposing credentials or unnecessary personal data.
12. **Security review** — deployment-time image digests, vendor advisories and relevant CVEs are rechecked before staging acceptance.

## Evidence matrix

Each staging execution must retain: environment identifier; deployed commit/release and immutable artifact digests; UTC start/end time; actor/automation identity; test command or workflow reference; machine-readable result; JUnit/logs where applicable; configuration parity record; secrets/TLS/network validation result; rollback/recovery result; unresolved findings; and acceptance decision.

A missing, inaccessible, queued, cancelled, failed, stale-head or non-production-equivalent item is not PASS.

## Governance invariants

RBAC, separation of duties, privacy, provenance, auditability and human share approval remain authoritative in staging. Technical deployment or incident roles never gain publication/share authority by virtue of staging access.

## Current decision

`READINESS_BASELINE_ONLY`. No staging deployment or staging acceptance is claimed by this document.

## Exactly one next priority

After this readiness baseline passes exact-head CI, provision or identify the production-equivalent staging environment and capture the immutable deployment-parity evidence before executing acceptance tests.
