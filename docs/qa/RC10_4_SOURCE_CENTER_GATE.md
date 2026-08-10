# RC10.4 Source Center Gate

Status: `CI_VALIDATION_PENDING`

## Scope
Repository-controlled acceptance for the bounded RC10.4 Source Center refinement.

## Required evidence
- `/ui/source-center` is wired into the RC10 application shell;
- `/api/v1/source-center/status` requires existing `MANAGE_CONNECTORS` permission and a human admin role;
- the projection integrates registered source identity, enabled state, interval/scheduling context, reliability, runtime health, latest success/failure, failure count/isolation and bounded provenance;
- secret references, raw quarantine evidence, request/response bodies and credentials are not projected;
- Source Center is read-only and delegates source mutations/manual runs to the accepted `/ui/admin-sources` control plane;
- ingestion does not grant review or external share approval;
- all registered GitHub workflows succeed on one final exact PR head.

## Claim boundary
PASS proves repository implementation/regression contracts only. It does not prove external source availability, real staging parity, genuine assistive-technology execution, penetration testing, external assurance or production readiness.
