# Governance & Operations deep functional recovery

Status: **repository-controlled exact-head evidence slice**

This slice follows the Automation & Playbooks trigger/rollback recovery and closes the next bounded item recorded in `docs/qa/CANONICAL_FUNCTIONAL_BROWSER_MATRIX.md`.

## Governance & Evidence journey

The canonical `/workbench/governance` route is exercised through the built same-origin workbench against the real `/api/v1/governance/knowledge` contract. The browser must render the explicit repository-backed framework coverage for Normenkader IBP, MITRE ATT&CK, NIST CSF, CVSS and internal DTMO governance, together with traceable mappings, separation-of-duties boundaries and the evidence claim boundary.

The journey deliberately proves visibility and traceability only. A framework row or mapping does **not** constitute certification, full compliance, semantic equivalence, control effectiveness, review approval, external-share authority or production authorization. Missing mappings remain missing rather than being inferred.

## Operations journey

The canonical `/workbench/operations` route is exercised against the real `/health`, `/api/v1/operations/summary` and `/connectors` same-origin contracts. The browser must render process health, request/latency observations, alert gauges, workload telemetry, connector capability and canonical pivots. The explicit refresh control must re-read those contracts without a `/ui/*` fallback.

Operations remains read-only. Point-in-time runtime observations and clear alert gauges do not prove absence of incidents, vulnerabilities or degraded dependencies. Connector enablement is capability state, not proof of successful collection or upstream health.

## Evidence boundary

The dedicated exact-head workflow uses repository-controlled PostgreSQL and the local DTMO process. No external connector is executed. Passing this slice is **not** owner functional acceptance, staging evidence, production-equivalent validation, penetration-test evidence, independent external assurance, compliance approval, production health assurance or production authorization.

Server-side RBAC, provenance, fail-closed handling, separate human review/share authority and server-side credential boundaries remain authoritative and are not weakened by this recovery evidence.
