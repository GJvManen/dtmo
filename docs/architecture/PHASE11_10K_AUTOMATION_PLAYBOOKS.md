# Phase 11.10k — Automation & Playbooks

## Purpose

Phase 11.10k turns the canonical `/automation` route into a governed DTMO control-plane workspace without creating a second orchestration plane. The workspace reuses the existing server-owned `SchedulerService`, `/health` scheduler observation, `/connectors` capability inventory and the already governed `/connectors/{id}/run` execution paths.

## Authority and trust boundaries

```mermaid
flowchart LR
    U[Authorized human operator] -->|DTMO session + RBAC| W[Automation Workspace]
    W -->|read| H[/health scheduler observation/]
    W -->|read| C[/connectors capability catalog/]
    W -->|explicit run request + request ID| R[/connectors/{id}/run/]
    R --> S[Server-side connector execution]
    S --> I[Canonical ingestion + provenance]
    S -. no authority .-> P[Review / case / share / publication]
```

The browser never receives upstream connector credentials and never calls an upstream service directly. Scheduler state is observational. A reported schedule does not authorize a browser to alter scheduler configuration. Explicit manual execution remains a server-authorized action and uses the accepted connector boundary.

## Human authority

The workspace exposes bounded execution only when the DTMO session includes `manage:connectors` and is not represented as a service-account browser session. This UX restriction does not replace backend RBAC; the server remains authoritative. Service-to-service collection jobs continue to operate only through their accepted server-side scheduler boundary.

Automation does not create an autonomous decision authority. A successful run can ingest attributable intelligence but cannot itself assert source truth, compromise, containment, remediation, review completion, case creation, external-share approval, publication approval or production authorization.

## Failure model

If session, scheduler health or connector capability state cannot be loaded, the workspace fails closed and does not synthesize a healthy/runnable state. Connector execution errors are rendered as returned by the DTMO control plane. A disabled feature flag remains disabled rather than being interpreted as a successful no-op.

## Replay and evidence

The browser supplies a fresh `X-Request-ID` for an explicit bounded invocation. Canonical connector persistence retains the accepted idempotent ingestion/search behavior. Repository browser fixtures and GitHub Actions prove only code/contract behavior at an exact commit; they are not live-runtime, production-equivalent or production-authorization evidence.
