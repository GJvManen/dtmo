# Phase 11.8d — HA and disruption runbook

## Purpose

Operate the bounded DTMO application availability controls without overstating live HA evidence.

## Pre-change checks

Confirm the target cluster exposes stable zone and hostname topology labels, the configured replica count is at least two, the PodDisruptionBudget is admitted, and backing stateful services have an approved environment-specific HA design. If any prerequisite is unknown, fail closed and do not claim HA.

## Deployment checks

Verify rendered topology spread constraints use `topology.kubernetes.io/zone` and `kubernetes.io/hostname`, `whenUnsatisfiable: DoNotSchedule`, required pod anti-affinity, graceful termination, and the expected PodDisruptionBudget. Confirm ready replicas are distributed as intended before planned maintenance.

## Disruption handling

For node maintenance, respect the PodDisruptionBudget and drain one failure domain at a time. Do not bypass PDB protection merely to complete maintenance. If scheduling cannot preserve the required topology, stop and investigate capacity or zone availability rather than weakening constraints silently.

Stateful service failover is provider-specific and must follow the approved PostgreSQL, Redis, OpenSearch and object-storage operating procedures. Application replica health is not proof of stateful durability or quorum.

## Rollback

Rollback to the last accepted GitOps revision if new placement constraints cause unschedulable replicas, unexpected capacity pressure or degraded service. Do not perform untracked live edits. After rollback, verify replica readiness, PDB state, topology placement and stateful dependency health. Record only non-sensitive evidence.

## Evidence boundary

Repository and operator checks do not prove survival of a real zone outage, stateful failover correctness, recovery objectives, independent assurance or production authorization. Missing or ambiguous evidence fails closed.
