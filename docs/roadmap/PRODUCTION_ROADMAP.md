# DTMO Production Readiness Roadmap

## Purpose

This roadmap separates repository-controlled engineering acceptance, functional product acceptance and external staging/assurance/production approval. A phase is complete only when its own evidence boundary is satisfied.

## Current status — 2026-08-12

| Phase | Scope | Status |
|---|---|---|
| 1 | CI and workflow integrity | `PASS` |
| 2 | Application security and identity | `PASS` |
| 3 | Data integrity and recovery | `PASS` |
| 4 | Connector reliability and provenance | `PASS` |
| 5 | Performance and scalability | `PASS` |
| 6 | Accessibility and operational UX | `PASS` |
| 7 | Observability and incident operations | `PASS` |
| RC13 | Functional unified-console acceptance | `PASS / OWNER_ACCEPTED` |
| 8 | Real staging acceptance | `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY` |
| 9 | Independent external assurance | `NOT COMPLETE` |
| 10 | Production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

## RC13 — complete

The final RC13 repair sequence is accepted:

1. PR #159 repaired refresh behavior, empty-data truthfulness, Chrome interactions, Administration clarity and graph empty states.
2. PR #160 repaired Compose runtime packaging for the Grafana reader provisioner.
3. PR #161 repaired Grafana datasource provisioning and added a real Grafana runtime health gate.
4. PR #163 repaired the source catalog secret-reference/bootstrap contract.
5. PR #165 repaired the local object-store credential contract.
6. PR #167 repaired canonical connector commit visibility.
7. PR #169 repaired supported-source normalization while preserving the HTTP(S)-only canonical URL boundary, raw upstream references, fail-closed unknown item types and commit-before-success behavior.
8. The accountable project owner explicitly accepted the repaired product on 2026-08-12: **“Het project werkt! Gefelciteerd!”**

PR #169 final exact head `53aaa670c75a2f404337620bcf1a8df172efe583` completed every returned workflow successfully and merged as `4d182879d851cd22d22ff4f0bab795ed49ee0c1b`.

Issue #150 is closed `completed`.

## Phase 8 — real external staging gate

Phase 8 is now ready to start. Issue #158 tracks Phase 8.1.

### Phase 8.1 — environment and immutable deployment identity

Required evidence includes:

- approved staging environment identifier;
- accountable staging owner;
- approved reachable staging access path;
- deployed release and exact commit;
- immutable application/supporting image digests;
- infrastructure/runtime inventory;
- configuration-parity evidence;
- approved least-privilege identities and secrets handling;
- TLS/network/data-sanitization/no-production-credential evidence;
- change/rollback records;
- deployment-time security/CVE review.

The staging application identity must remain distinct from root/admin infrastructure identities. Local-development compatibility exceptions do not alter staging or production requirements.

Repository CI, Docker Compose and staging emulators cannot substitute for real staging acceptance.

## Post-RC13 product enhancements

Issue #171 contains the owner's accepted post-RC13 product backlog. Suggested delivery order:

1. shared severity colour/filter contract across Overview and Intelligence;
2. governed manual source onboarding;
3. Visual Analytics trend analysis and richer visual semantics;
4. first-class evidence-backed framework mapping model;
5. richer Administration RBAC role/right management;
6. Governance framework coverage and evidence drill-down built on the verified mapping model.

These enhancements do not reopen RC13 and do not count as Phase 8 evidence unless separately demonstrated in real staging.

## Phase 9 — external assurance

Phase 9 covers independent penetration testing, representative load/stress validation, production-equivalent restoration, platform hardening, secrets-management acceptance and required operational/stakeholder approval.

## Phase 10 — production decision

Phase 10 is the formal production go/no-go and begins only after all prior gates are complete and reviewable.

## Evidence lineage

Historical run records remain immutable. RUN-206 remains historical evidence. PR #170 was closed unmerged after owner acceptance superseded its pending-retest status; branch-only RUN-207 is non-authoritative. RUN-208 records the owner-accepted transition to Phase 8 readiness.

## Exactly one next production-readiness priority

**Execute Phase 8.1 real staging environment and immutable deployment identity under issue #158.**
