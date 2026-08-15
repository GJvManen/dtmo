# Phase 8.2.6 — Bearer-token trust validation

## Purpose

Validate the authentication trust boundary on the owner-approved post-E8 production-equivalent staging deployment. This is external deployment evidence and must be attributable to the same immutable Phase 8.2 deployment identity as the other platform checks.

Repository CI, unit tests and synthetic token fixtures are supporting evidence only and cannot establish staging PASS.

## Preconditions

- approved staging environment and access path are known;
- `environment_id`, exact `deployed_commit`, immutable `application_image_digest` and deployment fingerprint are recorded;
- the intended staging token issuer/trust configuration is known;
- no production signing secret, private key, bearer token or production identity is used.

## Validation procedure

1. Record the deployment fingerprint and restricted evidence reference before testing.
2. Confirm the intended staging issuer/trust configuration is active for the deployed application.
3. Present a valid staging bearer token with the minimum claims required for one protected request and verify that the request is accepted.
4. Repeat the same request without a token and verify fail-closed rejection.
5. Present an expired token and verify rejection.
6. Present a malformed token or a token with an invalid signature and verify rejection.
7. Where issuer/audience validation is configured, present a token with the wrong issuer or audience and verify rejection.
8. Confirm that identity/authorization is derived from verified token claims rather than client-supplied identity headers.
9. Confirm authentication failures are observable in operational telemetry without logging bearer-token material or signing secrets.
10. Record reviewer, timestamp and the restricted evidence reference.

## Expected result

`checks.bearer_token_trust.result` may be set to `PASS` only when all applicable checks above succeed on the approved staging deployment and the evidence is bound to the same immutable Phase 8.2 deployment fingerprint.

Use the step-scoped validator:

```bash
python3 tools/phase8_platform_validation.py <manifest.json> --check bearer_token_trust
```

During step-scoped validation, both `phase8_2_pass` and `phase8_pass` must remain `false`.

## Fail-closed conditions

Record `FAIL` rather than `PASS` if any of the following occurs:

- invalid, expired, wrong-issuer or wrong-audience tokens are accepted when they should be rejected;
- protected routes accept missing bearer tokens;
- caller identity can be overridden by untrusted request headers;
- production credentials/signing material are reused;
- evidence cannot be attributed to the immutable staging deployment identity;
- authentication failure telemetry leaks token or secret material.

Related tracking: #221, #158.
