# RC11.10 Broadcom/VMware source gate

Status: PENDING_CI

## Objective

Connect Broadcom VMware Security Advisories to the unified source framework using Broadcom's first-party VMware Security Advisories landing page and first-party Broadcom Support VMSA detail documents.

## Acceptance contract

- catalog source `broadcom-vmware-advisories` is `supported`
- execution profile is `broadcom-vmware-vmsa-v1`
- discovery is restricted to VMSA identifiers and HTTPS `support.broadcom.com` SecurityAdvisories detail paths
- discovery is bounded to at most 25 advisories per run
- detail retrieval uses the existing bounded HTTPS/DNS/TLS/redirect/size transport
- detail records require the expected VMSA identifier and at least one published CVE
- VMSA identifier, canonical detail URL, discovery title and CVEs are preserved as provenance
- source execution is registered through `SourceAdapterRegistry`
- malformed/untrusted discovery and invalid detail documents fail closed

## Claim boundary

This gate proves DTMO integration with Broadcom's official VMware Security Advisories publication surface. It does not claim a separate public machine-readable VMSA list API, publication SLA, or provider availability guarantee.

## Evidence required for PASS

1. RC4 Quality Gate completes successfully on the exact PR head.
2. Source framework/catalog contract tests complete successfully.
3. Broadcom VMware adapter regression tests complete successfully.
4. All other required repository release gates complete successfully on the same exact head.

Do not mark PASS or merge while any required exact-head workflow is queued, in progress, cancelled, skipped unexpectedly, or failed.
