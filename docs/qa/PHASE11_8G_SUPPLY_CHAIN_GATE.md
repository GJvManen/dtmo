# Phase 11.8g — Software supply-chain gate

## Acceptance criteria

The bounded slice is repository-complete only when the exact PR head proves all of the following:

- exact-head checkout is enforced;
- a distributable wheel can be built and SHA-256 identified;
- a Python CycloneDX SBOM is generated from the resolved environment;
- Python dependency vulnerability auditing completes successfully;
- the candidate container image builds successfully;
- the candidate image is scanned for governed `HIGH`/`CRITICAL` OS and library vulnerabilities and findings fail closed;
- a container CycloneDX SBOM is generated;
- the governed release workflow contains OIDC-backed signed provenance and SBOM attestation steps for the release wheel and container archive;
- no long-lived signing key or credential is stored in repository configuration;
- professional architecture/security, operations, QA, evidence and lifecycle documentation is synchronized.

## Release signing boundary

PR CI validates the signing/attestation mechanism but does not manufacture release evidence. Signed provenance and SBOM attestations become evidence only when the governed release workflow actually executes for the exact release subject.

## Non-claims

A green repository gate **does not prove** future release signing, registry integrity, deployment admission, live verification, absence of all vulnerabilities, production-equivalent behavior, independent assurance or production authorization.

## Fail-closed rule

Missing SBOM, scan output, artifact identity, release attestation mechanism or required documentation is not accepted as `PASS`. Historical Phase 8/9 evidence cannot satisfy this materially changed candidate's supply-chain gate.
