# DTMO Security Risk Register

## Purpose

This register is the controlled index for material DTMO security and production-readiness risks. It uses the method defined in `RISK_MANAGEMENT.md`.

The register is intentionally conservative: only risks with sufficient evidence and ownership should be added as project risks. Unknown production-environment risks remain unknown until the relevant environment exists and is assessed.

## Current risk register

| Risk ID | Risk | Scope | Inherent rating | Treatment | Residual rating | Owner | Status | Evidence / next action |
|---|---|---|---|---|---|---|---|---|
| DTMO-RISK-001 | Production-equivalent staging deployment identity is not yet recorded | Phase 8 | High | Establish one approved staging environment and immutable deployment identity; bind all Phase 8 evidence to it | Not yet reassessed | Project / deployment owner | `OPEN` | Complete `docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md` with real environment evidence |
| DTMO-RISK-002 | Independent external security assurance is not yet complete | Phase 9 | High | Perform independent target-specific security assessment after Phase 8 environment is established; disposition and retest findings | Not yet reassessed | Security / project owner | `OPEN` | `docs/qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md` |
| DTMO-RISK-003 | Production authorization has not been granted | Phase 10 | High | Complete prerequisites and execute formal go/no-go decision | Not yet reassessed | Production governance | `OPEN` | `docs/project/PRODUCTION_GO_NO_GO_TEMPLATE.md` |
| DTMO-RISK-004 | External framework crosswalks are not yet first-class mappings | Governance | Moderate | Implement explicit provenance-backed mappings before claiming mapped status | Moderate | Governance / engineering | `TREATING` | Normenkader IBP and MITRE remain `UNMAPPED`; CVSS remains `CONTEXT_ONLY` |

## Interpretation

The ratings above are project-level governance assessments, not substitutes for target-environment risk analysis. Once a real staging environment is identified, Phase 8 must reassess environment-specific exposure such as network configuration, secrets, infrastructure identities, TLS, data handling, platform vulnerabilities and operational ownership.

No risk in `OPEN` or `TREATING` state is implicitly accepted. Formal residual-risk acceptance must record accountable authority and review/expiry conditions where applicable.

## Maintenance

Update this register when a material risk is identified, materially changed, accepted, closed or superseded. Detailed findings may remain in their originating assessment or issue; this register should retain the authoritative project-level risk state and reference the supporting evidence.
