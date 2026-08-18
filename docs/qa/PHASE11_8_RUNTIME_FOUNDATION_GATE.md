# Phase 11.8 Runtime Foundation Gate

## Acceptance scope

This gate accepts only the first bounded Phase 11.8 foundation slice: Helm/GitOps layout, immutable image identity, secure pod defaults, explicit secret reference, application-workload disruption protection, probes and default-deny network policy.

## PASS criteria

The exact-head CI must verify that the chart requires an immutable image digest; no secret material is embedded in Git-owned values; service-account token automounting is disabled; pods are non-root with read-only root filesystem, dropped capabilities, no privilege escalation and RuntimeDefault seccomp; resource requests/limits and health probes are present; NetworkPolicy is enabled with explicit external CIDR allowlisting; and a PodDisruptionBudget is defined.

Professional architecture, administration, operations, current-state, roadmap, evidence and portal documentation must remain synchronized. Repository CI must not be described as live-cluster, HA, recovery, supply-chain attestation or production evidence.

## Deferred gates

Later Phase 11.8 slices must independently cover stateful/multi-zone HA, external-secret/workload-identity implementation, ingress/TLS and finer network segmentation, centralized observability, backup/recovery exercises, SBOM/scanning/signing/attestation, capacity and upgrade/rollback exercises.
