# Phase 8.2.10 — Audit and correlation validation

## Purpose

Validate attributable audit and correlation behavior on the owner-approved production-equivalent staging deployment. This repository-side contract does not claim external PASS by itself.

## Preconditions

- Phase 8.2 is active.
- The approved staging deployment identity is captured as one immutable environment/deployed commit/application image identity.
- The same deployment fingerprint is used for all Phase 8.2 evidence.
- Testing uses staging identities and endpoints only; production credentials, logging endpoints, and secrets are not reused.

## Validation procedure

1. Perform a representative authenticated user action and retain restricted evidence showing the attributable audit event.
2. Perform a representative denied or failed authorization action where the product is designed to audit it and confirm the event is recorded without sensitive authorization material.
3. Execute one representative privileged Administration action and confirm the audit record contains actor, action, target, outcome, timestamp, and correlation context.
4. Capture the request/correlation identifier for one representative request and trace it through the relevant application and audit records.
5. Confirm the correlated records reconstruct the request path and preserve coherent event ordering.
6. Confirm human and service-account actor identities are distinguishable in the audit evidence.
7. Inspect representative logs/audit records for bearer tokens, passwords, signing material, connection secrets, or other secret leakage. None may be present.
8. Confirm audit/correlation evidence is available to the intended authorized role and denied to roles that should not have access.
9. Record reviewer, timestamp, restricted evidence reference, environment identity, deployed commit, application image digest, and deployment fingerprint.

## Required PASS conditions

- Representative user and privileged actions create attributable audit records.
- Designed denial/failure events are auditable.
- Correlation context is propagated sufficiently to trace a representative request across relevant records.
- Actor type remains distinguishable between human and service identities.
- Event timestamps permit reconstruction of event order.
- Audit/log records do not leak bearer tokens or other secrets.
- Audit visibility follows the intended authorization boundary.
- No production logging/audit credentials or endpoints are reused.
- Evidence is bound to the same immutable Phase 8.2 deployment fingerprint.

## Fail-closed conditions

Mark `audit_correlation` as FAIL or leave it pending if any required evidence is absent, the deployment identity is incomplete, correlation cannot be demonstrated, actor attribution is ambiguous, secrets appear in records, or the evidence cannot be bound to the approved staging deployment.

Repository CI and synthetic fixtures are supporting evidence only and cannot establish external staging PASS.

## Evidence manifest

Set `checks.audit_correlation.result` to `PASS` only after the external procedure above succeeds and set `checks.audit_correlation.evidence_reference` to the restricted evidence location.

Validate the single step with:

```bash
python3 tools/phase8_platform_validation.py <manifest.json> --check audit_correlation
```

During step-scoped validation, `phase8_2_pass` and `phase8_pass` must remain `false`.

Related: issue #232 and Phase 8 tracker #158.
