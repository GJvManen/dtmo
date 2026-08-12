# DTMO External Assessment Evidence Request

## Purpose

This checklist defines the evidence package to prepare for an authorized independent assessor. Evidence must be scoped to the approved assessment and must not expose secrets merely for convenience.

## Package index

| Evidence class | Expected material | Status before real assessment |
|---|---|---|
| Assessment identity | assessor, scope, dates, authorization | `NOT_PROVIDED` |
| Deployment identity | immutable staging identity and target inventory | `NOT_PROVIDED` |
| Architecture | context, trust boundaries, data flows | repository documentation available |
| Security model | RBAC, service accounts, approval boundaries | repository documentation available |
| Threat/risk | threat model, current risk register, accepted exceptions | repository documentation available |
| Operations | operating model, incident and recovery procedures | repository documentation available |
| Test accounts | purpose-created role-specific identities | `NOT_PROVIDED` |
| Runtime configuration | sanitized relevant environment configuration | `NOT_PROVIDED` |
| Dependency inventory | applicable dependency/SBOM evidence | subject to assessed identity |
| Prior findings | relevant open findings and dispositions | subject to controlled disclosure |
| Logs/observability | approved access or exported evidence | `NOT_PROVIDED` |
| Recovery evidence | environment-specific backup/restore evidence | `NOT_PROVIDED` |

## Evidence handling

Evidence should be classified before transfer. Repository-public or normal project documentation may be shared according to its classification. Restricted runtime artifacts, assessor credentials, security findings and sensitive logs must use the approved restricted transfer mechanism.

Do not provide raw secrets, reusable production credentials, unrelated personal data or unrelated environment details.

## Evidence manifest

For the real engagement, maintain a manifest containing:

- evidence identifier;
- title and description;
- classification;
- owner;
- source;
- commit/release/deployment identity where applicable;
- collection timestamp where applicable;
- integrity reference where required;
- assessor receipt or transfer reference.

## Claim boundary

Repository evidence can establish design and engineering facts. Claims about the production-equivalent environment require evidence collected from the recorded deployment identity. Independent-assurance conclusions must come from the authorized assessor and cannot be pre-populated by the project team.
