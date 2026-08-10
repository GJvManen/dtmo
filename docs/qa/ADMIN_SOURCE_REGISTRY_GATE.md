# Admin Configuration & Source Registry Release Gate

Release: 16.0.0rc8

Current decision: `CI_VALIDATION_PENDING`

## Scope

This gate covers the repository-controlled admin source-registry control plane only. It does not claim generic registered-source execution, real staging acceptance, external assurance or production readiness.

## Required controls

- source mutations require `manage:connectors` and a human `admin` role;
- service accounts cannot use the human admin mutation surface;
- source IDs and supported source types are constrained;
- only HTTPS public-host endpoint configuration is accepted at registration time;
- localhost/internal suffixes, non-global literal IPs, embedded URL credentials and non-default HTTPS ports are rejected;
- credentials are represented only by approved secret references, never raw secret values;
- create/update mutations append persistent audit events;
- enabled state, reliability and poll interval are explicit configuration fields;
- the admin UI exposes inventory, status, create, enable/disable and validation functions;
- review, share approval and publication authority remain unchanged.

## Claim boundary

`json-feed` registration is configuration-only in 16.0.0rc8. Safe execution requires a later adapter with DNS-resolution and redirect-time SSRF validation, bounded response handling, content validation, provenance normalization, failure isolation and replay semantics. Registry validation must not be described as proof that a remote source is reachable, trustworthy or safe to execute.

## Evidence required for PASS

1. all registered GitHub workflows succeed on one final exact head;
2. migration contract tests pass for `0007_source_registry`;
3. RBAC/service-account separation regression tests pass;
4. unsafe source URL and raw-secret regression tests pass;
5. UI/API wiring regression tests pass;
6. no failing, cancelled, skipped or absent required workflow is treated as PASS.

Until those conditions are evidenced, status remains `CI_VALIDATION_PENDING`.
