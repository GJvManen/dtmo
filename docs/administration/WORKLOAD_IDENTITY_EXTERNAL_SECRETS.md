# Workload Identity and External Secret Administration

Phase 11.8b keeps identity credentials and secret values outside Git.

## ServiceAccount identity

Configure only provider-required identity metadata in `serviceAccount.annotations`. The annotation value must identify an already governed workload identity; it must not contain a private key, bearer token, client secret or other credential material. `automountServiceAccountToken` remains `false`.

Example shape:

```yaml
serviceAccount:
  automountServiceAccountToken: false
  annotations:
    provider.example/workload-identity: dtmo-runtime
```

The annotation key is provider/deployment specific. Repository defaults deliberately do not choose a cloud provider or identity.

## External secret delivery

The default remains `externalSecret.enabled: false`, in which case DTMO consumes `existingSecret` as established in Phase 11.8a.

When an approved External Secrets controller and store already exist, configure an explicit store reference, target Secret and per-variable remote mappings:

```yaml
externalSecret:
  enabled: true
  refreshInterval: 1h
  secretStoreRef:
    name: production-secret-store
    kind: ClusterSecretStore
  targetName: dtmo-runtime
  remoteKeys:
    DTMO_DATABASE_URL: /dtmo/runtime/database-url
```

Do not commit actual secret values. Remote object paths are configuration metadata and must still follow organizational information-classification rules.

## Required review

Before deployment, an administrator must verify workload identity ownership, least-privilege secret-provider ACLs, controller namespace and RBAC, target Secret ownership, rotation/revocation procedure, audit logging and the absence of unexpected keys in the rendered Kubernetes Secret.

A repository-green chart is not evidence that any of these deployment controls exist or function correctly.
