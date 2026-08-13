# DTMO Framework Governance

Status: `ACCEPTED_MERGED`

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

Source references are stored on each framework record and were verified on 2026-08-12 against the official framework authorities.

## Mapping truth model

DTMO uses three user-visible states:

- `MAPPED`: at least one explicit mapping has been approved by a human reviewer;
- `UNMAPPED`: no approved explicit mapping exists;
- `CONTEXT_ONLY`: the framework is intentionally contextual and is not represented as a first-class mapping/scoring contract.

A mapping is never inferred from title text, tags, severity, a CVE identifier, source metadata, or semantic similarity.

## First-class mapping fields

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

Only `approved` mappings contribute to mapping coverage. Pending and rejected objects remain visible for governance and audit but do not make a framework appear mapped.

## Human authorization and audit

Creating and reviewing a framework mapping requires `review:intelligence`. The existing RBAC model does not grant that permission to service accounts, so automated connectors cannot independently create an authoritative framework mapping.

Every mapping create, approve and reject action appends an event to DTMO's existing append-only persistent audit chain. The audit event records actor, action, resource, request/correlation ID and the mapping provenance reference.

## API

Read endpoints:

- `GET /api/v1/governance/frameworks`
- `GET /api/v1/governance/frameworks/{framework_id}`
- `GET /api/v1/governance/intelligence/{intelligence_id}/framework-mappings`

Governed write endpoints:

- `POST /api/v1/governance/framework-mappings`
- `POST /api/v1/governance/framework-mappings/{mapping_id}/review`

New mappings start as `pending`.

## Console behaviour

The Governance view contains a first-class framework surface with:

- framework name, authority and exact version/revision;
- `MAPPED`, `UNMAPPED` or `CONTEXT_ONLY` state;
- approved, pending and rejected mapping counts;
- mapped-object count and coverage percentage where the authoritative scope count is known;
- drill-down from framework to control/technique/category;
- mapped intelligence title/ID;
- confidence, review state, reviewer, provenance and mapping reason.

The older RC13 repository-governance surface remains as the internal governance/evidence layer. It is not a substitute for the new first-class external framework registry.

## Database migration

Alembic migration `0010_framework_governance` follows `0009_managed_rbac_assignments` and creates:

- `governance_frameworks`;
- `intelligence_framework_mappings`.

The migration seeds only the framework inventory. It does **not** seed control/technique crosswalks because that would create unsupported mapping claims.

## Release evidence

Accepted with complete exact-head CI and merged through PR #181 on 2026-08-12. Merge commit: `1065cde58a10e5d7657d5e2a13d81aaaf3cc1a28`.
