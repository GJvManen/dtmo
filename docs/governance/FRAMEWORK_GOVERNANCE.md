# DTMO Framework Governance

Status: `ACCEPTED_MERGED` for E5/E7 framework inventory and intelligence mapping; explicit DTMO control crosswalk extension `CI_VALIDATION_PENDING`.

## Purpose

E5/E7 introduces first-class, versioned framework governance for the canonical DTMO console. Framework inventory and intelligence mappings are explicit data objects rather than free-form UI labels.

## Authoritative framework inventory

The initial registry contains:

| Framework | DTMO version/revision | Authority | DTMO treatment |
|---|---|---|---|
| Normenkader IBP | content revision `2024-06-06` | Kennisnet | explicit control mapping |
| MITRE ATT&CK | `19.1` | MITRE | explicit technique mapping |
| CVSS | `4.0` | FIRST | context only until DTMO has a first-class CVSS vector/score contract |
| NIST Cybersecurity Framework | `2.0` | NIST | explicit category/subcategory mapping |

For Normenkader IBP the registry records 69 information-security norms and 25 privacy norms (94 total) as the known scope for coverage reporting.

Source references are stored on each framework record and were verified against the official framework authorities.

## Mapping truth model

DTMO uses three user-visible states for intelligence mappings:

- `MAPPED`: at least one explicit mapping has been approved by a human reviewer;
- `UNMAPPED`: no approved explicit mapping exists;
- `CONTEXT_ONLY`: the framework is intentionally contextual and is not represented as a first-class mapping/scoring contract.

A mapping is never inferred from title text, tags, severity, a CVE identifier, source metadata, or semantic similarity.

## Explicit DTMO control crosswalk

The Governance surface also exposes a repository-backed crosswalk between concrete DTMO controls/capabilities and external framework objects through `GET /api/v1/governance/control-crosswalk`.

The initial crosswalk covers high-value implemented DTMO controls including:

| DTMO control | External mappings represented |
|---|---|
| `DTMO-IAM-01` Governed RBAC and least privilege | Normenkader IBP `ID.02`, `ID.05`; NIST CSF `PR.AA` |
| `DTMO-AUTH-01` Authenticated and attributable access | Normenkader IBP `SM.02`; MITRE ATT&CK `T1078` as detection/mitigation context |
| `DTMO-AUD-01` Tamper-evident audit and correlation | Normenkader IBP `SM.04`; NIST CSF `DE.CM` |
| `DTMO-TVM-01` Threat and vulnerability intelligence lifecycle | Normenkader IBP `SM.07`; MITRE ATT&CK `T1087` as threat-classification context; NIST CSF `ID.RA`; CVSS 4.0 context |
| `DTMO-NET-01` Network and deployment trust boundaries | Normenkader IBP `SM.11` |
| `DTMO-REC-01` Backup, restore and recovery evidence | Normenkader IBP `OP.02`, `BC.03`; NIST CSF `RC.RP` |
| `DTMO-GOV-01` Evidence-based release governance | Normenkader IBP `GO.03`; NIST CSF `GV` |

Each relationship records an explicit relationship type, rationale, authoritative framework source and DTMO implementation references. `supports`, `partial-support`, `context-only` and threat-context relationships are deliberately distinguished.

These mappings do **not** claim certification, complete Normenkader IBP compliance, full NIST CSF coverage, or semantic equivalence with ATT&CK techniques. Environment-dependent requirements remain partial until the required environment evidence exists.

## First-class intelligence mapping fields

`intelligence_framework_mappings` stores:

- framework ID and exact framework version;
- object type (`control`, `technique`, `category`, `scoring_context`);
- control/technique/category identifier and optional title;
- canonical intelligence UUID;
- mapping status;
- provenance reference;
- confidence score (0–100);
- written mapping reason;
- review state (`pending`, `approved`, `rejected`);
- creator/reviewer identities and timestamps.

Only `approved` intelligence mappings contribute to intelligence mapping coverage. Pending and rejected objects remain visible for governance and audit but do not make an intelligence framework appear mapped.

## Human authorization and audit

Creating and reviewing an intelligence framework mapping requires `review:intelligence`. The existing RBAC model does not grant that permission to service accounts, so automated connectors cannot independently create an authoritative intelligence mapping.

Every intelligence mapping create, approve and reject action appends an event to DTMO's existing append-only persistent audit chain. The audit event records actor, action, resource, request/correlation ID and the mapping provenance reference.

The repository control crosswalk is code-reviewed release content rather than a user-editable runtime crosswalk. Changes therefore require pull-request review and exact-head CI.

## API

Read endpoints:

- `GET /api/v1/governance/frameworks`
- `GET /api/v1/governance/frameworks/{framework_id}`
- `GET /api/v1/governance/intelligence/{intelligence_id}/framework-mappings`
- `GET /api/v1/governance/control-crosswalk`

Governed write endpoints:

- `POST /api/v1/governance/framework-mappings`
- `POST /api/v1/governance/framework-mappings/{mapping_id}/review`

New intelligence mappings start as `pending`.

## Console behaviour

The Governance view contains two complementary first-class surfaces:

1. **Framework inventory & intelligence mappings** — framework version, mapping state, review state, intelligence object, confidence and provenance.
2. **DTMO control crosswalk** — implemented DTMO control, external framework object, typed relationship, rationale, authoritative source and implementation evidence.

This ensures that a fresh environment with no intelligence-specific mapping records still shows the concrete governance relationships already implemented by DTMO, while intelligence-specific ATT&CK/control mappings remain governed and reviewable rather than fabricated.

The older RC13 repository-governance surface remains as the internal governance/evidence layer.

## Database migration

Alembic migration `0010_framework_governance` follows `0009_managed_rbac_assignments` and creates:

- `governance_frameworks`;
- `intelligence_framework_mappings`.

The migration seeds only the framework inventory. It does **not** fabricate intelligence-to-control/technique mappings. The new DTMO control crosswalk is repository-backed code with explicit source and rationale instead of synthetic intelligence rows.

## Release evidence

E5/E7 was accepted with complete exact-head CI and merged through PR #181. The explicit DTMO control crosswalk extension remains `CI_VALIDATION_PENDING` until its own exact-head workflows and functional Governance acceptance are green.
