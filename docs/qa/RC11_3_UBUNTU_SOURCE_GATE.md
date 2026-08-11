# RC11.3 Ubuntu Security Notices source gate

Status: `PENDING_CI`

## Objective

Connect Canonical Ubuntu Security Notices to the unified source framework using Canonical's official RSS distribution without adding a duplicate vendor-specific parser.

## Accepted source contract

- Canonical's Ubuntu Security Notices page explicitly exposes RSS and Atom subscription feeds.
- DTMO uses `https://ubuntu.com/security/notices/rss.xml` as the canonical execution endpoint.
- The source is authoritative and anonymous.
- Execution reuses the already accepted `rss-2.0` adapter.

## Security and execution boundaries

The source continues to use the existing registered-source transport controls: HTTPS-only URL validation, DNS re-resolution, rejection of non-global addresses, pinned TLS/SNI, redirect denial and the bounded response-size limit. XML parsing continues through `defusedxml`.

Catalog promotion does not grant publication authority. Records continue through existing provenance, ingestion, human review and separate publication/share approval controls.

## Regression evidence

`backend/tests/test_rc11_3_ubuntu_adapter.py` verifies catalog promotion, canonical endpoint/profile selection and representative USN RSS normalization with raw provenance retention. The RC11.1 framework contract continues to ensure every supported profile resolves through the central `SourceAdapterRegistry`.

## Release decision

Do not mark this gate PASS and do not merge the PR until the complete exact-head workflow set is `completed/success`.
