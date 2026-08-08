# Open-source Governance QA Gate

## Objective

Provide an auditable Apache-2.0 licensing and open-source governance baseline for DTMO without changing product runtime behavior.

## Required evidence

The gate requires all of the following on the exact pull-request head:

- root `LICENSE` contains the complete Apache License, Version 2.0 text;
- root `NOTICE` exists and does not imply third-party relicensing or endorsement;
- `pyproject.toml` declares SPDX licence identifier `Apache-2.0`;
- `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` and `SUPPORTED_VERSIONS.md` exist;
- `docs/legal/LICENSING.md` distinguishes project licensing from third-party rights;
- `docs/legal/THIRD_PARTY.md` keeps provider, dependency, data and trademark terms independent;
- README links the licensing/governance entry points and does not change production-readiness claims;
- the focused governance regressions execute successfully;
- the dedicated `Open Source Governance Gate` executes and retains its evidence artifact;
- all other required exact-head regression workflows execute successfully.

## Fail-closed rules

Missing, queued, cancelled or unexecuted CI is not PASS. A project-level Apache-2.0 licence does not prove that every dependency or external intelligence source can be redistributed under Apache-2.0. Version-specific dependency/SBOM and provider licence evidence remains a release responsibility.

## Governance invariants

This gate does not modify RBAC, separation of duties, privacy controls, provenance rules, auditability or human share approval. Security reporting guidance explicitly prohibits unauthorized testing and public disclosure of sensitive exploit, credential or personal-data material.

## Decision

`CI_VALIDATION_PENDING` until the exact pull-request head has complete successful workflow evidence and the retained open-source-governance artifact has been inspected.
