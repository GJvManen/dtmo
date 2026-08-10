# RC10.4 Source Center Gate

Status: `CI_VALIDATION_PENDING`

## Scope
Repository-controlled acceptance for the bounded RC10.4 Source Center refinement.

## Required evidence
- `/ui/source-center` is wired into the RC10 application shell;
- `/api/v1/source-center/status` requires existing `MANAGE_CONNECTORS` permission and a human admin role;
- the projection integrates registered source identity, enabled state, interval/scheduling context, reliability, runtime health, latest success/failure, failure count/isolation and bounded provenance;
- optional runtime timestamps are explicitly null-safe before ISO serialization;
- secret references, raw quarantine evidence, request/response bodies and credentials are not projected;
- Source Center is read-only and delegates source mutations/manual runs to the accepted `/ui/admin-sources` control plane;
- ingestion does not grant review or external share approval;
- all registered GitHub workflows succeed on one final exact PR head.

## Current CI evidence
Exact head `294dcd6490a9e9dde6d21d648578214529dd9b07` is not acceptable: RC4 lint passed but mypy failed on three nullable runtime timestamp serializations; tests and compile were skipped and the release gate failed closed. RUN-182 narrows the optional state/timestamps. Complete CI must execute again on the resulting exact head before PASS.

## Claim boundary
PASS proves repository implementation/regression contracts only. It does not prove external source availability, real staging parity, genuine assistive-technology execution, penetration testing, external assurance or production readiness.
