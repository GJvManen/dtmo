# Phase 8.2 — Platform and Identity Validation

**Status:** `IN PROGRESS / ACTIVE`

## Objective

Validate the deployed DTMO platform and identity/security controls against the **same owner-approved post-E8 staging deployment** and bind the resulting evidence to one immutable deployment identity.

All accepted Phase 8.2 results must ultimately bind to the **same immutable staging deployment identity**. Phase 8.2 does not create a new deployment identity and does not permit evidence to be mixed across deployments.

## Preconditions

The following preconditions are satisfied:

- Phases 1–7 are `PASS`;
- RC13 functional acceptance is `PASS / OWNER_ACCEPTED`;
- E8.1–E8.10 are repository-complete;
- the post-E8 external deployment has been extensively and successfully owner-tested;
- the production-equivalent staging environment is owner-approved.

The remaining exact commit/image/runtime identity fields may be collected while Phase 8.2 evidence is gathered, but **formal Phase 8.2 PASS requires all accepted results to be bound to that same immutable identity**. Evidence must be written to the approved restricted evidence location; raw secrets, tokens and unnecessary personal data are not committed.

If the environment, deployed commit or image identity materially changes, Phase 8.2 evidence must not be combined with evidence from the prior deployment without a new accountable deployment-identity decision.

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

Every class must have a `PASS` result and an attributable evidence reference before formal Phase 8.2 acceptance.

## Evidence manifest

Copy `PHASE8_2_PLATFORM_IDENTITY_EVIDENCE.template.json` into the approved evidence workspace and populate only facts observed from the accepted staging deployment. The evidence manifest may be populated progressively while immutable identity fields are collected; the validator remains fail-closed until all required values and checks are complete.

Calculate the deployment fingerprint with:

```bash
python3 tools/phase8_platform_validation.py <manifest.json> --print-fingerprint
```

Place that fingerprint into `deployment_identity_fingerprint`, then validate:

```bash
python3 tools/phase8_platform_validation.py <manifest.json>
```

A `PASS` from the validator means the Phase 8.2 evidence structure is complete and internally consistent. It does not independently prove that referenced external evidence is genuine; accountable review of the real environment remains required.

## Execution order

Perform Phase 8.2 in this order so failures are isolated before privileged checks are attempted:

1. **8.2.1 — application health/readiness**;
2. **8.2.2 — PostgreSQL connectivity/migrations**;
3. **8.2.3 — OpenSearch health/search**;
4. **8.2.4 — Redis coordination**;
5. **8.2.5 — object-storage read/write**;
6. **8.2.6 — bearer-token trust**;
7. **8.2.7 — RBAC enforcement**;
8. **8.2.8 — human/service-account separation**;
9. **8.2.9 — privileged Administration controls**;
10. **8.2.10 — audit/correlation behavior**;
11. **8.2.11 — Prometheus/operational metrics**;
12. **8.2.12 — separately authenticated Grafana access**;
13. **8.2.13 — evidence-manifest validation and accountable Phase 8.2 decision**.

## Security boundaries

- Staging application/service identities must remain distinct from infrastructure root/admin identities.
- Production credentials must not be introduced for convenience.
- Grafana remains separately authenticated for operational/advanced use.
- Staging execution or Administration access does not grant publication/share authority.
- Evidence references may point to restricted external storage; secret values must not be copied into the repository.

## Acceptance rule

Phase 8.2 may be marked `PASS` only when all required platform and identity checks succeed against one consistent immutable deployment identity and the accountable reviewer accepts the evidence package.

`phase8_pass` must remain `false`: **Phase 8.3** source-to-intelligence validation, Phase 8.4 operational/recovery validation and Phase 8.5 accountable staging acceptance remain required.

## Current step

**8.2.1 — application health/readiness** is the active validation step.

## Next step after acceptance

Proceed to **Phase 8.3 — source-to-intelligence validation** against the same accepted deployment identity only after all Phase 8.2 checks and evidence binding have passed.
