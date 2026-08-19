# Phase 11.8h — Capacity, resource planning and saturation boundaries

## Scope
This bounded slice adds repository-controlled CPU/memory requests, limits and HorizontalPodAutoscaler policy for the DTMO runtime. It does not claim production sizing, provider capacity, workload demand, SLO attainment or production authorization.

## Capacity trust boundary
```mermaid
flowchart LR
  Load[Observed workload] --> Metrics[CPU / memory metrics]
  Metrics --> HPA[autoscaling/v2 HPA]
  HPA --> Pods[DTMO replicas]
  Pods --> Limits[Requests and limits]
  Limits --> Saturation[Saturation evidence]
  Saturation --> Human[Human capacity decision]
```

## Invariants
- CPU and memory requests and limits remain explicit.
- Autoscaling has a bounded minimum and maximum replica count; `maxReplicas` may not be lower than `minReplicas`.
- Scale-down uses a stabilization window to reduce oscillation.
- CPU and memory targets are planning controls, not proof of production capacity.
- Saturation thresholds are evidence triggers. They do not silently increase authority, bypass RBAC, change publication/share authority or alter service-to-service licensing boundaries.
- Missing production-equivalent load evidence fails closed for any production-sizing claim.
- Historical Phase 8/9 evidence is not reused for the materially changed Phase 11 candidate.

## Acceptance boundary
Repository CI may prove rendering and contract correctness only. Phase 11.10 must collect fresh production-equivalent load, saturation and recovery evidence for the same immutable integrated candidate. Phase 11.11 remains independent assurance; Phase 12 remains the formal GO/NO-GO and production authorization decision.
