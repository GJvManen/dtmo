# Governed canonical screenshot promotion

## Status

This procedure promotes a visually reviewed canonical screenshot artifact into the governed documentation catalogue. Promotion is a repository documentation action only. It does **not** establish live integration connectivity, owner acceptance, production-equivalent behavior, penetration-test acceptance, independent assurance or production authorization.

## Why promotion is separate from capture

The Documentation Screenshot Artifact Gate may create deterministic runtime screenshots from the current DTMO browser application using sanitized fixture data. A technically successful capture is not automatically publishable. The image must first be reviewed for complete rendering, current navigation, disclosure boundaries and absence of secrets or unnecessary personal/restricted data.

Capture and promotion therefore remain separate actions:

1. exact-head CI creates the screenshot artifact;
2. a reviewer checks the exact PNG and its metadata;
3. the manual `Governed Documentation Screenshot Promotion` workflow is invoked with the exact source run, source commit, artifact digest and reviewed image SHA-256;
4. the workflow revalidates those immutable identities and the canonical metadata;
5. the workflow opens a new promotion PR containing only the governed UI-01 image replacement and its machine-readable review record;
6. that PR must pass fresh exact-head CI and normal review before merge.

The promotion workflow never merges its own PR.

## Current UI-01 reviewed candidate

The first canonical Command Center candidate was produced by Documentation Screenshot Artifact Gate run `33075823231` from exact head `d0d13b74a371e38c4fee965a4eb08f5d7f57cac9`.

- artifact: `dtmo-documentation-screenshots` (`9647926168`);
- artifact digest: `sha256:d08d609ada05f92ad7f4f4e69315ca56e61a7537c3ac1bf18a8ac4d9028a5ab0`;
- source image: `generated/command-center-workbench.png`;
- image SHA-256: `4003b7e57ad6d1ed52203778c8a9556276212e202477faf5b34900d8133beebd`;
- dimensions: `1440 × 1628`;
- canonical route: `/workbench/command-center`;
- capture classification: `documentation-illustration-only`;
- source metadata explicitly records `live_connectivity_proven = false`, `owner_acceptance_proven = false` and `production_equivalent_proven = false`.

The visual review confirmed complete Command Center rendering, current `/workbench/*` navigation, readable evidence-boundary text and no visible production credentials, secrets or operational personal data. This review authorizes only creation of a normal promotion PR; it does not authorize merging or any lifecycle acceptance claim.

## Fail-closed rules

Promotion must stop when the source run does not match the expected Git SHA, the artifact is expired or its digest differs, the reviewed image hash differs, the canonical metadata is missing or changes its claim boundaries, the PNG is malformed/undersized, or a promotion branch for the same run already exists.

Only the canonical UI-01 Command Center mapping is supported by the current promotion tool. Other screenshots must be migrated in later bounded slices rather than broadening this workflow implicitly.
