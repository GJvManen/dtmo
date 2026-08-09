# RC9.3 — CISO Token Revocation Browser Gate

Status: `PASS`

## Objective

Prove one bounded critical CISO browser journey for security-token revocation, with browser-visible capability derived from backend RBAC, direct backend denial for a non-authorized analyst, Redis-backed revocation state, and persistent audit-chain evidence.

## Accepted exact-head evidence

PR #55 exact head `e945702adff884f174a40393b3121f3aed99648b` completed all 22 registered workflows successfully, including RC4 Quality, RC9.1 browser share approval, RC9.2 analyst search and RC9.3 CISO token revocation.

Retained artifact `9037014726` has digest `sha256:69256fdcaa01c5b9832bd711a669ff73ef4db5923cc0bc66beab47034cf2b795` and is identity-bound to the exact accepted head.

Independent inspection confirmed:

- machine-readable decision `pass`;
- Chromium execution;
- CISO revoke control backend-derived from `revoke:tokens`;
- analyst revoke control hidden;
- direct analyst backend revocation denied;
- successful CISO revocation;
- Redis revoked-token state verified;
- persistent PostgreSQL audit chain verified;
- publication/share behavior unchanged;
- JUnit: 1 test, 0 failures, 0 errors, 0 skipped;
- server log: analyst POST `/api/v1/security/tokens/revoke` -> `403 Forbidden`;
- server log: CISO POST `/api/v1/security/tokens/revoke` -> `200 OK`.

PR #55 merged with expected-head protection as `3743203bc1a6d93743af53fcb8d4257af153a710`.

## Governance invariants

- UI revocation capability derives from `/api/v1/ui/session` and the backend permission model.
- UI hiding is not treated as authorization; backend denial is independently evidenced.
- Revocation is persisted in Redis and accompanied by a human-principal audit-chain event in PostgreSQL.
- Token revocation does not alter intelligence review, share approval or publication behavior.
- RBAC, separation of duties, privacy, provenance, auditability and separate human share approval remain mandatory.
- Issue #1 external production gates are not closed by this internal browser gate.

## Current decision

`PASS` for RC9.3. This historical gate remains accepted; current project status is tracked in `docs/development/RUN_LOG.md` and `docs/roadmap/PRODUCTION_ROADMAP.md`.
