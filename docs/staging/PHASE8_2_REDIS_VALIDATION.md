# Phase 8.2.4 — Redis Coordination Validation

**Status:** `READY_FOR_EXTERNAL_VALIDATION`

## Objective

Validate Redis coordination behavior against the owner-approved post-E8 production-equivalent staging deployment and bind the accepted result to the same immutable Phase 8.2 deployment identity.

## Preconditions

- Phase 8.2 is active on `main`.
- Step-scoped evidence validation is available.
- The accepted staging deployment remains unchanged for the evidence being collected.
- Immutable environment/deployed commit/application image identity must be captured before formal step acceptance.

## Required observations

1. Confirm application-to-Redis connectivity using the intended staging configuration and service identity.
2. Confirm no production credentials are reused.
3. Exercise the Redis-backed coordination primitive used by DTMO and record the successful behavior.
4. Where applicable, observe expiry/TTL behavior and confirm stale coordination state expires as designed.
5. Confirm duplicate/stale coordination state does not cause unsafe duplicate processing or inconsistent state transitions.
6. Exercise or observe Redis degradation/unavailability and confirm the application fails safely and the condition is observable.
7. Record timestamp, accountable reviewer and restricted evidence reference without secret values.
8. Bind the evidence to the same Phase 8.2 deployment fingerprint used by all other accepted checks.

## Evidence boundary

Repository CI, Docker Compose, emulators and synthetic fixtures are supporting evidence only. They cannot satisfy the external staging acceptance requirement. Do not commit Redis passwords, tokens or other secret material.

## Step validation

Populate `checks.redis_coordination` in the restricted Phase 8.2 evidence manifest and run:

```bash
python3 tools/phase8_platform_validation.py <manifest.json> --check redis_coordination
```

A step-level `PASS` confirms that the evidence record is internally consistent and identity-bound. It does not independently prove the external observations; accountable review remains required.

## Acceptance

Phase 8.2.4 is `PASS` only when Redis coordination succeeds on the approved staging deployment, safe degraded behavior is demonstrated or observed, and the evidence is attributable to the same immutable deployment identity used by the rest of Phase 8.2.

`phase8_2_pass` and `phase8_pass` must remain `false` until their later acceptance gates are complete.

## Next step

Proceed to **Phase 8.2.5 — object-storage read/write contract** after the Redis evidence is accepted or remains explicitly tracked against the same immutable deployment identity.
