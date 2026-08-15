# DTMO Framework Governance

Status: **`ACCEPTED / REPOSITORY_COMPLETE`** for versioned framework inventory, governed intelligence mappings, explicit DTMO control crosswalks and vulnerability-management evidence mappings.

## Purpose

DTMO implements first-class, versioned framework governance for the canonical console. Framework inventory, control crosswalks, intelligence mappings and evidence relationships are explicit governed objects rather than free-form UI labels or inferred semantic similarity.

## Authoritative framework inventory

| Framework | DTMO version/revision | Authority | DTMO treatment |
|---|---|---|---|
| Normenkader IBP | content revision `2024-06-06` | Kennisnet | explicit partial control/evidence relationships and governed intelligence mappings |
| MITRE ATT&CK | `19.1` | MITRE | explicit threat/detection/classification relationships and governed technique mappings |
| CVSS | `4.0` | FIRST | vulnerability-scoring context with explicit claim boundaries |
| NIST Cybersecurity Framework | `2.0` | NIST | explicit DTMO control outcome/category relationships |

The registry records source references and version/revision context so mapping claims can be reviewed against an explicit authority.

## Mapping truth model

DTMO distinguishes:

- `MAPPED` — an explicit governed relationship exists and is accepted for its declared scope;
- `UNMAPPED` — no approved explicit mapping exists for the object in question;
- `CONTEXT_ONLY` — the framework/model is deliberately used as context rather than as a first-class compliance/control mapping.

Mappings are never inferred from title text, tags, severity, CVE identifiers, source metadata or semantic similarity.

## Explicit DTMO control crosswalk

The Governance surface exposes repository-backed relationships between implemented DTMO controls/capabilities and external framework objects. High-value examples include:

| DTMO control | External mappings represented |
|---|---|
| `DTMO-IAM-01` Governed RBAC and least privilege | Normenkader IBP `ID.02`, `ID.05`; NIST CSF `PR.AA` |
| `DTMO-AUTH-01` Authenticated and attributable access | Normenkader IBP `SM.02`; MITRE ATT&CK `T1078` as security context |
| `DTMO-AUD-01` Audit and correlation | Normenkader IBP `SM.04`; NIST CSF `DE.CM` |
| `DTMO-TVM-01` Threat and vulnerability intelligence lifecycle | Normenkader IBP `SM.07`; NIST CSF `ID.RA`; ATT&CK threat context; CVSS context |
| `DTMO-NET-01` Network/deployment trust boundaries | Normenkader IBP `SM.11` |
| `DTMO-REC-01` Backup, restore and recovery evidence | Normenkader IBP `OP.02`, `BC.03`; NIST CSF `RC.RP` |
| `DTMO-GOV-01` Evidence-based release governance | Normenkader IBP `GO.03`; NIST CSF `GV` |

Each relationship records a typed relation, rationale, authoritative framework source and implementation/evidence references. `supports`, `partial-support`, `context-only`, `threat-context` and `evidence-support` are deliberately distinct semantics.

These mappings do **not** claim certification, complete Normenkader IBP compliance, full NIST CSF coverage or semantic equivalence with ATT&CK techniques.

## Vulnerability-management evidence mapping

The E8 governance evidence line adds explicit evidence relationships for the vulnerability/CTI capability chain, including OpenCVE, Vulnerability-Lookup, prioritization, vendor/product relevance, CVSS, EPSS, KEV, MISP and AIL.

The primary governance relationship is to Normenkader IBP `SM.07` for threat and vulnerability-management evidence, with supporting accountability/logging relationships where explicitly recorded. Semantic boundaries remain explicit:

- CVSS expresses vulnerability severity/scoring context, not organizational risk by itself;
- EPSS expresses exploitation probability context, not certainty;
- KEV expresses authoritative known-exploitation catalog status, not proof of local compromise;
- MITRE ATT&CK expresses threat/detection/classification context, not compliance;
- MISP TLP/distribution/taxonomy semantics constrain sharing and interpretation;
- AIL evidence remains bounded to governed read/enrichment/correlation behavior.

## First-class intelligence mapping fields

Governed intelligence mapping records retain framework ID/version, object type/identifier, canonical intelligence identity, mapping status, provenance, confidence, written reason, review state, creator/reviewer identity and timestamps.

Only approved intelligence mappings contribute to approved mapping coverage. Pending/rejected mappings remain visible for governance and audit but are not treated as accepted relationships.

## Human authorization and audit

Creating/reviewing governed intelligence mappings requires appropriate intelligence-review authority. Service accounts/connectors cannot independently establish authoritative human-approved mappings.

Mapping creation/review and privileged governance actions remain attributable through the audit/correlation model. Repository control/evidence crosswalks are reviewed release content rather than unaudited runtime edits.

## API and console behaviour

The canonical Governance area exposes versioned framework inventory, intelligence mapping drill-down, explicit DTMO control crosswalks and vulnerability-management evidence mappings through authenticated contracts.

The console separates:

1. framework inventory and intelligence mappings;
2. DTMO control crosswalks;
3. vulnerability-management evidence mappings and their claim boundaries.

This allows a fresh environment to show implemented governance relationships without fabricating intelligence-specific mappings.

## Data model and migration boundary

The framework-governance persistence model stores the framework inventory and governed intelligence mapping state. Seed data establishes the registry only; it does not fabricate intelligence-to-control/technique relationships.

Repository-backed control/evidence mappings remain reviewed release content with explicit sources and rationale.

## Production-readiness boundary

Framework governance is an accepted product capability within the repository evidence boundary. It does not prove Phase 8 environment effectiveness, Phase 9 independent assurance or Phase 10 production authorization.

**Current decision:** framework governance, control crosswalk and E8 vulnerability-management evidence mapping are repository-complete. Environment-specific effectiveness and broader compliance claims remain subject to attributable external evidence.
