# DTMO Security Responsibility Matrix

## Purpose

This matrix makes security ownership and authority boundaries explicit for engineering, operations, governance, assurance and accountable human decisions. It is designed for internal review and external assessment.

## Responsibility matrix

| Security domain | Engineering | Operations | Security / governance | Project owner | Independent assessor |
|---|---|---|---|---|---|
| Secure implementation | **R** | C | C | I | I |
| Architecture integrity | **R** | C | C | I | I |
| Identity integration | **R** | C | **A/C** | I | I |
| RBAC enforcement | **R** | I | **A/C** | I | I |
| Service-account separation | **R** | C | **A/C** | I | I |
| Secret handling design | **R** | **R** | **A/C** | I | I |
| Source/connector security | **R** | C | **A/C** | I | I |
| Provenance integrity | **R** | I | **A/C** | I | I |
| Logging / correlation | **R** | **R** | C | I | I |
| Vulnerability handling | **R** | C | **A** | I | C |
| Environment hardening | C | **R** | **A/C** | I | C |
| Backup / recovery controls | C | **R** | C | I | C |
| Security exceptions | C | C | **R** | **A** where accountable acceptance is required | I |
| Framework mapping claims | C | I | **R/A** | I | C |
| Phase 8 security acceptance | C | **R** | **R/A** | C | I |
| Phase 9 independent assurance | C | C | C | I | **R/A** |
| Production go/no-go | C | C | C | **A** | C |
| External-share approval | I | I | C | governed human authority | I |

**R** = Responsible, **A** = Accountable, **C** = Consulted, **I** = Informed.

Where organizational role assignments differ in a deployment, the deployment-specific responsibility record must identify the named accountable parties without weakening the authority boundaries above.

## Non-transferable authority boundaries

The following authorities must not be inferred from technical access:

- CI administration does not grant product-owner acceptance.
- Infrastructure administration does not grant intelligence publication authority.
- Connector execution does not grant review or external-share approval.
- Application Administration does not automatically grant security-risk acceptance.
- Repository write access does not grant Phase 8, Phase 9 or Phase 10 acceptance.
- External assessment does not itself authorize production deployment; it supplies evidence to the accountable production decision.

## Security evidence ownership

| Evidence class | Evidence producer | Acceptance boundary |
|---|---|---|
| Source code and automated security tests | Engineering / CI | Repository-controlled engineering |
| Runtime engineering tests | Engineering | Reference/runtime engineering |
| Staging configuration and hardening evidence | Operations + security | Phase 8 environment acceptance |
| Vulnerability/advisory disposition | Security + engineering/operations | Target-specific security acceptance |
| Penetration test / independent assessment | Independent assessor | Phase 9 external assurance |
| Risk exception | Security/governance + accountable risk owner | Explicit bounded exception |
| Production authorization | Accountable production authority | Phase 10 go/no-go |

## Separation of duties

At minimum, DTMO preserves separation between source administration, analysis, review, external sharing, principal/role administration, infrastructure administration, security governance and independent assurance. A deployment may combine individuals in roles only where the resulting risk is explicitly reviewed and accepted; the platform model must not silently collapse the authority boundaries.

## Related documents

- `SECURITY_OVERVIEW.md`
- `../project/PROJECT_GOVERNANCE.md`
- `../project/PRODUCTION_READINESS_REPORT.md`
- `../qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md`
