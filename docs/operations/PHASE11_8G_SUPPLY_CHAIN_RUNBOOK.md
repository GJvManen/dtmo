# Phase 11.8g — Software supply-chain runbook

## Preconditions

Use only an accepted source revision. Confirm that the release artifact being assessed is bound to the intended commit/tag and that no secret, credential or private signing key is present in repository configuration. Release attestations use short-lived OIDC-backed signing; no long-lived signing credential is permitted in Git.

## PR validation

1. Verify the workflow checked out the exact PR head.
2. Install the governed test environment and run the Phase 11.8g contract.
3. Build the DTMO wheel and record SHA-256 hashes.
4. Generate the Python CycloneDX SBOM and vulnerability report.
5. Build the candidate container image.
6. Run the container vulnerability scan; any governed `HIGH` or `CRITICAL` finding causes a fail-closed gate failure.
7. Generate the container CycloneDX SBOM.
8. Preserve only non-sensitive evidence artifacts.

PR evidence proves the repository mechanism and exact-head scan result only. It is not release signing evidence.

## Release signing and attestation

For an approved release artifact, run the governed release workflow from the intended release identity. The workflow builds the wheel and container archive, records SHA-256 subject identities, re-runs vulnerability/SBOM generation and produces signed provenance and SBOM attestations through the GitHub OIDC/Sigstore-backed attestation path.

Do not substitute a PR artifact, local workstation signature, copied attestation or historical release signature for the exact release subject.

## Verification

Before consumption or deployment, verify the artifact identity and its attestations with the GitHub CLI or an equivalent policy engine. Verification must bind the subject digest to the expected repository/workflow/release identity. An attestation is provenance evidence, not a declaration that the artifact is secure.

## Failure handling

- Missing SBOM, scan output, subject digest or attestation: fail closed.
- Vulnerability gate failure: do not suppress or relabel without a governed risk decision and traceable exception.
- Attestation subject mismatch: reject the artifact.
- OIDC/signing failure: do not fall back to a repository-stored long-lived signing key.
- Missing verification capability in the deployment environment: record the blocker; do not claim supply-chain admission is complete.

## Rollback

Rollback means returning to the last accepted artifact whose digest, SBOM, vulnerability evidence and required attestations can be verified. Re-run deployment verification against that immutable artifact identity. Do not rebuild an old source revision and call the new binary equivalent to the previously accepted artifact.

## Evidence boundary

Repository CI does **not prove** production admission, live registry integrity, deployment verification, runtime integrity, production-equivalent behavior, independent assurance or production authorization. Those remain later lifecycle gates.
