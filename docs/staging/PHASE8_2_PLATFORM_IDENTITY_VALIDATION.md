# Phase 8.2 — Platform and Identity Validation

## Objective

Validate the deployed DTMO platform and identity/security controls against the **same immutable staging deployment identity** accepted in Phase 8.1.

Phase 8.2 does not create a new deployment identity and does not permit evidence to be mixed across deployments.

## Preconditions

- Phase 8.1 is `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE`.
- The staging environment remains the approved production-equivalent environment.
- The exact deployed commit and immutable application/supporting image identities still match the accepted Phase 8.1 identity.
- Evidence is written to the approved restricted evidence location; raw secrets, tokens and unnecessary personal data are not committed.

If the environment, commit or image identity changes, Phase 8.2 evidence must not be combined with evidence from the prior identity without a new accountable deployment-identity decision.

## Required validation classes

1. application health and readiness;
2. PostgreSQL connectivity and migration state;
3. OpenSearch health and search behavior;
4. Redis coordination;
5. object-storage read/write contract;
6. bearer-token issuer/audience/key trust;
7. RBAC enforcement;
8. strict human/service-account separation;
9. privileged Administration controls;
10. audit/correlation behavior;
11. Prometheus/operational metrics;
12. separately authenticated Grafana operational access.

Every class must have a `PASS` result and an attributable evidence reference.

## Evidence manifest

Copy `PHASE8_2_PLATFORM_IDENTITY_EVIDENCE.template.json` into the approved evidence workspace, populate only facts observed from the accepted staging deployment and calculate the deployment fingerprint with:

```bash
python3 tools/phase8_platform_validation.py <manifest.json> --print-fingerprint
```

Place that fingerprint into `deployment_identity_fingerprint`, then validate:

```bash
python3 tools/phase8_platform_validation.py <manifest.json>
```

A `PASS` from the validator means the Phase 8.2 evidence structure is complete and internally consistent. It does not independently prove that referenced external evidence is genuine; accountable review of the real environment remains required.

## Security boundaries

- Staging application/service identities must remain distinct from infrastructure root/admin identities.
- Production credentials must not be introduced for convenience.
- Grafana remains separately authenticated for operational/advanced use.
- Staging execution or Administration access does not grant publication/share authority.
- Evidence references may point to restricted external storage; secret values must not be copied into the repository.

## Acceptance rule

Phase 8.2 may be marked `PASS` only when all required platform and identity checks succeed against one consistent immutable deployment identity and the accountable reviewer accepts the evidence package.

`phase8_pass` must remain `false`: **Phase 8.3** source-to-intelligence validation, Phase 8.4 operational/recovery validation and Phase 8.5 accountable staging acceptance remain required.

## Next step after acceptance

Proceed to **Phase 8.3 — source-to-intelligence validation** against the same accepted deployment identity.
