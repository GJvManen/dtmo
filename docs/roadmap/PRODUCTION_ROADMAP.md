# DTMO Production Readiness Roadmap

## Purpose
Controlled path from release candidate to production readiness. Missing evidence blocks the corresponding claim.

## Current status — 2026-08-11

Phases 1–7 repository-controlled internal gates are accepted within their documented boundaries. The RC11 source-framework/onboarding programme and RC12 unified-console/dashboard programme are complete within repository-controlled claim boundaries. Phase 6 remains externally blocked for genuine assistive-technology execution. Phase 8 is `BLOCKED_EXTERNAL`; Phase 9 is `NOT COMPLETE`; Phase 10 is `NOT STARTED`.

DTMO is **not production ready**.

## RC11 source framework and operational source onboarding

1. **RC11.1 unified source framework core** — `PASS`; PR #132.
2. **RC11.2 Red Hat Product Security** — `PASS`; PR #133.
3. **RC11.3 Ubuntu Security Notices** — `PASS`; PR #134.
4. **RC11.4 Debian Security Advisories** — `PASS`; PR #135.
5. **RC11.5 Apple Security Releases** — `PASS`; PR #136.
6. **RC11.6 Chrome security releases** — `PASS`; PR #137.
7. **RC11.7 Mozilla Security Advisories** — `PASS`; PR #138.
8. **RC11.8 Fortinet PSIRT** — `PASS`; PR #139.
9. **RC11.9 Palo Alto Networks Security Advisories** — `PASS`; PR #140.
10. **RC11.10 Broadcom/VMware Security Advisories** — `PASS`; PR #141.

Cisco PSIRT OpenVuln, MSRC, CERT-EU and NCSC-NL adapters were accepted immediately before RC11 in the RC10.11 remediation chain. The maintained `docs/qa/SOURCE_CONNECTION_MATRIX.md` is authoritative for the current connected-source contract.

## RC12 unified console and graphical analytics

1. **RC12.1 unified source administration and operations** — `PASS`; PR #142.
2. **RC12.2 Grafana-first operational dashboarding** — `PASS`; PR #143.
3. **RC12.3 least-privilege Grafana intelligence datasource** — `PASS`; PR #144.
4. **RC12.4 Grafana embedding in the unified console** — `PASS`; PR #145.
5. **RC12.5a same-origin Grafana gateway foundation** — `PASS`; PR #146.
6. **RC12.5b same-origin Grafana console switch** — `PASS`; PR #147; exact head `339207dd5ad038727da34e0a0058c74076847eea`, merge `6e74c5e45b6683e1fceba3ff14f554e36815b95f`.
7. **RC12.6 programme close-out and authoritative documentation reconciliation** — `PENDING_CI` in the current close-out PR. It may only become `PASS` on a fully green exact head.

RC12 does not collapse authority boundaries. Source administration, security/token administration, human review, external share approval and audit remain separately governed. Presentation preferences, ingestion rights, dashboard access or staging access grant no publication authority. RBAC, separation of duties, privacy, provenance and auditability remain authoritative.

## Remaining external gates

### Phase 6
Genuine VoiceOver/NVDA execution on supported real host/browser/screen-reader combinations is still required. Browser/DOM automation is not a substitute.

### Phase 8
Requires one approved production-equivalent staging environment and the complete ten-class deployment-parity package tied to one immutable release/deployment identity. Repository emulator, local Compose and CI evidence do not substitute for this gate.

### Phase 9
Requires independent penetration testing and the remaining external-assurance package, including representative load/stress validation, full backup/restoration exercise, production platform/security hardening evidence, secrets-management acceptance and required operational/stakeholder acceptance.

### Phase 10
Requires all prior blocking evidence, release/deployment artifacts, proven recovery and required approvals. Missing blocking evidence is `NO-GO`.

## Exactly one next priority

After RC12.6 exact-head CI is accepted, the next production-readiness priority is **Phase 8 real staging deployment parity**. Obtain one approved immutable staging deployment and collect the complete ten-class evidence package. Until that external dependency exists, repository-controlled progress cannot establish staging acceptance or production readiness.
