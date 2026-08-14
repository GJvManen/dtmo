# DTMO Governance Mapping Registry

Last updated: **2026-08-14**

## Purpose

This registry is the repository authority for framework and governance mapping claims exposed by DTMO. It distinguishes three different mapping domains that must not be conflated:

1. **DTMO control crosswalks** — explicit relationships between implemented DTMO controls/capabilities and external framework objects;
2. **intelligence mappings** — governed mappings between individual intelligence records and framework controls/techniques/categories;
3. **context-only frameworks** — frameworks such as CVSS where DTMO can present context without claiming a complete first-class scoring contract.

## Claim rule

DTMO never infers framework/control/technique equivalence merely because concepts appear related. Every exposed mapping requires an explicit identifier, relationship type, rationale and provenance/source reference.

A relationship such as `supports`, `partial-support`, `threat-classification-context` or `context-only` is not equivalent to certification or complete compliance.

## Framework inventory and current treatment

| Framework | Version/revision | Current DTMO treatment |
|---|---|---|
| Normenkader IBP | content revision `2024-06-06` | explicit partial DTMO-control crosswalk plus governed intelligence mappings where created/reviewed |
| MITRE ATT&CK | registry version `19.1` | explicit threat-context relationships plus governed intelligence technique mappings |
| NIST Cybersecurity Framework | `2.0` | explicit DTMO-control outcome/category relationships |
| CVSS | `4.0` | `CONTEXT_ONLY`; no claim of complete first-class vector/base-score support |

## Repository-backed explicit DTMO control crosswalk

The crosswalk is exposed by `GET /api/v1/governance/control-crosswalk` and rendered in the canonical Governance view.

| DTMO control | External objects currently represented |
|---|---|
| `DTMO-IAM-01` Governed RBAC and least privilege | Normenkader IBP `ID.02`, `ID.05`; NIST CSF `PR.AA` |
| `DTMO-AUTH-01` Authenticated and attributable access | Normenkader IBP `SM.02`; MITRE ATT&CK `T1078` as detection/mitigation context |
| `DTMO-AUD-01` Tamper-evident audit and request correlation | Normenkader IBP `SM.04`; NIST CSF `DE.CM` |
| `DTMO-TVM-01` Threat and vulnerability intelligence lifecycle | Normenkader IBP `SM.07`; MITRE ATT&CK `T1087` as threat-classification context; NIST CSF `ID.RA`; CVSS 4.0 context |
| `DTMO-NET-01` Network and deployment trust boundaries | Normenkader IBP `SM.11` |
| `DTMO-REC-01` Backup, restore and recovery evidence | Normenkader IBP `OP.02`, `BC.03`; NIST CSF `RC.RP` |
| `DTMO-GOV-01` Evidence-based release governance | Normenkader IBP `GO.03`; NIST CSF `GV` |

The crosswalk is intentionally partial. It describes verified relationships for implemented DTMO capabilities and leaves unrelated or unverified framework objects unmapped.

## E8 vulnerability & CTI evidence chain

The detailed implementation evidence behind `DTMO-TVM-01` / Normenkader IBP `SM.07` is maintained in `docs/governance/E8_VULNERABILITY_CTI_EVIDENCE_MAPPING.md`.

That mapping binds the completed E8 product slices to repository evidence for OpenCVE, CIRCL Vulnerability-Lookup, explainable prioritization, vendor/product relevance, vulnerability analytics, MISP read/export, AIL read/enrichment and AIL exact-match correlation. It also records supporting Normenkader IBP `SM.04` and `GO.03` relationships and preserves separate semantic boundaries for CVSS, EPSS, KEV, MITRE ATT&CK, MISP TLP/distribution, AIL and DTMO provenance.

The E8 mapping is an implementation-evidence chain under the existing explicit crosswalk; it is not a second authority model and does not convert repository CI into production, owner, legal or external assurance evidence.

## Intelligence mapping model

DTMO also maintains a persistent first-class intelligence mapping model in `intelligence_framework_mappings`. Those records bind a canonical intelligence UUID to a framework object and retain:

- framework ID and exact framework version;
- object type and identifier;
- provenance reference;
- confidence score;
- written mapping reason;
- review state;
- creator/reviewer identity and timestamps.

Only human-approved intelligence mappings count as intelligence mapping coverage. Pending or rejected mappings remain visible for governance and audit but are not treated as approved coverage.

## CVSS boundary

CVSS 4.0 remains context-only at the DTMO platform level until canonical intelligence has a first-class validated CVSS vector/base-score contract. A vulnerability record may therefore be related to `CVSS:4.0` as scoring context without DTMO claiming that its internal severity field is equivalent to a CVSS score.

## Source and implementation evidence

Every DTMO control crosswalk entry carries:

- authoritative external framework source URL;
- typed relationship;
- rationale;
- repository implementation references;
- crosswalk verification date.

The crosswalk is repository-controlled release content. Changes require normal pull-request review and exact-head CI rather than an unaudited runtime edit.

## Authority boundaries surfaced by Governance

1. Dashboard or console visibility never grants publication/share authority.
2. Human review and external-share approval remain separate authorities.
3. Service accounts/connectors do not receive human approval powers.
4. Missing, stale, inferred or inaccessible evidence is not `PASS`.
5. Governance knowledge and mappings do not themselves create authorization.
6. Framework mappings describe scoped relationships, not blanket compliance.
7. Environment-dependent controls remain partial until attributable environment evidence exists.

## Runtime contract

The canonical Governance area consumes complementary read contracts:

- `GET /api/v1/governance/knowledge` — internal governance/evidence boundaries;
- `GET /api/v1/governance/frameworks` — versioned framework inventory and intelligence-mapping coverage;
- `GET /api/v1/governance/frameworks/{framework_id}` — framework intelligence-mapping drill-down;
- `GET /api/v1/governance/control-crosswalk` — explicit DTMO-control-to-framework relationships.

Governed intelligence mapping writes remain available through the review-controlled API and require `review:intelligence` authority.

## Production-readiness boundary

The framework/control crosswalk and E8 evidence mapping are product and governance capabilities. They do not constitute Phase 8 production-equivalent environment evidence, Phase 9 independent assurance or Phase 10 production authorization.

Status of E8.10 on this branch: `CI_VALIDATION_PENDING` until the dedicated exact-head E8 governance evidence gate and the applicable regression matrix complete successfully.
