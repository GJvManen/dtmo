# Phase 11.8 Runtime Foundation Runbook

## Preconditions

Use an approved Kubernetes cluster and namespace, an immutable DTMO image digest, and an existing runtime Secret created outside Git. Required service endpoints, credentials, licensing and disclosure permissions remain separate deployment prerequisites.

## Render and review

Render the chart with `deploy/gitops/phase11-8/values.yaml` plus environment-specific approved values. The render must fail if `image.digest` is empty. Review the resulting Deployment, Service, ServiceAccount, PodDisruptionBudget and NetworkPolicy before reconciliation.

## Deployment checks

Confirm pods run as non-root UID 10001, the root filesystem is read-only, privilege escalation is disabled, capabilities are dropped, service-account token automounting is disabled, readiness/liveness probes reach `/health`, and the image reference is digest-pinned.

Confirm the NetworkPolicy permits only same-namespace traffic, DNS and explicitly approved external CIDRs. A connectivity exception must be reviewed as a trust-boundary change and must not bypass the licensing, RBAC, provenance, human publication/share authority or fail-closed evidence rules of the connected service.

## Failure and rollback

If admission, image verification, secret resolution, probes or required connectivity fails, stop reconciliation and retain the previous approved Git revision. Do not disable security controls to make the deployment pass. Rollback is a Git revision rollback to the last approved immutable configuration; runtime rollback evidence is not claimed until exercised in a later Phase 11.8 slice.

## Evidence

Record Git revision, chart version, image digest and rendered manifest checksum for later production-equivalent validation. Repository CI is engineering evidence only and is not live-cluster or production evidence.
