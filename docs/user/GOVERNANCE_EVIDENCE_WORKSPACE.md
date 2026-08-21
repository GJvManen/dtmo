# Governance & Evidence Workspace

The canonical **Governance & Evidence** workspace is available at `/workbench/governance`. It renders repository-backed governance knowledge from DTMO's same-origin `GET /api/v1/governance/knowledge` API and never converts missing mappings into compliance claims.

## Framework coverage

The workspace exposes explicit coverage states. Normenkader IBP and MITRE ATT&CK remain unmapped until an explicit repository-backed control or technique crosswalk exists. CVSS remains context-only where DTMO has no first-class governed score mapping. Internal DTMO security and release governance may be displayed as mapped only where the API returns repository provenance.

Seeing a framework in the workspace does not prove compliance, certification, control effectiveness, local compromise, remediation, independent assurance or production readiness.

## Repository mappings and provenance

Each governed internal mapping includes its source document and section. Operators should use those references to inspect the authoritative evidence rather than infer equivalence from labels or free-form tags. Missing or inaccessible canonical governance data fails closed: the workspace shows the unavailable state rather than a PASS or zero-risk result.

## Authority boundaries

Governance visibility does not grant human review, case creation, remediation, connector execution, external-share approval, publication authority or production authority. Those authorities remain separate server-side RBAC and human-governed decisions.

## Evidence interpretation

Repository CI and browser fixtures prove only repository-controlled exact-head behavior. They are not production-equivalent validation and are not independent external assurance. Historical Phase 8/9 evidence remains candidate-bound and cannot be reused as proof for the materially changed Phase 11 integrated candidate.
