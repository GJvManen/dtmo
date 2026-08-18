# Kubernetes ingress, TLS and network segmentation

## Administrative intent

Phase 11.8c keeps external ingress disabled until deployment owners provide an approved ingress class, DNS hostname, Kubernetes TLS Secret reference and explicit ingress-controller NetworkPolicy selectors. DTMO does not create certificate private keys or ingress-controller credentials in Git.

## Required values before enabling ingress

Set `ingress.enabled=true` only after all of the following are approved:

- `ingress.className`: the deployment-owned ingress controller class;
- `ingress.host`: the approved DNS hostname;
- `ingress.tls.enabled=true`;
- `ingress.tls.secretName`: a pre-existing or separately managed Kubernetes TLS Secret;
- `networkPolicy.enabled=true`;
- `networkPolicy.ingressController.namespaceSelector`: labels selecting only the ingress-controller namespace;
- `networkPolicy.ingressController.podSelector`: labels selecting only the approved ingress-controller pods.

Example deployment-owned values:

```yaml
ingress:
  enabled: true
  className: nginx
  host: dtmo.example.invalid
  tls:
    enabled: true
    secretName: dtmo-ingress-tls
networkPolicy:
  enabled: true
  ingressController:
    namespaceSelector:
      kubernetes.io/metadata.name: ingress-nginx
    podSelector:
      app.kubernetes.io/name: ingress-nginx
```

The example hostname is non-routable documentation data and is not deployment evidence.

## RBAC and authority

Only deployment administrators may approve ingress class, DNS, certificate Secret reference and network selectors. Application users and connector identities do not receive infrastructure mutation rights. Network reachability does not grant human publication/share authority or establish compromise evidence.

## Fail-closed behavior

Helm rendering must fail when ingress is enabled without an ingress class, host, TLS, TLS Secret name, NetworkPolicy, namespace selector or pod selector. Do not bypass these checks with live-cluster edits. Configuration changes must flow through reviewed GitOps state.
