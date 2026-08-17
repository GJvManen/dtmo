# Phase 11.7b Cortex Connector Gate

State: **`IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`**

## Acceptance objective

Accept the owner-required Cortex connector only when the bounded analyzer-only implementation and its professional documentation remain synchronized and all exact-head regressions are green.

## Required checks

- explicit owner requirement is recorded and the prior no-adoption decision is not rewritten as historical evidence;
- Cortex remains a separate service boundary; no upstream source is vendored;
- API key bearer authentication, HTTPS production requirement and explicit analyzer allowlisting are enforced;
- only analyzer execution and job report retrieval are implemented;
- responders and external side-effect actions remain excluded;
- observable type/value/TLP validation occurs before network I/O;
- stable job identity and analyzer identity are checked fail-closed;
- imported results cannot grant external-share authority or establish local compromise;
- result size is bounded;
- operational, security, integration, current-state, roadmap, evidence-index and portal documentation are reconciled;
- repository CI is not promoted as live Cortex or production evidence.

## Next

After protected acceptance, resume Phase 11.8 integrated runtime industrialisation. Cortex deployment itself must then participate in the same Kubernetes/Helm/GitOps, secrets, network, observability, recovery and supply-chain controls as the other integrated services.
