# RC10.6 UX Polish Gate

Status: `CI_VALIDATION_PENDING`

## Bounded increment

Repository-controlled acceptance for the first RC10.6 UX-polish increment: local theme and density preferences at `/ui/preferences`.

## Required evidence

- `/ui/preferences` is GET-only and wired into the application;
- theme is allowlisted to `dark` or `light`;
- density is allowlisted to `comfortable` or `compact`;
- preferences are browser-local presentation state only;
- no server-side mutation API is introduced;
- preferences do not grant or imply RBAC, review, source-management, security, publication or share-approval authority;
- dedicated regression tests pass;
- every registered GitHub workflow succeeds on one final exact PR head.

## Governance boundary

Server-side RBAC, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative and unchanged.

## Claim boundary

A PASS proves only the repository-controlled UX preference contract. It does not prove genuine assistive-technology execution, real staging parity, independent penetration testing, external assurance or production readiness.
