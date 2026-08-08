# Open-source Governance QA Gate

## Objective

Provide an auditable Apache-2.0 licensing and open-source governance baseline for DTMO without changing product runtime behavior.

## Accepted evidence

PR #44 exact head `38ba52f700a4324de6039db58422006ad8a17a96` completed all 16 registered required workflows successfully.

The dedicated `Open Source Governance Gate` succeeded and retained artifact `9028364655`, digest `sha256:0e63aed861c8e761d626413227f1f2817fe2e36d6a1291fa2a0ebcfac521d83a`. Independent inspection confirmed 5 focused tests, 0 failures, 0 errors and 0 skipped, plus the expected Apache-2.0/governance manifest.

Accepted controls:

- complete Apache License 2.0 root `LICENSE`;
- root `NOTICE`;
- Python package metadata `Apache-2.0`;
- `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`;
- project licensing and third-party rights policies;
- README governance entry points;
- focused regression protection and retained CI evidence.

## Fail-closed boundary

This PASS applies to DTMO's project-level licensing/governance baseline only. It does not prove licence compatibility or redistribution rights for every resolved dependency, provider feed, CVE/vendor-advisory source, threat-intelligence dataset or trademark. Version-specific SBOM/dependency licence and provider-terms evidence remains required for production/public distribution.

RBAC, separation of duties, privacy controls, provenance, auditability and human share approval were not weakened or modified.

## Decision

`PASS`. PR #44 merged with expected-head protection as `565c9df9eea133b2e7b1f58fb3d5d772c7753e9b`.
