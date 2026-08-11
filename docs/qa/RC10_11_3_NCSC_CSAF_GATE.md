# RC10.11.3 — NCSC-NL CSAF Source Adapter Gate

Status: `PENDING_CI`

## Objective

Make the curated `ncsc-nl-advisories` source genuinely executable from the unified DTMO console by using the official NCSC-NL CSAF provider distribution rather than HTML scraping.

## Acceptance boundary

The adapter MUST:

- use the official `https://advisories.ncsc.nl/csaf/` distribution;
- discover documents only through `v2/index.txt`;
- accept only bounded relative `YYYY/*.json` index entries;
- process at most 25 CSAF documents per run;
- fetch every index and advisory document through the existing HTTPS-only, DNS re-resolution, global-address, TLS/SNI-pinned, redirect-denying and 5 MiB bounded transport;
- normalize CSAF tracking identity, title, release date and notes to `security-advisory` records;
- retain the complete CSAF JSON as raw provenance;
- fail closed on malformed index entries, malformed documents or missing tracking identity;
- preserve the existing review/share/publication separation of duties.

## Claim boundary

This gate covers NCSC-NL CSAF only. CERT-EU, MSRC and other `planned-parser` sources remain non-executable until separate governed adapters are accepted.

## Release evidence

Do not mark PASS or merge until the exact PR head has completed the full required workflow set successfully, including RC4 Quality and all registered regression gates.
