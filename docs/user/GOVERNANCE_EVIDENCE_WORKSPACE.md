# Governance & Evidence Workspace

The canonical **Governance & Evidence** workspace is available at `/workbench/governance`. It renders repository-backed governance knowledge from DTMO's same-origin `GET /api/v1/governance/knowledge` API and never converts missing mappings into compliance claims.

## Framework coverage

The workspace exposes only explicit repository-backed relationships. The authoritative crosswalk is maintained in `backend/dtmo/governance_crosswalk.py` and documented in `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`.

Normenkader IBP has explicit partial control relationships where implementation evidence exists. MITRE ATT&CK has explicit typed detection/threat-classification context; DTMO does not infer techniques from free text. NIST CSF has explicit partial outcome/category relationships. CVSS remains `context-only` scoring context rather than a compliance framework or proof of local exposure.

The crosswalk is intentionally incomplete. Framework objects without an explicit typed relationship remain unmapped. Seeing a framework or mapping in the workspace does not prove compliance, certification, control effectiveness, local compromise, remediation, independent assurance, production readiness or production authorization.

## Repository mappings and provenance

Internal governance mappings include source document and section. External framework relationships retain their DTMO control identifier, framework/object identifier, relationship type, rationale and implementation/source references. Operators should inspect those references rather than infer equivalence from labels or free-form tags.

Missing or inaccessible canonical governance data fails closed: the workspace shows unavailable state rather than a PASS, compliant or zero-risk result. A partial mapping does not prove compliance.

## Authority boundaries

Governance visibility is read-oriented convenience, not authorization. It does not grant human review, case creation, remediation, connector execution, external-share approval, publication authority, administration authority or production authority. Those authorities remain separate server-side RBAC and human-governed decisions.

## Evidence interpretation

Repository CI and browser fixtures prove only repository-controlled exact-head behavior. They are not production-equivalent validation and are not independent external assurance. Historical Phase 8/9 evidence remains candidate-bound and cannot be reused as proof for the materially changed Phase 11 integrated candidate. Phase 10 remains **NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED**.
