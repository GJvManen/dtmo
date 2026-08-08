# Contributing to DTMO

Thank you for helping improve Dutch Threat Monitoring for Education (DTMO).

## License of contributions

DTMO is distributed under the Apache License, Version 2.0. Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in DTMO is provided under Apache-2.0, consistent with section 5 of the license.

By contributing, you confirm that you have the right to submit the contribution and that it does not knowingly include material that you are not permitted to redistribute.

## Development expectations

Contributions should be small, reviewable and evidence driven. Production-readiness work follows `docs/roadmap/PRODUCTION_ROADMAP.md` and the run discipline recorded in `docs/development/RUN_LOG.md`.

For code changes:

1. create a focused branch and pull request;
2. add or update regression tests for changed behavior;
3. preserve existing RBAC, separation-of-duties, privacy, provenance and human-share-approval controls;
4. do not weaken a fail-closed gate to make CI pass;
5. do not commit credentials, production secrets, personal data or unapproved threat-intelligence evidence;
6. document security-relevant assumptions and externally sourced provenance;
7. wait for required exact-head CI to execute successfully before claiming PASS.

## Threat intelligence and external content

Public threat intelligence, historical incidents, CVE material and vendor advisories must retain source provenance, collection date and confidence where used by DTMO. Do not copy third-party material beyond what its licence or terms permit. Prefer identifiers, factual fields, short attributed excerpts and links to authoritative sources over wholesale republication.

## Security-sensitive changes

Changes to identity, authentication, authorization, secrets, publication approval, connector trust, provenance, audit trails or recovery controls require explicit security review. Security vulnerabilities should be reported according to `SECURITY.md`, not through a public issue when exploit details would create risk.

## Documentation

Documentation should distinguish implemented behavior from planned behavior and internal CI evidence from external assurance. Missing, queued or unexecuted tests are never described as passing.
