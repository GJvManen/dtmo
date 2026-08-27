# Governance & Evidence deep functional recovery

Status: **repository-controlled exact-head recovery slice; owner acceptance remains pending**

## Verified gap

The canonical Governance & Evidence workspace already consumed `/api/v1/governance/knowledge`, but it rendered only framework summary rows, internal repository mappings and authority boundaries. The backend snapshot also contains the typed DTMO control crosswalk, framework-object relationships, implementation references and framework provenance. Those deeper evidence fields were not visible in the canonical workspace, so an operator or auditor could not follow a framework claim through the actual DTMO control to its repository implementation evidence.

## Bounded recovery

This slice exposes the existing repository-backed evidence without creating new mappings or inferring compliance. The canonical workspace now shows:

- framework coverage together with repository provenance;
- the typed DTMO control identifier and title;
- repository implementation references for each DTMO control;
- explicit framework object identifier, title and relationship type;
- the recorded mapping rationale;
- the existing crosswalk verification date and claim boundary.

The exact-head browser gate uses the built canonical DTMO workbench and same-origin `/api/v1/governance/knowledge` path with an auditor principal. It proves a deep `Normenkader IBP / MITRE ATT&CK / CVSS -> DTMO-TVM-01 -> repository implementation` journey and verifies that the canonical page continues to state its non-compliance and authority boundaries.

## Security and assurance boundaries

No mapping is generated from free text and no missing relationship is inferred. CVSS remains context-only. Visibility does not grant review, case, connector, external-share, publication, administration or production authority. Repository exact-head browser evidence does not establish framework certification, full compliance, environment control effectiveness, owner functional acceptance, staging, production-equivalent validation, penetration-test evidence or independent assurance.

## Next bounded priority

After this Governance & Evidence deep-evidence slice is exact-head green and merged, the next repository-controlled recovery priority is the **Operations deep runtime journey** from the canonical functional browser recovery order. External deployment or independent-assurance evidence must not be substituted for that repository work.
