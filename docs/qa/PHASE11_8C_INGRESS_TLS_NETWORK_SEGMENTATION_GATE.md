# Phase 11.8c ingress/TLS/network segmentation gate

## Acceptance target

The bounded repository gate accepts Phase 11.8c only when Helm configuration is fail-closed for external ingress and professional documentation preserves the network, authority and evidence boundaries.

## Required repository evidence

- ingress is disabled by default;
- enabling ingress requires explicit ingress class, hostname and TLS Secret reference;
- TLS cannot be disabled while ingress is enabled;
- the DTMO Service remains `ClusterIP`;
- NetworkPolicy must remain enabled with ingress;
- ingress traffic is allowed only from a peer constrained by both namespace and pod selectors;
- no TLS private key or secret value is stored in Git;
- architecture, administration and operations documentation describe rollback and live-validation requirements;
- lifecycle documentation identifies 11.8b as accepted and 11.8c as the sole active bounded objective.

## Non-claims

Repository CI **does not prove** DNS ownership, certificate validity, external routing, ingress-controller admission, CNI enforcement, cloud load-balancer/WAF policy, live availability, HA, recovery, production-equivalent validation, independent assurance or production authorization.

Missing, stale, skipped, cancelled or ambiguous evidence is not PASS.
