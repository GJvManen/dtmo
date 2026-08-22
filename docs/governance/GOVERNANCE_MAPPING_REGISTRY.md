# DTMO Governance Mapping Registry

Last updated: **2026-08-21**

## Purpose

This registry is the repository authority for framework and governance mapping claims exposed by DTMO. It separates explicit DTMO control crosswalks, governed intelligence mappings, evidence mappings and context-only semantics such as CVSS.

## Claim rule

DTMO never infers framework/control/technique equivalence merely because concepts appear related. Every exposed external relationship requires an explicit identifier, relationship type, rationale and provenance/source reference. `supports`, `partial-support`, `detection-and-mitigation-context`, `threat-classification-context`, `evidence-support` and `context-only` are **not** certification, complete compliance, maturity or demonstrated environment effectiveness.

## Framework inventory and current treatment

| Framework | Version/revision | Current DTMO treatment |
|---|---|---|
| Normenkader IBP | content revision `2024-06-06` | explicit partial DTMO control crosswalks and evidence relationships |
| MITRE ATT&CK | registry version `19.1` | explicit detection/threat-classification context; no inference from free text |
| NIST Cybersecurity Framework | `2.0` | explicit partial DTMO control outcome/category relationships |
| CVSS | `4.0` | vulnerability-scoring context only; not a compliance framework |

## Repository-backed DTMO control crosswalk

The canonical source is `backend/dtmo/governance_crosswalk.py`. The Governance & Evidence workspace may surface only relationships present there.

| DTMO control | Explicit external objects represented |
|---|---|
| `DTMO-IAM-01` Governed RBAC and least privilege | Normenkader IBP `ID.02`, `ID.05`; NIST CSF `PR.AA` |
| `DTMO-AUTH-01` Authenticated and attributable access | Normenkader IBP `SM.02`; MITRE ATT&CK `T1078` as detection/mitigation context |
| `DTMO-AUD-01` Audit and request correlation | Normenkader IBP `SM.04`; NIST CSF `DE.CM` |
| `DTMO-TVM-01` Threat and vulnerability intelligence lifecycle | Normenkader IBP `SM.07`; NIST CSF `ID.RA`; MITRE ATT&CK `T1087` threat-classification context; CVSS `4.0` context |
| `DTMO-NET-01` Network/deployment trust boundaries | Normenkader IBP `SM.11` |
| `DTMO-REC-01` Backup, restore and recovery evidence | Normenkader IBP `OP.02`, `BC.03`; NIST CSF `RC.RP` |
| `DTMO-GOV-01` Evidence-based release governance | Normenkader IBP `GO.03`; NIST CSF `GV` |

The crosswalk is intentionally partial. Unrelated, unrecorded or unverified framework objects remain unmapped.

## Vulnerability-management evidence mapping

The repository maps concrete vulnerability/CTI capabilities to scoped governance evidence objectives without claiming blanket compliance. OpenCVE/Vulnerability-Lookup provenance, explainable prioritization, vendor/product relevance, CVSS, EPSS, KEV, MISP/AIL boundaries and Normenkader IBP `SM.07` may provide defined evidence context. These relationships do not prove organizational maturity, implementation effectiveness in a deployment, certification, local exposure, exploitability, compromise or remediation completion.

## Intelligence mapping model

Persistent intelligence mapping records bind canonical intelligence to framework objects and retain framework/version, object type/identifier, provenance, confidence, mapping reason, review state and creator/reviewer context. Only explicitly reviewed/approved mappings count as approved intelligence mapping coverage; pending or rejected records are not accepted coverage.

## CVSS boundary

CVSS 4.0 remains scoring context. DTMO does not equate internal severity/classification directly with a CVSS base score and does not treat CVSS as a compliance-control mapping. CVSS, EPSS, KEV, source confidence, local relevance and analyst decision state remain semantically distinct.

## Authority boundaries surfaced by Governance

1. Console/workbench visibility never grants publication/share authority.
2. Human review and external-share approval remain separate authorities.
3. Case handoff, connector execution and administration remain separate permissions.
4. Service accounts/connectors do not receive human approval powers.
5. Missing, stale, inferred or inaccessible evidence is not `PASS`.
6. Framework mappings describe scoped relationships, not blanket compliance.
7. Environment-dependent controls remain incomplete until attributable environment evidence exists.
8. Repository evidence does not replace accountable owner acceptance, production-equivalent validation or independent external assurance.
9. Governance knowledge does not create production authorization.

## Phase 11.10l runtime contract

The canonical `/workbench/governance` surface consumes same-origin `GET /api/v1/governance/knowledge`, protected by server-side `read:intelligence`. The snapshot combines internal governance mappings with the explicit crosswalk above. Browser code does not infer control/technique relationships and does not require external framework-service credentials.

Phase 11.10l is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 11.10a–11.10k are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 overall remains `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`.

## Production-readiness boundary

Phase 8 remains `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE`; Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`; Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. Historical evidence cannot be reused for the materially changed candidate.

Phase 11.10m–11.10o, Phase 11.11 and Phase 12 remain `NOT STARTED`; Phase 11.10p is `NOT STARTED / CANDIDATE FREEZE REQUIRED`. Repository governance/control mappings and CI are repository engineering evidence only. DTMO remains **not production authorized**.
