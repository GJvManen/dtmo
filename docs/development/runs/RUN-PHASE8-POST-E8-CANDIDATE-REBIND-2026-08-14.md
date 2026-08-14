# Phase 8 post-E8 candidate rebind — 2026-08-14

## Decision

The E8 Vulnerability & CTI ecosystem workstream is repository-complete through E8.10. The resulting `main` candidate is materially different from the deployment identity covered by the earlier owner-verified Phase 8.1 staging evidence.

Therefore the historical Phase 8.1 evidence remains valid only for the immutable deployment identity it originally covered. It is not extended, relabelled or inferred to cover the post-E8 candidate.

## Current candidate boundary

Repository baseline after E8.10 merge:

`b5d485ba2770a66ef6cf7e387ebab1613f77c9a4`

This Git commit identifies the repository candidate only. It does **not** prove that this commit is deployed to a production-equivalent staging environment and does not provide application/supporting image digests, environment identity, access path, runtime inventory, IAM/secrets evidence, TLS/network evidence, deployment/change evidence or owner verification.

## Required next external evidence

Before Phase 8.2 execution resumes, an accountable staging owner must provide or verify a new immutable deployment identity for the post-E8 candidate, including the existing Phase 8.1 identity classes:

- approved staging environment identifier and owner;
- approved reachable staging access path;
- deployed release and exact Git commit;
- immutable application and supporting image digests;
- infrastructure/runtime inventory and configuration parity/deviations;
- least-privilege identities and approved secret handling;
- TLS/network/data-sanitization evidence;
- explicit no-production-credential reuse confirmation;
- change/deployment and rollback records;
- deployment-time security/CVE review.

Phase 8.2–8.5 evidence must then bind to that same new immutable identity unless a redeployment triggers another explicit rebind.

## Evidence boundary

Repository CI, staging emulators, Docker Compose and synthetic browser fixtures are repository evidence only. They cannot substitute for a real staging deployment identity or accountable external verification. No Phase 8.2, 8.3, 8.4 or 8.5 acceptance is claimed by this run record.
