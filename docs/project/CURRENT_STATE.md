# DTMO Current Project State

Last reconciled: 2026-08-11 — RC11 source onboarding and RC12 unified-console/dashboard programme accepted through PR #147.

## Executive status

- Phases 1–7 repository-controlled internal gates: accepted within documented claim boundaries.
- Phase 6 genuine assistive-technology evidence: `BLOCKED_EXTERNAL` for real VoiceOver/NVDA execution.
- RC11 unified source framework and operational vendor onboarding: `COMPLETE` within repository-controlled scope.
- RC12 unified console and graphical dashboard integration: `COMPLETE` within repository-controlled scope through PR #147.
- Phase 8 staging acceptance: `BLOCKED_EXTERNAL` for approved real deployment-parity evidence.
- Phase 9 external assurance: `NOT COMPLETE`.
- Phase 10 production go/no-go: `NOT STARTED`.

DTMO is **not production ready**.

## RC11 source-framework acceptance

RC11 established one governed source adapter registry and execution dispatcher, then completed the current operational vendor onboarding set. The maintained source connection matrix records CISA KEV, NVD, GitHub Security Advisories, NCSC-NL, CERT-EU, MSRC, Cisco, Red Hat, Ubuntu, Debian, Apple, Chrome, Mozilla, Fortinet, Palo Alto Networks and Broadcom/VMware as connected through accepted built-in or framework adapters. ENISA Threat Landscape remains a deliberate research reference rather than a high-frequency executable feed.

The framework preserves bounded HTTPS/DNS/TLS/redirect/response controls, raw provenance, fail-closed parsing/execution, logical secret references for credentialed adapters and the existing human review/share-approval boundary.

## RC12 unified-console acceptance

RC12.1 / PR #142 unified source administration and operations inside the canonical DTMO console. Registration/bootstrap, enable/disable, interval management, validation and manual execution use the existing governed admin APIs and server-side authorization.

RC12.2 / PR #143 adopted self-hosted Grafana for production-grade operational dashboarding while retaining native DTMO summary graphics as a governed fallback. RC12.3 / PR #144 added a dedicated least-privilege PostgreSQL reporting role and explicit reporting views for intelligence dashboards; Grafana does not receive the DTMO application database identity or unrestricted application-table access.

RC12.4 / PR #145 embedded DTMO Operations and DTMO Intelligence dashboards inside the unified console. RC12.5a / PR #146 added the managed same-origin Nginx/Grafana subpath foundation. RC12.5b / PR #147 switched browser-facing embeds from the compatibility `:3000` origin to relative `/grafana/...` URLs. PR #147 exact head `339207dd5ad038727da34e0a0058c74076847eea` completed the returned exact-head workflow set successfully and merged as `6e74c5e45b6683e1fceba3ff14f554e36815b95f`.

The canonical product entry point is `/` (with `/ui/console` as alias). Legacy `/ui/*` routes may remain for compatibility but no longer define the intended product architecture. Source operations, administration, intelligence investigation and graphical analytics are presented in one shell while RBAC, separation of duties, privacy, provenance, auditability, human review and separate share approval remain authoritative.

## Remaining external blockers

No approved real staging endpoint/environment identity and no complete ten-class deployment-parity package tied to one immutable release are available. Genuine assistive-technology execution, independent penetration testing and remaining external assurance also remain absent. Repository emulators, local Compose runs and exact-head CI do not satisfy those external gates.

## Exactly one current priority

**Phase 8 real staging deployment parity**: obtain one approved production-equivalent staging deployment and collect the complete ten-class deployment-parity evidence package against one immutable release/deployment identity. Until that external dependency exists, repository-controlled work may improve implementation or documentation but cannot establish staging acceptance or production readiness.
