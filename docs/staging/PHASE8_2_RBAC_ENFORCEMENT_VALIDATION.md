# Phase 8.2.7 — RBAC enforcement validation

Status: `REPOSITORY_CONTRACT_READY / EXTERNAL_EVIDENCE_REQUIRED`

## Objective
Validate positive and negative RBAC behavior on the owner-approved post-E8 production-equivalent staging deployment. This step is accepted only when the evidence is bound to the same immutable Phase 8.2 deployment identity used by all other staging checks.

## Preconditions
- Approved staging environment and owner-verified external deployment exist.
- Capture `environment_id`, exact deployed commit, immutable application image digest, Phase 8.1 identity fingerprint and deployment identity fingerprint before accepting the result.
- Use staging identities/credentials only. Production IAM credentials, tokens or signing material must not be reused.
- Repository CI, browser fixtures and emulator evidence are supporting evidence only and cannot substitute for external staging validation.

## Validation procedure
1. Authenticate with a representative least-privilege staging identity and verify it can perform only its intended read operations.
2. Attempt at least one privileged operation with that least-privilege identity and verify fail-closed denial.
3. Authenticate with a representative privileged identity and verify one explicitly granted administrative operation succeeds.
4. Verify a non-granted administrative operation remains denied, even for an otherwise privileged identity where the permission is outside scope.
5. Confirm direct API requests enforce the same authorization boundary as the UI; hidden UI controls are not an authorization control.
6. Where object/resource scoping applies, verify cross-scope access is denied.
7. Attempt to influence authorization with client-controlled role/identity headers or parameters and verify they are ignored/rejected unless they are part of the trusted authenticated claim path.
8. Change a test role/permission where operationally safe, confirm the new decision takes effect as designed, and verify stale privileges are not retained beyond the documented propagation boundary.
9. Verify denied actions create observable/auditable evidence without exposing sensitive authorization context or bearer material.
10. Record timestamp, reviewer, restricted evidence reference and the deployment fingerprint.

## Evidence record
Record the result in `checks.rbac_enforcement` with:

```json
{
  "result": "PASS",
  "evidence_reference": "<restricted evidence reference>"
}
```

Then validate only this step:

```bash
python3 tools/phase8_platform_validation.py <manifest.json> --check rbac_enforcement
```

`phase8_2_pass` and `phase8_pass` must remain `false` during this step-scoped validation.

## Acceptance
`PASS` requires both allowed and denied RBAC decisions to be demonstrated on the approved staging deployment, including API enforcement and resistance to client-controlled privilege escalation. Evidence must be attributable to the same immutable Phase 8.2 deployment identity.

Related: issue #225, #221, #158; PR #212, #224.
