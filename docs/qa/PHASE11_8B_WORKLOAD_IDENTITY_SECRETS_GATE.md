# Phase 11.8b Workload Identity and External Secrets Gate

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**

## Repository acceptance criteria

The exact PR head must demonstrate that:

- the DTMO ServiceAccount keeps token automount disabled;
- workload identity metadata is configurable only through explicit ServiceAccount annotations and no credential value is supplied by repository defaults;
- external secret delivery is disabled by default;
- enabling it requires an explicit SecretStore/ClusterSecretStore name, target Secret and at least one remote-key mapping;
- the application consumes only the resulting Kubernetes Secret and does not call the external provider directly;
- no Kubernetes Secret containing runtime values is added to Git;
- service-to-service licensing/identity boundaries, RBAC, human publication/share authority and fail-closed evidence semantics remain unchanged;
- architecture, administration, operations, current-state, roadmap, evidence and documentation portal material remains synchronized.

## Non-claims

A green repository gate is not evidence of live workload identity federation, cloud IAM permissions, secret-store reachability, controller installation/admission, secret rotation/revocation, HA, production-equivalent runtime behavior, independent assurance or production authorization.

## Required evidence

Dedicated contract test: `backend/tests/test_phase11_8b_workload_identity_secrets.py`.

Dedicated workflow: `.github/workflows/phase11-workload-identity-secrets.yml`.

Only a fully green exact-head result can satisfy this bounded repository gate.
