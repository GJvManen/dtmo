# Kubernetes Runtime Configuration

Phase 11.8 deploys DTMO through `deploy/helm/dtmo` with GitOps-owned overrides under `deploy/gitops/phase11-8`.

Administrators must pin `image.digest` to an approved immutable `sha256:` digest. The chart intentionally fails when no digest is supplied. Do not place credentials, API keys or tokens in Helm values or Git. `existingSecret` must reference a Kubernetes Secret populated through an approved external-secret or equivalent deployment process.

The default workload is non-root, uses UID/GID 10001, disables service-account token automounting, drops Linux capabilities, disallows privilege escalation, uses `RuntimeDefault` seccomp and a read-only root filesystem. `/tmp` is the only writable ephemeral mount supplied by the chart.

NetworkPolicy is fail-closed by default. Same-namespace traffic and DNS are allowed. Any external service CIDR must be explicitly approved and added to `networkPolicy.egressCIDRs`; adding connectivity does not by itself establish licensing, disclosure or data-processing authority for Taranis AI, IntelOwl, Cortex, OpenCTI, MISP, TheHive or external analyzer/provider services.

The two-replica default and PodDisruptionBudget are only application-workload foundations. They are not evidence that PostgreSQL, Redis, OpenSearch, object storage or integrated Phase 11 services are highly available.
