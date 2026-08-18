# Phase 11.8b Workload Identity and External Secrets Runbook

## Purpose

Operate the bounded DTMO workload-identity and external-secret delivery path without placing credential material in Git or broadening application authority.

## Pre-deployment checks

Confirm that the target cluster already has the required external-secret controller and the referenced SecretStore/ClusterSecretStore. Confirm that the workload identity exists outside Git, is attributable to the DTMO runtime, and has only read access to the specifically approved secret objects. Confirm the chart still renders `automountServiceAccountToken: false` and that the target Secret name matches the DTMO deployment configuration.

## Rotation

Rotate values at the secret provider, not in Git. Observe controller reconciliation and verify the Kubernetes Secret changes as expected. Restart or roll DTMO pods only when the application/runtime semantics require it. Record the provider-side change identity and deployment change record; do not copy secret values into evidence.

## Revocation

If an identity or secret is suspected compromised, revoke or disable the external workload identity/provider grant first, rotate affected secrets, then verify that the controller can no longer retrieve revoked material. Treat missing or ambiguous revocation evidence as fail closed.

## Failure handling

If the ExternalSecret is not Ready, the target Secret is absent, remote keys are missing, identity federation fails, or provider authorization is ambiguous, do not bypass the control by committing a Secret manifest or plaintext values. Restore the approved external identity/secret path or stop the deployment.

## Rollback

Rollback must return the deployment to the last reviewed GitOps revision whose secret-delivery mode and workload-identity assumptions are known and accepted. Revert the reviewed Helm values/revision rather than editing live resources ad hoc. If 11.8b external secret delivery had been enabled, disable it only by reverting to an accepted revision that consumes the previously governed existing Kubernetes Secret; never replace it with plaintext values or a credential-bearing manifest in Git.

Before allowing DTMO pods to resume, verify that the reverted ServiceAccount still has `automountServiceAccountToken: false`, the expected target Secret exists from an approved source, and no abandoned ExternalSecret or workload-identity grant retains unintended access. Revoke obsolete provider grants when they are no longer required. Missing, ambiguous or conflicting rollback evidence is fail closed: keep the affected deployment stopped rather than claiming successful recovery.

Record the reverted GitOps revision, non-sensitive resource status and provider-side revocation/change identifiers. Do not record secret values, bearer tokens, private keys or identity credentials as rollback evidence.

## Evidence boundary

Acceptable operational evidence includes resource status, controller reconciliation metadata, secret-version identifiers where non-sensitive, workload identity audit events and change records. Secret values, private keys, bearer tokens and provider credentials must never be captured in repository evidence.

Repository CI does not prove live secret retrieval, rotation, revocation, cloud IAM correctness or production availability.
