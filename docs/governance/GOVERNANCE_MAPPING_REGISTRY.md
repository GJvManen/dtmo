# DTMO Governance Mapping Registry

Last updated: **2026-08-15**

## Purpose

This registry is the repository authority for framework and governance mapping claims exposed by DTMO. It separates:

1. **DTMO control crosswalks** — explicit relationships between implemented DTMO capabilities and external framework objects;
2. **intelligence mappings** — governed mappings between individual intelligence records and framework controls/techniques/categories;
3. **evidence mappings** — explicit relationships between repository-backed security/vulnerability capabilities and governance evidence objectives;
4. **context-only semantics** — models such as CVSS that provide analytical context without becoming a compliance framework.

## Claim rule

DTMO never infers framework/control/technique equivalence merely because concepts appear related. Every exposed mapping requires an explicit identifier, relationship type, rationale and provenance/source reference.

A relationship such as `supports`, `partial-support`, `threat-classification-context`, `evidence-support` or `context-only` is not equivalent to certification, complete compliance, maturity or demonstrated effectiveness in a specific environment.

## Framework inventory and current treatment

| Framework | Version/revision | Current DTMO treatment |
|---|---|---|
| Normenkader IBP | content revision `2024-06-06` | explicit partial DTMO control crosswalks, governed intelligence mappings and vulnerability-management evidence mappings |
| MITRE ATT&CK | registry version `19.1` | explicit threat/detection/classification relationships plus governed intelligence technique mappings |
| NIST Cybersecurity Framework | `2.0` | explicit DTMO control outcome/category relationships |
| CVSS | `4.0` | vulnerability-scoring context with explicit claim boundaries; not a compliance framework |

## Repository-backed DTMO control crosswalk

The canonical Governance surface exposes explicit DTMO-control-to-framework relationships, including:

| DTMO control | External objects represented |
|---|---|
| `DTMO-IAM-01` Governed RBAC and least privilege | Normenkader IBP `ID.02`, `ID.05`; NIST CSF `PR.AA` |
| `DTMO-AUTH-01` Authenticated and attributable access | Normenkader IBP `SM.02`; MITRE ATT&CK `T1078` as security context |
| `DTMO-AUD-01` Audit and request correlation | Normenkader IBP `SM.04`; NIST CSF `DE.CM` |
| `DTMO-TVM-01` Threat and vulnerability intelligence lifecycle | Normenkader IBP `SM.07`; NIST CSF `ID.RA`; MITRE ATT&CK threat context; CVSS context |
| `DTMO-NET-01` Network/deployment trust boundaries | Normenkader IBP `SM.11` |
| `DTMO-REC-01` Backup, restore and recovery evidence | Normenkader IBP `OP.02`, `BC.03`; NIST CSF `RC.RP` |
| `DTMO-GOV-01` Evidence-based release governance | Normenkader IBP `GO.03`; NIST CSF `GV` |

The crosswalk is intentionally partial. Unrelated or unverified framework objects remain unmapped.

## Vulnerability-management evidence mapping

The E8 governance evidence line is repository-complete and maps concrete vulnerability/CTI capabilities to governed evidence objectives without claiming blanket compliance.

The mapping includes explicit semantics for:

- OpenCVE and Vulnerability-Lookup ingestion/provenance;
- explainable vulnerability prioritization;
- vendor/product/CPE relevance;
- CVSS as scoring context rather than compliance evidence by itself;
- EPSS as exploitation-probability context rather than certainty;
- KEV as authoritative known-exploitation catalog context rather than proof of local compromise;
- MITRE ATT&CK as threat/detection/classification context;
- MISP taxonomy/TLP/distribution and governed read/share boundaries;
- AIL read/enrichment/correlation boundaries;
- Normenkader IBP `SM.07` as the primary vulnerability-management evidence relationship with supporting accountability/logging context where explicitly mapped.

These mappings demonstrate that DTMO can produce or retain repository-backed evidence relevant to defined governance objectives. They do not prove organizational control maturity, implementation effectiveness in a specific deployment, certification, local exposure, exploitability, compromise or remediation completion.

## Intelligence mapping model

Persistent intelligence mapping records bind canonical intelligence to framework objects and retain framework/version, object type/identifier, provenance, confidence, written mapping reason, review state and creator/reviewer context.

Only explicitly reviewed/approved mappings count as approved mapping coverage. Pending or rejected relationships remain visible but are not treated as accepted coverage.

## CVSS boundary

CVSS 4.0 remains a vulnerability-scoring context. DTMO does not equate its internal severity/classification directly with a CVSS base score or claim that a CVSS relationship is a compliance-control mapping.

Where CVSS data is present, its source/provenance and semantic meaning remain distinct from EPSS, KEV, source confidence, local relevance and analyst decision state.

## Source and implementation evidence

Control/evidence mappings use explicit framework identifiers, typed relationships, rationale, provenance and repository-backed implementation/test evidence. Changes are normal reviewed release content and require applicable exact-head CI.

## Authority boundaries surfaced by Governance

1. Console visibility never grants publication/share authority.
2. Human review and external-share approval remain separate authorities.
3. Service accounts/connectors do not receive human approval powers.
4. Missing, stale, inferred or inaccessible evidence is not `PASS`.
5. Governance knowledge/mappings do not themselves create authorization.
6. Framework mappings describe scoped relationships, not blanket compliance.
7. Environment-dependent controls remain incomplete until attributable environment evidence exists.
8. Repository evidence does not replace independent external assurance.

## Runtime contract

The canonical Governance area consumes versioned framework knowledge, framework drill-down, explicit DTMO control crosswalks and vulnerability-management evidence mappings through authenticated read contracts. Governed intelligence mapping writes remain review-controlled and require appropriate intelligence-review authority.

## Production-readiness boundary

Governance mappings are product/governance capabilities. They do not constitute Phase 8 production-equivalent environment acceptance, Phase 9 independent assurance or Phase 10 production authorization.

**Current status:** repository governance/control/evidence mapping capability is accepted within the repository evidence boundary, including E8.10. External environment effectiveness and assurance claims remain subject to the applicable Phase 8 and Phase 9 gates.
