# Phase 11.8d — HA and disruption gate

## Acceptance objective

Accept only the repository-controlled multi-zone scheduling and disruption-hardening contract for the DTMO application workload, while keeping stateful HA and live failover claims deployment-bound.

## Required exact-head evidence

- DTMO replica count is at least two;
- topology spread covers zone and hostname with `DoNotSchedule`;
- required pod anti-affinity prevents same-host concentration;
- graceful termination is explicit;
- PodDisruptionBudget remains enabled with a non-zero minimum availability;
- stateful PostgreSQL, Redis, OpenSearch and object-store HA remain explicit external deployment requirements rather than inferred repository claims;
- architecture, runbook, QA and lifecycle documentation remain synchronized;
- service/licensing boundaries, provenance, RBAC, human publication/share authority and fail-closed evidence rules remain unchanged.

## Non-claims

A green repository gate **does not prove** live multi-zone placement, node or zone failure survival, stateful quorum/failover, storage durability, recovery objectives, production-equivalent behavior, independent assurance or production authorization.

## Decision rule

Any missing, failed, skipped, cancelled, stale or inaccessible mandatory exact-head evidence is not PASS. Merge only after all required exact-head workflows are successful and expected-head protection confirms the accepted head.
