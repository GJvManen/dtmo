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

## CI remediation evidence

Exact head `c81f9d77a7e91e0706a1c96fd417a1c454cebf3b` failed multiple workflows. The first concrete root cause inspected was application startup failure because `backend/dtmo/main.py` referenced nonexistent `Permission.READ_METRICS`. Diff inspection showed that the RC10.6 change had also unintentionally replaced accepted baseline health/connectors/metrics definitions. The bounded remediation restores `main.py` to accepted RC10.5 behavior and adds only the RC10.6 preferences-router import/mount. No PASS is claimed until full CI succeeds on one later exact head.

## Governance boundary

Server-side RBAC, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative and unchanged.

## Claim boundary

A PASS proves only the repository-controlled UX preference contract. It does not prove genuine assistive-technology execution, real staging parity, independent penetration testing, external assurance or production readiness.
