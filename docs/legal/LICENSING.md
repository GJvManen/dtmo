# DTMO Licensing Policy

## Project license

DTMO source code and project-authored documentation are intended to be distributed under the Apache License, Version 2.0 (`Apache-2.0`), unless a file or directory explicitly states otherwise.

The canonical license text is in the repository-root `LICENSE` file. The repository-root `NOTICE` file contains project attribution and distribution notices.

Apache-2.0 was selected because it is a permissive open-source licence that supports commercial and non-commercial reuse and includes an express patent licence from contributors. It does not require derivative works to be distributed under the same licence, provided its conditions are met.

## Contributions

Unless a contributor explicitly states otherwise, an intentionally submitted contribution is accepted under Apache-2.0 in accordance with section 5 of the licence. Contributors must have the right to submit their work and must not introduce third-party content that cannot lawfully be redistributed.

## Source-file identifiers

New project-authored source files should use the SPDX identifier `Apache-2.0` where the file format permits a comment header. Existing files are not bulk-modified by this governance run because a repository-wide header rewrite would create a large, low-signal diff and should be handled as a separately reviewed mechanical change if required.

## Third-party software and content

Apache-2.0 applies to DTMO's own work; it does not relicense third-party dependencies, container images, APIs, feeds, vulnerability databases, threat-intelligence material, trademarks or other external content. Those materials remain governed by their own licences and terms. See `docs/legal/THIRD_PARTY.md`.

## Distribution controls

Before a production or public binary distribution is approved, release engineering should verify at minimum:

- the root `LICENSE` and `NOTICE` files are included;
- package metadata declares `Apache-2.0` accurately;
- an SBOM/dependency inventory is generated for the release candidate;
- bundled third-party material has compatible redistribution terms and required attribution;
- connector/provider data licences and terms are separately accepted where applicable;
- no confidential, personal or restricted intelligence content is inadvertently included.

## No trademark grant

The Apache-2.0 licence does not grant rights to third-party names, marks or branding. DTMO documentation and UI must not imply affiliation or endorsement by the Apache Software Foundation, vendors, schools, government bodies or intelligence providers unless such affiliation is real and authorized.
