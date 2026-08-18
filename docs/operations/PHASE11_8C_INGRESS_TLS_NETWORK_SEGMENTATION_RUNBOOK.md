# Phase 11.8c ingress/TLS/network runbook

## Purpose

Operate the bounded Phase 11.8c ingress boundary without treating repository CI as live deployment evidence.

## Pre-change checks

1. Confirm the reviewed GitOps revision and immutable DTMO image digest.
2. Confirm the approved ingress class and DNS hostname.
3. Confirm the referenced TLS Secret exists through the deployment-owned certificate process; do not record private key material in evidence.
4. Confirm the ingress-controller namespace and pod labels used by the NetworkPolicy selectors.
5. Confirm `networkPolicy.enabled=true` and that no emergency live-cluster edits are being used as the authoritative configuration source.

## Deployment verification

After deployment, collect non-sensitive evidence for:

- rendered Ingress class, hostname and TLS Secret reference;
- Service type remaining `ClusterIP`;
- NetworkPolicy selecting the DTMO pods;
- ingress peer containing both namespace and pod selectors;
- expected controller-to-service connectivity;
- denied connectivity from a non-selected test pod/namespace;
- TLS endpoint/certificate validation in the production-equivalent environment.

Repository CI does not prove any of these live behaviors.

## Failure handling

If the ingress controller cannot reach DTMO, TLS is invalid, selectors are ambiguous, unexpected peers can connect or evidence cannot be attributed to the intended deployment revision, fail closed. Do not broaden selectors to `{}` or disable NetworkPolicy as a workaround. Restore the last accepted configuration or disable ingress while the fault is investigated.

## Rollback

Rollback is GitOps-owned. Revert to the last accepted revision, or set `ingress.enabled=false` in a reviewed revision if north-south exposure must be removed. Verify that the Ingress object is removed, the DTMO Service remains `ClusterIP`, and the application NetworkPolicy no longer admits ingress-controller traffic. Do not delete or expose TLS private-key material as part of rollback evidence.

## Evidence handling

Record only non-sensitive manifests, selector labels, certificate metadata needed for validation, timestamps and immutable deployment identity. Credentials, private keys, secret values and unnecessary personal data are prohibited in evidence artifacts.
